import sqlite3
import pandas as pd
import joblib
import os
import datetime
from sklearn.ensemble import RandomForestRegressor

def trigger_learning():
    # 1. PATHS
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, '..', 'backend', 'parking_system.db')
    csv_path = os.path.join(base_dir, '..', 'dataset', 'parking_data.csv')
    model_path = os.path.join(base_dir, 'parking_model.pkl')

    # 2. COLLECT LIVE DATA FROM SQL
    if not os.path.exists(db_path):
        print("❌ Database not found. No new data to learn from.")
        return

    conn = sqlite3.connect(db_path)
    # Get current live counts and their locations
    query = """
        SELECT l.name, l.lat, l.lng, s.live_available as available_spots, l.total_capacity
        FROM landmarks l
        JOIN live_status s ON l.name = s.name
    """
    new_data_df = pd.read_sql_query(query, conn)
    conn.close()

    # 3. ADD TIME CONTEXT
    now = datetime.datetime.now()
    new_data_df['hour'] = now.hour
    new_data_df['day'] = now.weekday()

    # 4. APPEND TO HISTORY (The "Learning" part)
    # We add this new "reality" to our old CSV
    old_df = pd.read_csv(csv_path)
    updated_df = pd.concat([old_df, new_data_df], ignore_index=True)
    updated_df.to_csv(csv_path, index=False)

    # 5. RETRAIN THE BRAIN
    print(f"🧠 Learning from {len(new_data_df)} new user reports...")
    X = updated_df[['lat', 'lng', 'hour', 'day']]
    y = updated_df['available_spots']
    
    new_model = RandomForestRegressor(n_estimators=100, random_state=42)
    new_model.fit(X, y)
    
    # Save the smarter brain
    joblib.dump(new_model, model_path)
    print("✅ Model updated with real user behavior!")

if __name__ == "__main__":
    trigger_learning()