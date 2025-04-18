## deprecated due to known issues with the jupyter notebook and anaconda...
from playwright.async_api import async_playwright

async def get_facility_alerts_async():
    alerts = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://app.rtd-denver.com/alerts", timeout=60000)

        await page.click("text=Facilities")
        await page.wait_for_timeout(2000)

        alert_items = await page.query_selector_all(".alert-item")
        print(f"🔍 Found {len(alert_items)} alert blocks")

        for item in alert_items:
            try:
                title_elem = await item.query_selector(".alert-title")
                body_elem = await item.query_selector(".alert-body")

                if title_elem and body_elem:
                    location = await title_elem.inner_text()
                    message = await body_elem.inner_text()
                    alerts.append({
                        "location": location.strip(),
                        "message": message.strip()
                    })
            except Exception as e:
                print("⚠️ Failed to parse alert:", e)

        if len(alerts) == 0:
            print("🛠 Dumping HTML for debugging...")
            with open("page_dump.html", "w", encoding="utf-8") as f:
                f.write(await page.content())

        await browser.close()

    return alerts

async def get_alerts_for_stop_async(stop_name):
    stop_name = stop_name.lower()
    alerts = await get_facility_alerts_async()

    return [
        alert["message"]
        for alert in alerts
        if stop_name in alert["location"].lower() or stop_name in alert["message"].lower()
    ]
