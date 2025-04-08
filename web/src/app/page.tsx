"use client";

import { useState } from "react";
import { UI_CONSTANTS } from "../constants";
import Header from "../components/Header";
import QueryInput from "../components/QueryInput";
import AgentDiscussion from "../components/AgentDiscussion";
import ConsensusOutput from "../components/ConsensusOutput";
import { useDiscussionStore } from "../store/discussionStore";

export default function Home() {
  const [systemInstruction, setSystemInstruction] = useState<string>("");
  const [userQuery, setUserQuery] = useState<string>("");
  const { 
    isLoading, 
    isDiscussing, 
    messages, 
    consensus, 
    startDiscussion, 
    resetDiscussion 
  } = useDiscussionStore();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (userQuery.trim()) {
      await startDiscussion(userQuery, systemInstruction);
    }
  };

  const handleReset = () => {
    resetDiscussion();
    setUserQuery("");
  };

  return (
    <main className="min-h-screen px-4 py-8" style={{ backgroundColor: "var(--background)" }}>
      <div className="container mx-auto max-w-6xl">
        <Header />
        
        <div className="mb-8">
          <QueryInput 
            systemInstruction={systemInstruction}
            setSystemInstruction={setSystemInstruction}
            userQuery={userQuery}
            setUserQuery={setUserQuery}
            onSubmit={handleSubmit}
            onReset={handleReset}
            isLoading={isLoading || isDiscussing}
          />
        </div>
        
        <div className="grid grid-cols-1 gap-6 md:gap-8 lg:grid-cols-5">
          <div className="lg:col-span-3">
            <AgentDiscussion 
              messages={messages} 
              isLoading={isLoading} 
              isDiscussing={isDiscussing} 
            />
          </div>
          
          <div className="lg:col-span-2">
            <ConsensusOutput consensus={consensus} />
          </div>
        </div>
      </div>
    </main>
  );
}
