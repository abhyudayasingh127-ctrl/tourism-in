from flask import Blueprint, request, jsonify
from services.crowd_detector import analyze_crowd_density
from services.chatbot import get_ai_bot_response

ai_bp = Blueprint('ai', __name__)

# AI Chatbot Endpoint
@ai_bp.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_msg = data.get('message', '')
    history = data.get('history', [])
    
    if not user_msg:
        return jsonify({"error": "Message is required"}), 400
        
    reply = get_ai_bot_response(user_msg, history)
    return jsonify({"response": reply})

# Crowd Detection Endpoint
@ai_bp.route('/api/detect-crowd', methods=['POST'])
def detect_crowd():
    if 'file' not in request.files:
        return jsonify({"error": "No image file provided"}), 400
        
    file = request.files['file']
    file_path = f"/tmp/{file.filename}"
    file.save(file_path)
    
    result = analyze_crowd_density(file_path)
    return jsonify(result)
