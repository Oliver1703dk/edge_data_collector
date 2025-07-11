import time
import os
from dotenv import load_dotenv

from edge_data_collector.camera.camera_handler import CameraHandler
from edge_data_collector.sensors.sensor_handler import SensorHandler
from edge_data_collector.metadata.metadata_handler import MetadataHandler
from edge_data_collector.formatter.data_formatter import format_data
from edge_data_sender.transmission.mqtt_handler import MqttHandler

import config


def reload_env():
    """Force reload the .env file and clear cached Netatmo variables."""
    keys_to_clear = [
        "NETATMO_CLIENT_ID",
        "NETATMO_CLIENT_SECRET",
        "NETATMO_USERNAME",
        "NETATMO_PASSWORD",
        "NETATMO_SENSOR_ID_INDOOR",
        "NETATMO_SENSOR_ID_OUTDOOR",
        "NETATMO_ACCESS_TOKEN",
        "NETATMO_REFRESH_TOKEN",
    ]
    for key in keys_to_clear:
        os.environ.pop(key, None)

    load_dotenv(override=True)


if __name__ == "__main__":
    reload_env()

    # Load configuration from config.py
    use_mqtt = config.USE_MQTT
    mqtt_broker = config.MQTT_BROKER
    mqtt_port = config.MQTT_PORT
    mqtt_topic = config.MQTT_TOPIC

    # Retrieve Netatmo credentials from environment variables
    client_id = os.getenv("NETATMO_CLIENT_ID")
    client_secret = os.getenv("NETATMO_CLIENT_SECRET")
    sensor_id = os.getenv("NETATMO_SENSOR_ID_INDOOR")
    access_token = os.getenv("NETATMO_ACCESS_TOKEN")
    refresh_token = os.getenv("NETATMO_REFRESH_TOKEN")

    # Initialize modules with configuration values
    camera_handler = CameraHandler(camera_id="camera_01")
    sensor_handler = SensorHandler(
        sensor_id=sensor_id,
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri="https://example.com",
        access_token=access_token,
        refresh_token=refresh_token,
        simulate_sensor=config.SIMULATE_SENSOR_DATA,
    )
    metadata_handler = MetadataHandler()

    if use_mqtt:
        mqtt_handler = MqttHandler(mqtt_broker, mqtt_port, mqtt_topic)
        mqtt_handler.connect()
        try:
            while True:
                image_data = camera_handler.capture_image()
                sensor_data = sensor_handler.read_sensor_data()
                metadata = metadata_handler.add_metadata({}, camera_id="camera_01")
                formatted_data = format_data(image_data, sensor_data, metadata)
                mqtt_handler.publish(formatted_data)
                print("Published Data:", formatted_data)
                time.sleep(5)
        except KeyboardInterrupt:
            print("Stopping data sender...")
    else:
        image_data = camera_handler.capture_image()
        sensor_data = sensor_handler.read_sensor_data()
        metadata = metadata_handler.add_metadata({}, camera_id="camera_01")
        formatted_data = format_data(image_data, sensor_data, metadata)
        print("Formatted Data:")
        print(formatted_data)
