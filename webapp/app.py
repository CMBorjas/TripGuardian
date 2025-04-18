import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask, render_template, request
import pandas as pd
import numpy as np
from src.utils.io_utils import load_model
import folium
from folium.plugins import MarkerCluster
import logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Load the model
model = load_model(os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')), 'notebooks/core/crowdedness_model.pkl'))

# Correct the path to the CSV file
csv_path = os.path.join(os.path.dirname(__file__), "..", "notebooks", "crowdedness_train.csv")

# Dummy stop data for demo
stops_df = pd.read_csv(csv_path, low_memory=False)

@app.route("/", methods=["GET", "POST"])
def index():
    logging.debug("Request received at the root route")

    prediction = None
    if request.method == "POST":
        hour = int(request.form["hour"])
        route_type = int(request.form["route_type"])
        input_df = pd.DataFrame([[hour, route_type]], columns=["hour", "route_type"])
        prediction = model.predict(input_df)[0]
        logging.debug(f"Prediction: {prediction}")

    # Generate map
    stops_df['predicted'] = model.predict(stops_df[['hour', 'route_type']])
    logging.debug("Map is being generated")

    # Ensure static directory exists
    static_dir = os.path.join(os.getcwd(), 'webapp', 'static')
    os.makedirs(static_dir, exist_ok=True)

    # Define map_path
    map_path = os.path.join(static_dir, "crowdedness_map.html")

    # Generate the map and save it
    m = folium.Map(location=[39.7392, -104.9903], zoom_start=11)
    cluster = MarkerCluster().add_to(m)
    
    for _, row in stops_df.iterrows():
        color = 'green' if row['predicted'] < 0.3 else 'orange' if row['predicted'] < 0.6 else 'red'
        folium.CircleMarker(
            location=[row['stop_lat'], row['stop_lon']],
            radius=5,
            popup=f"{row['stop_name']} - {row['predicted']:.2f}",
            color=color,
            fill=True,
            fill_opacity=0.7
        ).add_to(cluster)

    m.save(map_path)
    logging.debug(f"Map saved to {map_path}")

    return render_template("index.html", prediction=prediction)

if __name__ == "__main__":
    app.run(debug=True)
