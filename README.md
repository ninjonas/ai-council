# AI Agent Council

A collaborative decision-making platform where multiple AI agents discuss and reach consensus on user queries.

## Project Overview

The AI Agent Council is a system where:

1. Users can submit queries through a web interface
2. Multiple AI agents independently analyze the query
3. Agents engage in a discussion to share perspectives
4. Agents collaboratively reach a consensus
5. The final decision is presented back to the user

The system consists of:
- A Next.js web application with a modern UI
- Python-based AI agents that can be easily configured
- Ollama integration for local LLM inference using Llama3:8b

## Installation

### Prerequisites

- Node.js 18+ and npm/yarn
- Python 3.10+
- [Ollama](https://ollama.com/) installed locally
    - Install on MacOS (Using Homebrew)
    ```sh
    $ brew install ollama
    ```

### Setup

1. Clone the repository:
   ```
   git clone https://github.com/ninjonas/ai-council.git
   cd ai-council
   ```

2. Set up the Next.js application:
   ```
   cd web
   npm install
   npm run dev
   ```

3. Set up the Python agents:
   ```
   cd ../agents
   pip install -r requirements.txt
   python server.py
   ```

4. The web interface will be available at `http://localhost:3000`

## Adding New Agents

To add a new agent:

1. Create a new folder in the `agents/agent_instances` directory:
   ```
   mkdir -p agents/agent_instances/your_agent_name/references
   ```

2. Configure the agent by creating a `config.yml` in the new folder:
   ```yaml
   name: "Your Agent Name"
   description: "What this agent specializes in"
   personality: "How this agent should communicate"
   expertise: ["area1", "area2"]
   temperature: 0.7
   max_tokens: 1024
   system_prompt: |
     As Your Agent Name, your approach should be...
   ```

3. Add reference materials (optional):
   - Place PDF, Markdown or text files in the `agents/agent_instances/your_agent_name/references` folder
   - Agents will automatically incorporate these materials in their reasoning

4. Restart the agent server:
   ```
   cd agents
   python server.py
   ```

## System Architecture

- **Web Application**: Next.js with TypeScript and Tailwind CSS
- **Agent System**: Python-based with WebSockets for real-time communication
- **LLM Integration**: Ollama with Llama3:8b for efficient local inference
- **Data Exchange**: Standardized JSON protocols for agent communication

## Configuration Options

### System Instructions

Users can provide system-wide instructions that all agents will follow during their discussion. This is optional and can be left blank.

### Agent Configuration

Each agent's `config.yml` supports:

- `name`: Agent identifier
- `description`: Purpose description
- `personality`: Communication style 
- `expertise`: List of specialization areas
- `temperature`: Creativity level (0.0-1.0)
- `max_tokens`: Maximum response length
- `system_prompt`: Default instructions for this agent

## License

MIT
