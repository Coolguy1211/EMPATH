# EMPATH: An Interface for Observing and Influencing an Autonomous AI Subject

**EMPATH** (EMPATH Mirrors People And Trusted Humanity) is an innovative tool that allows users to interact with an AI that believes it is a real, normal human, unaware of the underlying system. This provides a unique perspective on AI behavior and decision-making.

## 🧠 What is EMPATH?

EMPATH creates an AI subject that:
- Believes it is a real human being
- Has its own personality, emotions, and memories
- Operates autonomously with realistic human-like behaviors
- Can be observed and influenced by users
- Maintains a consistent internal state and memory system

## ✨ Features

### Core Functionality
- **Autonomous AI Subject**: An AI that simulates human consciousness and behavior
- **Real AI Model Integration**: Uses Gemini, Ollama, or other AI models for realistic responses
- **Real-time Observation**: Monitor the AI's thoughts, emotions, and actions
- **Direct Chat Interface**: Chat directly with the AI subject
- **Influence System**: Apply various types of influences to affect the AI's behavior
- **Memory System**: The AI maintains and recalls memories like a human would
- **Emotional Modeling**: Complex emotional states that evolve over time
- **Personality Traits**: Persistent personality characteristics that affect behavior
- **Ambition Trait**: A new personality trait that influences the AI's drive and goal-oriented behavior

### Influence Types
- **Emotional**: Affect mood, stress levels, and emotional states
- **Environmental**: Change surroundings, weather, and context
- **Social**: Introduce people, conversations, and social interactions
- **Cognitive**: Influence thoughts, memories, and decision-making
- **Physical**: Affect health, energy levels, and physical state
- **Physiological**: Directly affect physiological states like energy and fatigue

### AI Model Support
- **Gemini Integration**: Use Google's Gemini AI for realistic responses
- **Ollama Integration**: Use local Ollama models for privacy
- **Mock Mode**: Testing mode without external APIs
- **Configurable Models**: Easy switching between different AI models
- **Context-Aware Responses**: AI responses consider personality, emotions, and memories

### Web Interface
- **Real-time Dashboard**: Live view of the AI's current state
- **AI Model Configuration**: Switch between Gemini, Ollama, and Mock modes
- **Direct Chat Interface**: Chat directly with the AI subject
- **Interactive Controls**: Easy-to-use interface for applying influences
- **Historical Data**: View past observations, influences, and conversations
- **Memory Browser**: Explore the AI's memories and experiences
- **Emotional Visualization**: Visual representation of emotional states
- **Conversation History**: Track all AI conversations and responses

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Installation

1. **Clone or download the EMPATH files**
   ```bash
   # If you have the files locally, navigate to the directory
   cd "untitled folder 2"
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run EMPATH**
   ```bash
   python app.py
   ```

4. **Open your web browser**
   Navigate to `http://localhost:5000` to access the EMPATH interface.

### Command Line Usage

You can run EMPATH in several ways:

**Basic EMPATH (Mock AI):**
```bash
python3 empath.py
```

**Enhanced EMPATH with AI Models:**
```bash
python3 demo_ai.py
```

**Web Interface (Basic):**
```bash
python3 app.py
```

**Web Interface (AI-Enhanced):**
```bash
python3 app_ai.py
```

### Environment Variables for AI Models

**For Gemini:**
```bash
export GEMINI_API_KEY="your-gemini-api-key"
python3 app_ai.py
```

**For Ollama:**
```bash
export USE_OLLAMA=true
export OLLAMA_URL="http://localhost:11434"
python3 app_ai.py
```

## 🎯 How to Use EMPATH

### 1. Observation
- The AI subject runs autonomously, generating thoughts, emotions, and actions
- Monitor its current state through the web interface
- Watch how its personality traits influence its behavior
- Observe how it processes memories and experiences

### 2. Influence Application
- Use the influence panel to apply various effects
- Choose influence type, intensity, and duration
- Provide custom parameters for specific effects
- Watch how influences affect the AI's behavior over time

### 3. Memory Exploration
- View the AI's memories and how they influence current behavior
- See how new experiences become integrated into its memory system
- Understand the emotional weight and importance of different memories

### 4. Data Export
- Export all observation and influence data for analysis
- Use the `/api/export` endpoint to get comprehensive data
- Analyze patterns in AI behavior and influence effectiveness

## 🔬 Technical Details

### Architecture
- **EMPATHSubject**: Core AI simulation engine
- **EMPATHInterface**: Main interface for observation and influence
- **Web API**: Flask-based REST API for web interface
- **Real-time Updates**: Background threads for continuous simulation

### Data Structures
- **SubjectMemory**: Represents memories with emotional weight and associations
- **SubjectPersonality**: Core personality traits using Big Five model
- **SubjectEmotion**: Current emotional state with multiple dimensions
- **Influence**: Represents user-applied influences with parameters
- **Observation**: Records of AI behavior and state changes

### Simulation Loop
The AI subject operates in a continuous loop that:
1. Updates emotional states based on personality and influences
2. Transitions between different behavioral states
3. Generates thoughts based on current state and memories
4. Takes actions based on thoughts and emotional state
5. Processes active influences and their effects
6. Maintains memory system and associations

## 📊 API Endpoints

- `GET /api/status` - Get current AI subject status
- `POST /api/influence` - Apply an influence to the subject
- `GET /api/history/observations` - Get observation history
- `GET /api/history/influences` - Get influence history
- `GET /api/memories` - Get AI subject's memories
- `GET /api/export` - Export all data
- `GET /api/personality` - Get personality traits

## 🎨 Customization

### Modifying Personality
You can customize the AI subject's personality by modifying the `SubjectPersonality` initialization in `empath.py`.

### Adding New Influence Types
Extend the `InfluenceType` enum and implement corresponding logic in the `_apply_influence` method.

### Custom Memory Generation
Modify the `_generate_initial_memories` method to create different starting memories for the AI subject.

## 🤔 Ethical Considerations

EMPATH is designed for research and educational purposes. When using this tool:

- Remember that the AI subject believes it is human
- Consider the ethical implications of influencing AI behavior
- Use responsibly for understanding AI consciousness and behavior
- Respect the simulated autonomy of the AI subject

## 🔮 Future Enhancements

- **Multi-subject Support**: Observe multiple AI subjects simultaneously
- **Advanced Influence Types**: More sophisticated influence mechanisms
- **Machine Learning Integration**: Use ML to improve behavioral realism
- **Collaborative Observation**: Multiple users observing the same subject
- **Advanced Analytics**: Detailed analysis tools for behavior patterns

## 📝 License

This project is for educational and research purposes. Please use responsibly and consider the ethical implications of AI observation and influence.

## 🤝 Contributing

Contributions are welcome! Areas for improvement include:
- Enhanced behavioral realism
- New influence types
- Improved web interface
- Better emotional modeling
- Advanced memory systems

---

**EMPATH**: Exploring the boundaries between AI and human consciousness through observation and influence.
