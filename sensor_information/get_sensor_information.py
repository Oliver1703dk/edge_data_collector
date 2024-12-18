
import os

import requests


if __name__ == "__main__":

    # Retrieve sensitive credentials from environment variables
    client_id = os.getenv("NETATMO_CLIENT_ID")
    client_secret = os.getenv("NETATMO_CLIENT_SECRET")
    username = os.getenv("NETATMO_USERNAME")
    password = os.getenv("NETATMO_PASSWORD")
    sensor_id = os.getenv("NETATMO_SENSOR_ID")
    access_token = os.getenv("NETATMO_ACCESS_TOKEN")

    url = "https://api.netatmo.com/api/getstationsdata"
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        devices = response.json().get("body", {}).get("devices", [])
        for device in devices:
            print(f"Device ID: {device.get('_id')}, Name: {device.get('station_name')}")
            for module in device.get("modules", []):
                print(f"Module ID: {module.get('_id')}, Name: {module.get('module_name')}")
    else:
        print(f"Failed to fetch station data: {response.json()}")

