from flask import Blueprint, request, jsonify, session
from models.trip import Trip
from models.place import Place

trips_bp = Blueprint('trips_bp', __name__)

@trips_bp.route('/api/trips', methods=['POST'])
def generate_and_save_trip():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Unauthorized. Please login to save trips.'}), 401

    data = request.get_json()
    days = int(data.get('number_of_days', 1))
    trip_name = data.get('trip_name', f'{days}-Day Varanasi Experience')
    start_date = data.get('start_date')
    budget = data.get('budget', 'Moderate')
    interests = data.get('interests', 'General')

    places = Place.get_all()
    place_assignments = []
    
    if places:
        for i, place in enumerate(places):
            day_number = (i % days) + 1
            visit_order = (i // days) + 1
            place_assignments.append({
                'place_id': place['id'],
                'day_number': day_number,
                'visit_order': visit_order
            })

    trip_id = Trip.create_trip(user_id, trip_name, start_date, days, budget, interests, place_assignments)
    return jsonify({'message': 'Trip created successfully', 'trip_id': trip_id}), 201

@trips_bp.route('/api/trips', methods=['GET'])
def get_user_trips():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    trips = Trip.get_by_user(user_id)
    return jsonify({'trips': trips}), 200
