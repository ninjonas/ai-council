import asyncio
import json
import os
import uuid
from typing import Dict, List, Optional

import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from agent_manager import AgentManager
from discussion_manager import DiscussionManager
from models import DiscussionRequest, MessageType, WebSocketMessage
from ollama_service import OllamaService
from constants import MODEL_NAME

app = FastAPI(title="AI Agent Council")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
ollama_service = OllamaService()
agent_manager = AgentManager()
discussion_manager = DiscussionManager(agent_manager, ollama_service)

# Active WebSocket connections
connections: Dict[str, WebSocket] = {}


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    # Check if model exists and download if not
    await ollama_service.ensure_model_exists(MODEL_NAME)
    # Initialize agent instances
    await agent_manager.initialize_agents()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Handle WebSocket connections for real-time agent discussions"""
    await websocket.accept()
    connection_id = str(uuid.uuid4())
    connections[connection_id] = websocket
    
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message.get("type") == MessageType.QUERY:
                query_data = message.get("data", {})
                request = DiscussionRequest(
                    query=query_data.get("query", ""),
                    system_instruction=query_data.get("systemInstruction")
                )
                
                # Start discussion in background task
                asyncio.create_task(
                    handle_discussion(connection_id, request)
                )
    except WebSocketDisconnect:
        if connection_id in connections:
            del connections[connection_id]


async def handle_discussion(connection_id: str, request: DiscussionRequest):
    """Process a discussion and send updates through WebSocket"""
    websocket = connections.get(connection_id)
    if not websocket:
        return
    
    try:
        # Create and run discussion
        discussion_id = str(uuid.uuid4())
        async for update in discussion_manager.run_discussion(discussion_id, request):
            message = WebSocketMessage(
                type=update["type"],
                data=update["data"]
            )
            await websocket.send_text(message.json())
    except Exception as e:
        # Send error message
        error_message = WebSocketMessage(
            type=MessageType.ERROR,
            data={"message": f"Discussion error: {str(e)}"}
        )
        await websocket.send_text(error_message.json())


@app.get("/agents")
async def get_agents():
    """Get information about available agents"""
    return {"agents": agent_manager.get_agent_info()}


if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
