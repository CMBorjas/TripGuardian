import pandas as pd
import numpy as np

def generate_synthetic_scores(df):
    np.random.seed(42)
    df['synthetic_crowd_score'] = (
        df['stop_activity'] * 0.4 +
        df['time_of_day_score'] * 0.3 +
        df['weather_score'] * 0.2 +
        np.random.normal(0, 5, size=len(df))
    ).clip(0, 100)
    return df

def extract_features(df):
    return df[['stop_activity', 'time_of_day_score', 'weather_score']]
