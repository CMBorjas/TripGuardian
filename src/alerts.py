import os
import json
from datetime import datetime
from playwright.sync_api import sync_playwright

def get_facility_alerts():
    """
    Scrapes the Facilities tab on the RTD Service Alerts page.
    Returns a list of alerts with stop-specific locations.
    """
    alerts = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://app.rtd-denver.com/alerts", timeout=60000)

        # Click the "Facilities" tab
        page.click("text=Facilities")
        page.wait_for_timeout(2000)

        alert_items = page.query_selector_all(".alert-item")
        print(f"📌 Found {len(alert_items)} facility alerts")

        for item in alert_items:
            try:
                title_elem = item.query_selector(".alert-title")
                body_elem = item.query_selector(".alert-body")

                if title_elem and body_elem:
                    location = title_elem.inner_text().strip()
                    message = body_elem.inner_text().strip()
                    alerts.append({
                        "location": location,
                        "message": message
                    })
            except Exception as e:
                print("⚠️ Failed to parse alert:", e)

        if len(alerts) == 0:
            print("🛠 Dumping HTML for debugging...")
            with open("page_dump.html", "w", encoding="utf-8") as f:
                f.write(page.content())

        browser.close()

    return alerts


def get_alerts_for_stop(stop_name):
    """
    Checks if a stop name matches any active facility alerts.
    """
    stop_name = stop_name.lower()
    alerts = get_facility_alerts()

    return [
        alert["message"]
        for alert in alerts
        if stop_name in alert["location"].lower() or stop_name in alert["message"].lower()
    ]

def get_route_alerts(route_id):
    from playwright.sync_api import sync_playwright
    alerts = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        url = f"https://app.rtd-denver.com/route/{route_id}/alerts"
        print(f"🌐 Visiting {url}")
        page.goto(url, timeout=60000)
        page.wait_for_timeout(3000)  # Let content load

        # Select all alert containers
        alert_blocks = page.query_selector_all("div[class^='rtdAlertItem__StyledAlertItem']")

        print(f"📦 Found {len(alert_blocks)} alert blocks for route {route_id}")

        for block in alert_blocks:
            try:
                title = block.query_selector("h3")
                body = block.query_selector("p")
                if title and body:
                    alerts.append({
                        "title": title.inner_text().strip(),
                        "message": body.inner_text().strip()
                    })
            except Exception as e:
                print(f"⚠️ Error parsing alert: {e}")

        browser.close()

    return alerts




def export_alerts_to_json(alerts, path="data/alerts_dump.json"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "alerts": alerts
        }, f, indent=2)
    print(f"✅ Exported {len(alerts)} alerts to {path}")


def load_alert_dump(path="data/alerts_dump.json"):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["alerts"]


# Optional CLI test block
if __name__ == "__main__":
    print("🔍 Testing stop-based alert scan:")
    results = get_alerts_for_stop("Nine Mile")
    for r in results:
        print("⚠️", r)

    print("\n🔍 Testing route alert scan:")
    route_alerts = get_route_alerts("44")
    for alert in route_alerts:
        print(f"🚍 Route {alert['route']} @ {alert['location']}")
        print(f"   ➤ {alert['message']}\n")
    
    print("🔎 Testing 15L alerts")
    alerts = get_route_alerts("15L")
    for alert in alerts:
        print(f"🚨 {alert['title']}\n   {alert['message']}\n")


    export_alerts_to_json(route_alerts)
