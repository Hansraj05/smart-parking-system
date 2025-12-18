# 🚗 Smart Parking System (Cloud-Deployed)

An AI-powered, full-stack geospatial application that predicts parking availability using real-time user telemetry and Machine Learning.

**🌍 Live Demo:** [https://hansraj05.github.io/smart-parking-system/]  
**⚙️ Backend API:** [https://smart-parking-system-8.onrender.com/]

---

## 🌟 Overview
Traditional parking apps rely on expensive sensors. This project implements a **Crowdsourced Intelligence** model, using GPS geofencing and historical data to predict spot availability. It features a decoupled architecture with a Python/Flask microservice and a lightweight Leaflet.js frontend.

## 🚀 Key Features
* **Real-time Prediction:** Uses a Random Forest Regressor to forecast occupancy based on time, day, and location.
* **Geospatial Search:** Integrated OpenStreetMap (Nominatim) API for global city searches.
* **Live Handshake:** Real-time "Park/Unpark" updates that synchronize with a persistent SQLite database.
* **Haversine Logic:** Custom mathematical implementation to calculate distances between user coordinates and urban landmarks.
* **Autonomous Learning:** Built-in retraining loop to merge new crowdsourced data points into the ML model.

## 🛠️ Tech Stack
| Component | Technology |
| :--- | :--- |
| **Frontend** | JavaScript (ES6+), Leaflet.js, OpenStreetMap API, CSS3 |
| **Backend** | Python, Flask, Gunicorn |
| **Machine Learning** | Scikit-Learn (Random Forest), Pandas, Joblib |
| **Database** | SQLite3 |
| **DevOps** | Render (PaaS), GitHub Pages (CDN), CORS Management |



## 🏗️ Architecture
The system uses a **Decoupled Microservices Architecture**:
1.  **Client Tier:** Hosted on GitHub Pages. It handles user interaction and geospatial rendering.
2.  **Logic Tier:** A Flask API hosted on Render. It processes Haversine calculations and ML inferences.
3.  **Data Tier:** A persistent SQLite engine that tracks live occupancy states.




## ⚖️ Competitive Analysis: Why this is Different
Most commercial parking solutions (e.g., SpotHero, ParkMe) rely on static data or expensive IoT hardware. This project addresses the "Infrastructure Gap" through:
* **Infrastructure-Less Intelligence:** Eliminates the need for \$500+ ground sensors per spot by utilizing user GPS telemetry as the primary data source.
* **Predictive vs. Reactive:** While Google Maps shows "Live Busyness," this system uses a Random Forest Regressor to predict occupancy for specific future time-slots, enabling proactive trip planning.
* **Low Latency Handshake:** By decoupling the Flask ML engine from the Leaflet UI, the system achieves sub-200ms response times for geospatial queries.

## 🔮 Future Scope & Scalability
This project is designed as a **Headless API**, allowing for seamless expansion:
1. **Mobile Integration:** The Render backend can serve as the data layer for a React Native or Flutter mobile app.
2. **Computer Vision Fusion:** Integrating OpenCV to process city traffic camera feeds to verify crowdsourced data.
3. **Dynamic Pricing Logic:** Implementing a "Surge Pricing" algorithm based on ML-predicted demand to optimize urban parking distribution.
4. **Auto-Geofencing:** Implementing Background Geolocation API to automatically "unpark" users when their GPS coordinates move 50m away from a marker.
## 📥 Installation & Setup
To run this project locally:

1. **Clone the repo:**
   ```bash
   git clone [https://github.com/Hansraj05/smart-parking-system.git](https://github.com/Hansraj05/smart-parking-system.git)
