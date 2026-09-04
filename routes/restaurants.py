from flask import Blueprint, request, jsonify, session
from models.restaurant import Restaurant

restaurants_bp = Blueprint('restaurants_bp', __name__)

@restaurants_bp.route('/api/restaurants', methods=['GET'])
def get_restaurants():
    restaurants = Restaurant.get_all()
    return jsonify({'restaurants': restaurants}), 200

@restaurants_bp.route('/api/restaurants', methods=['POST'])
def create_restaurant():
    if not session.get('is_admin'):
        return jsonify({'error': 'Admin privilege required'}), 403
    data = request.get_json()
    rest_id = Restaurant.create(data)
    return jsonify({'message': 'Restaurant created successfully', 'restaurant_id': rest_id}), 201
