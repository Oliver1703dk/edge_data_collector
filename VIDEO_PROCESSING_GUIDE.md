# Video Processing Mode - Quick Start Guide

This guide will help you get started with processing video files using `main_video.py`.

## Prerequisites

1. **Python 3.7+** installed
2. **Required packages** installed:
   ```bash
   pip install -r requirements.txt
   ```

## Quick Start

### Step 1: Prepare Your Video File

Place your video file in an accessible location. Supported formats:
- MP4 (`.mp4`) - Recommended
- AVI (`.avi`)
- MOV (`.mov`)
- MKV (`.mkv`)
- Any format supported by OpenCV

### Step 2: Configure main_video.py

Open `main_video.py` and update the configuration section (around line 150):

```python
# Configuration
VIDEO_PATH = "path/to/your/video.mp4"  # ← Change this!
CAMERA_ID = "video_camera_01"

# Static sensor data configuration
STATIC_TEMPERATURE = 22.5  # Celsius
STATIC_HUMIDITY = 55.0     # Percentage
STATIC_PRESSURE = 1013.25  # hPa

# Frame processing interval (in seconds)
FRAME_INTERVAL = 1.0  # Process one frame per second
```

### Step 3: Configure MQTT (Optional)

Edit `config.py` to enable/disable MQTT:

```python
USE_MQTT = False  # Set to True to publish data via MQTT
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "sensor/data"
```

### Step 4: Run the Script

```bash
python main_video.py
```

## Usage Examples

### Example 1: Process Video Without MQTT

```python
# In config.py
USE_MQTT = False

# In main_video.py
VIDEO_PATH = "/home/user/videos/test.mp4"
FRAME_INTERVAL = 1.0  # One frame per second
```

Run:
```bash
python main_video.py
```

This will process one frame and display the formatted data.

### Example 2: Stream Video Frames via MQTT

```python
# In config.py
USE_MQTT = True
MQTT_BROKER = "192.168.1.100"  # Your MQTT broker IP
MQTT_PORT = 1883
MQTT_TOPIC = "camera/video_feed"

# In main_video.py
VIDEO_PATH = "/data/surveillance.mp4"
FRAME_INTERVAL = 0.5  # Two frames per second
```

Run:
```bash
python main_video.py
```

Press `Ctrl+C` to stop.

### Example 3: Fast Batch Processing

Process all frames as quickly as possible:

```python
# In main_video.py
VIDEO_PATH = "/recordings/archive_2024.mp4"
FRAME_INTERVAL = 0  # Process as fast as possible
```

### Example 4: Real-Time Simulation

Simulate real-time playback of a 30fps video:

```python
# In main_video.py
VIDEO_PATH = "/videos/realtime_test.mp4"
FRAME_INTERVAL = 1/30  # 30 frames per second (0.033 seconds)
```

## Customizing Sensor Data

You can adjust the static sensor values to match your scenario:

### Indoor Environment
```python
STATIC_TEMPERATURE = 21.0  # Comfortable room temperature
STATIC_HUMIDITY = 45.0     # Typical indoor humidity
STATIC_PRESSURE = 1013.25  # Standard atmospheric pressure
```

### Outdoor Environment
```python
STATIC_TEMPERATURE = 15.5  # Cool outdoor temperature
STATIC_HUMIDITY = 75.0     # Higher outdoor humidity
STATIC_PRESSURE = 1010.0   # Slightly lower pressure
```

### Cold Storage
```python
STATIC_TEMPERATURE = 4.0   # Refrigerator temperature
STATIC_HUMIDITY = 80.0     # High humidity
STATIC_PRESSURE = 1013.25  # Standard pressure
```

## Output

### Extracted Frames
Frames are saved to: `edge_data_collector/camera/images/`

Filename format: `video_frame_{camera_id}_{timestamp}_{frame_number}.jpg`

Example: `video_frame_video_camera_01_1704123456_42.jpg`

### Console Output
```
Video loaded: /path/to/video.mp4
FPS: 30.0, Total frames: 900
Static sensor data initialized: {'temperature': 22.5, 'humidity': 55.0, 'pressure': 1013.25}
Frame 1/900 saved to edge_data_collector/camera/images/video_frame_video_camera_01_1704123456_1.jpg
Data Published
Frame 2/900 saved to edge_data_collector/camera/images/video_frame_video_camera_01_1704123457_2.jpg
Data Published
...
```

## Troubleshooting

### Error: "Could not open video file"
- Check that VIDEO_PATH is correct
- Verify the video file exists and is not corrupted
- Ensure OpenCV supports the video format
- Try converting the video to MP4 format

### Error: "No module named 'cv2'"
Install OpenCV:
```bash
pip install opencv-python
```

### Video Processing is Too Slow
- Increase FRAME_INTERVAL to skip more frames
- Use a lower resolution video
- Disable MQTT if not needed

### Video Processing is Too Fast
- Increase FRAME_INTERVAL
- Set FRAME_INTERVAL to match video FPS: `1/fps`

### Out of Disk Space
Extracted frames can consume significant disk space. To manage:
- Process shorter video segments
- Increase FRAME_INTERVAL to extract fewer frames
- Periodically clean the `edge_data_collector/camera/images/` folder
- Modify the code to delete frames after processing

## Differences from main.py

| Feature | main.py | main_video.py |
|---------|---------|---------------|
| Image Source | Live camera | Video file |
| Sensor Data | Real sensors (Netatmo) | Static values |
| Processing | Continuous loop | Until video ends |
| Frame Rate | Camera dependent | Configurable |
| Hardware Required | Raspberry Pi + Camera | None |

## Advanced Usage

### Processing Multiple Videos

Create a wrapper script:

```python
import os
from main_video import VideoHandler, StaticSensorHandler, MetadataHandler
from edge_data_collector.formatter.data_formatter import format_data

video_files = [
    "/videos/video1.mp4",
    "/videos/video2.mp4",
    "/videos/video3.mp4"
]

for video_path in video_files:
    print(f"Processing {video_path}...")
    video_handler = VideoHandler(video_path, "batch_camera")
    sensor_handler = StaticSensorHandler()
    metadata_handler = MetadataHandler()
    
    while video_handler.has_frames():
        frame_path = video_handler.capture_frame()
        if frame_path:
            sensor_data = sensor_handler.read_sensor_data()
            metadata = metadata_handler.add_metadata({}, camera_id="batch_camera")
            formatted_data = format_data(frame_path, sensor_data, metadata)
            # Process formatted_data...
    
    video_handler.close()
```

### Dynamic Sensor Data

Modify `StaticSensorHandler` to vary sensor values:

```python
import random

class DynamicSensorHandler:
    def __init__(self, base_temp=22.5, base_humidity=55.0, base_pressure=1013.25):
        self.base_temp = base_temp
        self.base_humidity = base_humidity
        self.base_pressure = base_pressure
    
    def read_sensor_data(self):
        # Add small random variations
        return {
            "temperature": self.base_temp + random.uniform(-2, 2),
            "humidity": self.base_humidity + random.uniform(-5, 5),
            "pressure": self.base_pressure + random.uniform(-5, 5)
        }
```

## Support

For issues or questions:
1. Check the main README.md
2. Review the inline documentation in main_video.py
3. Refer to config_video_example.py for configuration examples
