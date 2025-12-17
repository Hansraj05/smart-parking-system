import sqlite3
import pandas as pd
import os

def setup_database():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(current_dir, '..', 'dataset', 'parking_data.csv')
    db_path = os.path.join(current_dir, 'parking_system.db')

    conn = sqlite3.connect(db_path)
    df = pd.read_csv(csv_path)

    # Landmarks table
    landmarks = df[['name', 'lat', 'lng', 'total_capacity']].drop_duplicates()
    landmarks.to_sql('landmarks', conn, if_exists='replace', index=False)

    # Live status table
    live_status = landmarks[['name']].copy()
    live_status['live_available'] = [int(x * 0.4) for x in landmarks['total_capacity']]
    live_status.to_sql('live_status', conn, if_exists='replace', index=False)

    conn.close()
    print(f"✅ Database created at {db_path}.")

if __name__ == "__main__":
    setup_database()