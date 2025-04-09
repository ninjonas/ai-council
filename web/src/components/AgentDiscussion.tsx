import React, { useEffect, useRef } from "react";
import { UI_CONSTANTS, AGENT_CONSTANTS } from "../constants";
import { Message } from "../types/discussion";
import ReactMarkdown from "react-markdown";

interface AgentDiscussionProps {
  messages: Message[];
  isLoading: boolean;
  isDiscussing: boolean;
}

const AgentDiscussion: React.FC<AgentDiscussionProps> = ({
  messages,
  isLoading,
  isDiscussing,
}) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const messagesContainerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (messagesEndRef.current) {
      // Scroll the container to the bottom smoothly
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]);

  const getAgentAvatar = (agentName: string) => {
    const lowerName = agentName.toLowerCase();
    for (const [key, value] of Object.entries(AGENT_CONSTANTS.AVATARS)) {
      if (lowerName.includes(key)) {
        return value;
      }
    }
    return AGENT_CONSTANTS.DEFAULT_AGENT_AVATAR;
  };

  return (
    <div className="card h-[600px] flex flex-col">
      <div className="p-4 border-b border-gray-200 dark:border-gray-700">
        <h2 className="text-xl font-semibold">
          {UI_CONSTANTS.AGENT_SECTION_TITLE}
        </h2>
      </div>
      
      <div 
        ref={messagesContainerRef}
        className="flex-1 overflow-y-auto p-4 space-y-4 scroll-smooth bg-gray-50 dark:bg-gray-800 rounded-lg shadow-inner"
      >
        {messages.length === 0 && !isLoading && !isDiscussing ? (
          <div className="h-full flex items-center justify-center text-gray-500 dark:text-gray-400">
            <p>Submit a query to start a discussion between AI agents</p>
          </div>
        ) : null}

        {isLoading && (
          <div className="flex items-center p-3 bg-gray-50 dark:bg-gray-800 rounded-lg animate-pulse">
            <div className="mr-3 text-2xl">{AGENT_CONSTANTS.DEFAULT_AGENT_AVATAR}</div>
            <div>
              <div className="h-2 bg-gray-300 dark:bg-gray-600 rounded w-24 mb-2"></div>
              <div className="h-2 bg-gray-300 dark:bg-gray-600 rounded w-64"></div>
            </div>
          </div>
        )}

        {messages.map((message, index) => (
          <div
            key={index}
            className="flex message-appear"
            style={{ animationDelay: `${index * 0.1}s` }}
          >
            <div className="flex-shrink-0 mr-3 mt-1 text-2xl">
              {getAgentAvatar(message.agentName)}
            </div>
            <div className="flex-grow">
              <div className="font-medium mb-1" style={{ color: "var(--primary)" }}>
                {message.agentName}
              </div>
              <div className="prose prose-sm max-w-none" style={{ color: "var(--text-primary)" }}>
                <ReactMarkdown>{message.content}</ReactMarkdown>
              </div>
              <div className="text-xs mt-1" style={{ color: "var(--text-secondary)" }}>
                {new Date(message.timestamp).toLocaleTimeString()}
              </div>
            </div>
            <hr class="w-48 h-1 mx-auto my-4 bg-gray-100 border-0 rounded-sm md:my-10 dark:bg-gray-700" />
          </div>
          
        ))}

        {isDiscussing && (
          <div className="flex items-center p-3 bg-blue-50 dark:bg-blue-900/30 rounded-lg animate-pulse">
            <div className="mr-3 text-2xl">💭</div>
            <div style={{ color: "var(--primary)" }}>
              {UI_CONSTANTS.THINKING_MESSAGE}
            </div>
          </div>
        )}

        <div ref={messagesEndRef}></div>
      </div>
    </div>
  );
};

export default AgentDiscussion;
