#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EMPATH AI Demo Script
Demonstrates the enhanced EMPATH system with real AI model integration
"""

import time
import json
import os
from empath_ai import EMPATHWithAI, create_gemini_config, create_ollama_config, create_mock_config, AIModelType
from empath import InfluenceType

def print_separator(title=""):
    """Print a visual separator"""
    print("\n" + "="*60)
    if title:
        print(" " + title)
        print("="*60)

def print_subject_state(empath_ai):
    """Print current subject state"""
    obs = empath_ai.get_current_observation()
    print(f"\n🧠 Current State: {obs['state']}")
    print(f"🤖 AI Thought: {obs['current_thought']}")
    print(f"🎬 Action: {obs['current_action']}")
    print(f"🌍 Environment: {obs['environment_context']}")
    
    emotion = obs['emotion']
    print(f"\n😊 Emotions:")
    print(f"   Happiness: {emotion['happiness']:.2f}")
    print(f"   Energy: {emotion['energy']:.2f}")
    print(f"   Stress: {emotion['stress']:.2f}")
    print(f"   Confidence: {emotion['confidence']:.2f}")

def demo_ai_model_selection():
    """Demo AI model selection"""
    print_separator("AI MODEL SELECTION DEMO")
    
    print("Available AI models:")
    print("1. Mock (Testing) - No API required")
    print("2. Gemini (Google) - Requires API key")
    print("3. Ollama (Local) - Requires local Ollama installation")
    
    choice = input("\nSelect model (1-3): ").strip()
    
    if choice == "2":
        api_key = input("Enter your Gemini API key: ").strip()
        if api_key:
            config = create_gemini_config(api_key)
            print("✅ Using Gemini AI model")
        else:
            config = create_mock_config()
            print("⚠️  No API key provided, using Mock model")
    elif choice == "3":
        base_url = input("Enter Ollama base URL (default: http://localhost:11434): ").strip()
        if not base_url:
            base_url = "http://localhost:11434"
        config = create_ollama_config(base_url=base_url)
        print("✅ Using Ollama AI model")
    else:
        config = create_mock_config()
        print("✅ Using Mock AI model")
    
    return config

def demo_ai_enhanced_observation(config):
    """Demo AI-enhanced observation"""
    print_separator("AI-ENHANCED OBSERVATION DEMO")
    
    empath_ai = EMPATHWithAI(config)
    empath_ai.start_observation()
    
    print("🤖 Observing AI subject with real AI model...")
    print("The AI subject now generates realistic thoughts using the selected AI model.")
    
    for i in range(5):
        time.sleep(3)
        print(f"\n--- AI Observation {i+1} ---")
        print_subject_state(empath_ai)
    
    empath_ai.stop_observation()
    return empath_ai

def demo_ai_chat(empath_ai):
    """Demo direct chat with AI subject"""
    print_separator("AI CHAT DEMO")
    
    empath_ai.start_observation()
    
    print("💬 Chatting directly with the AI subject...")
    print("Type 'quit' to exit chat")
    
    while True:
        message = input("\nYou: ").strip()
        if message.lower() == 'quit':
            break
        
        if message:
            # Get current context
            context = {
                "personality": empath_ai.empath_interface.subject.personality.__dict__,
                "emotion": empath_ai.empath_interface.subject.emotion.__dict__,
                "state": empath_ai.empath_interface.subject.state.value,
                "environment": empath_ai.empath_interface.subject.environment_context,
                "memories": empath_ai.empath_interface.subject.get_memories(5)
            }
            
            # Generate AI response
            response = empath_ai.ai_model.generate_response(message, context)
            print(f"AI Subject: {response}")
    
    empath_ai.stop_observation()

def demo_ai_influence_system(empath_ai):
    """Demo AI influence system"""
    print_separator("AI INFLUENCE SYSTEM DEMO")
    
    empath_ai.start_observation()
    
    print("🎯 Applying influences to AI subject...")
    
    # Emotional influence
    print("\n1. Applying emotional influence...")
    empath_ai.apply_influence(
        InfluenceType.EMOTIONAL,
        intensity=0.8,
        duration=30,
        description="Make the subject feel very happy and energetic",
        parameters={'emotions': {'happiness': 0.5, 'energy': 0.6}}
    )
    
    time.sleep(5)
    print_subject_state(empath_ai)
    
    # Environmental influence
    print("\n2. Applying environmental influence...")
    empath_ai.apply_influence(
        InfluenceType.ENVIRONMENTAL,
        intensity=0.6,
        duration=45,
        description="Change environment to a peaceful garden",
        parameters={'environment': 'sitting in a peaceful garden with birds singing'}
    )
    
    time.sleep(5)
    print_subject_state(empath_ai)
    
    # Social influence
    print("\n3. Applying social influence...")
    empath_ai.apply_influence(
        InfluenceType.SOCIAL,
        intensity=0.7,
        duration=60,
        description="Create a memory of meeting an old friend",
        parameters={
            'social_interaction': 'I just ran into my old friend Sarah at the garden. We had such a wonderful conversation about old times.',
            'people': ['Sarah'],
            'places': ['garden']
        }
    )
    
    time.sleep(5)
    print_subject_state(empath_ai)
    
    empath_ai.stop_observation()

def demo_ai_conversation_history(empath_ai):
    """Demo AI conversation history"""
    print_separator("AI CONVERSATION HISTORY DEMO")
    
    print("🗣️ AI Conversation History:")
    history = empath_ai.get_conversation_history()
    
    if history:
        for i, exchange in enumerate(history[-10:], 1):  # Last 10 exchanges
            print(f"\n{i}. {exchange['role'].upper()}: {exchange['content']}")
    else:
        print("No conversation history yet.")

def demo_ai_data_export(empath_ai):
    """Demo AI data export"""
    print_separator("AI DATA EXPORT DEMO")
    
    print("📊 Exporting all EMPATH AI data...")
    data = empath_ai.export_data()
    
    # Save to file
    with open('empath_ai_demo_export.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"✅ Data exported to 'empath_ai_demo_export.json'")
    print(f"📈 Total observations: {len(data['observations'])}")
    print(f"🎯 Total influences: {len(data['influences'])}")
    print(f"🧠 Total memories: {len(data['memories'])}")
    print(f"💬 AI conversations: {len(data['ai_conversation_history'])}")
    print(f"🤖 AI model: {data['ai_model_config']['model_type']} ({data['ai_model_config']['model_name']})")

def main():
    """Main demo function"""
    print("🤖 EMPATH AI DEMO")
    print("EMPATH Mirrors People And Trusted Humanity")
    print("Enhanced AI Subject Observation with Real AI Models")
    
    try:
        # AI model selection
        config = demo_ai_model_selection()
        
        # AI-enhanced observation demo
        empath_ai = demo_ai_enhanced_observation(config)
        
        # AI chat demo
        demo_ai_chat(empath_ai)
        
        # AI influence system demo
        demo_ai_influence_system(empath_ai)
        
        # AI conversation history demo
        demo_ai_conversation_history(empath_ai)
        
        # AI data export demo
        demo_ai_data_export(empath_ai)
        
        print_separator("DEMO COMPLETE")
        print("🎉 EMPATH AI demo completed successfully!")
        print("\nTo run the enhanced web interface:")
        print("  python3 app_ai.py")
        print("  Then open http://localhost:5000 in your browser")
        print("\nEnvironment variables for automatic configuration:")
        print("  GEMINI_API_KEY=your_key (for Gemini)")
        print("  USE_OLLAMA=true (for Ollama)")
        print("  OLLAMA_URL=http://localhost:11434 (Ollama URL)")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
