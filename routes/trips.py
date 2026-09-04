# routes/trips.py में यह लॉजिक जोड़ें या अपडेट करें

@trips_bp.route('/plan', methods=['POST'])
def plan_trip():
    data = request.form
    total_budget = float(data.get('budget', 0))
    num_days = int(data.get('days', 1))
    num_people = int(data.get('people', 1))

    # 1. Budget Ratio Breakdown (प्रतिशत विभाजन)
    # Hotel: 45%, Food: 35%, Boat/Activities: 20%
    hotel_budget = total_budget * 0.45
    food_budget = total_budget * 0.35
    boat_budget = total_budget * 0.20

    # 2. Daily Limits Calculate करें
    max_hotel_price_per_night = hotel_budget / num_days
    max_food_price_per_day = food_budget / (num_days * num_people)
    max_boat_price = boat_budget / num_people

    # 3. Database queries से ऐसे ऑप्शन्स निकालें जो बजट में फिट हों
    selected_hotels = Hotel.query.filter(Hotel.price_per_night <= max_hotel_price_per_night).all()
    selected_restaurants = Restaurant.query.filter(Restaurant.avg_price <= max_food_price_per_day).all()
    
    # Boat booking (Places or Activities Table से)
    selected_boats = Place.query.filter(
        Place.category == 'boat', 
        Place.price <= max_boat_price
    ).all()

    return render_template('trip_planner.html', 
                           hotels=selected_hotels, 
                           restaurants=selected_restaurants, 
                           boats=selected_boats, 
                           total_budget=total_budget)
