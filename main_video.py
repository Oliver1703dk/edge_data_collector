"""
main_video.py - Video-based Edge Data Collection System

This script processes a video file frame-by-frame instead of using a live camera feed,
and uses static sensor data instead of querying real sensors. It maintains the same
functionality as main.py but operates on pre-recorded video.

SETUP:
------
1. Install OpenCV (required for video processing):
   pip install opencv-python

2. Update the VIDEO_PATH variable (line ~150) to point to your video file:
   VIDEO_PATH = "path/to/your/video.mp4"

3. (Optional) Adjust static sensor values:
   STATIC_TEMPERATURE = 22.5  # Celsius
   STATIC_HUMIDITY = 55.0     # Percentage
   STATIC_PRESSURE = 1013.25  # hPa

4. (Optional) Adjust frame processing interval:
   FRAME_INTERVAL = 1.0  # Process one frame per second

USAGE:
------
Run the script:
    python main_video.py

The script will:
- Extract frames from the video file
- Attach static sensor data to each frame
- Add metadata (timestamp, camera ID)
- Format and publish data via MQTT (if enabled in config.py)
- Save extracted frames to edge_data_collector/camera/images/

Press Ctrl+C to stop processing.

FEATURES:
---------
- VideoHandler: Extracts frames from video files using OpenCV
- StaticSensorHandler: Provides consistent sensor readings
- Compatible with existing MQTT and data formatting infrastructure
- Processes video at configurable frame rates
- Automatically handles video end and cleanup
"""

import time
import os
import cv2
from dotenv import load_dotenv

from edge_data_collector.sensors.sensor_handler import SensorHandler
from edge_data_collector.metadata.metadata_handler import MetadataHandler
from edge_data_collector.formatter.data_formatter import format_data
from edge_data_sender.transmission.mqtt_handler import MqttHandler

import config

import config


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
        
        print(f"Video loaded: {video_path}")
        print(f"FPS: {self.fps}, Total frames: {self.total_frames}")
    
    def capture_frame(self, compress=False):
        """
        Extract the next frame from the video.
        
        Args:
            compress (bool): Whether to compress the frame (not implemented, kept for compatibility)
        
        Returns:
            str: Path to the saved frame image, or None if video ended
        """
        ret, frame = self.video_capture.read()
        
        if not ret:
            print("End of video reached or error reading frame.")
            return None
        
        self.current_frame += 1
        timestamp = int(time.time())
        frame_path = os.path.join(
            self.image_folder, 
            f"video_frame_{self.camera_id}_{timestamp}_{self.current_frame}.jpg"
        )
        
        # Save the frame as an image
        cv2.imwrite(frame_path, frame)
        print(f"Frame {self.current_frame}/{self.total_frames} saved to {frame_path}")
        
        return frame_path
    
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

    # Configuration
    VIDEO_PATH = "path/to/your/video.mp4"  # Change this to your video file path
    CAMERA_ID = "video_camera_01"
    
    # Static sensor data configuration
    STATIC_TEMPERATURE = 22.5  # Celsius
    STATIC_HUMIDITY = 55.0     # Percentage
    STATIC_PRESSURE = 1013.25  # hPa
    
    # Frame processing interval (in seconds)
    # Set to 0 to process frames as fast as possible
    # Set to match video FPS for real-time playback (e.g., 1/30 for 30fps video)
    FRAME_INTERVAL = 1.0  # Process one frame per second
    
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
        mqtt_handler = MqttHandler(mqtt_broker, mqtt_port, mqtt_topic)
        mqtt_handler.connect()
        try:
            while video_handler.has_frames():
                # Extract frame from video
                frame_path = video_handler.capture_frame()
                
                if frame_path is None:
                    print("No more frames to process.")
                    break
                
                # Get static sensor data
                sensor_data = sensor_handler.read_sensor_data()
                
                # Add metadata
                metadata = metadata_handler.add_metadata({}, camera_id=CAMERA_ID)
                
                # Format and publish data
                formatted_data = format_data(frame_path, sensor_data, metadata)
                mqtt_handler.publish(formatted_data)
                print('Data Published')
                
                # Wait before processing next frame
                time.sleep(FRAME_INTERVAL)
                
        except KeyboardInterrupt:
            print("\nStopping video processing...")
        finally:
            video_handler.close()
            print("Video processing completed.")
    else:
        # Process a single frame without MQTT
        frame_path = video_handler.capture_frame()
        
        if frame_path:
            sensor_data = sensor_handler.read_sensor_data()
            metadata = metadata_handler.add_metadata({}, camera_id=CAMERA_ID)
            print("Sensor Data:", sensor_data)
            formatted_data = format_data(frame_path, sensor_data, metadata)
            print("Formatted Data:")
            print(formatted_data)
        else:
            print("Failed to extract frame from video.")
        
        video_handler.close()
