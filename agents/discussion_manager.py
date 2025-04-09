import asyncio
import time
from typing import Dict, List, AsyncGenerator, Any, Tuple

from loguru import logger

from agent_manager import AgentManager
from models import Discussion, DiscussionRequest, DiscussionStatus, MessageType
from ollama_service import OllamaService
from constants import MAX_DISCUSSION_ROUNDS, MODEL_NAME, CONSENSUS_PROMPT


class DiscussionManager:
    """Manages discussions between agents"""
    
    def __init__(self, agent_manager: AgentManager, ollama_service: OllamaService):
        """
        Initialize the discussion manager
        
        Args:
            agent_manager: Manager for agent instances
            ollama_service: Service for LLM interactions
        """
        self.agent_manager = agent_manager
        self.ollama_service = ollama_service
        self.discussions: Dict[str, Discussion] = {}
    
    async def run_discussion(
        self, 
        discussion_id: str, 
        request: DiscussionRequest
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Run a discussion between agents
        
        Args:
            discussion_id: Unique ID for this discussion
            request: Discussion request with query and system instruction
            
        Yields:
            Dictionary with update type and data
        """
        # Initialize discussion
        discussion = Discussion(
            id=discussion_id,
            query=request.query,
            system_instruction=request.system_instruction,
            status=DiscussionStatus.IN_PROGRESS
        )
        self.discussions[discussion_id] = discussion
        
        try:
            agents = self.agent_manager.get_all_agents()
            if not agents:
                yield {
                    "type": MessageType.ERROR,
                    "data": {"message": "No agents available for discussion"}
                }
                discussion.status = DiscussionStatus.FAILED
                return
            
            # Initial round - each agent responds to the query
            for agent in agents:
                # Generate agent response
                system_prompt = agent.get_system_prompt(discussion.system_instruction)
                messages = [{"role": "user", "content": request.query}]
                
                response = await self.ollama_service.generate_response(
                    model=MODEL_NAME,
                    system_prompt=system_prompt,
                    messages=messages,
                    temperature=agent.config.temperature,
                    max_tokens=agent.config.max_tokens
                )
                
                # Create and add message
                agent_message = agent.create_message(response)
                discussion.messages.append(agent_message)
                
                # Send update
                yield {
                    "type": MessageType.AGENT_MESSAGE,
                    "data": agent_message.dict()
                }
                
                # Brief pause between agents for better UX
                await asyncio.sleep(0.5)
                
            # Discussion rounds - agents respond to each other
            for round_num in range(MAX_DISCUSSION_ROUNDS - 1):
                for agent in agents:
                    # Build message history
                    messages = self._format_messages_for_agent(discussion, agent.id)
                    
                    # Generate agent response
                    system_prompt = agent.get_system_prompt(discussion.system_instruction)
                    response = await self.ollama_service.generate_response(
                        model=MODEL_NAME,
                        system_prompt=system_prompt,
                        messages=messages,
                        temperature=agent.config.temperature,
                        max_tokens=agent.config.max_tokens
                    )
                    
                    # Create and add message
                    agent_message = agent.create_message(response)
                    discussion.messages.append(agent_message)
                    
                    # Send update
                    yield {
                        "type": MessageType.AGENT_MESSAGE,
                        "data": agent_message.dict()
                    }
                    
                    # Brief pause between agents
                    await asyncio.sleep(0.5)
            
            # Generate consensus
            consensus = await self._generate_consensus(discussion)
            discussion.consensus = consensus
            discussion.status = DiscussionStatus.COMPLETED
            
            # Send consensus update
            yield {
                "type": MessageType.CONSENSUS,
                "data": {"content": consensus}
            }
            
        except Exception as e:
            logger.error(f"Error in discussion {discussion_id}: {str(e)}")
            discussion.status = DiscussionStatus.FAILED
            
            yield {
                "type": MessageType.ERROR,
                "data": {"message": f"Discussion failed: {str(e)}"}
            }
    
    def _format_messages_for_agent(self, discussion: Discussion, agent_id: str) -> List[Dict[str, str]]:
        """Format discussion messages for an agent"""
        formatted_messages = [
            {"role": "user", "content": discussion.query}
        ]
        
        for msg in discussion.messages:
            role = "assistant" if msg.agent_id == agent_id else "user"
            prefix = "" if msg.agent_id == agent_id else f"{msg.agent_name}: "
            formatted_messages.append({
                "role": role,
                "content": f"{prefix}{msg.content}"
            })
            
        return formatted_messages
    
    async def _generate_consensus(self, discussion: Discussion) -> str:
        """Generate consensus from agent messages"""
        system_prompt = CONSENSUS_PROMPT
        
        # Build message history for consensus generation
        messages = [
            {"role": "user", "content": f"Original Query: {discussion.query}"}
        ]
        
        # Add all agent messages
        for msg in discussion.messages:
            messages.append({
                "role": "user", 
                "content": f"{msg.agent_name}: {msg.content}"
            })
        
        # Add request for consensus
        messages.append({
            "role": "user",
            "content": "Based on the discussion above, please provide a final consensus response."
        })
        
        # Generate consensus
        consensus = await self.ollama_service.generate_response(
            model=MODEL_NAME,
            system_prompt=system_prompt,
            messages=messages,
            temperature=0.5,  # Lower temperature for more focused consensus
            max_tokens=2048   # Allow longer consensus response
        )
        
        return consensus
