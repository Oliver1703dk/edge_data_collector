import paho.mqtt.client as mqtt
import json
import time
import logging

# Set up logging for error handling
logger = logging.getLogger(__name__)

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
        # Fixed client ID and clean session enabled
        self.client = mqtt.Client(
            client_id="flood-detection-collector",
            clean_session=True
        )
        # Limit internal buffer to prevent memory buildup
        self.client.max_queued_messages_set(10)

    def connect(self):
        """Connects to the MQTT broker with keep-alive interval."""
        try:
            # Connect with 60 second keep-alive interval
            self.client.connect(self.broker_address, self.port, keepalive=60)
            # Start non-blocking background loop
            self.client.loop_start()
        except Exception as e:
            logger.error(f"Failed to connect to MQTT broker: {e}")
            raise

    def publish(self, payload):
        """
        Publishes a message to the MQTT topic with QoS 0 (fire-and-forget).
        Args:
            payload (dict): JSON-serializable data to be sent.
        """
        try:
            metadata = payload.setdefault("metadata", {})
            capture_ts = metadata.get("collector_capture_ts")
            if capture_ts is not None:
                metadata["collector_capture_ts"] = float(capture_ts)

            metadata["collector_publish_ts"] = time.time()
            payload["metadata"] = metadata

            # Publish with QoS 0, retain=False (explicit for clarity)
            result = self.client.publish(
                self.topic, 
                json.dumps(payload),
                qos=0,
                retain=False
            )
            
            # Log errors but don't block - QoS 0 is fire-and-forget
            if result.rc != mqtt.MQTT_ERR_SUCCESS:
                logger.error(f"Failed to publish message: {mqtt.error_string(result.rc)}")
        except Exception as e:
            # Log errors but continue publishing
            logger.error(f"Error during publish: {e}")
