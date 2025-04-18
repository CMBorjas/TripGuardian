from sklearn.ensemble import RandomForestRegressor
import joblib

def train_crowd_model(X, y):
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model

def save_model(model, path="models/crowd_model.pkl"):
    joblib.dump(model, path)

def load_model(path="models/crowd_model.pkl"):
    return joblib.load(path)
