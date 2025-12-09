# Edge Data Collector (Gathering Pi)

This repository contains the **Gathering Pi / Edge Data Collector** used in the ICSA 2026 paper:

> *Edge-Based Standing-Water Detection via FSM-Guided Tiering and Multi-Model Consensus*
> Oliver Larsen, Mahyar T. Moghaddam, SDU – MMMI

It runs on a Raspberry-Pi-class device and is responsible for capturing images and sensor readings, attaching metadata, and publishing them as a single, schema-stable MQTT message. In the paper’s architecture this corresponds to the **Gathering Pi** node feeding the Processing Pi and Jetson worker.

This repository is part of the replication package together with the Processing/Jetson system:

* Processing/Jetson system (FSM, inference, evaluation): `flood_detection_system`
* Gathering Pi / Edge Data Collector (this repo): `edge_data_collector`

---

## Entry Points

The project provides two entry points for different use cases:

| Entry Point     | Purpose                               | Data Source                               |
| --------------- | ------------------------------------- | ----------------------------------------- |
| `main.py`       | Live deployment on edge devices       | Camera + Netatmo sensors                  |
| `main_video.py` | Hardware-in-the-loop replay & testing | Pre-recorded video + static sensor values |

* **`main.py`** — Designed for deployment on a Raspberry Pi with a camera module and Netatmo weather station. Captures live images and real sensor data and publishes them via MQTT to the Processing Pi.
* **`main_video.py`** — Designed for development, testing, and **hardware-in-the-loop evaluation**. Processes pre-recorded video files and attaches configurable static sensor values, reproducing the image/sensor streams used in the paper’s experiments.

---

## Configuration

MQTT settings, simulation flags, and basic runtime parameters are configured in `config.py`.

Netatmo credentials are provided via a `.env` file which the application loads at runtime.

### Simulation Flags

Two flags in `config.py` allow running without real hardware or network access:

* `SIMULATE_IMAGE_CREATION` – when set to `True` the camera handler creates dummy images instead of using a camera.
* `SIMULATE_SENSOR_DATA` – when set to `True` the sensor handler generates random temperature, humidity, and pressure values instead of contacting Netatmo sensors.

Adjust these settings in `config.py` to switch between simulated and real data sources.

---

## Video Processing Mode (`main_video.py`)

`main_video.py` is used when processing pre-recorded video files instead of a live camera feed. This mode was used in the **hardware-in-the-loop replays** described in the paper, where identical video streams are paired with different sensor regimes (e.g., “Real-wet”, “Neutral”, “Anti-flood”).

Typical use cases:

* Replaying recorded flood sequences into the Processing Pi for experiments
* Testing and development without a physical camera
* Batch processing of archived video data

### Setup for Video Mode

1. **Install dependencies** (OpenCV is required for video processing):

   ```bash
   pip install opencv-python
   # or
   pip install -r requirements.txt
   ```

2. **Configure the video source** in `main_video.py`:

   ```python
   VIDEO_PATH = "path/to/your/video.mp4"  # Update this path
   CAMERA_ID = "video_camera_01"          # Camera identifier for metadata
   ```

3. **Configure motion state** (optional, matches paper’s stopped/slow/fast):

   ```python
   MOTION = "slow"   # Options: "slow", "fast", "stop"
   ```

4. **Set static sensor values** (used to emulate sensor regimes):

   ```python
   STATIC_TEMPERATURE = 12.0   # Celsius
   STATIC_HUMIDITY    = 88.0   # Percentage
   STATIC_PRESSURE    = 995.0  # hPa
   ```

   By changing these values you can approximate the different regimes used in the paper (e.g. “Real-wet”, “Neutral”, “Anti-flood”).

5. **Set frame processing interval** (aligned with video timestamps):

   ```python
   FRAME_INTERVAL = 0.5  # Seconds between frames
   ```

### Running Video Mode

```bash
python main_video.py
```

The script will:

* Extract frames at time-aligned intervals (based on `FRAME_INTERVAL`)
* Attach static sensor data to each frame
* Add metadata (timestamp, camera ID, video timestamp, motion state)
* Format and publish data via MQTT (if enabled in `config.py`)
* Save extracted frames to `edge_data_collector/camera/images/`

Press `Ctrl+C` to stop processing.

### Video Mode Features

* **VideoHandler**: Extracts frames from video files using OpenCV
* **StaticSensorHandler**: Provides consistent sensor readings throughout video processing
* **Time-aligned extraction**: Frames are extracted at stable time intervals
* **MQTT compatible**: Publishes to the same topics and schema as live mode
* **Format compatible**: Message format matches live camera mode for downstream processing

### Supported Video Formats

Any format supported by OpenCV, including:

* MP4 (`.mp4`)
* AVI (`.avi`)
* MOV (`.mov`)
* MKV (`.mkv`)

---

## Live Production Mode (`main.py`)

For live camera and sensor data collection on edge devices (e.g., Raspberry Pi):

```bash
python main.py
```

This mode requires:

* Raspberry Pi with a compatible camera module (or `SIMULATE_IMAGE_CREATION = True`)
* Netatmo weather station credentials in `.env` (or `SIMULATE_SENSOR_DATA = True`)
* An MQTT broker accessible at the configured address

In this mode the device acts as the **Gathering Pi** in the architecture, streaming frames and sensor readings to the Processing Pi.

---

## MQTT Contract

Both live and video modes publish a single message type on the configured `sensor/data` topic with a JSON structure similar to:

```json
{
  "image_data": "<base64-jpeg>",
  "sensor_data": {
    "temperature": 25.0,
    "humidity": 55.0,
    "pressure": 1013.25
  },
  "metadata": {
    "timestamp": "2025-02-07T12:00:00Z",
    "location": "50.8503,4.3517",
    "camera_id": "video_camera_01",
    "motion": "slow",
    "resource_constrained": false,
    "collector_capture_ts": 1738929600.123,
    "collector_publish_ts": 1738929600.456,
    "video_timestamp_sec": 12.345,
    "video_file": "flood_video_20251005_150618.mp4"
  }
}
```

| Field | Description |
| ----- | ----------- |
| `timestamp` | ISO 8601 timestamp when the frame was captured |
| `location` | GPS coordinates (latitude, longitude) |
| `camera_id` | Identifier for the camera or video source |
| `motion` | Motion state hint (`slow`, `fast`, or `stop`) |
| `resource_constrained` | Flag indicating resource-constrained mode |
| `collector_capture_ts` | Unix timestamp (seconds) when the frame was captured |
| `collector_publish_ts` | Unix timestamp (seconds) when the message was published |
| `video_timestamp_sec` | *(Video mode only)* Timestamp within the source video |
| `video_file` | *(Video mode only)* Filename of the source video |

The Processing Pi (in the `flood_detection_system` repo) subscribes to this topic and performs FSM orchestration, inference, scoring, and logging as described in the paper.

---

## Reproducing the Paper’s Experiments (High Level)

To reproduce the ablation results reported in the paper:

1. **Start the Processing/Jetson system** from the `flood_detection_system` repository using the desired configuration (e.g. production, static baselines, sensor variants).
2. **Run this Edge Data Collector**:

   * Use `main.py` for live data collection in the field, or
   * Use `main_video.py` to replay recorded videos with static sensor values matching the desired regime.
3. The Processing Pi will consume `sensor/data` messages, perform inference and logging, and write per-frame JSON results as described in the paper’s evaluation section.

For exact configuration folders, thresholds, and analysis scripts, see the README and scripts in the `flood_detection_system` repository.

---

## License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.
