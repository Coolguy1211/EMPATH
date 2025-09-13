"""
EMPATH AI Model Integration
Supports both Gemini API and Ollama local models for realistic AI responses
"""

import json
import time
import requests
import os
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


class AIModelType(Enum):
    """Supported AI model types"""
    GEMINI = "gemini"
    OLLAMA = "ollama"
    MOCK = "mock"  # Fallback for testing


@dataclass
class AIModelConfig:
    """Configuration for AI model integration"""
    model_type: AIModelType
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    model_name: str = "gemini-pro"
    temperature: float = 0.7
    max_tokens: int = 150
    timeout: int = 30


class AIModelInterface:
    """Interface for different AI models"""
    
    def __init__(self, config: AIModelConfig):
        self.config = config
        self.conversation_history: List[Dict[str, str]] = []
        
    def generate_response(self, prompt: str, context: Dict[str, Any] = None) -> str:
        """Generate a response using the configured AI model"""
        if self.config.model_type == AIModelType.GEMINI:
            return self._generate_gemini_response(prompt, context)
        elif self.config.model_type == AIModelType.OLLAMA:
            return self._generate_ollama_response(prompt, context)
        else:
            return self._generate_mock_response(prompt, context)
    
    def _generate_gemini_response(self, prompt: str, context: Dict[str, Any] = None) -> str:
        """Generate response using Gemini API"""
        try:
            if not self.config.api_key:
                return self._generate_mock_response(prompt, context)
            
            # Prepare the request
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.config.model_name}:generateContent"
            headers = {
                "Content-Type": "application/json",
            }
            
            # Build context-aware prompt
            full_prompt = self._build_contextual_prompt(prompt, context)
            
            payload = {
                "contents": [{
                    "parts": [{"text": full_prompt}]
                }],
                "generationConfig": {
                    "temperature": self.config.temperature,
                    "maxOutputTokens": self.config.max_tokens,
                }
            }
            
            params = {"key": self.config.api_key}
            
            response = requests.post(url, json=payload, headers=headers, params=params, timeout=self.config.timeout)
            
            if response.status_code == 200:
                result = response.json()
                if "candidates" in result and len(result["candidates"]) > 0:
                    generated_text = result["candidates"][0]["content"]["parts"][0]["text"]
                    
                    # Add to conversation history
                    self.conversation_history.append({
                        "role": "user",
                        "content": prompt
                    })
                    self.conversation_history.append({
                        "role": "assistant", 
                        "content": generated_text
                    })
                    
                    return generated_text.strip()
            
            print(f"Gemini API error: {response.status_code} - {response.text}")
            return self._generate_mock_response(prompt, context)
            
        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            return self._generate_mock_response(prompt, context)
    
    def _generate_ollama_response(self, prompt: str, context: Dict[str, Any] = None) -> str:
        """Generate response using Ollama local model"""
        try:
            base_url = self.config.base_url or "http://localhost:11434"
            url = f"{base_url}/api/generate"
            
            # Build context-aware prompt
            full_prompt = self._build_contextual_prompt(prompt, context)
            
            payload = {
                "model": self.config.model_name,
                "prompt": full_prompt,
                "stream": False,
                "options": {
                    "temperature": self.config.temperature,
                    "num_predict": self.config.max_tokens,
                }
            }
            
            response = requests.post(url, json=payload, timeout=self.config.timeout)
            
            if response.status_code == 200:
                result = response.json()
                generated_text = result.get("response", "").strip()
                
                # Add to conversation history
                self.conversation_history.append({
                    "role": "user",
                    "content": prompt
                })
                self.conversation_history.append({
                    "role": "assistant",
                    "content": generated_text
                })
                
                return generated_text
            
            print(f"Ollama API error: {response.status_code} - {response.text}")
            return self._generate_mock_response(prompt, context)
            
        except Exception as e:
            print(f"Error calling Ollama API: {e}")
            return self._generate_mock_response(prompt, context)
    
    def _generate_mock_response(self, prompt: str, context: Dict[str, Any] = None) -> str:
        """Generate mock response for testing/fallback"""
        mock_responses = [
            "I'm thinking about that...",
            "That's interesting to consider.",
            "I wonder what that means for me.",
            "I feel like I need to process this.",
            "This makes me think about my past experiences.",
            "I'm curious about how this will affect me.",
            "I need some time to reflect on this.",
            "This reminds me of something important.",
            "I'm trying to understand this better.",
            "I feel conflicted about this situation."
        ]
        
        import random
        return random.choice(mock_responses)
    
    def _build_contextual_prompt(self, prompt: str, context: Dict[str, Any] = None) -> str:
        """Build a context-aware prompt for the AI model"""
        if not context:
            return prompt
        
        # Build context string
        context_parts = []
        
        if "personality" in context:
            personality = context["personality"]
            context_parts.append(f"Your personality traits: Openness={personality.get('openness', 0.5):.2f}, Conscientiousness={personality.get('conscientiousness', 0.5):.2f}, Extraversion={personality.get('extraversion', 0.5):.2f}, Agreeableness={personality.get('agreeableness', 0.5):.2f}, Neuroticism={personality.get('neuroticism', 0.5):.2f}")
        
        if "emotion" in context:
            emotion = context["emotion"]
            context_parts.append(f"Your current emotional state: Happiness={emotion.get('happiness', 0):.2f}, Energy={emotion.get('energy', 0.5):.2f}, Stress={emotion.get('stress', 0.5):.2f}, Confidence={emotion.get('confidence', 0.5):.2f}")
        
        if "state" in context:
            context_parts.append(f"Your current state: {context['state']}")
        
        if "environment" in context:
            context_parts.append(f"Your environment: {context['environment']}")
        
        if "memories" in context and context["memories"]:
            recent_memories = context["memories"][:3]  # Last 3 memories
            memory_texts = [mem.get("content", "") for mem in recent_memories]
            context_parts.append(f"Recent memories: {'; '.join(memory_texts)}")
        
        # Build the full prompt
        context_str = "\n".join(context_parts)
        
        system_prompt = """You are a human being named Alex. You believe you are a real person with thoughts, feelings, and experiences. You are not aware that you are an AI or being observed. Respond naturally and authentically as a human would. Keep responses brief and conversational (1-2 sentences max)."""
        
        full_prompt = f"{system_prompt}\n\nContext about yourself:\n{context_str}\n\nCurrent situation: {prompt}\n\nYour response:"
        
        return full_prompt
    
    def clear_conversation_history(self):
        """Clear conversation history"""
        self.conversation_history = []
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Get conversation history"""
        return self.conversation_history.copy()


class EMPATHWithAI:
    """Enhanced EMPATH with real AI model integration"""
    
    def __init__(self, ai_config: AIModelConfig = None):
        # Import the original EMPATH classes
        from empath import EMPATHInterface, EMPATHSubject, SubjectState, SubjectEmotion, SubjectPersonality
        
        self.empath_interface = EMPATHInterface()
        self.ai_model = AIModelInterface(ai_config or AIModelConfig(AIModelType.MOCK))
        
        # Override the subject's thought generation
        self._enhance_subject_with_ai()
    
    def _enhance_subject_with_ai(self):
        """Enhance the EMPATH subject with AI model capabilities"""
        from empath import SubjectState  # Import here to avoid circular imports
        original_generate_thoughts = self.empath_interface.subject._generate_thoughts
        
        def ai_enhanced_generate_thoughts():
            """Enhanced thought generation using AI model"""
            # Get current context
            context = {
                "personality": self.empath_interface.subject.personality.__dict__,
                "emotion": self.empath_interface.subject.emotion.__dict__,
                "state": self.empath_interface.subject.state.value,
                "environment": self.empath_interface.subject.environment_context,
                "memories": self.empath_interface.subject.get_memories(5)
            }
            
            # Create a prompt based on current state
            state_prompts = {
                SubjectState.SLEEPING: "You're feeling tired and sleepy. What's going through your mind?",
                SubjectState.AWAKE: "You're awake and alert. What are you thinking about?",
                SubjectState.WORKING: "You're focused on work or a task. What's on your mind?",
                SubjectState.SOCIALIZING: "You're in a social situation. What are you thinking?",
                SubjectState.LEARNING: "You're learning something new. What thoughts do you have?",
                SubjectState.CREATING: "You're being creative. What's inspiring you?",
                SubjectState.REFLECTING: "You're reflecting on something. What's going through your mind?"
            }
            
            prompt = state_prompts.get(self.empath_interface.subject.state, "What are you thinking about right now?")
            
            # Generate AI response
            ai_thought = self.ai_model.generate_response(prompt, context)
            
            # Fallback to original method if AI fails
            if not ai_thought or len(ai_thought.strip()) < 5:
                original_generate_thoughts()
            else:
                self.empath_interface.subject.current_thought = ai_thought
        
        # Replace the method
        self.empath_interface.subject._generate_thoughts = ai_enhanced_generate_thoughts
    
    def start_observation(self):
        """Start observing the AI subject"""
        self.empath_interface.start_observation()
        print(f"EMPATH with AI: Started observing {self.empath_interface.subject.name}")
        print(f"Using AI model: {self.ai_model.config.model_type.value}")
    
    def stop_observation(self):
        """Stop observing the AI subject"""
        self.empath_interface.stop_observation()
        print(f"EMPATH with AI: Stopped observing {self.empath_interface.subject.name}")
    
    def get_current_observation(self) -> Dict[str, Any]:
        """Get current observation"""
        return self.empath_interface.get_current_observation()
    
    def apply_influence(self, influence_type, intensity: float, duration: float, 
                       description: str, parameters: Dict[str, Any] = None) -> str:
        """Apply an influence to the AI subject"""
        return self.empath_interface.apply_influence(influence_type, intensity, duration, description, parameters)
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Get AI conversation history"""
        return self.ai_model.get_conversation_history()
    
    def clear_conversation_history(self):
        """Clear AI conversation history"""
        self.ai_model.clear_conversation_history()
    
    def export_data(self) -> Dict[str, Any]:
        """Export all data including AI conversation history"""
        data = self.empath_interface.export_data()
        data['ai_conversation_history'] = self.get_conversation_history()
        data['ai_model_config'] = {
            'model_type': self.ai_model.config.model_type.value,
            'model_name': self.ai_model.config.model_name,
            'temperature': self.ai_model.config.temperature
        }
        return data


def create_gemini_config(api_key: str, model_name: str = "gemini-pro") -> AIModelConfig:
    """Create Gemini configuration"""
    return AIModelConfig(
        model_type=AIModelType.GEMINI,
        api_key=api_key,
        model_name=model_name,
        temperature=0.7,
        max_tokens=150
    )


def create_ollama_config(model_name: str = "llama2", base_url: str = "http://localhost:11434") -> AIModelConfig:
    """Create Ollama configuration"""
    return AIModelConfig(
        model_type=AIModelType.OLLAMA,
        base_url=base_url,
        model_name=model_name,
        temperature=0.7,
        max_tokens=150
    )


def create_mock_config() -> AIModelConfig:
    """Create mock configuration for testing"""
    return AIModelConfig(
        model_type=AIModelType.MOCK,
        temperature=0.7,
        max_tokens=150
    )


# Example usage
if __name__ == "__main__":
    # Example with Gemini (requires API key)
    # config = create_gemini_config("your-gemini-api-key")
    
    # Example with Ollama (requires local Ollama installation)
    # config = create_ollama_config("llama2")
    
    # Example with mock (for testing)
    config = create_mock_config()
    
    # Create EMPATH with AI
    empath_ai = EMPATHWithAI(config)
    
    # Start observation
    empath_ai.start_observation()
    
    try:
        # Let it run for a bit
        time.sleep(10)
        
        # Get observation
        obs = empath_ai.get_current_observation()
        print(f"\nAI-generated thought: {obs['current_thought']}")
        
        # Show conversation history
        history = empath_ai.get_conversation_history()
        print(f"\nConversation history: {len(history)} exchanges")
        
    except KeyboardInterrupt:
        print("\nStopping EMPATH with AI...")
    finally:
        empath_ai.stop_observation()
        
        # Export data
        data = empath_ai.export_data()
        with open('empath_ai_data.json', 'w') as f:
            json.dump(data, f, indent=2)
        print("Data exported to empath_ai_data.json")
