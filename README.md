# Edge Data Collector

This project captures images and sensor information and can transmit the data via MQTT.

## Configuration

MQTT settings and simulation flags are configured directly in `config.py`.
Netatmo credentials are still provided via a `.env` file which the application
loads at runtime.

## Simulation Options

Two flags in `config.py` allow running the application without real hardware or
network access:

- `SIMULATE_IMAGE_CREATION` &ndash; when set to `True` the camera handler
  creates dummy images instead of using a camera.
- `SIMULATE_SENSOR_DATA` &ndash; when set to `True` the sensor handler generates
  random temperature, humidity and pressure values instead of contacting
  Netatmo sensors.

Adjust these settings in `config.py` to switch between simulated and real data
sources.

## Video Processing Mode

The project includes `main_video.py` for processing pre-recorded video files instead of live camera feeds. This is useful for:
- Testing the system with recorded footage
- Processing archived video data
- Development without camera hardware
- Batch processing of video files

### Setup for Video Mode

1. **Install OpenCV** (required for video processing):
   ```bash
   pip install opencv-python
   ```
   Or install all requirements:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure the video source** in `main_video.py`:
   ```python
   VIDEO_PATH = "path/to/your/video.mp4"  # Update this path
   ```

3. **Adjust static sensor values** (optional):
   ```python
   STATIC_TEMPERATURE = 22.5  # Celsius
   STATIC_HUMIDITY = 55.0     # Percentage
   STATIC_PRESSURE = 1013.25  # hPa
   ```

4. **Set frame processing interval** (optional):
   ```python
   FRAME_INTERVAL = 1.0  # Process one frame per second
   ```

### Running Video Mode

```bash
python main_video.py
```

The script will:
- Extract frames from the video file sequentially
- Attach static sensor data to each frame
- Add metadata (timestamp, camera ID)
- Format and publish data via MQTT (if enabled in `config.py`)
- Save extracted frames to `edge_data_collector/camera/images/`

Press `Ctrl+C` to stop processing at any time.

### Video Mode Features

- **VideoHandler**: Extracts frames from video files using OpenCV
- **StaticSensorHandler**: Provides consistent sensor readings throughout video processing
- **Frame-by-frame processing**: Processes video at configurable intervals
- **Automatic cleanup**: Properly releases video resources when done
- **MQTT compatible**: Works with existing MQTT infrastructure
- **Format compatible**: Uses the same data formatting as live camera mode

### Supported Video Formats

The video handler supports common video formats including:
- MP4 (`.mp4`)
- AVI (`.avi`)
- MOV (`.mov`)
- MKV (`.mkv`)
- Any format supported by OpenCV

## Running the Standard Mode

For live camera and sensor data collection:

```bash
python main.py
```
