import time
import os
import math
import cv2
from dotenv import load_dotenv

from edge_data_collector.sensors.sensor_handler import SensorHandler
from edge_data_collector.metadata.metadata_handler import MetadataHandler
from edge_data_collector.formatter.data_formatter import format_data
from edge_data_sender.transmission.mqtt_handler import MqttHandler

import config


# ============================================================================
# CONFIGURATION - Comment/uncomment sections to change settings
# ============================================================================

# Video file path configuration
VIDEO_PATH = "video_gather/best_videos/flood_video_20251005_150257.mp4"
# VIDEO_PATH = "video_gather/best_videos/flood_video_20251005_145739.mp4"
# VIDEO_PATH = "video_gather/best_videos/flood_video_20251005_150218.mp4"
# VIDEO_PATH = "video_gather/best_videos/flood_video_20251005_150338.mp4"

CAMERA_ID = "video_camera_01"

# Motion configuration
MOTION = "slow"
# MOTION = "fast"
# MOTION = "stop"

# Sensor values configuration
## REAL WORLD conditions — no anomaly, sensor_boost
STATIC_TEMPERATURE = 12.0   # ΔT = 
STATIC_HUMIDITY    = 88.0   # ΔRH = 
STATIC_PRESSURE    = 995.0 # ΔP = 

## FLOODING conditions — triggers strong positive boost
# STATIC_TEMPERATURE = 13.5   # ΔT = 13.5 – 17.0 = -3.5 °C → triggers temp drop (-2.5 °C) → +0.05 (or +0.10 if severe)
# STATIC_HUMIDITY    = 96.0   # ΔRH = 96.0 – 78.0 = +18 % → with cooling → triggers humidity boost +0.10 → +0.20 if >30
# STATIC_PRESSURE    = 1008.0 # ΔP = 1008.0 – 1016.0 = -8 hPa → triggers pressure drop → +0.03 → +0.06 if <–10

## NOT FLOODING / HOT & DRY — triggers negative boost
# STATIC_TEMPERATURE = 27.0   # ΔT = 27.0 – 17.0 = +10.0 °C → very hot anomaly
# STATIC_HUMIDITY    = 45.0   # ΔRH = 45.0 – 78.0 = -33 % → extremely dry
# STATIC_PRESSURE    = 1018.0 # ΔP = +2 hPa → neutral/high (no storm signal)

## NEUTRAL conditions — no anomaly, sensor_boost = 0.0
# STATIC_TEMPERATURE = 17.0   # ΔT = 0.0 °C
# STATIC_HUMIDITY    = 78.0   # ΔRH = 0.0 %
# STATIC_PRESSURE    = 1016.0 # ΔP = 0.0 hPa

# Frame processing interval (seconds). The capture aligns to the equivalent
# timestamp in the video (e.g., 1.0 sends frames from 1s, 2s, 3s...).
# Must be greater than zero.
FRAME_INTERVAL = 0.5  # Example: capture and publish once per second


class VideoHandler:
    """Handler for processing video files frame by frame."""
    
    def __init__(self, video_path, camera_id, image_folder="edge_data_collector/camera/images"):
        """
        Initialize the video handler.
        
        Args:
            video_path (str): Path to the video file
            camera_id (str): Identifier for the camera/video source
            image_folder (str): Folder to save extracted frames
        """
        self.video_path = video_path
        self.camera_id = camera_id
        self.image_folder = image_folder
        os.makedirs(self.image_folder, exist_ok=True)
        
        # Open the video file
        self.video_capture = cv2.VideoCapture(video_path)
        if not self.video_capture.isOpened():
            raise ValueError(f"Could not open video file: {video_path}")
        
        # Get video properties
        self.fps = self.video_capture.get(cv2.CAP_PROP_FPS)
        self.total_frames = int(self.video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
        self.current_frame = 0
        self.duration_seconds = (
            self.total_frames / self.fps if self.fps not in (0, None) else 0.0
        )
        
        print(f"Video loaded: {video_path}")
        print(f"FPS: {self.fps}, Total frames: {self.total_frames}, Duration: {self.duration_seconds:.3f}s")

    def capture_frame(self, compress=False):
        """
        Extract the next frame from the video.
        
        Args:
            compress (bool): Whether to compress the frame (not implemented, kept for compatibility)
        
        Returns:
            tuple[str | None, float | None]: Path to the saved frame image and
            the capture timestamp (seconds since epoch), or (None, None) if video ended
        """
        ret, frame = self.video_capture.read()
        
        if not ret:
            print("End of video reached or error reading frame.")
            return None, None
        
        self.current_frame += 1
        capture_time = time.time()
        frame_path = os.path.join(
            self.image_folder, 
            f"video_frame_{self.camera_id}_{int(capture_time)}_{self.current_frame}.jpg"
        )
        
        # Save the frame as an image
        cv2.imwrite(frame_path, frame)
        print(f"Frame {self.current_frame}/{self.total_frames} saved to {frame_path}")
        
        return frame_path, capture_time

    def capture_frame_at(self, time_seconds, sequence_number):
        """
        Extract the frame that corresponds to a given timestamp.

        Args:
            time_seconds (float): Target timestamp (seconds) inside the video.
            sequence_number (int): Sequential number for naming consistency.

        Returns:
            tuple[str | None, float | None]: Path to the saved frame image and its
            capture timestamp (seconds since epoch), or (None, None) if extraction failed.
        """
        if self.fps in (0, None):
            raise ValueError("Video FPS is zero; cannot align frames by time.")

        frame_index = min(
            int(math.floor(time_seconds * self.fps)),
            max(self.total_frames - 1, 0)
        )

        if frame_index < 0 or frame_index >= self.total_frames:
            print(f"Requested frame at {time_seconds:.3f}s is outside video duration.")
            return None, None

        self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
        ret, frame = self.video_capture.read()

        if not ret or frame is None:
            print(f"Failed to read frame at {time_seconds:.3f}s (index {frame_index}).")
            return None, None

        capture_time = time.time()
        frame_path = os.path.join(
            self.image_folder,
            f"video_frame_{self.camera_id}_{int(capture_time)}_{sequence_number}.jpg"
        )
        cv2.imwrite(frame_path, frame)
        self.current_frame = frame_index + 1
        print(
            f"Aligned frame {sequence_number} (video t={time_seconds:.3f}s, index {frame_index + 1}/{self.total_frames}) "
            f"saved to {frame_path}"
        )

        return frame_path, capture_time
    
    def reset_video(self):
        """Reset video to the beginning."""
        self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
        self.current_frame = 0
        print("Video reset to beginning.")
    
    def close(self):
        """Release the video capture object."""
        if self.video_capture:
            self.video_capture.release()
        print("Video handler closed.")
    
    def has_frames(self):
        """Check if there are more frames to process."""
        return self.current_frame < self.total_frames


class StaticSensorHandler:
    """Handler for providing static sensor data."""
    
    def __init__(self, temperature=22.5, humidity=55.0, pressure=1013.25):
        """
        Initialize with static sensor values.
        
        Args:
            temperature (float): Temperature in Celsius
            humidity (float): Humidity percentage
            pressure (float): Pressure in hPa
        """
        self.sensor_data = {
            "temperature": temperature,
            "humidity": humidity,
            "pressure": pressure
        }
        print(f"Static sensor data initialized: {self.sensor_data}")
    
    def read_sensor_data(self):
        """
        Return the static sensor data.
        
        Returns:
            dict: Dictionary containing temperature, humidity, and pressure
        """
        return self.sensor_data.copy()


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

    # Load MQTT configuration from config.py
    use_mqtt = config.USE_MQTT
    mqtt_broker = config.MQTT_BROKER
    mqtt_port = config.MQTT_PORT
    mqtt_topic = config.MQTT_TOPIC

    # Initialize modules
    try:
        video_handler = VideoHandler(
            video_path=VIDEO_PATH,
            camera_id=CAMERA_ID
        )
    except ValueError as e:
        print(f"Error: {e}")
        print(f"Please update VIDEO_PATH in main_video.py to point to a valid video file.")
        exit(1)
    
    sensor_handler = StaticSensorHandler(
        temperature=STATIC_TEMPERATURE,
        humidity=STATIC_HUMIDITY,
        pressure=STATIC_PRESSURE
    )
    
    metadata_handler = MetadataHandler()

    if use_mqtt:
        if FRAME_INTERVAL <= 0:
            raise ValueError("FRAME_INTERVAL must be greater than zero for aligned capture.")

        if video_handler.duration_seconds <= 0:
            print("Video duration is zero; nothing to process.")
        else:
            mqtt_handler = MqttHandler(mqtt_broker, mqtt_port, mqtt_topic)
            mqtt_handler.connect()
            start_time = time.time()
            sample_index = 1

            try:
                while True:
                    target_video_time = sample_index * FRAME_INTERVAL

                    if target_video_time > video_handler.duration_seconds:
                        print("Reached end of video based on configured interval.")
                        break

                    # Wait until the scheduled wall-clock time before sending
                    scheduled_wall_time = start_time + target_video_time
                    sleep_duration = scheduled_wall_time - time.time()
                    if sleep_duration > 0:
                        time.sleep(sleep_duration)

                    frame_path, capture_ts = video_handler.capture_frame_at(
                        time_seconds=target_video_time,
                        sequence_number=sample_index
                    )

                    if not frame_path:
                        print("Failed to capture aligned frame; stopping.")
                        break

                    sensor_data = sensor_handler.read_sensor_data()
                    metadata = metadata_handler.add_metadata({}, camera_id=CAMERA_ID, motion=MOTION)
                    metadata["collector_capture_ts"] = capture_ts
                    metadata["video_timestamp_sec"] = round(target_video_time, 3)
                    metadata["video_file"] = os.path.basename(VIDEO_PATH)
                    formatted_data = format_data(frame_path, sensor_data, metadata)
                    mqtt_handler.publish(formatted_data)
                    print(f"Data Published (interval index {sample_index}, video t={target_video_time:.3f}s)")

                    sample_index += 1

            except KeyboardInterrupt:
                print("\nStopping video processing...")
            finally:
                video_handler.close()
                print("Video processing completed.")
    else:
        # Process a single frame without MQTT
        frame_path, capture_ts = video_handler.capture_frame()
        
        if frame_path:
            sensor_data = sensor_handler.read_sensor_data()
            metadata = metadata_handler.add_metadata({}, camera_id=CAMERA_ID, motion=MOTION)
            metadata["collector_capture_ts"] = capture_ts
            if video_handler.fps not in (0, None):
                frame_index = max(video_handler.current_frame - 1, 0)
                metadata["video_timestamp_sec"] = round(frame_index / video_handler.fps, 3)
            else:
                metadata["video_timestamp_sec"] = None
            metadata["video_file"] = os.path.basename(VIDEO_PATH)
            print("Sensor Data:", sensor_data)
            formatted_data = format_data(frame_path, sensor_data, metadata)
            print("Formatted Data:")
            print(formatted_data)
        else:
            print("Failed to extract frame from video.")
        
        video_handler.close()
