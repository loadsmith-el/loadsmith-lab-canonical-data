# Data Pools

The generator draws categorical values from fixed pools, so the dataset is
realistic but bounded and reproducible.

- **Spacecrafts (20):** SC-001 … SC-020
- **Missions (5):** MISSION-ALPHA, MISSION-BETA, MISSION-GAMMA, MISSION-DELTA,
  MISSION-EPSILON
- **Sensor types → names:**
  - THERMAL: core_temp, hull_temp, engine_temp, solar_panel_temp
  - RADIATION: cosmic_ray_counter, gamma_detector, xray_sensor
  - POWER: solar_output, battery_monitor, power_bus_voltage
  - NAVIGATION: gps_receiver, star_tracker, imu_sensor, gyroscope
  - COMMS: antenna_signal, transponder, uplink_receiver
- **Severities (weighted):** LOW 60%, MEDIUM 25%, HIGH 10%, CRITICAL 5%
- **Tags pool:** nominal, anomaly, warning, science, maintenance, downlink,
  uplink, attitude (0–3 per row, comma-separated)
