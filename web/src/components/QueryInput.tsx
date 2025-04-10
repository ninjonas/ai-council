import React from "react";
import { UI_CONSTANTS } from "../constants";

interface QueryInputProps {
  systemInstruction: string;
  setSystemInstruction: (instruction: string) => void;
  userQuery: string;
  setUserQuery: (query: string) => void;
  onSubmit: (e: React.FormEvent) => void;
  onReset: () => void;
  isLoading: boolean;
}

const QueryInput: React.FC<QueryInputProps> = ({
  systemInstruction,
  setSystemInstruction,
  userQuery,
  setUserQuery,
  onSubmit,
  onReset,
  isLoading,
}) => {
  return (
    <form onSubmit={onSubmit} className="bg-white p-8 rounded-xl shadow-lg border border-gray-200 space-y-6">
      <div className="mb-6">
        <label
          htmlFor="systemInstruction"
          className="block text-sm font-semibold text-gray-700 mb-2"
          style={{fontWeight: '600', marginBottom: '0.5rem'}}
        >
          System Instructions (Optional)
        </label>
        <textarea
          id="systemInstruction"
          value={systemInstruction}
          onChange={(e) => setSystemInstruction(e.target.value)}
          placeholder={UI_CONSTANTS.SYSTEM_INSTRUCTION_PLACEHOLDER}
          className="w-full p-4 border border-gray-300 rounded-lg transition-all duration-200 
                   focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
          style={{
            width: '100%',
            padding: '1rem',
            border: '1px solid #d1d5db',
            borderRadius: '0.5rem',
          }}
          rows={2}
          disabled={isLoading}
        />
      </div>

      <div className="mb-6">
        <label
          htmlFor="userQuery"
          className="block text-sm font-semibold text-gray-700 mb-2"
          style={{fontWeight: '600', marginBottom: '0.5rem'}}
        >
          Query for AI Agents
        </label>
        <textarea
          id="userQuery"
          value={userQuery}
          onChange={(e) => setUserQuery(e.target.value)}
          placeholder={UI_CONSTANTS.QUERY_PLACEHOLDER}
          className="w-full p-4 border border-gray-300 rounded-lg transition-all duration-200
                   focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
          style={{
            width: '100%',
            padding: '1rem',
            border: '1px solid #d1d5db',
            borderRadius: '0.5rem',
          }}
          rows={3}
          required
          disabled={isLoading}
        />
      </div>

      <div className="flex space-x-4">
        <button
          type="submit"
          className="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 me-2 mb-2 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800"
          disabled={isLoading}
        >
          {isLoading ? (
            <span className="flex items-center">
              <svg
                className="animate-spin -ml-1 mr-2 h-4 w-4 text-white"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
              >
                <circle
                  className="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="4"
                ></circle>
                <path
                  className="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                ></path>
              </svg>
              Processing...
            </span>
          ) : (
            UI_CONSTANTS.SUBMIT_BUTTON
          )}
        </button>
        <button
          type="button"
          onClick={onReset}
          className="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 me-2 mb-2 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800"
          disabled={isLoading}
        >
          {UI_CONSTANTS.RESET_BUTTON}
        </button>
      </div>
    </form>
  );
};

export default QueryInput;
