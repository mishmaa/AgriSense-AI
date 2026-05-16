# AgriSense AI IoT Simulation System

The IoT simulator generates realistic smart agriculture telemetry for soil moisture, temperature, humidity, pH, water tank level, rain, light intensity, and wind speed.

## Architecture

```txt
iot-simulator
  -> FastAPI POST /api/v1/sensors/readings
  -> PostgreSQL sensor_readings table
  -> Alert engine evaluates thresholds
  -> notifications table stores alerts
  -> WebSocket /ws/sensors/{farm_id} broadcasts live telemetry
  -> WebSocket /ws/alerts/{user_id} broadcasts critical alerts
  -> React dashboard receives live updates
```

## Realistic Fluctuations

- Soil moisture slowly decreases during hot/light hours and increases during rain or irrigation pulses.
- Temperature follows a daily sinusoidal curve with random noise.
- Humidity inversely tracks temperature and rises with rainfall.
- Water tank level slowly falls during irrigation and recovers during refill/rain events.
- pH is mostly stable with tiny drift.
- Light intensity peaks around midday and drops at night.
- Wind speed uses gust-like random variation.
- Rain sensor produces event-based rainfall pulses.

## Alert Thresholds

Default alert rules:

- Soil moisture below 30%: critical irrigation alert.
- Temperature above 36 C: heat stress alert.
- Humidity above 88% with rain: fungal disease risk.
- Water tank below 20%: water reserve alert.
- pH below 5.5 or above 8.0: soil chemistry alert.
- Wind speed above 35 km/h: spray/drone operation warning.

## MQTT Option

The simulator can run without MQTT by posting directly to FastAPI. `mqtt_adapter.py` provides an optional publisher interface for Mosquitto, EMQX, or HiveMQ. Install `paho-mqtt` only if MQTT is required.

## Historical Analytics

Use `historical_generator.py` to generate CSV history or post batches into the API. The frontend analytics pages consume historical readings through:

```txt
GET /api/v1/sensors/readings/{farm_id}?limit=1000
```

## Run

```bash
python simulator.py --api-url http://localhost:8000/api/v1 --token YOUR_JWT --sensor-id SENSOR_UUID
```

Dry run without backend:

```bash
python simulator.py --dry-run
```
