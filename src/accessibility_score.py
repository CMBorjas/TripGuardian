# src/accesibility_score.py
def compute_accessibility_score(route):
    score = 100

    elevator_outages = ["Florida Station", "Nine Mile Station"]
    construction_zones = ["Perry Station", "Table Mesa Park-n-Ride"]

    start = route.get("stop_name_start", "").lower()
    end = route.get("stop_name_end", "").lower()

    for station in elevator_outages:
        if station.lower() in start or station.lower() in end:
            score -= 30

    for station in construction_zones:
        if station.lower() in start or station.lower() in end:
            score -= 20

    if route.get("walk_time", 0) > 8:
        score -= 15

    if "shuttle" in route.get("route_id", "").lower():
        score -= 10

    if route.get("weather", "").lower() in ["rain", "snow"]:
        score -= 10

    if route.get("user_is_disabled", False):
        score -= 20
        if route.get("weather", "").lower() in ["rain", "snow"]:
            score -= 10

    return max(score, 0)
