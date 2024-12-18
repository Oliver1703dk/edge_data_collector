import requests
import jwt
from datetime import datetime, timezone
from urllib.parse import urlencode
from dotenv import load_dotenv, set_key
import os


class SensorHandler:
    def __init__(self, sensor_id, client_id, client_secret, redirect_uri, access_token=None, refresh_token=None):
        # load_dotenv()  # Load environment variables from .env
        self.sensor_id = sensor_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.access_token = access_token 
        self.refresh_token = refresh_token
        # self.access_token = os.getenv("NETATMO_ACCESS_TOKEN")
        # self.refresh_token = os.getenv("NETATMO_REFRESH_TOKEN")

    def save_tokens(self):
        """Save access and refresh tokens to the .env file."""
        if self.access_token:
            set_key(".env", "NETATMO_ACCESS_TOKEN", self.access_token)
        if self.refresh_token:
            set_key(".env", "NETATMO_REFRESH_TOKEN", self.refresh_token)
        print("Tokens saved to .env file.")

    def generate_auth_url(self, state="unique_state_string"):
        """Generate the URL to redirect the user for authorization."""
        url = "https://api.netatmo.com/oauth2/authorize"
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": "read_station",
            "state": state,
            "response_type": "code"
        }
        auth_url = f"{url}?{urlencode(params)}"
        print(f"Please visit the following URL to authorize the application:\n{auth_url}")
        print("After authorization, you will be redirected to your redirect URI with a 'code' parameter in the URL.")
        return auth_url

    def exchange_authorization_code(self, authorization_code):
        """Exchange the authorization code for access and refresh tokens."""
        print("Exchanging authorization code for tokens...")
        url = "https://api.netatmo.com/oauth2/token"
        payload = {
            "grant_type": "authorization_code",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": authorization_code,
            "redirect_uri": self.redirect_uri
        }
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            data = response.json()
            self.access_token = data.get("access_token")
            self.refresh_token = data.get("refresh_token")
            self.save_tokens()
            print("Tokens retrieved and saved successfully.")
        else:
            print(f"Failed to exchange authorization code: {response.json()}")
            raise Exception("Token exchange failed.")

    def refresh_access_token(self):
        """Refresh the access token using the refresh token."""
        if not self.refresh_token:
            print("No refresh token available. Redirecting to reauthenticate.")
            self.reauthenticate()
            return

        print("Refreshing access token...")
        url = "https://api.netatmo.com/oauth2/token"
        payload = {
            "grant_type": "refresh_token",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": self.refresh_token
        }

        response = requests.post(url, data=payload)
        print(f"Refresh token request status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            self.access_token = data.get("access_token")
            self.refresh_token = data.get("refresh_token")
            self.save_tokens()
            print("Access token refreshed and saved successfully.")
        else:
            try:
                error_details = response.json()
                print(f"Failed to refresh access token. Error details: {error_details}")
            except ValueError:
                print("Failed to parse error details. Raw response:")
                print(response.text)

            if "invalid_grant" in error_details.get("error", ""):
                print("The refresh token is invalid or expired. Redirecting to reauthenticate.")
                self.reauthenticate()
            else:
                raise Exception(f"Unexpected error during token refresh: {response.json()}")

    def is_token_expired(self, token):
        """Check if the access token is expired."""
        try:
            decoded_token = jwt.decode(token, options={"verify_signature": False})
            exp_timestamp = decoded_token.get("exp")
            if not exp_timestamp:
                print("No expiration field in token.")
                return True  # Assume expired if no exp field
            now = datetime.now(timezone.utc).timestamp()
            return now >= exp_timestamp
        except jwt.DecodeError:
            print("Invalid token format.")
            return True  # Treat invalid token as expired

    def reauthenticate(self):
        """Guide the user to reauthorize the application."""
        print("Reauthentication required.")
        self.generate_auth_url()
        authorization_code = input("Enter the authorization code provided after authorization: ").strip()
        self.exchange_authorization_code(authorization_code)

    def read_sensor_data(self):
        """Read data from the sensor, refreshing the token if necessary."""
        if not self.access_token or self.is_token_expired(self.access_token):
            print("Access token expired or unavailable, attempting to refresh...")
            self.refresh_access_token()

        print(f"Reading data from Netatmo sensor {self.sensor_id}...")
        url = "https://api.netatmo.com/api/getstationsdata"
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        response = requests.get(url, headers=headers)

        if response.status_code == 401:  # Token expired or invalid
            print("Access token expired or invalid, refreshing token...")
            self.refresh_access_token()
            headers["Authorization"] = f"Bearer {self.access_token}"
            response = requests.get(url, headers=headers)

        if response.status_code == 200:
            devices = response.json().get("body", {}).get("devices", [])
            if devices:
                station_data = devices[0].get("dashboard_data", {})
                sensor_data = {
                    "temperature": station_data.get("Temperature"),
                    "humidity": station_data.get("Humidity"),
                    "pressure": station_data.get("Pressure")
                }
                return sensor_data
            else:
                print("No devices found in the response.")
                return None
        else:
            raise Exception(f"Failed to fetch sensor data: {response.status_code} {response.json()}")
