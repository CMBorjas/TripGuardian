import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pandas as pd
from datetime import datetime
from src.route_finder import find_routes
from src.crowd_predictor import load_model, predict_crowdedness
from src.reranker import rerank_routes
from src.summarizer import generate_trip_summary
from src.accessibility_score import compute_accessibility_score


def plan_trip(user_start, user_end, departure_time, route_graph, weather="Clear", user_is_disabled=False):
    """
    Inputs:
        user_start: string stop name
        user_end: string stop name
        departure_time: datetime object
        route_graph: dict of {route_id: [stop1, stop2, ...]}
        weather: "Clear", "Rainy", "Snowy", etc.
    Returns:
        reranked DataFrame with trip summaries and crowd predictions
    """
    hour_of_day = departure_time.hour
    day_of_week = departure_time.strftime('%A')

    candidate_routes = find_routes(user_start, user_end, route_graph)

    if not candidate_routes:
        return pd.DataFrame(), "❌ No direct route found."

    for route in candidate_routes:
        route["hour_of_day"] = hour_of_day
        route["day_of_week"] = day_of_week
        route["weather"] = weather
        route["walk_time"] = 5  # Placeholder — could be dynamic
        route["delay_minutes"] = 3  # Placeholder — could be live from alerts
        route["user_is_disabled"] = user_is_disabled
        route["safety_score"] = compute_accessibility_score(route)
        route["stop_name_start"] = user_start
        route["stop_name_end"] = user_end
        route["departure_time"] = departure_time.strftime("%I:%M %p").lstrip("0")
        route["arrival_time"] = (
            departure_time.replace(minute=departure_time.minute + route["bus_time"])
            .strftime("%I:%M %p")
            .lstrip("0")
        )
        route["destination"] = user_end
        route["accessibility_score"] = compute_accessibility_score(route)

    df = pd.DataFrame(candidate_routes)

    # Predict crowd level
    model = load_model("models/crowd_model.pkl")
    df["crowdedness_score"] = predict_crowdedness(model, df)
    df["crowdedness_label"] = df["crowdedness_score"].map({0: "🟢 Low", 1: "🟡 Medium", 2: "🔴 High"})

    # Rerank based on ML + user experience preferences
    reranked = rerank_routes(df)

    # Add smart trip summary for UI or dashboard
    reranked["trip_summary"] = reranked.apply(generate_trip_summary, axis=1)

    return reranked, "✅ Trip plan ready!"
