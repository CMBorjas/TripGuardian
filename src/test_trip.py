from datetime import datetime
from src.user_input_planner import plan_trip

graph = {
    "15L": ["A", "B", "C", "D", "E"]
}

results, msg = plan_trip(
    user_start="Florida Station",
    user_end="Nine Mile Station",
    departure_time=datetime.strptime("2025-04-17 17:00", "%Y-%m-%d %H:%M"),
    route_graph=graph,
    weather="Rain",
    user_is_disabled=True
)

print(msg)
print(results[["route_id", "trip_summary", "alert_summary"]])
