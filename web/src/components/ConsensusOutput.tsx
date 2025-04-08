import React from "react";
import { UI_CONSTANTS } from "../constants";
import ReactMarkdown from "react-markdown";

interface ConsensusOutputProps {
  consensus: string | null;
}

const ConsensusOutput: React.FC<ConsensusOutputProps> = ({ consensus }) => {
  return (
    <div className="bg-white rounded-lg shadow-md h-[600px] flex flex-col border border-gray-200">
      <div className="p-4 border-b border-gray-200 bg-gray-100">
        <h2 className="text-xl font-semibold text-gray-800">
          {UI_CONSTANTS.CONSENSUS_SECTION_TITLE}
        </h2>
      </div>
      
      <div className="flex-1 overflow-y-auto p-4 prose prose-sm max-w-none">
        {consensus ? (
          <div>
            <ReactMarkdown>{consensus}</ReactMarkdown>
          </div>
        ) : (
          <div className="h-full flex items-center justify-center text-gray-500">
            <p>Agents will provide their consensus here after discussion</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default ConsensusOutput;
