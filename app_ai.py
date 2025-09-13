"""
Enhanced EMPATH Web Interface with AI Model Support
Supports Gemini and Ollama integration
"""

from flask import Flask, render_template, request, jsonify, session
import json
import time
import threading
import os
from datetime import datetime
from empath import EMPATHInterface, InfluenceType, SubjectState
from empath_ai import EMPATHWithAI, create_gemini_config, create_ollama_config, create_mock_config, AIModelType
import uuid

app = Flask(__name__)
app.secret_key = 'empath_ai_secret_key_2024'

# Global EMPATH instance
empath_interface = None
empath_thread = None
ai_model_type = AIModelType.MOCK

def start_empath_background():
    """Start EMPATH in background thread"""
    global empath_interface, empath_thread, ai_model_type
    
    if empath_interface is None:
        # Determine AI model type from environment or config
        gemini_key = os.getenv('GEMINI_API_KEY')
        ollama_url = os.getenv('OLLAMA_URL', 'http://localhost:11434')
        
        if gemini_key:
            config = create_gemini_config(gemini_key)
            ai_model_type = AIModelType.GEMINI
        elif os.getenv('USE_OLLAMA', 'false').lower() == 'true':
            config = create_ollama_config(base_url=ollama_url)
            ai_model_type = AIModelType.OLLAMA
        else:
            config = create_mock_config()
            ai_model_type = AIModelType.MOCK
        
        empath_interface = EMPATHWithAI(config)
        empath_interface.start_observation()
        
        # Start background thread to periodically update observations
        empath_thread = threading.Thread(target=update_observations_loop, daemon=True)
        empath_thread.start()

def update_observations_loop():
    """Background loop to update observations"""
    while True:
        if empath_interface:
            empath_interface.get_current_observation()
        time.sleep(5)  # Update every 5 seconds

@app.route('/')
def index():
    """Main EMPATH interface"""
    return render_template('index_ai.html')

@app.route('/api/status')
def get_status():
    """Get current status of the AI subject"""
    if not empath_interface:
        return jsonify({'error': 'EMPATH not initialized'}), 400
    
    observation = empath_interface.get_current_observation()
    memories = empath_interface.empath_interface.subject.get_memories(5)
    conversation_history = empath_interface.get_conversation_history()
    
    return jsonify({
        'observation': observation,
        'memories': memories,
        'conversation_history': conversation_history[-10:],  # Last 10 exchanges
        'active_influences': len(empath_interface.empath_interface.subject.active_influences),
        'total_observations': len(empath_interface.empath_interface.observations),
        'total_influences': len(empath_interface.empath_interface.influences_applied),
        'ai_model_type': ai_model_type.value,
        'ai_model_name': empath_interface.ai_model.config.model_name
    })

@app.route('/api/influence', methods=['POST'])
def apply_influence():
    """Apply an influence to the AI subject"""
    if not empath_interface:
        return jsonify({'error': 'EMPATH not initialized'}), 400
    
    data = request.json
    influence_type = InfluenceType(data['type'])
    intensity = float(data['intensity'])
    duration = float(data['duration'])
    description = data['description']
    parameters = data.get('parameters', {})
    
    influence_id = empath_interface.apply_influence(
        influence_type, intensity, duration, description, parameters
    )
    
    return jsonify({
        'success': True,
        'influence_id': influence_id,
        'message': f'Applied {influence_type.value} influence: {description}'
    })

@app.route('/api/chat', methods=['POST'])
def chat_with_subject():
    """Chat directly with the AI subject"""
    if not empath_interface:
        return jsonify({'error': 'EMPATH not initialized'}), 400
    
    data = request.json
    message = data.get('message', '')
    
    if not message:
        return jsonify({'error': 'Message is required'}), 400
    
    # Get current context
    context = {
        "personality": empath_interface.empath_interface.subject.personality.__dict__,
        "emotion": empath_interface.empath_interface.subject.emotion.__dict__,
        "state": empath_interface.empath_interface.subject.state.value,
        "environment": empath_interface.empath_interface.subject.environment_context,
        "memories": empath_interface.empath_interface.subject.get_memories(5)
    }
    
    # Generate AI response
    response = empath_interface.ai_model.generate_response(message, context)
    
    return jsonify({
        'success': True,
        'response': response,
        'timestamp': time.time()
    })

@app.route('/api/config/ai', methods=['GET', 'POST'])
def ai_config():
    """Get or update AI model configuration"""
    if request.method == 'GET':
        if not empath_interface:
            return jsonify({'error': 'EMPATH not initialized'}), 400
        
        return jsonify({
            'model_type': ai_model_type.value,
            'model_name': empath_interface.ai_model.config.model_name,
            'temperature': empath_interface.ai_model.config.temperature,
            'max_tokens': empath_interface.ai_model.config.max_tokens
        })
    
    elif request.method == 'POST':
        data = request.json
        model_type = data.get('model_type', 'mock')
        
        try:
            if model_type == 'gemini':
                api_key = data.get('api_key')
                if not api_key:
                    return jsonify({'error': 'API key required for Gemini'}), 400
                config = create_gemini_config(api_key, data.get('model_name', 'gemini-pro'))
            elif model_type == 'ollama':
                config = create_ollama_config(
                    data.get('model_name', 'llama2'),
                    data.get('base_url', 'http://localhost:11434')
                )
            else:
                config = create_mock_config()
            
            # Update the global interface
            global empath_interface
            empath_interface.ai_model.config = config
            empath_interface.ai_model.clear_conversation_history()
            
            return jsonify({
                'success': True,
                'message': f'AI model configuration updated to {model_type}'
            })
            
        except Exception as e:
            return jsonify({'error': f'Failed to update configuration: {str(e)}'}), 400

@app.route('/api/history/observations')
def get_observation_history():
    """Get observation history"""
    if not empath_interface:
        return jsonify({'error': 'EMPATH not initialized'}), 400
    
    limit = request.args.get('limit', 50, type=int)
    history = empath_interface.empath_interface.get_observation_history(limit)
    
    return jsonify({'observations': history})

@app.route('/api/history/influences')
def get_influence_history():
    """Get influence history"""
    if not empath_interface:
        return jsonify({'error': 'EMPATH not initialized'}), 400
    
    limit = request.args.get('limit', 20, type=int)
    history = empath_interface.empath_interface.get_influence_history(limit)
    
    return jsonify({'influences': history})

@app.route('/api/history/conversation')
def get_conversation_history():
    """Get AI conversation history"""
    if not empath_interface:
        return jsonify({'error': 'EMPATH not initialized'}), 400
    
    history = empath_interface.get_conversation_history()
    return jsonify({'conversation': history})

@app.route('/api/memories')
def get_memories():
    """Get AI subject's memories"""
    if not empath_interface:
        return jsonify({'error': 'EMPATH not initialized'}), 400
    
    limit = request.args.get('limit', 20, type=int)
    memories = empath_interface.empath_interface.subject.get_memories(limit)
    
    return jsonify({'memories': memories})

@app.route('/api/export')
def export_data():
    """Export all EMPATH data including AI conversations"""
    if not empath_interface:
        return jsonify({'error': 'EMPATH not initialized'}), 400
    
    data = empath_interface.export_data()
    return jsonify(data)

@app.route('/api/personality')
def get_personality():
    """Get AI subject's personality traits"""
    if not empath_interface:
        return jsonify({'error': 'EMPATH not initialized'}), 400
    
    personality = empath_interface.empath_interface.subject.personality
    return jsonify({
        'personality': {
            'openness': personality.openness,
            'conscientiousness': personality.conscientiousness,
            'extraversion': personality.extraversion,
            'agreeableness': personality.agreeableness,
            'neuroticism': personality.neuroticism,
            'creativity': personality.creativity,
            'empathy': personality.empathy,
            'curiosity': personality.curiosity,
            'ambition': personality.ambition
        }
    })

if __name__ == '__main__':
    start_empath_background()
    app.run(debug=True, host='0.0.0.0', port=5000)
