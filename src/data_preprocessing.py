# data_preprocessing.py

import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def normalize_column(df, col_name):
    scaler = MinMaxScaler()
    df[col_name] = scaler.fit_transform(df[[col_name]])
    return df

def merge_scores(crime_df, schedule_df):
    # Normalize both scores
    crime_df = normalize_column(crime_df.copy(), 'crime_score')
    schedule_df = normalize_column(schedule_df.copy(), 'schedule_score')

    # Merge on stop_id
    merged = pd.merge(crime_df, schedule_df, on='stop_id', how='inner')
    return merged
