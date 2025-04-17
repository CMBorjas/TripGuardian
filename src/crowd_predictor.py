import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib

def prepare_data(df):
    df_encoded = df.copy()
    df_encoded["route_id"] = df["route_id"].astype("category").cat.codes
    df_encoded["day_of_week"] = df["day_of_week"].astype("category").cat.codes
    df_encoded["crowdedness"] = df["crowdedness"].map({"Low": 0, "Medium": 1, "High": 2})
    X = df_encoded[["route_id", "hour_of_day", "day_of_week"]]
    y = df_encoded["crowdedness"]
    return train_test_split(X, y, test_size=0.2, random_state=42)

def train_model(X_train, y_train):
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    return clf

def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))

def save_model(model, path="models/crowd_model.pkl"):
    joblib.dump(model, path)

def load_model(path="models/crowd_model.pkl"):
    return joblib.load(path)

def predict_crowdedness(model, df):
    df_encoded = df.copy()
    df_encoded["route_id"] = df["route_id"].astype("category").cat.codes
    df_encoded["day_of_week"] = df["day_of_week"].astype("category").cat.codes
    X = df_encoded[["route_id", "hour_of_day", "day_of_week"]]
    return model.predict(X)
