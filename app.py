import os
import joblib
from flask import Flask, request, jsonify
from flask_cors import CORS  # <--- This is the key library
from datetime import datetime

app = Flask(__name__)

# This line gives the 'Permission Slip' to your GitHub Map
CORS(app, resources={r"/*": {"origins": "https://hansraj05.github.io"}})

# Pathing for the model (flat structure)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'parking_model.pkl')

@app.route('/')
def home():
    return jsonify({
        "status": "Online",
        "message": "CORS Fixed. Hello Hansraj!",
        "allowed_origin": "https://hansraj05.github.io"
    })

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    # Handle the 'Preflight' request browsers send
    if request.method == 'GET':
        return jsonify({"message": "Predict endpoint is ready."})

    try:
        # Mock data for markers - Replace with your actual model logic
        return jsonify({
            "status": "Success",
            "spots": [
                {"name": "Main Gate", "lat": 26.14, "lng": 91.73, "live_count": 8, "ml_count": 10, "distance": 0.2},
                {"name": "Block C", "lat": 26.15, "lng": 91.74, "live_count": 2, "ml_count": 5, "distance": 0.5}
            ]
        })
    except Exception as e:
        return jsonify({"status": "Error", "message": str(e)}), 400

@app.route('/update_activity', methods=['POST'])
def update_activity():
    return jsonify({"status": "Success", "message": "Activity recorded"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

