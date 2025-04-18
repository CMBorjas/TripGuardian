# src/summarizer.py
# This module provides a function to generate a human-friendly summary of a trip.

def generate_trip_summary(trip):
    """
    Generate a human-friendly trip summary using simple templating.
    Input: trip dictionary with expected keys.
    Output: natural language string.
    """
    walk_time = trip.get("walk_time", 0)
    bus = trip.get("route_id", "unknown route")
    start_stop = trip.get("stop_name_start", "start stop")
    end_stop = trip.get("stop_name_end", "end stop")
    depart = trip.get("departure_time", "TBD")
    arrive = trip.get("arrival_time", "TBD")
    destination = trip.get("destination", "your destination")

    summary = (
        f"Walk {walk_time} minutes to {start_stop}. "
        f"Take the {bus} bus at {depart}. "
        f"Get off at {end_stop}. "
        f"You’ll arrive at {destination} by {arrive}."
    )

    return summary
