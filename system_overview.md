# System Overview

## Purpose
Edge Data Processor collects imagery and environmental telemetry at the network edge and optionally relays the packaged payload to a backend via MQTT. It targets devices such as Raspberry Pi with camera modules and Netatmo weather sensors but can also run in a fully simulated mode for development.

## High-Level Workflow
1. `main.py` reloads the `.env` file to ensure Netatmo tokens are fresh and reads runtime switches from `config.py`.
2. Handlers are instantiated for the camera, Netatmo sensor integration, metadata enrichment, and optional MQTT transport.
3. On each iteration the camera captures or simulates an image, sensor data is fetched or synthesized, and metadata is appended.
4. `format_data` normalizes the metadata, base64-encodes the image, and the composed payload is either published to MQTT or printed for inspection when MQTT is disabled.

## Key Components
### Configuration (`config.py`)
- Flags such as `USE_MQTT`, `SIMULATE_IMAGE_CREATION`, and `SIMULATE_SENSOR_DATA` steer runtime behaviour.
- MQTT broker, port, and topic defaults are set here but can be overridden via environment variables.
- Secrets and Netatmo OAuth tokens remain in `.env`, keeping credentials out of source control.

### Entry Point (`main.py`)
- Performs an environment reload that clears cached Netatmo-related variables before reading `.env`.
- Creates the `CameraHandler`, `SensorHandler`, `MetadataHandler`, and (when enabled) `MqttHandler`.
- Runs a five-second publishing loop when MQTT is active; otherwise captures one cycle and prints raw readings plus the formatted payload.

### Data Collection (`edge_data_collector`)
- `camera/camera_handler.py` abstracts PiCamera v2, legacy PiCamera, or a mock camera. In simulation mode it writes 1 MB of random bytes to timestamped image files inside `edge_data_collector/camera/images`. Optional compression uses `camera/utils.py::compress_image` (Pillow-backed) to shrink captures before transmission.
- `sensors/sensor_handler.py` authenticates with Netatmo's API using OAuth tokens, exposes helper flows for token exchange/refresh, and can synthesize random temperature/humidity/pressure readings when simulation is enabled. Fetched tokens are persisted back to `.env` for reuse.
- `metadata/metadata_handler.py` enriches payloads with a timestamp, static GPS coordinates, the camera identifier, and contextual hints such as motion state and resource constraints.
- `sensor_information/get_sensor_information.py` is a utility script that lists available Netatmo devices/modules to help configure the correct sensor IDs.

### Data Formatting (`edge_data_collector/formatter/data_formatter.py`)
- `format_data` copies any incoming metadata, normalises motion hints to `fast/slow/stop`, coerces resource flags to booleans, and injects the camera metadata.
- `encode_image` opens the captured file with Pillow, converts it to RGB JPEG, and base64-encodes the bytes so the payload can travel over text transports.

### Data Transmission (`edge_data_sender`)
- `transmission/mqtt_handler.py` wraps `paho-mqtt` to connect to a broker and publish JSON-serialised payloads to a configured topic.
- `connection/connection_manager.py` and `error_handling/error_handler.py` are present as placeholders for future connection lifecycle and fault-management logic.

## Data Payload Shape
Payloads emitted by `format_data` follow this structure:
```json
{
  "image_data": "<base64-encoded JPEG>",
  "sensor_data": {
    "temperature": 23.4,
    "humidity": 55.0,
    "pressure": 1012.3
  },
  "metadata": {
    "timestamp": "2024-05-01T12:34:56.789123",
    "location": "50.8503,4.3517",
    "camera_id": "camera_01",
    "motion": "slow",
    "resource_constrained": false
  }
}
```
Additional metadata supplied by callers is merged into the metadata block before normalisation.

## Simulation & Development Support
- Controlled via `config.py` flags allowing development without physical hardware. Image simulation produces repeatable binary files, and sensor simulation returns random but bounded values.
- When Netatmo access tokens expire, the sensor handler can either automatically refresh them or guide the operator through re-authentication. Updated tokens are written back to `.env`.
- The project ships with pytest scaffolding inside `tests/` for handlers, though most suites are currently stubs awaiting implementation.

## External Integrations
- **Netatmo Weather Station API** supplies environmental data and requires OAuth credentials (`NETATMO_*` variables in `.env`). The handler depends on `requests`, `python-dotenv`, and `PyJWT`.
- **MQTT Broker** receives the formatted payload when `USE_MQTT` is True. Any broker reachable at `MQTT_BROKER:MQTT_PORT` can be targeted; defaults fall back to localhost.
- **Pillow & PiCamera** support image handling. `picamera2` is imported when available on ARM hardware and falls back to legacy PiCamera or a bundled mock.

## Repository Layout
- `main.py` – orchestrates the data capture/publish loop.
- `edge_data_collector/` – camera, sensor, metadata, and formatting logic.
- `edge_data_sender/` – outbound transport abstractions.
- `config.py` – runtime switches and defaults.
- `tests/` – pytest entry points for core modules.
- `requirements.txt` – pinned dependencies for both runtime and development.

## Operational Notes
- Run `python main.py` after setting required `.env` values. Toggle simulation flags in `config.py` to match available hardware.
- When `USE_MQTT` is disabled the system still exercises the full capture/format pipeline and prints the payload, which is useful for debugging.
- Images captured in simulation mode accumulate under `edge_data_collector/camera/images`; clean up the directory periodically on constrained devices.
