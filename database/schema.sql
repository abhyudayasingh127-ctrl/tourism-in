CREATE DATABASE IF NOT EXISTS varanasi_tourism;
USE varanasi_tourism;

-- Users Table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tourist Places Table
CREATE TABLE IF NOT EXISTS tourist_places (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    description TEXT NOT NULL,
    category VARCHAR(50) NOT NULL,
    location VARCHAR(200) NOT NULL,
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL,
    visiting_hours VARCHAR(100) NOT NULL,
    estimated_duration VARCHAR(50) NOT NULL,
    image_url VARCHAR(255) NOT NULL
);

-- Hotels Table
CREATE TABLE IF NOT EXISTS hotels (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    location VARCHAR(200) NOT NULL,
    price_range VARCHAR(50) NOT NULL,
    rating DECIMAL(2, 1) DEFAULT 4.0,
    facilities TEXT NOT NULL,
    contact VARCHAR(50) NOT NULL,
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL
);

-- Restaurants Table
CREATE TABLE IF NOT EXISTS restaurants (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    location VARCHAR(200) NOT NULL,
    cuisine VARCHAR(100) NOT NULL,
    price_range VARCHAR(50) NOT NULL,
    rating DECIMAL(2, 1) DEFAULT 4.5,
    contact VARCHAR(50) NOT NULL,
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL
);

-- Trips Table
CREATE TABLE IF NOT EXISTS trips (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    trip_name VARCHAR(150) NOT NULL,
    start_date DATE NOT NULL,
    number_of_days INT NOT NULL,
    budget VARCHAR(50),
    interests VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Trip Places Junction Table
CREATE TABLE IF NOT EXISTS trip_places (
    id INT AUTO_INCREMENT PRIMARY KEY,
    trip_id INT NOT NULL,
    place_id INT NOT NULL,
    day_number INT NOT NULL,
    visit_order INT NOT NULL,
    FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE CASCADE,
    FOREIGN KEY (place_id) REFERENCES tourist_places(id) ON DELETE CASCADE
);

-- Favorites Table
CREATE TABLE IF NOT EXISTS favorites (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    place_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (place_id) REFERENCES tourist_places(id) ON DELETE CASCADE,
    UNIQUE KEY user_place_unique (user_id, place_id)
);

-- Seed Data: Tourist Places
INSERT INTO tourist_places (name, description, category, location, latitude, longitude, visiting_hours, estimated_duration, image_url) VALUES
('Kashi Vishwanath Temple', 'One of the most famous Hindu temples dedicated to Lord Shiva, located on the western bank of the holy river Ganga.', 'Temple', 'Lahori Tola, Varanasi', 25.3109, 83.0107, '4:00 AM - 11:00 PM', '2 Hours', 'https://images.unsplash.com/photo-1561361513-2d000a50f0dc?auto=format&fit=crop&w=600&q=80'),
('Dashashwamedh Ghat', 'The main and most spectacular ghat on the Ganges River, famous for its magnificent evening Ganga Aarti.', 'Ghat', 'Dashashwamedh Ghat Rd, Varanasi', 25.3072, 83.0103, 'Open 24 Hours (Aarti at 6:45 PM)', '1.5 Hours', 'https://images.unsplash.com/photo-1571536802807-30451e3955d8?auto=format&fit=crop&w=600&q=80'),
('Assi Ghat', 'The southernmost ghat in Varanasi, popular for morning yoga, cultural performances, and peaceful boat rides.', 'Ghat', 'Assi Ghat, Shivala, Varanasi', 25.2882, 82.9998, 'Open 24 Hours (Subah-e-Banaras at 5:00 AM)', '2 Hours', 'https://images.unsplash.com/photo-1609949279531-cf48d64bed89?auto=format&fit=crop&w=600&q=80'),
('Sarnath', 'A revered Buddhist pilgrimage site located 10 km from Varanasi where Gautama Buddha first taught the Dhamma.', 'Historical', 'Sarnath, Varanasi', 25.3811, 83.0214, '8:00 AM - 6:00 PM', '3 Hours', 'https://images.unsplash.com/photo-1627894483216-2138af692e32?auto=format&fit=crop&w=600&q=80'),
('Banaras Hindu University (BHU)', 'A premier public central university featuring the famous New Vishwanath Temple (VT) and Bharat Kala Bhavan museum.', 'Cultural', 'Lanka, Varanasi', 25.2677, 82.9913, '4:00 AM - 12:00 PM, 1:00 PM - 9:00 PM', '2 Hours', 'https://images.unsplash.com/photo-1590050752117-238cb0fb12b1?auto=format&fit=crop&w=600&q=80');

-- Seed Data: Hotels
INSERT INTO hotels (name, location, price_range, rating, facilities, contact, latitude, longitude) VALUES
('BrijRama Palace', 'Darbhanga Ghat, Dashashwamedh', '₹15,000 - ₹30,000', 4.8, 'Free WiFi, River View, Spa, Fine Dining', '+91 542 245 6100', 25.3045, 83.0112),
('Ganges View Hotel', 'Assi Ghat, Varanasi', '₹4,000 - ₹8,000', 4.5, 'AC, Free Breakfast, Roof Terrace, Library', '+91 542 231 3218', 25.2889, 83.0002),
('Hotel Surya, Kaiser Palace', 'Cantonment, Varanasi', '₹3,500 - ₹7,000', 4.3, 'Swimming Pool, Spa, Gardens, Parking', '+91 542 250 8466', 25.3331, 82.9832);

-- Seed Data: Restaurants
INSERT INTO restaurants (name, location, cuisine, price_range, rating, contact, latitude, longitude) VALUES
('Kashi Chat Bhandar', 'Godowlia Chowk, Varanasi', 'Street Food, Chaat, Indian', '₹100 - ₹300', 4.7, '+91 98390 64808', 25.3101, 83.0065),
('Pizzeria Vaatika Cafe', 'Assi Ghat, Varanasi', 'Italian, Pizza, Desserts', '₹400 - ₹800', 4.5, '+91 542 231 0249', 25.2885, 83.0001),
('Blue Lassi Shop', 'Kachauri Gali, Chowk', 'Lassi, Indian Sweets', '₹80 - ₹200', 4.6, '+91 93369 11626', 25.3122, 83.0115);

-- Default Admin User (Password: admin123)
INSERT INTO users (name, email, password_hash, is_admin) VALUES
('Admin', 'admin@kashi.com', 'scrypt:32768:8:1$uH3dZb62s3kH2lZJ$6e02a9b6c0e5a8f4b00512fdb1f0d3b6641e7f60742d131f4a4768ad1d50c60ed7121774026330fb3984d4b1a4a4f8ad2fdfb99f2a969bf1bb10bb073fbb39d4', TRUE);
