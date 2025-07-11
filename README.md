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
