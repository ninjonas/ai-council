import os
import time
from typing import Dict, List, Optional

from loguru import logger
import fitz  # PyMuPDF

from models import AgentConfig, AgentMessage
from constants import (
    BASE_SYSTEM_PROMPT, 
    SUPPORTED_REFERENCE_FORMATS, 
    MAX_REFERENCE_LENGTH,
    ERROR_REFERENCE_LOADING
)


class Agent:
    """
    Represents an AI agent with a specific configuration and reference materials
    """
    
    def __init__(self, agent_id: str, config: AgentConfig, references_dir: str):
        """
        Initialize an agent with its configuration
        
        Args:
            agent_id: Unique identifier for the agent
            config: Agent configuration
            references_dir: Directory containing reference materials
        """
        self.id = agent_id
        self.config = config
        self.references_dir = references_dir
        self.reference_content: Optional[str] = None
    
    async def initialize(self):
        """Initialize agent by loading reference materials"""
        await self._load_references()
    
    async def _load_references(self):
        """Load and process reference materials from the references directory"""
        if not os.path.exists(self.references_dir):
            logger.info(f"References directory not found for agent {self.id}. Creating it.")
            os.makedirs(self.references_dir, exist_ok=True)
            return
        
        reference_files = [
            f for f in os.listdir(self.references_dir) 
            if os.path.isfile(os.path.join(self.references_dir, f)) and 
            any(f.endswith(ext) for ext in SUPPORTED_REFERENCE_FORMATS)
        ]
        
        if not reference_files:
            logger.info(f"No reference materials found for agent {self.id}")
            return
        
        all_content = []
        
        for filename in reference_files:
            filepath = os.path.join(self.references_dir, filename)
            try:
                if filename.endswith(".pdf"):
                    content = self._extract_pdf_content(filepath)
                elif filename.endswith(".md") or filename.endswith(".txt"):
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read()
                else:
                    logger.warning(f"Unsupported file format: {filename}")
                    continue
                
                all_content.append(f"--- From {filename} ---\n{content}\n")
            except Exception as e:
                logger.error(ERROR_REFERENCE_LOADING.format(str(e)))
        
        # Combine all reference content
        if all_content:
            combined = "\n\n".join(all_content)
            # Truncate if too long
            if len(combined) > MAX_REFERENCE_LENGTH:
                logger.warning(f"Reference content for agent {self.id} exceeds limit. Truncating.")
                combined = combined[:MAX_REFERENCE_LENGTH] + "...[content truncated]"
            
            self.reference_content = combined
            logger.info(f"Loaded {len(reference_files)} reference files for agent {self.id}")
    
    def _extract_pdf_content(self, filepath: str) -> str:
        """Extract text content from a PDF file"""
        try:
            doc = fitz.open(filepath)
            text = ""
            for page in doc:
                text += page.get_text()
            return text
        except Exception as e:
            logger.error(f"Error extracting PDF content: {str(e)}")
            return f"[Error extracting content from {os.path.basename(filepath)}]"
    
    def get_system_prompt(self, user_system_instruction: Optional[str] = None) -> str:
        """
        Generate the system prompt for this agent
        
        Args:
            user_system_instruction: Optional user-provided system instruction
            
        Returns:
            Complete system prompt string
        """
        prompts = [BASE_SYSTEM_PROMPT]
        
        # Add agent-specific information
        agent_info = f"""
        ## Your Identity
        Name: {self.config.name}
        Role: {self.config.description}
        Personality: {self.config.personality}
        Areas of Expertise: {', '.join(self.config.expertise)}
        """
        prompts.append(agent_info)
        
        # Add agent's specific system prompt if available
        if self.config.system_prompt:
            prompts.append(self.config.system_prompt)
        
        # Add user system instruction if available
        if user_system_instruction:
            prompts.append(f"## Additional Instructions\n{user_system_instruction}")
        
        # Add reference materials if available
        if self.reference_content:
            prompts.append(f"## Reference Materials\n{self.reference_content}")
        
        return "\n\n".join(prompts)
    
    def create_message(self, content: str) -> AgentMessage:
        """Create a message from this agent"""
        return AgentMessage(
            agent_id=self.id,
            agent_name=self.config.name,
            content=content,
            timestamp=int(time.time() * 1000)
        )
