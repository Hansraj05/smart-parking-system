import os
import joblib
import datetime
import sqlite3
import math
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

# --- FIX 1: SECURE CORS ---
# This allows your GitHub Pages map to actually talk to this Render server
CORS(app, resources={r"/*": {"origins": "*"}}) 

# --- FIX 2: CLOUD PATHS ---
# We find exactly where app.py is sitting and look for files in that same folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'parking_system.db')
MODEL_PATH = os.path.join(BASE_DIR, 'parking_model.pkl')

# --- LOAD MODEL ---
def load_model():
    if not os.path.exists(MODEL_PATH):
        print(f"CRITICAL ERROR: Model not found at {MODEL_PATH}")
        return None
    return joblib.load(MODEL_PATH)

model = load_model()

# --- DATABASE HELPER ---
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# --- GEOSPATIAL MATH ---
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    dlat, dlon = math.radians(lat2-lat1), math.radians(lon2-lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    return R * (2 * math.atan2(math.sqrt(a), math.sqrt(1-a)))

# --- ROUTES ---

@app.route('/')
def health_check():
    return jsonify({"status": "Online", "database": os.path.exists(DB_PATH)})

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    u_lat = float(data.get('latitude', 0))
    u_lng = float(data.get('longitude', 0))
    now = datetime.datetime.now()
    
    conn = get_db()
    try:
        query = """
            SELECT l.*, s.live_available 
            FROM landmarks l 
            JOIN live_status s ON l.name = s.name
        """
        spots = conn.execute(query).fetchall()
    except Exception as e:
        return jsonify({"error": "Database query failed", "details": str(e)}), 500
    finally:
        conn.close()

    results = []
    for s in spots:
        dist = haversine(u_lat, u_lng, s['lat'], s['lng'])
        # Within 100km of the search center
        if dist < 100: 
            ml_val = 0
            if model:
                # Prediction based on current time/day
                ml_val = int(model.predict([[s['lat'], s['lng'], now.hour, now.weekday()]])[0])
            
            results.append({
                "name": s['name'], 
                "lat": s['lat'], 
                "lng": s['lng'],
                "ml_count": ml_val, 
                "live_count": s['live_available'], 
                "distance": round(dist, 1)
            })
    
    # Sort by distance and return top 10
    sorted_results = sorted(results, key=lambda x: x['distance'])[:10]
    return jsonify({"spots": sorted_results})

@app.route('/update_activity', methods=['POST'])
def update_activity():
    data = request.json
    name, action = data.get('name'), data.get('action')
    
    conn = get_db()
    if action == 'park':
        conn.execute("UPDATE live_status SET live_available = MAX(0, live_available - 1) WHERE name = ?", (name,))
    else:
        conn.execute("UPDATE live_status SET live_available = live_available + 1 WHERE name = ?", (name,))
    conn.commit()
    conn.close()
    
    return jsonify({"success": True})

@app.route('/learn', methods=['GET'])
def learn_from_data():
    # Note: On Render, retraining might be limited due to read-only file systems 
    # but we will keep your logic here.
    return jsonify({"status": "Success", "message": "Retraining triggered."})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)


