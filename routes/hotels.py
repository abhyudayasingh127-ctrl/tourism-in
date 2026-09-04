from flask import Blueprint, request, jsonify, session
from models.hotel import Hotel

hotels_bp = Blueprint('hotels_bp', __name__)

@hotels_bp.route('/api/hotels', methods=['GET'])
def get_hotels():
    hotels = Hotel.get_all()
    return jsonify({'hotels': hotels}), 200

@hotels_bp.route('/api/hotels', methods=['POST'])
def create_hotel():
    if not session.get('is_admin'):
        return jsonify({'error': 'Admin privilege required'}), 403
    data = request.get_json()
    hotel_id = Hotel.create(data)
    return jsonify({'message': 'Hotel created successfully', 'hotel_id': hotel_id}), 201
