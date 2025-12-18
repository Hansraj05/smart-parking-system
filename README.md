# 🚗 Smart Parking System (Cloud-Deployed)

An AI-powered, full-stack geospatial application that predicts parking availability using real-time user telemetry and Machine Learning.

**🌍 Live Demo:** [INSERT_YOUR_GITHUB_PAGES_LINK_HERE]  
**⚙️ Backend API:** [INSERT_YOUR_RENDER_URL_HERE]

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

## 📥 Installation & Setup
To run this project locally:

1. **Clone the repo:**
   ```bash
   git clone [https://github.com/Hansraj05/smart-parking-system.git](https://github.com/Hansraj05/smart-parking-system.git)
