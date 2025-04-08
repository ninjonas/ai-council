export const UI_CONSTANTS = {
  TITLE: "AI Agent Council",
  SUBTITLE: "Collaborative AI Decision Making",
  SYSTEM_INSTRUCTION_PLACEHOLDER: "Enter system instructions for all agents (optional)",
  QUERY_PLACEHOLDER: "What would you like the AI agents to discuss?",
  SUBMIT_BUTTON: "Submit Query",
  RESET_BUTTON: "Reset Discussion",
  LOADING_MESSAGE: "Initializing agents...",
  THINKING_MESSAGE: "Agents are discussing...",
  AGENT_SECTION_TITLE: "Agent Dialogue",
  CONSENSUS_SECTION_TITLE: "Final Consensus",
  DEFAULT_ERROR_MESSAGE: "An error occurred while communicating with the agents."
};

export const API_CONSTANTS = {
  WEBSOCKET_URL: "ws://localhost:8000/ws",
  HTTP_BASE_URL: "http://localhost:8000",
  ENDPOINTS: {
    START_DISCUSSION: "/discussions/start",
    GET_AGENTS: "/agents",
    GET_DISCUSSION: "/discussions/",
  },
  MESSAGE_TYPES: {
    QUERY: "query",
    AGENT_MESSAGE: "agent_message",
    CONSENSUS: "consensus",
    ERROR: "error"
  }
};

export const AGENT_CONSTANTS = {
  MAX_DISCUSSION_ROUNDS: 3,
  DEFAULT_AGENT_AVATAR: "👩‍💻",
  AVATARS: {
    "analyst": "📊",
    "creative": "🎨",
    "critic": "🔍",
    "advisor": "💼",
    "technical": "💻",
    "ethical": "⚖️"
  }
};
