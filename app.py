from flask import Flask, render_template, session
from config import Config
from routes.auth import auth_bp
from routes.places import places_bp
from routes.hotels import hotels_bp
from routes.restaurants import restaurants_bp
from routes.trips import trips_bp

app = Flask(__name__)
app.config.from_object(Config)

app.register_blueprint(auth_bp)
app.register_blueprint(places_bp)
app.register_blueprint(hotels_bp)
app.register_blueprint(restaurants_bp)
app.register_blueprint(trips_bp)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/places')
def places():
    return render_template('places.html')

@app.route('/hotels')
def hotels():
    return render_template('hotels.html')

@app.route('/restaurants')
def restaurants():
    return render_template('restaurants.html')

@app.route('/trip-planner')
def trip_planner():
    return render_template('trip_planner.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
