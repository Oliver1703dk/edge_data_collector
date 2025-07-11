import os
import time
from dotenv import load_dotenv
import requests
from edge_data_collector.camera.camera_handler import CameraHandler
from edge_data_collector.sensors.sensor_handler import SensorHandler
from edge_data_collector.metadata.metadata_handler import MetadataHandler
from edge_data_collector.formatter.data_formatter import *
from edge_data_sender.transmission.mqtt_handler import MqttHandler



from dotenv import load_dotenv
import os




# def reload_env():
#     """Force reload the .env file and clear cached variables."""
#     for key in list(os.environ.keys()):
#         if key.startswith("NETATMO_"):  # Adjust prefix if needed
#             del os.environ[key]
#     load_dotenv()  # Reload the .env file
def reload_env():
    """Force reload the .env file and clear cached variables."""
    # List all keys used in your project to clear them explicitly
    keys_to_clear = [
        "NETATMO_CLIENT_ID", "NETATMO_CLIENT_SECRET", "NETATMO_USERNAME", "NETATMO_PASSWORD",
        "NETATMO_SENSOR_ID_INDOOR", "NETATMO_SENSOR_ID_OUTDOOR", "NETATMO_ACCESS_TOKEN", "NETATMO_REFRESH_TOKEN",
        "USE_MQTT", "MQTT_BROKER", "MQTT_PORT", "MQTT_TOPIC",
        "SIMULATE_IMAGE_CREATION", "SIMULATE_SENSOR_DATA"
    ]
    for key in keys_to_clear:
        os.environ.pop(key, None)  # Safer than del, avoids KeyError if missing
    
    # Load with override=True to ensure .env values take precedence
    # Optionally specify path if .env isn't in cwd: dotenv_path=os.path.join(os.path.dirname(__file__), '.env')
    loaded = load_dotenv(override=True)  # Add dotenv_path=... if needed
    print(f"Dotenv loaded successfully: {loaded}")
    if not loaded:
        print("Warning: .env file not found! Check path and working directory.")




if __name__ == "__main__":
    MQTT_BOOLEAN = True
    # Load environment variables
    # load_dotenv()

    reload_env()


    # Load configurations
    use_mqtt = os.getenv("USE_MQTT", "false").lower() == "true"
    mqtt_broker = os.getenv("MQTT_BROKER", "localhost")
    mqtt_port = int(os.getenv("MQTT_PORT", 1883))
    mqtt_topic = os.getenv("MQTT_TOPIC", "sensor/data")
    simulate_image_creation = os.getenv("SIMULATE_IMAGE_CREATION", "false").lower() == "true"
    simulate_sensor_data = os.getenv("SIMULATE_SENSOR_DATA", "false").lower() == "true"


    # Retrieve sensitive credentials from environment variables
    client_id = os.getenv("NETATMO_CLIENT_ID")
    client_secret = os.getenv("NETATMO_CLIENT_SECRET")
    username = os.getenv("NETATMO_USERNAME")
    password = os.getenv("NETATMO_PASSWORD")
    sensor_id = os.getenv("NETATMO_SENSOR_ID_INDOOR")
    access_token = os.getenv("NETATMO_ACCESS_TOKEN")
    refresh_token = os.getenv("NETATMO_REFRESH_TOKEN")

    
    

    # Initialize modules
    camera_handler = CameraHandler(camera_id="camera_01")
    sensor_handler = SensorHandler(
        sensor_id=sensor_id,
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri="https://example.com",
        access_token=access_token,
        refresh_token=refresh_token,
        simulate_sensor=simulate_sensor_data,
    )
    metadata_handler = MetadataHandler()


    if(use_mqtt): 
        # Initialize MQTT handler
        mqtt_handler = MqttHandler(mqtt_broker, mqtt_port, mqtt_topic)
        mqtt_handler.connect()
        try:
            while True:
                # Capture data
                image_data = camera_handler.capture_image()
                sensor_data = sensor_handler.read_sensor_data()

                # Add metadata
                metadata = metadata_handler.add_metadata({}, camera_id="camera_01")

                # Format data
                formatted_data = format_data(image_data, sensor_data, metadata)

                # Publish data via MQTT
                mqtt_handler.publish(formatted_data)
                print("Published Data:", formatted_data)
                time.sleep(5)

        except KeyboardInterrupt:
            print("Stopping data sender...")

    else: 
        # Capture data
        image_data = camera_handler.capture_image()
        sensor_data = sensor_handler.read_sensor_data()

        # Add metadata
        metadata = metadata_handler.add_metadata({}, camera_id="camera_01")

        # Format data
        formatted_data = format_data(image_data, sensor_data, metadata)

        # Output for verification
        print("Formatted Data:")
        print(formatted_data)







