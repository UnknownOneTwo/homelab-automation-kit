import requests
import os
from dotenv import load_dotenv

load_dotenv()

GRAFANA_URL = os.getenv("GRAFANA_URL", "http://192.168.10.102:3000")
DASHBOARD_UID = os.getenv("GRAFANA_DASHBOARD_UID", "dem0v6zlwt7nkb")
PANEL_ID = int(os.getenv("GRAFANA_SUMMARY_PANEL_ID", "3"))  # default to panel 3
API_KEY = os.getenv("GRAFANA_API_KEY")

SUMMARY_FILE = "latest_summary.txt"

def update_panel(content):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    url = f"{GRAFANA_URL}/api/dashboards/uid/{DASHBOARD_UID}"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("❌ Failed to fetch dashboard:", response.text)
        return

    dashboard = response.json()
    if "dashboard" not in dashboard:
        print("❌ Response missing 'dashboard' key.")
        return

    for panel in dashboard["dashboard"].get("panels", []):
        if panel["id"] == PANEL_ID:
            panel["options"]["content"] = content
            break
    else:
        print(f"❌ Panel ID {PANEL_ID} not found in dashboard.")
        return

    payload = {
        "dashboard": dashboard["dashboard"],
        "folderId": 0,
        "overwrite": True,
        "message": "🤖 Updated system summary panel"
    }

    res = requests.post(f"{GRAFANA_URL}/api/dashboards/db", headers=headers, json=payload)
    if res.status_code == 200:
        print("✅ System summary updated in Grafana.")
    else:
        print("❌ Failed to update panel:", res.text)

def main():
    if not os.path.exists(SUMMARY_FILE):
        print("❌ No summary file found.")
        return

    with open(SUMMARY_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    update_panel(content)

if __name__ == "__main__":
    main()
