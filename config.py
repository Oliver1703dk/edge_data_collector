"""Application configuration settings.

Edit the values below to adjust runtime behaviour. MQTT options and simulation
flags are defined here, while Netatmo credentials remain in the ``.env`` file
and are loaded by the main application.
"""

import os


USE_MQTT = True
# If .env file has MQTT_BROKER use that, otherwise use localhost
if os.getenv("MQTT_BROKER"):
    MQTT_BROKER = os.getenv("MQTT_BROKER")
else:
    MQTT_BROKER = "localhost"
# MQTT_BROKER = "192.168.10.1"
MQTT_PORT = 1883
MQTT_TOPIC = "sensor/data"

SIMULATE_IMAGE_CREATION = False
SIMULATE_SENSOR_DATA = False
