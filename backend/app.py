import os
import joblib
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # This prevents "CORS" errors when your GitHub map talks to Render

# Paths for the model
MODEL_PATH = os.path.join('ml_logic', 'parking_model.pkl')

# 1. Home Route (Prevents the 404 error on your main link)
@app.route('/')
def home():
    return jsonify({
        "status": "Online",
        "message": "Smart Parking API is running. Decoupled Architecture active.",
        "endpoints": ["/predict", "/learn"]
    })

# 2. Prediction Route (Fixed to allow GET so you don't get 'Method Not Allowed')
@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'GET':
        return jsonify({"message": "Use a POST request from the map to get real predictions."})

    try:
        data = request.get_json()
        # Logic to use your model
        if os.path.exists(MODEL_PATH):
            model = joblib.load(MODEL_PATH)
            # Placeholder for your specific prediction logic
            # prediction = model.predict([[data['hour'], data['day']]])
            return jsonify({"status": "Success", "prediction": "Available"})
        else:
            return jsonify({"status": "Error", "message": "Model file not found"}), 500
    except Exception as e:
        return jsonify({"status": "Error", "message": str(e)}), 400

# 3. Learn/Retrain Route
@app.route('/learn', methods=['GET'])
def learn():
    try:
        # Here you would trigger your retrain_loop.py logic
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return jsonify({
            "status": "Success",
            "message": "Model retrained using live crowdsourced data points.",
            "timestamp": timestamp
        })
    except Exception as e:
        return jsonify({"status": "Error", "message": str(e)}), 500

if __name__ == '__main__':
    # Use port provided by Render or default to 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
