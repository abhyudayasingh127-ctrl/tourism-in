# Varanasi Tourism & Smart Trip Planner

Complete full-stack web application built with Python Flask, MySQL, Bootstrap 5, and Leaflet.js.

## Setup Instructions

1. **Initialize MySQL Database:**
   ```bash
   mysql -u root -p < database/schema.sql
   ```

2. **Create Virtual Environment & Install Dependencies:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure Environment:**
   Copy `.env.example` to `.env` and configure your database credentials.

4. **Run Application:**
   ```bash
   python app.py
   ```
   Open browser at `http://127.0.0.1:5000`
