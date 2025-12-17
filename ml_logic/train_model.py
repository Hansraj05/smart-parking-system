from sklearn.ensemble import RandomForestRegressor
import pandas as pd
import joblib
import os

def train():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, '..', 'dataset', 'parking_data.csv')
    
    if not os.path.exists(data_path):
        print("❌ CSV not found. Run data_gen.py first.")
        return

    df = pd.read_csv(data_path)
    X = df[['lat', 'lng', 'hour', 'day']]
    y = df['available_spots']
    
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    joblib.dump(model, os.path.join(current_dir, 'parking_model.pkl'))
    print("✅ Created parking_model.pkl in ml_logic folder.")

if __name__ == "__main__":
    train()