import os
import joblib
import datetime
import sqlite3
import math
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS

# This allows app.py to find the ml_logic folder to trigger retraining
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ml_logic.retrain_loop import trigger_learning

app = Flask(__name__)
CORS(app)

# --- PATHS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'parking_system.db')
MODEL_PATH = os.path.join(BASE_DIR, '..', 'ml_logic', 'parking_model.pkl')

# --- LOAD MODEL ---
def load_model():
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

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    u_lat, u_lng = float(data.get('latitude', 0)), float(data.get('longitude', 0))
    now = datetime.datetime.now()
    
    conn = get_db()
    # Pull data from the persistent SQL tables
    query = """
        SELECT l.*, s.live_available 
        FROM landmarks l 
        JOIN live_status s ON l.name = s.name
    """
    spots = conn.execute(query).fetchall()
    conn.close()

    results = []
    for s in spots:
        dist = haversine(u_lat, u_lng, s['lat'], s['lng'])
        if dist < 100:  # Within 100km
            # ML Model Prediction based on time/day
            ml_val = int(model.predict([[s['lat'], s['lng'], now.hour, now.weekday()]])[0])
            
            results.append({
                "name": s['name'], 
                "lat": s['lat'], 
                "lng": s['lng'],
                "ml_count": ml_val, 
                "live_count": s['live_available'], 
                "distance": round(dist, 1)
            })
    
    # Return top 10 closest landmarks
    return jsonify({"spots": sorted(results, key=lambda x: x['distance'])[:10]})

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
    
    print(f"✅ User reported {action} at {name}. SQL Updated.")
    return jsonify({"success": True})

@app.route('/learn', methods=['GET'])
def learn_from_data():
    """
    SECRET ENDPOINT: Trigger this to merge SQL data into CSV and retrain the model.
    Access this via browser: http://127.0.0.1:5000/learn
    """
    global model
    try:
        trigger_learning() # Calls the retrain_loop.py logic
        model = load_model() # Reload the newly trained brain into memory
        return jsonify({
            "status": "Success", 
            "message": "Model retrained using live crowdsourced data points.",
            "timestamp": str(datetime.datetime.now())
        })
    except Exception as e:
        return jsonify({"status": "Error", "message": str(e)}), 500

if __name__ == '__main__':
    print("🚀 SmartPark Engine Running on http://127.0.0.1:5000")
    app.run(debug=True, port=5000)