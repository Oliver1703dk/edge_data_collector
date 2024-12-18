import os
from dotenv import load_dotenv
import requests
from edge_data_collector.camera.camera_handler import CameraHandler
from edge_data_collector.sensors.sensor_handler import SensorHandler
from edge_data_collector.metadata.metadata_handler import MetadataHandler
from edge_data_collector.formatter.data_formatter import DataFormatter



from dotenv import load_dotenv
import os



def reload_env():
    """Force reload the .env file and clear cached variables."""
    for key in list(os.environ.keys()):
        if key.startswith("NETATMO_"):  # Adjust prefix if needed
            del os.environ[key]
    load_dotenv()  # Reload the .env file




if __name__ == "__main__":
    # Load environment variables
    # load_dotenv()

    reload_env()

    # Retrieve sensitive credentials from environment variables
    client_id = os.getenv("NETATMO_CLIENT_ID")
    client_secret = os.getenv("NETATMO_CLIENT_SECRET")
    username = os.getenv("NETATMO_USERNAME")
    password = os.getenv("NETATMO_PASSWORD")
    sensor_id = os.getenv("NETATMO_SENSOR_ID_INDOOR")
    access_token = os.getenv("NETATMO_ACCESS_TOKEN")
    refresh_token = os.getenv("NETATMO_REFRESH_TOKEN")

    # # Debug prints
    # print(f"Client ID: {client_id}")
    # print(f"Client Secret: {client_secret}")
    # print(f"Username: {username}")
    # print(f"Password: {password}")  # WARNING: Use only for debugging; remove in production
    # print(f"Sensor ID: {sensor_id}")
    # print(f"Access Token: {access_token}")
    # print(f"Refresh Token: {refresh_token}")


    # Initialize modules
    camera_handler = CameraHandler(camera_id="camera_01")
    # sensor_handler = SensorHandler(
    #     sensor_id=sensor_id,
    #     client_id=client_id,
    #     client_secret=client_secret,
    #     username=username,
    #     password=password, 
    #     access_token=None,
    #     refresh_token=None
    # )
    
    sensor_handler = SensorHandler(
        sensor_id=sensor_id,
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri="https://example.com",
        access_token=access_token,
        refresh_token=refresh_token

    )

    # Capture data
    # image_data = camera_handler.capture_image()
    sensor_data = sensor_handler.read_sensor_data()

    # Add metadata
    metadata_handler = MetadataHandler()
    metadata = metadata_handler.add_metadata({}, camera_id="camera_01")

    # Format data
    formatter = DataFormatter()
    # formatted_data = formatter.format_data(image_data, sensor_data, metadata)

    # Output for verification
    print("Formatted Data:")
    # print(formatted_data)
