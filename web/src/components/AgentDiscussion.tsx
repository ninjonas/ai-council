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
    if (messagesEndRef.current && messagesContainerRef.current) {
      // Use scrollIntoView on the end reference, but within the container's context
      const container = messagesContainerRef.current;
      const scrollElement = messagesEndRef.current;
      
      // Scroll the container to the bottom smoothly
      container.scrollTo({
        top: scrollElement.offsetTop,
        behavior: "smooth",
      });
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
    <div className="bg-white rounded-lg shadow-md h-[600px] flex flex-col">
      <div className="p-4 border-b border-gray-200">
        <h2 className="text-xl font-semibold text-gray-800">
          {UI_CONSTANTS.AGENT_SECTION_TITLE}
        </h2>
      </div>
      
      <div 
        ref={messagesContainerRef}
        className="flex-1 overflow-y-auto p-4 space-y-4 scroll-smooth"
      >
        {messages.length === 0 && !isLoading && !isDiscussing ? (
          <div className="h-full flex items-center justify-center text-gray-500">
            <p>Submit a query to start a discussion between AI agents</p>
          </div>
        ) : null}

        {isLoading && (
          <div className="flex items-center p-3 bg-gray-50 rounded-lg animate-pulse">
            <div className="mr-3 text-2xl">{AGENT_CONSTANTS.DEFAULT_AGENT_AVATAR}</div>
            <div>
              <div className="h-2 bg-gray-300 rounded w-24 mb-2"></div>
              <div className="h-2 bg-gray-300 rounded w-64"></div>
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
              <div className="font-medium text-blue-700 mb-1">
                {message.agentName}
              </div>
              <div className="prose prose-sm max-w-none text-gray-700">
                <ReactMarkdown>{message.content}</ReactMarkdown>
              </div>
              <div className="text-xs text-gray-500 mt-1">
                {new Date(message.timestamp).toLocaleTimeString()}
              </div>
            </div>
          </div>
        ))}

        {isDiscussing && (
          <div className="flex items-center p-3 bg-blue-50 rounded-lg animate-pulse">
            <div className="mr-3 text-2xl">💭</div>
            <div className="text-blue-700">
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
