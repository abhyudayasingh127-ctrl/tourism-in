from flask import Blueprint, request, jsonify
from services.crowd_detector import analyze_crowd_density
from services.chatbot import get_ai_bot_response

ai_services_bp = Blueprint('ai_services', __name__)

# AI Chatbot Endpoint
@ai_services_bp.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_msg = data.get('message', '')
    history = data.get('history', [])
    
    if not user_msg:
        return jsonify({"error": "Message is required"}), 400
        
    reply = get_ai_bot_response(user_msg, history)
    return jsonify({"response": reply})

# Crowd Detection Endpoint
@ai_services_bp.route('/api/detect-crowd', methods=['POST'])
def detect_crowd():
    if 'file' not in request.files:
        return jsonify({"error": "No image file provided"}), 400
        
    file = request.files['file']
    file_path = f"/tmp/{file.filename}"
    file.save(file_path)
    
    result = analyze_crowd_density(file_path)
    return jsonify(result)

# Lightweight Quick Budget Estimator Endpoint
@ai_services_bp.route('/api/quick-budget', methods=['POST'])
def calculate_budget():
    """Calculates live cost breakdown and taxes without server latency."""
    data = request.get_json() or {}
    items = data.get('items', [])
    
    total_cost = sum(item.get('price', 0) for item in items)
    estimated_tax = total_cost * 0.05
    
    return jsonify({
        'status': 'success',
        'subtotal': total_cost,
        'tax': estimated_tax,
        'grand_total': total_cost + estimated_tax
    }), 200
