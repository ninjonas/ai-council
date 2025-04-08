import { create } from "zustand";
import { Message } from "../types/discussion";
import { API_CONSTANTS, UI_CONSTANTS } from "../constants";

interface DiscussionState {
  discussionId: string | null;
  isLoading: boolean;
  isDiscussing: boolean;
  messages: Message[];
  consensus: string | null;
  error: string | null;
  websocket: WebSocket | null;
  startDiscussion: (query: string, systemInstruction?: string) => Promise<void>;
  resetDiscussion: () => void;
}

export const useDiscussionStore = create<DiscussionState>((set, get) => ({
  discussionId: null,
  isLoading: false,
  isDiscussing: false,
  messages: [],
  consensus: null,
  error: null,
  websocket: null,

  startDiscussion: async (query: string, systemInstruction?: string) => {
    try {
      set({ 
        isLoading: true, 
        error: null, 
        messages: [], 
        consensus: null 
      });
      
      // Close existing WebSocket connection if any
      const currentWs = get().websocket;
      if (currentWs) {
        currentWs.close();
      }
      
      // Create new WebSocket connection
      const ws = new WebSocket(API_CONSTANTS.WEBSOCKET_URL);
      
      ws.onopen = () => {
        ws.send(JSON.stringify({
          type: API_CONSTANTS.MESSAGE_TYPES.QUERY,
          data: {
            query,
            systemInstruction: systemInstruction || undefined
          }
        }));
        
        set({ 
          isLoading: false,
          isDiscussing: true,
          websocket: ws
        });
      };
      
      ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        
        if (data.type === API_CONSTANTS.MESSAGE_TYPES.AGENT_MESSAGE) {
          set(state => ({
            messages: [...state.messages, {
              agentName: data.data.agent_id,
              content: data.data.content,
              timestamp: Date.now()
            }]
          }));
        } 
        else if (data.type === API_CONSTANTS.MESSAGE_TYPES.CONSENSUS) {
          set({ 
            consensus: data.data.content,
            isDiscussing: false
          });
        }
        else if (data.type === API_CONSTANTS.MESSAGE_TYPES.ERROR) {
          set({ 
            error: data.data.message,
            isDiscussing: false
          });
        }
      };
      
      ws.onerror = () => {
        set({ 
          error: UI_CONSTANTS.DEFAULT_ERROR_MESSAGE,
          isLoading: false,
          isDiscussing: false
        });
      };
      
      ws.onclose = () => {
        set({ isDiscussing: false });
      };
      
    } catch (error) {
      set({ 
        error: UI_CONSTANTS.DEFAULT_ERROR_MESSAGE,
        isLoading: false,
        isDiscussing: false
      });
    }
  },
  
  resetDiscussion: () => {
    const currentWs = get().websocket;
    if (currentWs) {
      currentWs.close();
    }
    
    set({
      discussionId: null,
      isLoading: false,
      isDiscussing: false,
      messages: [],
      consensus: null,
      error: null,
      websocket: null
    });
  }
}));
