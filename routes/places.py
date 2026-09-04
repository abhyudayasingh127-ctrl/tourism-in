from flask import Blueprint, request, jsonify, session
from models.place import Place

places_bp = Blueprint('places_bp', __name__)

@places_bp.route('/api/places', methods=['GET'])
def get_places():
    category = request.args.get('category')
    places = Place.get_all(category)
    return jsonify({'places': places}), 200

@places_bp.route('/api/places/<int:place_id>', methods=['GET'])
def get_place(place_id):
    place = Place.get_by_id(place_id)
    if not place:
        return jsonify({'error': 'Place not found'}), 404
    return jsonify({'place': place}), 200

@places_bp.route('/api/places', methods=['POST'])
def create_place():
    if not session.get('is_admin'):
        return jsonify({'error': 'Admin privilege required'}), 403
    data = request.get_json()
    place_id = Place.create(data)
    return jsonify({'message': 'Place created successfully', 'place_id': place_id}), 201

@places_bp.route('/api/places/<int:place_id>', methods=['DELETE'])
def delete_place(place_id):
    if not session.get('is_admin'):
        return jsonify({'error': 'Admin privilege required'}), 403
    Place.delete(place_id)
    return jsonify({'message': 'Place deleted successfully'}), 200
