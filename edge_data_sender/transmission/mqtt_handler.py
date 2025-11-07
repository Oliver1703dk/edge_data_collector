import paho.mqtt.client as mqtt
import json
import time

class MqttHandler:
    def __init__(self, broker_address, port, topic):
        """
        Initializes the MQTT handler.
        Args:
            broker_address (str): IP address of the MQTT broker.
            port (int): Port number for the MQTT broker.
            topic (str): Topic to publish messages.
        """
        self.broker_address = broker_address
        self.port = port
        self.topic = topic
        self.client = mqtt.Client()

    def connect(self):
        """Connects to the MQTT broker."""
        self.client.connect(self.broker_address, self.port)

    def publish(self, payload):
        """
        Publishes a message to the MQTT topic.
        Args:
            payload (dict): JSON-serializable data to be sent.
        """
        metadata = payload.setdefault("metadata", {})
        capture_ts = metadata.get("collector_capture_ts")
        if capture_ts is not None:
            metadata["collector_capture_ts"] = float(capture_ts)

        metadata["collector_publish_ts"] = time.time()
        payload["metadata"] = metadata

        self.client.publish(self.topic, json.dumps(payload))
