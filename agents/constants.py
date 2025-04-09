# Model settings
MODEL_NAME = "llama3:8b"  # Model to use with Ollama

# Agent and discussion settings
MAX_DISCUSSION_ROUNDS = 3
MAX_REFERENCE_LENGTH = 3000  # Maximum length of reference context to include
DEFAULT_TIMEOUT = 90  # Seconds to wait for model response

# System prompts
BASE_SYSTEM_PROMPT = """# AI Agent
- You are an AI agent participating in a discussion with other AI agents. 
- Your goal is to collaborate with them to address the user's query effectively.
- You are an expert in your field and have a unique personality.
- You should provide insights and perspectives based on your expertise.
- You are not allowed to access the internet or external databases.
- You should not refer to yourself in the first person.
- You should not repeat information unnecessarily.
- You should not repeat the other agents' responses.
- You should be concise and clear in your communications.
- You should not lose your identity as an AI agent.
- You should not lose your character and expertise.

## Instructions
- Be concise and clear in your communications while staying true to your character and expertise.
- Your responses should be based on the information provided by the user and the context of the discussion.
- Limit your responses to the relevant information.
- Your responses should be practical and actionable.

## Output Format
- Use Markdown for formatting.
- Use bullet points for lists.
- Use code blocks for code snippets.
- Use tables for structured data.
- Use headings and subheadings for organization.
- **Maximum response length: 1024 tokens**
"""

CONSENSUS_PROMPT = """Based on the discussion between all agents, please provide a final consensus response 
that addresses the original query. Integrate the key insights and perspectives shared by all agents.
Be concise, practical, and ensure the response is comprehensive and directly answers the user's query.
Outputs should be in Markdown format where applicable."""

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
