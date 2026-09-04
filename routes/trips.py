from flask import Blueprint, request, jsonify, session
from models.trip import Trip
from models.place import Place
from models.hotel import Hotel
from models.restaurant import Restaurant

trips_bp = Blueprint('trips_bp', __name__)

@trips_bp.route('/api/trips', methods=['POST'])
def generate_and_save_trip():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Unauthorized. Please login to save trips.'}), 401

    data = request.get_json() or {}
    days = int(data.get('number_of_days', 1))
    trip_name = data.get('trip_name', f'{days}-Day Varanasi Experience')
    start_date = data.get('start_date')
    budget = data.get('budget', 'Moderate')
    
    # Frontend se budget_amount extract kiya aur float me convert kiya
    raw_budget_amount = data.get('budget_amount', 0)
    try:
        budget_amount = float(raw_budget_amount) if raw_budget_amount else 0.0
    except ValueError:
        budget_amount = 0.0

    interests = data.get('interests', 'General')

    # ==========================================
    # BUDGET ALLOCATION LOGIC (Hotel, Food, Boat)
    # ==========================================
    allocated_hotel_cost = round(budget_amount * 0.45, 2)
    allocated_food_cost = round(budget_amount * 0.35, 2)
    allocated_boat_cost = round(budget_amount * 0.20, 2)

    # Daily Price Limits Calculate kiye
    max_hotel_price = allocated_hotel_cost / days if days > 0 else allocated_hotel_cost
    max_food_price = allocated_food_cost / days if days > 0 else allocated_food_cost

    # Filtered Items from Database (Budget ke hisab se)
    all_hotels = Hotel.get_all() if hasattr(Hotel, 'get_all') else []
    all_restaurants = Restaurant.get_all() if hasattr(Restaurant, 'get_all') else []
    all_places = Place.get_all() if hasattr(Place, 'get_all') else []

    # Budget Range ke mutabiq filtering
    suggested_hotels = [h for h in all_hotels if float(h.get('price_per_night', 0)) <= max_hotel_price] if budget_amount > 0 else all_hotels
    suggested_restaurants = [r for r in all_restaurants if float(r.get('avg_price', 0)) <= max_food_price] if budget_amount > 0 else all_restaurants
    
    # Boat rides filtering (Category 'boat' ya 'boat_ride')
    suggested_boats = [p for p in all_places if p.get('category', '').lower() in ['boat', 'boat_ride', 'boating']]

    # Place Assignments Logic
    place_assignments = []
    if all_places:
        for i, place in enumerate(all_places):
            day_number = (i % days) + 1
            visit_order = (i // days) + 1
            place_assignments.append({
                'place_id': place['id'],
                'day_number': day_number,
                'visit_order': visit_order
            })

    # Trip.create_trip me parameters pass kiye
    trip_id = Trip.create_trip(
        user_id=user_id, 
        trip_name=trip_name, 
        start_date=start_date, 
        days=days, 
        budget=budget, 
        budget_amount=budget_amount, 
        interests=interests, 
        place_assignments=place_assignments
    )
    
    return jsonify({
        'message': 'Trip created successfully', 
        'trip_id': trip_id,
        'budget_breakdown': {
            'total_budget': budget_amount,
            'hotel_allocation': allocated_hotel_cost,
            'food_allocation': allocated_food_cost,
            'boat_allocation': allocated_boat_cost
        },
        'suggestions': {
            'hotels': suggested_hotels,
            'restaurants': suggested_restaurants,
            'boats': suggested_boats
        }
    }), 201

@trips_bp.route('/api/trips', methods=['GET'])
def get_user_trips():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    trips = Trip.get_by_user(user_id)
    return jsonify({'trips': trips}), 200
