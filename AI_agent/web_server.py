"""Flask web server for the AI chatbot"""
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from agent.config import load_config
from agent.controller import AgentController
import threading
import base64
import io
import wave
import uuid
from datetime import datetime, timezone

app = Flask(__name__)
CORS(app)

# Initialize the agent
config = load_config()
controller = AgentController(config)

# Store conversation history
conversation_history = []
# Store task history for UI
task_history = []

WAITING_STATUSES = {
    'login_required',
    'awaiting_login',
    'missing_recipient',
    'missing_body',
    'needs_review',
    'manual_required',
}

RUNNING_STATUSES = {
    'opened',
    'portal_opened',
    'form_filled',
    'manual',
    'submission_ready',
}


def _status_from_result(result):
    data = result.data or {}
    status = data.get('status', '')
    if status in WAITING_STATUSES:
        return 'waiting'
    if status in RUNNING_STATUSES:
        return 'running'
    return 'done' if result.success else 'error'


def _title_from_message(message: str) -> str:
    title = message.strip()
    if len(title) > 48:
        return title[:45].rstrip() + '...'
    return title or 'New task'


def _upsert_task(user_message: str, result):
    if not result:
        return None
    data = result.data or {}
    task_id = data.get('task_id') or str(uuid.uuid4())
    title = data.get('task_title') or _title_from_message(user_message)
    status = _status_from_result(result)
    detail = data.get('task_detail') or (result.message.splitlines()[0] if result.message else '')
    task = {
        'id': task_id,
        'title': title,
        'status': status,
        'detail': detail,
        'updated_at': datetime.now(timezone.utc).isoformat()
    }

    for idx, existing in enumerate(task_history):
        if existing['id'] == task_id:
            task_history[idx].update(task)
            return task_history[idx]

    task_history.insert(0, task)
    return task


@app.route('/')
def index():
    """Serve the main chatbot page"""
    return render_template('chatbot.html')


@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle text chat messages"""
    try:
        data = request.json
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Empty message'}), 400
        
        # Process the message
        response, result = controller.handle_text(user_message, speak_response=False, return_result=True)
        
        # Store in history
        conversation_history.append({
            'user': user_message,
            'agent': response
        })

        task_entry = _upsert_task(user_message, result)
        
        return jsonify({
            'success': True,
            'response': response,
            'task': task_entry,
            'timestamp': None
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/voice', methods=['POST'])
def voice():
    """Handle voice input"""
    try:
        # Get audio data from request
        audio_data = request.files.get('audio')
        
        if not audio_data:
            return jsonify({'error': 'No audio data'}), 400
        
        # For now, return a message that voice processing is available
        # In production, you'd process the audio here
        return jsonify({
            'success': True,
            'text': 'Voice processing available - use microphone button',
            'response': 'Please use the microphone button in the interface'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/tts', methods=['POST'])
def text_to_speech():
    """Convert text to speech"""
    try:
        data = request.json
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Speak the text
        controller.speech_engine.speak(text, async_mode=False)
        
        return jsonify({
            'success': True,
            'message': 'Speech played'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/status', methods=['GET'])
def status():
    """Get system status"""
    try:
        speech_status = controller.speech_engine.get_status()
        
        return jsonify({
            'success': True,
            'status': {
                'voice_enabled': config.voice_enabled,
                'tts_enabled': config.tts_enabled,
                'stt_available': speech_status['stt_enabled'],
                'tts_available': speech_status['tts_enabled'],
                'microphone_available': speech_status['microphone_available']
            }
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/history', methods=['GET'])
def history():
    """Get conversation history"""
    return jsonify({
        'success': True,
        'history': conversation_history
    })


@app.route('/api/tasks', methods=['GET'])
def tasks():
    """Get task history for UI"""
    return jsonify({
        'success': True,
        'tasks': task_history
    })


@app.route('/api/clear', methods=['POST'])
def clear():
    """Clear conversation history"""
    global conversation_history
    conversation_history = []
    task_history.clear()
    controller.workflow_state.reset()
    
    return jsonify({
        'success': True,
        'message': 'History cleared'
    })


if __name__ == '__main__':
    print("="*70)
    print("Starting Web Chatbot Server")
    print("="*70)
    print("\nSystem Status:")
    print(f"  - Voice Input: {'Enabled' if config.voice_enabled else 'Disabled'}")
    print(f"  - Voice Output: {'Enabled' if config.tts_enabled else 'Disabled'}")
    print("\nAccess the chatbot at:")
    print("  http://localhost:5000")
    print("\nPress Ctrl+C to stop the server")
    print("="*70 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
