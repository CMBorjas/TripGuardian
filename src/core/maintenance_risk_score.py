# maintenance_risk_score.py

import pandas as pd

def calculate_maintenance_risk(row, weights=None):
    """
    Calculate maintenance risk score from normalized components in the row.
    Expected columns: ['crime_score', 'schedule_score']
    """
    if weights is None:
        weights = {
            'crime_score': 0.6,
            'schedule_score': 0.4
        }

    crime = row.get('crime_score', 0)
    schedule = row.get('schedule_score', 0)

    score = (
        weights['crime_score'] * crime +
        weights['schedule_score'] * schedule
    )
    return round(score, 3)


def apply_risk_model(merged_df, weights=None):
    """
    Apply the risk scoring model to each row of the merged dataframe.
    Expects columns: ['stop_id', 'crime_score', 'schedule_score']
    
    Returns:
        DataFrame with ['stop_id', 'risk_score']
    """
    merged_df = merged_df.copy()
    merged_df['risk_score'] = merged_df.apply(
        lambda row: calculate_maintenance_risk(row, weights), axis=1
    )
    return merged_df[['stop_id', 'risk_score']]
