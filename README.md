# Edge Data Collector

This project captures images and sensor information and can transmit the data via MQTT.

## Simulation Options

Two environment variables allow running the application without real hardware or network access:

- `SIMULATE_IMAGE_CREATION` &ndash; when set to `true` the camera handler creates dummy images instead of using a camera.
- `SIMULATE_SENSOR_DATA` &ndash; when set to `true` the sensor handler generates random temperature, humidity and pressure values instead of contacting Netatmo sensors.

These flags can be toggled in your `.env` file to switch between simulated and real data sources.
