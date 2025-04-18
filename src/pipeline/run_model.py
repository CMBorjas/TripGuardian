# run_model.py

import pandas as pd
import numpy as np
import folium

from Ipython.display import Iframe
from scipy.spatial import cKDTree
from sklearn.preprocessing import MinMaxScaler
from data_preprocessing import merge_scores
from src.core.maintenance_risk_score import apply_risk_model

# Setup the base map
denver_map = folium.Map(location=[39.7392, -104.9903], zoom_start=11)

# ---------- Load Input Files ----------
print("📥 Loading data...")
stops_df = pd.read_csv("../data/google_transit/stops.txt", comment='#', encoding='utf-8')
crime_df = pd.read_csv("../data/ODC_CRIME_OFFENSES_P_-3254178225590307312.csv")
stop_times_df = pd.read_csv("../data/google_transit/stop_times.txt", comment='#')

# ---------- Preprocess Stops and Crime ----------
stops_df = stops_df[['stop_id', 'stop_lat', 'stop_lon']].dropna()
crime_df = crime_df[['GEO_LAT', 'GEO_LON']].dropna()

# ---------- Convert Lat/Lon to Meters ----------
def latlon_to_xy(lat, lon):
    R = 6371000  # Earth's radius in meters
    x = np.radians(lon) * R * np.cos(np.radians(lat))
    y = np.radians(lat) * R
    return np.column_stack((x, y))

stop_coords = latlon_to_xy(stops_df['stop_lat'].values, stops_df['stop_lon'].values)
crime_coords = latlon_to_xy(crime_df['GEO_LAT'].values, crime_df['GEO_LON'].values)

# ---------- Build KDTree and Count Crimes Near Each Stop ----------
print("🧠 Calculating crime scores...")
tree = cKDTree(crime_coords)
crime_radius_m = 100  # meters

crime_counts = tree.query_ball_point(stop_coords, r=crime_radius_m)
crime_scores = [{'stop_id': sid, 'crime_score': len(matches)}
                for sid, matches in zip(stops_df['stop_id'], crime_counts)]

crime_scores_df = pd.DataFrame(crime_scores)

# ---------- Real Schedule Score from stop_times.txt ----------
print("📅 Calculating schedule scores from stop_times.txt...")
schedule_df = (
    stop_times_df['stop_id']
    .value_counts()
    .reset_index()
    .rename(columns={'index': 'stop_id', 'stop_id': 'stop_frequency'})
)

scaler = MinMaxScaler()
schedule_df['schedule_score'] = scaler.fit_transform(schedule_df[['stop_frequency']])

# Save the map as an HTML file
denver_map.save("denver_map.html")

# Display the map inline
IFrame("denver_map.html", width=800, height=600)

# ---------- Merge and Model ----------
print("📊 Merging scores...")
merged_df = merge_scores(crime_scores_df, schedule_df)

print("⚙️ Applying maintenance risk model...")
risk_df = apply_risk_model(merged_df)

# ---------- Output ----------
risk_df.to_csv("maintenance_risk_scores.csv", index=False)
print("✅ Maintenance risk scores written to maintenance_risk_scores.csv")
