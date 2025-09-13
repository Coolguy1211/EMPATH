"""
EMPATH Web Interface
A Flask-based web application for observing and influencing the AI subject
"""

from flask import Flask, render_template, request, jsonify, session
import json
import time
import threading
from datetime import datetime
from empath import EMPATHInterface, InfluenceType, SubjectState
import uuid

app = Flask(__name__)
app.secret_key = 'empath_secret_key_2024'

# Global EMPATH instance
empath_interface = None
empath_thread = None

def start_empath_background():
    """Start EMPATH in background thread"""
    global empath_interface, empath_thread
    
    if empath_interface is None:
        empath_interface = EMPATHInterface()
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
    return render_template('index.html')

@app.route('/api/status')
def get_status():
    """Get current status of the AI subject"""
    if not empath_interface:
        return jsonify({'error': 'EMPATH not initialized'}), 400
    
    observation = empath_interface.get_current_observation()
    memories = empath_interface.subject.get_memories(5)
    
    return jsonify({
        'observation': observation,
        'memories': memories,
        'active_influences': len(empath_interface.subject.active_influences),
        'total_observations': len(empath_interface.observations),
        'total_influences': len(empath_interface.influences_applied)
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

@app.route('/api/history/observations')
def get_observation_history():
    """Get observation history"""
    if not empath_interface:
        return jsonify({'error': 'EMPATH not initialized'}), 400
    
    limit = request.args.get('limit', 50, type=int)
    history = empath_interface.get_observation_history(limit)
    
    return jsonify({'observations': history})

@app.route('/api/history/influences')
def get_influence_history():
    """Get influence history"""
    if not empath_interface:
        return jsonify({'error': 'EMPATH not initialized'}), 400
    
    limit = request.args.get('limit', 20, type=int)
    history = empath_interface.get_influence_history(limit)
    
    return jsonify({'influences': history})

@app.route('/api/memories')
def get_memories():
    """Get AI subject's memories"""
    if not empath_interface:
        return jsonify({'error': 'EMPATH not initialized'}), 400
    
    limit = request.args.get('limit', 20, type=int)
    memories = empath_interface.subject.get_memories(limit)
    
    return jsonify({'memories': memories})

@app.route('/api/export')
def export_data():
    """Export all EMPATH data"""
    if not empath_interface:
        return jsonify({'error': 'EMPATH not initialized'}), 400
    
    data = empath_interface.export_data()
    return jsonify(data)

@app.route('/api/personality')
def get_personality():
    """Get AI subject's personality traits"""
    if not empath_interface:
        return jsonify({'error': 'EMPATH not initialized'}), 400
    
    personality = empath_interface.subject.personality
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
