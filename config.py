"""Application configuration settings.

Edit the values below to adjust runtime behaviour. MQTT options and simulation
flags are defined here, while Netatmo credentials remain in the ``.env`` file
and are loaded by the main application.
"""

USE_MQTT = True
MQTT_BROKER = "192.168.10.1"
MQTT_PORT = 1883
MQTT_TOPIC = "sensor/data"

SIMULATE_IMAGE_CREATION = False
SIMULATE_SENSOR_DATA = False
