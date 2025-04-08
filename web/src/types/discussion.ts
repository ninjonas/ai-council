export interface Message {
  agentName: string;
  content: string;
  timestamp: number;
}

export interface Discussion {
  id: string;
  query: string;
  systemInstruction?: string;
  messages: Message[];
  consensus: string | null;
  status: 'pending' | 'in_progress' | 'completed' | 'failed';
}

export interface Agent {
  id: string;
  name: string;
  description: string;
  expertise: string[];
}

export interface DiscussionRequest {
  query: string;
  systemInstruction?: string;
}

export interface WebSocketMessage {
  type: string;
  data: any;
}
