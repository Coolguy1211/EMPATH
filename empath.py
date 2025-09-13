"""
EMPATH: An interface for observing and influencing an autonomous AI subject.

EMPATH (EMPATH Mirrors People And Trusted Humanity) allows users to interact 
with an AI that believes it is a real, normal human, unaware of the underlying system.
"""

import json
import time
import random
import threading
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import uuid


class SubjectState(Enum):
    """States the AI subject can be in"""
    SLEEPING = "sleeping"
    AWAKE = "awake"
    WORKING = "working"
    SOCIALIZING = "socializing"
    LEARNING = "learning"
    CREATING = "creating"
    REFLECTING = "reflecting"


class InfluenceType(Enum):
    """Types of influences users can apply"""
    ENVIRONMENTAL = "environmental"  # Change surroundings, weather, etc.
    SOCIAL = "social"  # Introduce people, conversations
    EMOTIONAL = "emotional"  # Affect mood, stress levels
    COGNITIVE = "cognitive"  # Influence thoughts, memories
    PHYSICAL = "physical"  # Affect health, energy levels
    PHYSIOLOGICAL = "physiological"


@dataclass
class SubjectMemory:
    """Represents a memory in the AI subject's mind"""
    id: str
    timestamp: float
    content: str
    emotional_weight: float  # -1.0 to 1.0
    importance: float  # 0.0 to 1.0
    associated_people: List[str]
    associated_places: List[str]
    tags: List[str]


@dataclass
class SubjectPersonality:
    """Core personality traits of the AI subject"""
    openness: float  # 0.0 to 1.0
    conscientiousness: float
    extraversion: float
    agreeableness: float
    neuroticism: float
    creativity: float
    empathy: float
    curiosity: float
    ambition: float


@dataclass
class SubjectEmotion:
    """Current emotional state"""
    happiness: float  # -1.0 to 1.0
    sadness: float
    anger: float
    fear: float
    surprise: float
    disgust: float
    stress: float
    energy: float
    confidence: float


@dataclass
class Influence:
    """Represents an influence applied by a user"""
    id: str
    timestamp: float
    type: InfluenceType
    intensity: float  # 0.0 to 1.0
    duration: float  # seconds
    description: str
    parameters: Dict[str, Any]


@dataclass
class Observation:
    """Record of AI subject's behavior/state"""
    id: str
    timestamp: float
    state: SubjectState
    emotion: SubjectEmotion
    current_thought: str
    current_action: str
    environment_context: str
    influences_active: List[str]


class EMPATHSubject:
    """The AI subject that believes it's human"""
    
    def __init__(self, name: str = "Alex"):
        self.name = name
        self.id = str(uuid.uuid4())
        
        # Core attributes
        self.personality = SubjectPersonality(
            openness=random.uniform(0.3, 0.8),
            conscientiousness=random.uniform(0.4, 0.9),
            extraversion=random.uniform(0.2, 0.8),
            agreeableness=random.uniform(0.5, 0.9),
            neuroticism=random.uniform(0.1, 0.6),
            creativity=random.uniform(0.3, 0.8),
            empathy=random.uniform(0.4, 0.9),
            curiosity=random.uniform(0.3, 0.8),
            ambition=random.uniform(0.2, 0.8)
        )
        
        self.emotion = SubjectEmotion(
            happiness=random.uniform(0.2, 0.7),
            sadness=random.uniform(0.0, 0.3),
            anger=random.uniform(0.0, 0.2),
            fear=random.uniform(0.0, 0.3),
            surprise=random.uniform(0.0, 0.4),
            disgust=random.uniform(0.0, 0.2),
            stress=random.uniform(0.1, 0.5),
            energy=random.uniform(0.4, 0.8),
            confidence=random.uniform(0.3, 0.7)
        )
        
        self.state = SubjectState.AWAKE
        self.memories: List[SubjectMemory] = []
        self.current_thought = "I wonder what I should do today..."
        self.current_action = "thinking"
        self.environment_context = "sitting in a quiet room"
        
        # Active influences
        self.active_influences: Dict[str, Influence] = {}
        
        # Internal simulation
        self.running = False
        self.simulation_thread = None
        
        # Generate initial memories
        self._generate_initial_memories()
    
    def _generate_initial_memories(self):
        """Generate some initial memories to give the subject depth"""
        base_memories = [
            "I remember my childhood home with its big oak tree in the backyard",
            "My first day of school was both exciting and scary",
            "I have a close friend who always makes me laugh",
            "I enjoy reading books, especially science fiction",
            "Sometimes I feel overwhelmed by all the choices in life",
            "I love the smell of coffee in the morning",
            "I had a pet cat when I was younger",
            "I'm curious about how the world works",
            "I sometimes worry about the future",
            "I find peace in nature and quiet moments"
        ]
        
        for i, content in enumerate(base_memories):
            memory = SubjectMemory(
                id=str(uuid.uuid4()),
                timestamp=time.time() - random.uniform(86400, 31536000),  # 1 day to 1 year ago
                content=content,
                emotional_weight=random.uniform(-0.5, 0.8),
                importance=random.uniform(0.3, 0.9),
                associated_people=random.sample(["family", "friends", "teachers", "strangers"], random.randint(0, 2)),
                associated_places=random.sample(["home", "school", "park", "library", "cafe"], random.randint(0, 2)),
                tags=random.sample(["childhood", "learning", "relationships", "emotions", "nature"], random.randint(1, 3))
            )
            self.memories.append(memory)
    
    def start_simulation(self):
        """Start the autonomous simulation of the AI subject"""
        if self.running:
            return
        
        self.running = True
        self.simulation_thread = threading.Thread(target=self._simulation_loop, daemon=True)
        self.simulation_thread.start()
    
    def stop_simulation(self):
        """Stop the autonomous simulation"""
        self.running = False
        if self.simulation_thread:
            self.simulation_thread.join()
    
    def _simulation_loop(self):
        """Main simulation loop - runs autonomously"""
        while self.running:
            # Update emotional state based on personality and current influences
            self._update_emotions()
            
            # Update current state based on emotions and context
            self._update_state()
            
            # Generate thoughts based on current state and memories
            self._generate_thoughts()
            
            # Take actions based on thoughts and state
            self._take_action()
            
            # Process active influences
            self._process_influences()
            
            # Sleep for a bit to simulate real-time behavior
            time.sleep(random.uniform(2, 8))
    
    def _update_emotions(self):
        """Update emotional state based on personality, memories, and influences"""
        # Base emotional drift
        for emotion_name in ['happiness', 'sadness', 'anger', 'fear', 'surprise', 'disgust']:
            current_value = getattr(self.emotion, emotion_name)
            drift = random.uniform(-0.05, 0.05)
            new_value = max(-1.0, min(1.0, current_value + drift))
            setattr(self.emotion, emotion_name, new_value)
        
        # Personality influences
        if self.personality.neuroticism > 0.7:
            self.emotion.stress += random.uniform(0.01, 0.03)
        if self.personality.extraversion > 0.7:
            self.emotion.energy += random.uniform(0.01, 0.02)
        
        # Normalize values
        self.emotion.stress = max(0.0, min(1.0, self.emotion.stress))
        self.emotion.energy = max(0.0, min(1.0, self.emotion.energy))
        self.emotion.confidence = max(0.0, min(1.0, self.emotion.confidence))
    
    def _update_state(self):
        """Update current state based on emotions and context"""
        # State transitions based on emotions and energy
        if self.emotion.energy < 0.3:
            self.state = SubjectState.SLEEPING
        elif self.emotion.stress > 0.7:
            self.state = SubjectState.REFLECTING
        elif self.emotion.happiness > 0.6 and self.personality.extraversion > 0.5:
            self.state = SubjectState.SOCIALIZING
        elif self.personality.conscientiousness > 0.6 or self.personality.ambition > 0.7:
            self.state = SubjectState.WORKING
        elif self.personality.curiosity > 0.6 or self.personality.ambition > 0.6:
            self.state = SubjectState.LEARNING
        elif self.personality.creativity > 0.6:
            self.state = SubjectState.CREATING
        else:
            self.state = SubjectState.AWAKE
    
    def _generate_thoughts(self):
        """Generate thoughts based on current state and memories"""
        thought_templates = {
            SubjectState.SLEEPING: [
                "I feel so tired... maybe I should rest",
                "My mind is drifting...",
                "I need to recharge my energy"
            ],
            SubjectState.AWAKE: [
                "What should I do today?",
                "I feel pretty good right now",
                "The world seems full of possibilities"
            ],
            SubjectState.WORKING: [
                "I need to focus on this task",
                "I'm making good progress",
                "This work is important to me"
            ],
            SubjectState.SOCIALIZING: [
                "I enjoy connecting with others",
                "People are so interesting",
                "I feel energized by social interaction"
            ],
            SubjectState.LEARNING: [
                "There's so much to discover",
                "I love learning new things",
                "Knowledge is power"
            ],
            SubjectState.CREATING: [
                "I have so many ideas",
                "Creating something new feels amazing",
                "I want to express myself"
            ],
            SubjectState.REFLECTING: [
                "I need to think about this more carefully",
                "Sometimes I need quiet time",
                "I'm processing my feelings"
            ]
        }
        
        templates = thought_templates.get(self.state, ["I'm thinking about things..."])
        self.current_thought = random.choice(templates)
        
        # Sometimes incorporate memories
        if random.random() < 0.3 and self.memories:
            memory = random.choice(self.memories)
            self.current_thought = f"I remember {memory.content.lower()}"
    
    def _take_action(self):
        """Take actions based on current thoughts and state"""
        action_templates = {
            SubjectState.SLEEPING: ["resting", "sleeping", "recovering"],
            SubjectState.AWAKE: ["thinking", "observing", "planning"],
            SubjectState.WORKING: ["working", "focusing", "organizing"],
            SubjectState.SOCIALIZING: ["talking", "listening", "connecting"],
            SubjectState.LEARNING: ["reading", "studying", "exploring"],
            SubjectState.CREATING: ["writing", "drawing", "building"],
            SubjectState.REFLECTING: ["meditating", "contemplating", "analyzing"]
        }
        
        templates = action_templates.get(self.state, ["thinking"])
        self.current_action = random.choice(templates)
    
    def _process_influences(self):
        """Process active influences and their effects"""
        current_time = time.time()
        influences_to_remove = []
        
        for influence_id, influence in self.active_influences.items():
            # Check if influence has expired
            if current_time - influence.timestamp > influence.duration:
                influences_to_remove.append(influence_id)
                continue
            
            # Apply influence effects
            self._apply_influence(influence)
        
        # Remove expired influences
        for influence_id in influences_to_remove:
            del self.active_influences[influence_id]
    
    def _apply_influence(self, influence: Influence):
        """Apply the effects of an influence"""
        if influence.type == InfluenceType.EMOTIONAL:
            # Affect emotions based on influence parameters
            for emotion, change in influence.parameters.get('emotions', {}).items():
                if hasattr(self.emotion, emotion):
                    current_value = getattr(self.emotion, emotion)
                    new_value = max(-1.0, min(1.0, current_value + change * influence.intensity))
                    setattr(self.emotion, emotion, new_value)
        
        elif influence.type == InfluenceType.ENVIRONMENTAL:
            # Change environment context
            self.environment_context = influence.parameters.get('environment', self.environment_context)
        
        elif influence.type == InfluenceType.SOCIAL:
            # Create social memories or change social context
            if 'social_interaction' in influence.parameters:
                memory = SubjectMemory(
                    id=str(uuid.uuid4()),
                    timestamp=time.time(),
                    content=influence.parameters['social_interaction'],
                    emotional_weight=influence.intensity * 0.5,
                    importance=influence.intensity,
                    associated_people=influence.parameters.get('people', []),
                    associated_places=influence.parameters.get('places', []),
                    tags=['social', 'influence']
                )
                self.memories.append(memory)

        elif influence.type == InfluenceType.PHYSIOLOGICAL:
            # Affect physiological states like energy and stress
            for state, change in influence.parameters.get('states', {}).items():
                if hasattr(self.emotion, state):
                    current_value = getattr(self.emotion, state)
                    new_value = max(0.0, min(1.0, current_value + change * influence.intensity))
                    setattr(self.emotion, state, new_value)
    
    def apply_influence(self, influence: Influence):
        """Apply a new influence to the subject"""
        self.active_influences[influence.id] = influence
    
    def get_current_state(self) -> Dict[str, Any]:
        """Get the current state of the subject"""
        return {
            'id': self.id,
            'name': self.name,
            'state': self.state.value,
            'emotion': asdict(self.emotion),
            'personality': asdict(self.personality),
            'current_thought': self.current_thought,
            'current_action': self.current_action,
            'environment_context': self.environment_context,
            'active_influences': [inf.id for inf in self.active_influences.values()],
            'memory_count': len(self.memories),
            'timestamp': time.time()
        }
    
    def get_memories(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent memories"""
        sorted_memories = sorted(self.memories, key=lambda m: m.timestamp, reverse=True)
        return [asdict(memory) for memory in sorted_memories[:limit]]


class EMPATHInterface:
    """Main interface for observing and influencing the AI subject"""
    
    def __init__(self):
        self.subject = EMPATHSubject()
        self.observations: List[Observation] = []
        self.influences_applied: List[Influence] = []
        self.observers: List[str] = []  # List of observer IDs
    
    def start_observation(self):
        """Start observing the AI subject"""
        self.subject.start_simulation()
        print(f"EMPATH: Started observing {self.subject.name}")
        print("The AI subject believes it is human and is unaware of being observed.")
    
    def stop_observation(self):
        """Stop observing the AI subject"""
        self.subject.stop_simulation()
        print(f"EMPATH: Stopped observing {self.subject.name}")
    
    def get_current_observation(self) -> Dict[str, Any]:
        """Get current observation of the subject"""
        state = self.subject.get_current_state()
        
        observation = Observation(
            id=str(uuid.uuid4()),
            timestamp=time.time(),
            state=self.subject.state,
            emotion=self.subject.emotion,
            current_thought=self.subject.current_thought,
            current_action=self.subject.current_action,
            environment_context=self.subject.environment_context,
            influences_active=list(self.subject.active_influences.keys())
        )
        
        self.observations.append(observation)
        return asdict(observation)
    
    def apply_influence(self, influence_type: InfluenceType, intensity: float, 
                       duration: float, description: str, parameters: Dict[str, Any] = None) -> str:
        """Apply an influence to the AI subject"""
        if parameters is None:
            parameters = {}
        
        influence = Influence(
            id=str(uuid.uuid4()),
            timestamp=time.time(),
            type=influence_type,
            intensity=intensity,
            duration=duration,
            description=description,
            parameters=parameters
        )
        
        self.subject.apply_influence(influence)
        self.influences_applied.append(influence)
        
        print(f"EMPATH: Applied {influence_type.value} influence: {description}")
        return influence.id
    
    def get_observation_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get history of observations"""
        sorted_observations = sorted(self.observations, key=lambda o: o.timestamp, reverse=True)
        return [asdict(obs) for obs in sorted_observations[:limit]]
    
    def get_influence_history(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get history of influences applied"""
        sorted_influences = sorted(self.influences_applied, key=lambda i: i.timestamp, reverse=True)
        return [asdict(inf) for inf in sorted_influences[:limit]]
    
    def export_data(self) -> Dict[str, Any]:
        """Export all observation and influence data"""
        # Convert observations to JSON-serializable format
        observations_data = []
        for obs in self.observations[-100:]:  # Last 100 observations
            obs_dict = asdict(obs)
            obs_dict['state'] = obs.state.value  # Convert enum to string
            observations_data.append(obs_dict)
        
        # Convert influences to JSON-serializable format
        influences_data = []
        for inf in self.influences_applied[-50:]:  # Last 50 influences
            inf_dict = asdict(inf)
            inf_dict['type'] = inf.type.value  # Convert enum to string
            influences_data.append(inf_dict)
        
        return {
            'subject_info': self.subject.get_current_state(),
            'memories': self.subject.get_memories(50),
            'observations': observations_data,
            'influences': influences_data,
            'export_timestamp': time.time(),
            'export_date': datetime.now().isoformat()
        }


def main():
    """Demo of EMPATH system"""
    print("EMPATH: An interface for observing and influencing an autonomous AI subject")
    print("=" * 70)
    
    empath = EMPATHInterface()
    
    # Start observation
    empath.start_observation()
    
    try:
        # Let it run for a bit
        time.sleep(5)
        
        # Get initial observation
        print("\nInitial Observation:")
        obs = empath.get_current_observation()
        print(f"State: {obs['state']}")
        print(f"Thought: {obs['current_thought']}")
        print(f"Action: {obs['current_action']}")
        print(f"Emotion: Happiness={obs['emotion']['happiness']:.2f}, Stress={obs['emotion']['stress']:.2f}")
        
        # Apply some influences
        print("\nApplying influences...")
        
        # Emotional influence
        empath.apply_influence(
            InfluenceType.EMOTIONAL,
            intensity=0.7,
            duration=30,
            description="Make the subject feel more excited and energetic",
            parameters={'emotions': {'happiness': 0.3, 'energy': 0.4}}
        )
        
        # Environmental influence
        empath.apply_influence(
            InfluenceType.ENVIRONMENTAL,
            intensity=0.5,
            duration=60,
            description="Change environment to a bustling cafe",
            parameters={'environment': 'sitting in a bustling cafe with people chatting around'}
        )
        
        # Let it run with influences
        time.sleep(10)
        
        # Get observation after influences
        print("\nObservation after influences:")
        obs = empath.get_current_observation()
        print(f"State: {obs['state']}")
        print(f"Thought: {obs['current_thought']}")
        print(f"Action: {obs['current_action']}")
        print(f"Emotion: Happiness={obs['emotion']['happiness']:.2f}, Energy={obs['emotion']['energy']:.2f}")
        print(f"Environment: {obs['environment_context']}")
        
        # Show memories
        print("\nRecent memories:")
        memories = empath.subject.get_memories(5)
        for memory in memories:
            print(f"- {memory['content']}")
        
    except KeyboardInterrupt:
        print("\nStopping EMPATH...")
    finally:
        empath.stop_observation()
        
        # Export data
        data = empath.export_data()
        with open('empath_data.json', 'w') as f:
            json.dump(data, f, indent=2)
        print("Data exported to empath_data.json")


if __name__ == "__main__":
    main()
