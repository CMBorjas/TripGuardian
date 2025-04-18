from alerts import get_route_alerts
import time

# Add more route IDs to this list to expand test coverage
route_ids_to_test = [
    "0", "1", "15", "15L", "20", "30", "44", "45", "46", "120X",
    "228A", "76", "D", "E", "H", "R", "W"
]

print("🚦 Starting route alert scan...\n")

for route_id in route_ids_to_test:
    print(f"🔎 Checking route: {route_id}")
    alerts = get_route_alerts(route_id)
    if alerts:
        print(f"✅ {len(alerts)} alerts found for route {route_id}:")
        for alert in alerts:
            print(f" • {alert['location']} → {alert['message']}")
    else:
        print(f"✔️ No alerts for route {route_id}.")
    
    print("-" * 50)
    
    time.sleep(1.5)  # Optional pause to reduce load on RTD servers
