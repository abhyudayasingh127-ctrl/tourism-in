from flask import Blueprint, request, jsonify, session
from models.user import User

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/api/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    if not data.get('email') or not data.get('password') or not data.get('name'):
        return jsonify({'error': 'Name, Email, and Password are required'}), 400
    try:
        user_id = User.create(data['name'], data['email'], data['password'], data.get('phone', ''))
        session['user_id'] = user_id
        return jsonify({'message': 'User registered successfully', 'user_id': user_id}), 201
    except Exception as e:
        return jsonify({'error': 'Email already exists or invalid data'}), 400

@auth_bp.route('/api/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    user = User.get_by_email(data.get('email'))
    if user and User.verify_password(user['password_hash'], data.get('password', '')):
        session['user_id'] = user['id']
        session['is_admin'] = user['is_admin']
        return jsonify({
            'message': 'Login successful',
            'user': {'id': user['id'], 'name': user['name'], 'email': user['email'], 'is_admin': user['is_admin']}
        }), 200
    return jsonify({'error': 'Invalid credentials'}), 401

@auth_bp.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logged out successfully'}), 200

@auth_bp.route('/api/profile', methods=['GET'])
def profile():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    user = User.get_by_id(user_id)
    return jsonify({'user': user}), 200
