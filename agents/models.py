from enum import Enum
from typing import Dict, List, Optional, Any
from datetime import datetime
import uuid

from pydantic import BaseModel, Field
import time


class MessageType(str, Enum):
    """Types of messages that can be sent via WebSocket"""
    QUERY = "query"
    AGENT_MESSAGE = "agent_message"
    CONSENSUS = "consensus"
    ERROR = "error"


class AgentMessage(BaseModel):
    """Represents a message from an agent in a discussion"""
    agent_id: str
    agent_name: str
    content: str  # Add the missing content attribute
    timestamp: int = Field(default_factory=lambda: int(time.time() * 1000))
    message_id: str = Field(default_factory=lambda: str(uuid.uuid4()))

    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary representation"""
        return {
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "content": self.content,
            "timestamp": self.timestamp,
            "message_id": self.message_id
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AgentMessage":
        """Create message from dictionary representation"""
        return cls(
            agent_id=data["agent_id"],
            agent_name=data["agent_name"],
            content=data["content"],
            timestamp=data["timestamp"],
            message_id=data.get("message_id")
        )


class WebSocketMessage(BaseModel):
    """Message sent through WebSocket"""
    type: str
    data: Dict[str, Any]


class DiscussionRequest(BaseModel):
    """Request to start a new discussion"""
    query: str
    system_instruction: Optional[str] = None


class DiscussionStatus(str, Enum):
    """Status of a discussion"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class Discussion(BaseModel):
    """Discussion between agents"""
    id: str
    query: str
    system_instruction: Optional[str] = None
    messages: List[AgentMessage] = Field(default_factory=list)
    consensus: Optional[str] = None
    status: DiscussionStatus = DiscussionStatus.PENDING


class AgentConfig(BaseModel):
    """Configuration for an agent"""
    name: str
    description: str
    personality: str
    expertise: List[str]
    temperature: float = 0.7
    max_tokens: int = 1024
    system_prompt: Optional[str] = None


class AgentInfo(BaseModel):
    """Public information about an agent"""
    id: str
    name: str
    description: str
    expertise: List[str]
