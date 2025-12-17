import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_landmark_data():
    city_data = {
        'Guwahati': [
            {'name': 'City Centre Mall', 'lat': 26.152, 'lng': 91.776, 'total': 120},
            {'name': 'Guwahati Railway Station', 'lat': 26.181, 'lng': 91.750, 'total': 300},
            {'name': 'Indira Gandhi Athletic Stadium', 'lat': 26.111, 'lng': 91.761, 'total': 500}
        ],
        'Mumbai': [
            {'name': 'Phoenix Marketcity', 'lat': 19.088, 'lng': 72.882, 'total': 400},
            {'name': 'Gateway of India Parking', 'lat': 18.922, 'lng': 72.834, 'total': 80},
            {'name': 'Chhatrapati Shivaji Terminus', 'lat': 18.940, 'lng': 72.835, 'total': 150}
        ],
        'Delhi': [
            {'name': 'Select CITYWALK', 'lat': 28.528, 'lng': 77.218, 'total': 350},
            {'name': 'Connaught Place', 'lat': 28.631, 'lng': 77.219, 'total': 200},
            {'name': 'India Gate Parking', 'lat': 28.612, 'lng': 77.229, 'total': 100}
        ],
        'Bengaluru': [
            {'name': 'UB City Mall', 'lat': 12.971, 'lng': 77.595, 'total': 200},
            {'name': 'M Chinnaswamy Stadium', 'lat': 12.978, 'lng': 77.599, 'total': 600}
        ]
    }

    data = []
    for _ in range(5000):
        city = np.random.choice(list(city_data.keys()))
        loc = np.random.choice(city_data[city])
        dt = datetime.now() - timedelta(days=np.random.randint(0, 30), hours=np.random.randint(0, 24))
        
        is_weekend = dt.weekday() >= 5
        occ_rate = np.random.uniform(0.8, 0.95) if (is_weekend and "Mall" in loc['name']) else np.random.uniform(0.2, 0.6)
        available = int(loc['total'] * (1 - occ_rate))
        
        data.append([loc['name'], loc['lat'], loc['lng'], dt.hour, dt.weekday(), available, loc['total']])

    df = pd.DataFrame(data, columns=['name', 'lat', 'lng', 'hour', 'day', 'available_spots', 'total_capacity'])
    df.to_csv('parking_data.csv', index=False)
    print(f"✅ Created parking_data.csv in dataset folder.")

if __name__ == "__main__":
    generate_landmark_data()