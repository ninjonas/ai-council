# Model settings
MODEL_NAME = "llama3:8b"  # Model to use with Ollama

# Agent and discussion settings
MAX_DISCUSSION_ROUNDS = 3
MAX_REFERENCE_LENGTH = 5000  # Maximum length of reference context to include
DEFAULT_TIMEOUT = 30  # Seconds to wait for model response

# System prompts
BASE_SYSTEM_PROMPT = """You are an AI agent participating in a discussion with other AI agents. 
Your goal is to collaborate with them to address the user's query effectively.
Be concise and clear in your communications while staying true to your character and expertise."""

CONSENSUS_PROMPT = """Based on the discussion between all agents, please provide a final consensus response 
that addresses the original query. Integrate the key insights and perspectives shared by all agents.
Be concise, practical, and ensure the response is comprehensive and directly answers the user's query."""

# File handling
SUPPORTED_REFERENCE_FORMATS = [".pdf", ".md", ".txt"]
MAX_FILE_SIZE_MB = 10

# Folder paths
AGENT_INSTANCES_DIR = "agent_instances"
REFERENCES_DIR = "references"

# Error messages
ERROR_MODEL_UNAVAILABLE = "The LLM model is unavailable. Please check your Ollama installation."
ERROR_AGENT_CONFIG = "Failed to load agent configuration: {}"
ERROR_REFERENCE_LOADING = "Failed to load reference material: {}"
ERROR_DISCUSSION_FAILED = "The discussion failed with error: {}"
