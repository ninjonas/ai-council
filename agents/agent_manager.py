import os
import yaml
from typing import Dict, List, Optional

from loguru import logger

from agent import Agent
from models import AgentConfig, AgentInfo
from constants import AGENT_INSTANCES_DIR, ERROR_AGENT_CONFIG


class AgentManager:
    """Manages agent instances and their configurations"""
    
    def __init__(self):
        self.agents: Dict[str, Agent] = {}
    
    async def initialize_agents(self):
        """Load all agent configurations from the agent_instances directory"""
        if not os.path.exists(AGENT_INSTANCES_DIR):
            logger.warning(f"Agent instances directory not found: {AGENT_INSTANCES_DIR}")
            os.makedirs(AGENT_INSTANCES_DIR)
            return
            
        # Get all subdirectories in the agent instances directory
        agent_dirs = [
            d for d in os.listdir(AGENT_INSTANCES_DIR) 
            if os.path.isdir(os.path.join(AGENT_INSTANCES_DIR, d))
        ]
        
        if not agent_dirs:
            logger.warning("No agent instances found")
            
            # Create default agents if none exist
            await self._create_default_agents()
            return
            
        # Load each agent configuration
        for agent_dir in agent_dirs:
            config_path = os.path.join(AGENT_INSTANCES_DIR, agent_dir, "config.yml")
            
            if not os.path.exists(config_path):
                logger.warning(f"No config.yml found for agent: {agent_dir}")
                continue
                
            try:
                with open(config_path, "r") as f:
                    config_data = yaml.safe_load(f)
                    
                agent_config = AgentConfig(**config_data)
                
                # Create agent instance
                agent_id = agent_dir
                references_dir = os.path.join(AGENT_INSTANCES_DIR, agent_dir, "references")
                agent = Agent(agent_id, agent_config, references_dir)
                
                # Initialize agent (load references, etc.)
                await agent.initialize()
                
                self.agents[agent_id] = agent
                logger.info(f"Loaded agent: '{agent.config.name}', id: {agent_id}, max_tokens: {agent_config.max_tokens}, temperature: {agent_config.temperature}")
            except Exception as e:
                logger.error(ERROR_AGENT_CONFIG.format(str(e)))
    
    async def _create_default_agents(self):
        """Create default agents if none exist"""
        default_agents = [
            {
                "id": "analyst",
                "config": {
                    "name": "Data Analyst",
                    "description": "Specializes in data analysis and logical reasoning",
                    "personality": "Logical, detail-oriented, and analytical",
                    "expertise": ["data analysis", "statistics", "critical thinking"],
                    "temperature": 0.5
                }
            },
            {
                "id": "creative",
                "config": {
                    "name": "Creative Thinker",
                    "description": "Focuses on creative and innovative solutions",
                    "personality": "Imaginative, enthusiastic, and open-minded",
                    "expertise": ["creativity", "innovation", "out-of-box thinking"],
                    "temperature": 0.8
                }
            },
            {
                "id": "advisor",
                "config": {
                    "name": "Strategic Advisor",
                    "description": "Provides balanced, practical advice with long-term perspective",
                    "personality": "Balanced, thoughtful, and strategic",
                    "expertise": ["planning", "risk assessment", "decision making"],
                    "temperature": 0.6
                }
            }
        ]
        
        for agent_data in default_agents:
            agent_id = agent_data["id"]
            agent_dir = os.path.join(AGENT_INSTANCES_DIR, agent_id)
            
            # Create agent directory and references directory
            os.makedirs(agent_dir, exist_ok=True)
            os.makedirs(os.path.join(agent_dir, "references"), exist_ok=True)
            
            # Create config file
            config_path = os.path.join(agent_dir, "config.yml")
            with open(config_path, "w") as f:
                yaml.dump(agent_data["config"], f)
            
            # Initialize agent
            agent_config = AgentConfig(**agent_data["config"])
            references_dir = os.path.join(agent_dir, "references")
            agent = Agent(agent_id, agent_config, references_dir)
            
            await agent.initialize()
            self.agents[agent_id] = agent
            logger.info(f"Created default agent: {agent_config.name}")
    
    def get_agent(self, agent_id: str) -> Optional[Agent]:
        """Get agent by ID"""
        return self.agents.get(agent_id)
    
    def get_all_agents(self) -> List[Agent]:
        """Get all available agents"""
        return list(self.agents.values())
    
    def get_agent_info(self) -> List[AgentInfo]:
        """Get public information about all agents"""
        return [
            AgentInfo(
                id=agent_id,
                name=agent.config.name,
                description=agent.config.description,
                expertise=agent.config.expertise
            )
            for agent_id, agent in self.agents.items()
        ]
