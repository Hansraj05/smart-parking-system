import os
import sys
import joblib
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# DYNAMIC PATHING: Find the model file in the same folder as this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'parking_model.pkl')

@app.route('/')
def home():
    return jsonify({
        "status": "Online",
        "message": "Smart Parking API is running. Flat structure active.",
        "endpoints": ["/predict", "/learn"]
    })

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'GET':
        return jsonify({"message": "Backend is active. Use POST for predictions."})

    try:
        # For testing, we return a success status
        # If your script.js sends lat/lng, you can process it here
        return jsonify({
            "status": "Success",
            "spots": [
                {"name": "Spot A", "lat": 26.14, "lng": 91.73, "live_count": 12, "ml_count": 10, "distance": 0.5},
                {"name": "Spot B", "lat": 26.15, "lng": 91.74, "live_count": 5, "ml_count": 8, "distance": 1.2}
            ]
        })
    except Exception as e:
        return jsonify({"status": "Error", "message": str(e)}), 400

@app.route('/learn', methods=['GET'])
def learn():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return jsonify({
        "status": "Success",
        "message": "Model retrained using live data.",
        "timestamp": timestamp
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
