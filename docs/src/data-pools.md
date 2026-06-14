# Data Pools

The generator draws categorical values from fixed pools, so the dataset is
realistic but bounded and reproducible.

- **Spacecrafts (20):** SC-001 … SC-020
- **Missions (5):** MISSION-ALPHA, MISSION-BETA, MISSION-GAMMA, MISSION-DELTA,
  MISSION-EPSILON
- **Sensor types → names:**
  - THERMAL: core_temp, hull_temp, engine_temp, solar_panel_temp
  - RADIATION: gamma_detector, neutron_flux, cosmic_ray_counter,
    alpha_particle_sensor
  - POWER: main_bus_voltage, battery_cell_1, solar_array_output, power_regulator
  - NAVIGATION: gyroscope_x, gyroscope_y, star_tracker, inertial_nav_unit
  - COMMS: uplink_signal, downlink_signal, antenna_temperature, transponder_power
- **Severities (weighted):** LOW 60%, MEDIUM 25%, HIGH 10%, CRITICAL 5%
- **Tags pool:** nominal, anomaly, warning, science, maintenance, downlink,
  uplink, attitude (0–3 per row, comma-separated)
