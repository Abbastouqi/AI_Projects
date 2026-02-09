"""Flask web server for the AI chatbot"""
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from agent.config import load_config
from agent.controller import AgentController
import threading
import base64
import io
import wave

app = Flask(__name__)
CORS(app)

# Initialize the agent
config = load_config()
controller = AgentController(config)

# Store conversation history
conversation_history = []


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
        response = controller.handle_text(user_message, speak_response=False)
        
        # Store in history
        conversation_history.append({
            'user': user_message,
            'agent': response
        })
        
        return jsonify({
            'success': True,
            'response': response,
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


@app.route('/api/clear', methods=['POST'])
def clear():
    """Clear conversation history"""
    global conversation_history
    conversation_history = []
    controller.workflow_state.reset()
    
    return jsonify({
        'success': True,
        'message': 'History cleared'
    })


if __name__ == '__main__':
    print("="*70)
    print("🌐 Starting Web Chatbot Server")
    print("="*70)
    print("\n📊 System Status:")
    print(f"  • Voice Input: {'✅ Enabled' if config.voice_enabled else '❌ Disabled'}")
    print(f"  • Voice Output: {'✅ Enabled' if config.tts_enabled else '❌ Disabled'}")
    print("\n🔗 Access the chatbot at:")
    print("  http://localhost:5000")
    print("\n⚠️ Press Ctrl+C to stop the server")
    print("="*70 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
