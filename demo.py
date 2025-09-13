#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EMPATH Demo Script
Demonstrates the core functionality of EMPATH
"""

import time
import json
from empath import EMPATHInterface, InfluenceType

def print_separator(title=""):
    """Print a visual separator"""
    print("\n" + "="*60)
    if title:
        print(" " + title)
        print("="*60)

def print_subject_state(empath):
    """Print current subject state"""
    obs = empath.get_current_observation()
    personality = empath.subject.personality
    print(f"\n🧠 Current State: {obs['state']}")
    print(f"💭 Thought: {obs['current_thought']}")
    print(f"🎬 Action: {obs['current_action']}")
    print(f"🌍 Environment: {obs['environment_context']}")
    
    emotion = obs['emotion']
    print(f"\n😊 Emotions:")
    print(f"   Happiness: {emotion['happiness']:.2f}")
    print(f"   Energy: {emotion['energy']:.2f}")
    print(f"   Stress: {emotion['stress']:.2f}")
    print(f"   Confidence: {emotion['confidence']:.2f}")

    print(f"\n👤 Personality:")
    print(f"   Ambition: {personality.ambition:.2f}")

def demo_basic_observation():
    """Demo basic observation functionality"""
    print_separator("BASIC OBSERVATION DEMO")
    
    empath = EMPATHInterface()
    empath.start_observation()
    
    print("🔍 Observing AI subject for 10 seconds...")
    print("The AI believes it is human and is unaware of being observed.")
    
    for i in range(5):
        time.sleep(2)
        print(f"\n--- Observation {i+1} ---")
        print_subject_state(empath)
    
    empath.stop_observation()
    return empath

def demo_influence_system(empath):
    """Demo the influence system"""
    print_separator("INFLUENCE SYSTEM DEMO")
    
    empath.start_observation()
    
    print("🎯 Applying emotional influence...")
    empath.apply_influence(
        InfluenceType.EMOTIONAL,
        intensity=0.8,
        duration=30,
        description="Make the subject feel very happy and energetic",
        parameters={'emotions': {'happiness': 0.5, 'energy': 0.6}}
    )
    
    print("\n⏳ Waiting 5 seconds to see the effect...")
    time.sleep(5)
    print_subject_state(empath)
    
    print("\n🌍 Applying environmental influence...")
    empath.apply_influence(
        InfluenceType.ENVIRONMENTAL,
        intensity=0.6,
        duration=45,
        description="Change environment to a peaceful garden",
        parameters={'environment': 'sitting in a peaceful garden with birds singing'}
    )
    
    print("\n⏳ Waiting 5 seconds to see the effect...")
    time.sleep(5)
    print_subject_state(empath)
    
    print("\n👥 Applying social influence...")
    empath.apply_influence(
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
    
    print("\n⏳ Waiting 5 seconds to see the effect...")
    time.sleep(5)
    print_subject_state(empath)
    
    print("\n🛌 Applying physiological influence (fatigue)...")
    empath.apply_influence(
        InfluenceType.PHYSIOLOGICAL,
        intensity=0.9,
        duration=20,
        description="Make the subject feel tired and drained",
        parameters={'states': {'energy': -0.5, 'stress': 0.2}}
    )

    print("\n⏳ Waiting 5 seconds to see the effect...")
    time.sleep(5)
    print_subject_state(empath)

    empath.stop_observation()

def demo_memory_system(empath):
    """Demo the memory system"""
    print_separator("MEMORY SYSTEM DEMO")
    
    print("🧠 Recent memories:")
    memories = empath.subject.get_memories(5)
    for i, memory in enumerate(memories, 1):
        print(f"\n{i}. {memory['content']}")
        print(f"   Emotional weight: {memory['emotional_weight']:.2f}")
        print(f"   Importance: {memory['importance']:.2f}")
        print(f"   Tags: {', '.join(memory['tags'])}")
        print(f"   Date: {time.ctime(memory['timestamp'])}")

def demo_data_export(empath):
    """Demo data export functionality"""
    print_separator("DATA EXPORT DEMO")
    
    print("📊 Exporting all EMPATH data...")
    data = empath.export_data()
    
    # Save to file
    with open('empath_demo_export.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"✅ Data exported to 'empath_demo_export.json'")
    print(f"📈 Total observations: {len(data['observations'])}")
    print(f"🎯 Total influences: {len(data['influences'])}")
    print(f"🧠 Total memories: {len(data['memories'])}")

def main():
    """Main demo function"""
    print("🧠 EMPATH DEMO")
    print("EMPATH Mirrors People And Trusted Humanity")
    print("An interface for observing and influencing an autonomous AI subject")
    
    try:
        # Basic observation demo
        empath = demo_basic_observation()
        
        # Influence system demo
        demo_influence_system(empath)
        
        # Memory system demo
        demo_memory_system(empath)
        
        # Data export demo
        demo_data_export(empath)
        
        print_separator("DEMO COMPLETE")
        print("🎉 EMPATH demo completed successfully!")
        print("\nTo run the web interface:")
        print("  python app.py")
        print("  Then open http://localhost:5000 in your browser")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
