import asyncio
import json
from typing import Dict, List, Optional, AsyncGenerator

import ollama
from loguru import logger

from constants import DEFAULT_TIMEOUT, ERROR_MODEL_UNAVAILABLE


class OllamaService:
    """Service for interacting with Ollama LLM API"""
    
    async def ensure_model_exists(self, model_name: str) -> bool:
        """
        Check if model exists locally and pull if not
        
        Args:
            model_name: Name of the model to check/pull
            
        Returns:
            True if model is available, False otherwise
        """
        try:
            # Check if model exists in a non-blocking way
            loop = asyncio.get_event_loop()
            models = await loop.run_in_executor(
                None, lambda: ollama.list()
            )
            
            model_exists = any(model["name"] == model_name for model in models.get("models", []))
            
            if not model_exists:
                logger.info(f"Model {model_name} not found. Downloading...")
                await loop.run_in_executor(
                    None, lambda: ollama.pull(model_name)
                )
                logger.info(f"Model {model_name} downloaded successfully")
            else:
                logger.info(f"Model {model_name} already exists")
                
            return True
        except Exception as e:
            logger.error(f"Error checking/pulling model: {str(e)}")
            return False
            
    async def generate_response(
        self, 
        model: str, 
        system_prompt: str, 
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 1024
    ) -> str:
        """
        Generate a response from the LLM
        
        Args:
            model: Name of the model to use
            system_prompt: System instructions for the model
            messages: List of conversation messages
            temperature: Sampling temperature (0.0-1.0)
            max_tokens: Maximum response length
            
        Returns:
            Generated response text
        """
        try:
            loop = asyncio.get_event_loop()
            
            formatted_messages = self._format_messages(messages)
            
            response = await asyncio.wait_for(
                loop.run_in_executor(
                    None,
                    lambda: ollama.chat(
                        model=model,
                        messages=formatted_messages,
                        options={
                            "temperature": temperature,
                            "num_predict": max_tokens,
                            "system": system_prompt
                        }
                    )
                ),
                timeout=DEFAULT_TIMEOUT
            )
            
            return response["message"]["content"]
        except asyncio.TimeoutError:
            logger.error(f"Request to Ollama timed out after {DEFAULT_TIMEOUT} seconds")
            return "I'm sorry, but I'm taking too long to respond. Please try again with a simpler query."
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return "I encountered an error while processing your request."
    
    def _format_messages(self, messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Format messages for Ollama API
        
        Args:
            messages: List of messages with 'role' and 'content'
            
        Returns:
            Formatted message list for Ollama
        """
        return [
            {"role": msg["role"], "content": msg["content"]}
            for msg in messages
        ]
