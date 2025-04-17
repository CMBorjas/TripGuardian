# src/accesibility_score.py

def compute_accessibility_score(route):
    """
    Assigns an accessibility score(0-100) based on route features and known issues.

    Example penalty logic:
    - working elevators: +30 points
    - out-of-service elevators: -30 points
    - Cronstruction: -20 points
    - long walk times: -15 if > 0.5 miles (walk_time > 8 minutes)
    - Shuttle replacement: -10 points
    """

    score = 100  # Start with a perfect score

    # Simulate known elevator outages

    elevator_outages = ["Florida Station","Nine Mile Station"]
    construction_zones = ["Perry Station", "Table Mesa Park-n-Ride"]

    # Station names in this route
    start = route.get("stop_name_start","").lower()
    end = route.get("stop_name_end","").lower()

    # Check for elevator issues
    for station in elevator_outages:
        if station.lower() in start or station.lower() in end:
            score -= 30

    # Check for construction zones
    for station in construction_zones:
        if station.lower() in start or station.lower() in end:
            score -= 20

    #simulated long walking penalty
    if route.get("walk_time", 0) > 8:
        score -= 15

    #placeholder for shuttle service penalty
    if "shuttle" in route.get("route_id", "").lower():
        score -= 10

    return max(score, 0)  # Ensure score doesn't go below 0