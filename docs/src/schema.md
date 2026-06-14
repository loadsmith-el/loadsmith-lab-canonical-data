# Schema

This repo is the **schema source of truth**. The 34 columns, their order, types,
and null rates below are **canonical**. Every consumer must match them:

- each service image's `init.sql` (e.g.
  `loadsmith-lab-canonical-images/images/lab-postgres-15/init.sql`) recreates this
  exact schema in its database dialect and bulk-loads the CSV (header row
  present, empty = NULL);
- the CSV column order is exactly the order below.

When you change the schema here, **bump `VERSION` + the tag** and update every
image's `init.sql` to match — see [Versioning](./versioning.md).

```sql
CREATE TABLE spacecraft_telemetry_events (
    -- Identity
    id               VARCHAR(36)      NOT NULL PRIMARY KEY,
    spacecraft_id    VARCHAR(50)      NOT NULL,
    mission_id       VARCHAR(50)      NOT NULL,
    event_sequence   BIGINT           NOT NULL,

    -- Sensor identity
    sensor_name      VARCHAR(100)     NOT NULL,
    sensor_type      VARCHAR(50)      NOT NULL,

    -- Sensor readings (nullable — ~30% null)
    reading_int      INTEGER,
    reading_bigint   BIGINT,
    reading_decimal  DECIMAL(18, 6),
    reading_double   DOUBLE PRECISION,
    reading_bool     BOOLEAN,
    reading_text     TEXT,

    -- Event classification
    status_code      SMALLINT         NOT NULL,
    severity         VARCHAR(20)      NOT NULL,
    is_anomaly       BOOLEAN          NOT NULL,

    -- Temporal
    event_date       DATE             NOT NULL,
    event_time       TIME,                           -- ~15% null
    event_timestamp  TIMESTAMP        NOT NULL,
    received_at      TIMESTAMP,                      -- ~10% null

    -- Position and motion (nullable — ~30% null)
    latitude         DECIMAL(9, 6),
    longitude        DECIMAL(9, 6),
    altitude_km      DECIMAL(12, 3),
    velocity_kmh     DECIMAL(12, 3),

    -- Physical telemetry (nullable — ~30% null)
    temperature_c    DECIMAL(8, 3),
    radiation_level  DECIMAL(10, 5),
    battery_percent  DECIMAL(5, 2),
    payload_mass_kg  DECIMAL(10, 3),

    -- Payload and notes
    operator_notes   TEXT,                           -- ~30% null
    raw_payload_json TEXT,                           -- ~40% null
    tags             TEXT,                           -- comma-separated; ~30% null
    checksum         CHAR(64),                       -- SHA-256 hex; ~5% null

    -- Audit timestamps
    created_at       TIMESTAMP        NOT NULL,
    updated_at       TIMESTAMP        NOT NULL,
    deleted_at       TIMESTAMP                       -- ~92% null
);
```

## Column reference

| # | Column | Postgres type | Arrow type | Nullable | Description |
|---|---|---|---|---|---|
| 1 | `id` | `VARCHAR(36)` | `Utf8` | No | UUID v4 string |
| 2 | `spacecraft_id` | `VARCHAR(50)` | `Utf8` | No | SC-001 … SC-020 |
| 3 | `mission_id` | `VARCHAR(50)` | `Utf8` | No | MISSION-ALPHA … MISSION-EPSILON |
| 4 | `event_sequence` | `BIGINT` | `Int64` | No | 1–100,000, unique per row |
| 5 | `sensor_name` | `VARCHAR(100)` | `Utf8` | No | Type-specific sensor identifier |
| 6 | `sensor_type` | `VARCHAR(50)` | `Utf8` | No | THERMAL, RADIATION, POWER, NAVIGATION, COMMS |
| 7 | `reading_int` | `INTEGER` | `Int32` | Yes (~30%) | Nullable integer reading |
| 8 | `reading_bigint` | `BIGINT` | `Int64` | Yes (~30%) | Nullable bigint reading |
| 9 | `reading_decimal` | `DECIMAL(18,6)` | `Utf8` | Yes (~30%) | Stringified decimal |
| 10 | `reading_double` | `DOUBLE PRECISION` | `Float64` | Yes (~30%) | Nullable float |
| 11 | `reading_bool` | `BOOLEAN` | `Boolean` | Yes (~30%) | Nullable boolean |
| 12 | `reading_text` | `TEXT` | `Utf8` | Yes (~30%) | Free-form string |
| 13 | `status_code` | `SMALLINT` | `Int32` | No | 0, 1, 2, or 3 |
| 14 | `severity` | `VARCHAR(20)` | `Utf8` | No | LOW, MEDIUM, HIGH, CRITICAL |
| 15 | `is_anomaly` | `BOOLEAN` | `Boolean` | No | True ~5% of rows |
| 16 | `event_date` | `DATE` | `Date32` | No | Random date in 2024 |
| 17 | `event_time` | `TIME` | `Utf8` | Yes (~15%) | Stringified time (HH:MM:SS) |
| 18 | `event_timestamp` | `TIMESTAMP` | `Timestamp(ms)` | No | Random timestamp in 2024 |
| 19 | `received_at` | `TIMESTAMP` | `Timestamp(ms)` | Yes (~10%) | ~event_timestamp + 0–60s |
| 20 | `latitude` | `DECIMAL(9,6)` | `Utf8` | Yes (~30%) | -90.0 to 90.0 |
| 21 | `longitude` | `DECIMAL(9,6)` | `Utf8` | Yes (~30%) | -180.0 to 180.0 |
| 22 | `altitude_km` | `DECIMAL(12,3)` | `Utf8` | Yes (~30%) | 200–42,000 km |
| 23 | `velocity_kmh` | `DECIMAL(12,3)` | `Utf8` | Yes (~30%) | 7,000–28,000 km/h |
| 24 | `temperature_c` | `DECIMAL(8,3)` | `Utf8` | Yes (~30%) | -270 to 1,500 °C |
| 25 | `radiation_level` | `DECIMAL(10,5)` | `Utf8` | Yes (~30%) | 0.0–100.0 |
| 26 | `battery_percent` | `DECIMAL(5,2)` | `Utf8` | Yes (~30%) | 0.0–100.0 |
| 27 | `payload_mass_kg` | `DECIMAL(10,3)` | `Utf8` | Yes (~30%) | 100–5,000 kg |
| 28 | `operator_notes` | `TEXT` | `Utf8` | Yes (~30%) | Free-form sentence |
| 29 | `raw_payload_json` | `TEXT` | `Utf8` | Yes (~40%) | Simulated JSON payload string |
| 30 | `tags` | `TEXT` | `Utf8` | Yes (~30%) | Comma-separated from pool of 8 |
| 31 | `checksum` | `CHAR(64)` | `Utf8` | Yes (~5%) | SHA-256 hex of `id + event_sequence` |
| 32 | `created_at` | `TIMESTAMP` | `Timestamp(ms)` | No | Same as `event_timestamp` |
| 33 | `updated_at` | `TIMESTAMP` | `Timestamp(ms)` | No | `created_at` + 0–3,600s |
| 34 | `deleted_at` | `TIMESTAMP` | `Timestamp(ms)` | Yes (~92%) | `created_at` + 1–365 days when set |

## Why DECIMAL/TIME columns are Utf8 in Arrow

The Postgres source plugin uses `simple_query` (the text wire protocol), so every
value arrives as its exact string form — `DECIMAL(18,6)` as `"1234567.890000"`.
Arrow has no native decimal type that covers arbitrary precision losslessly, so
the source preserves the text representation and maps all NUMERIC, DECIMAL, and
TIME columns to `Utf8`. A destination needing native decimals parses the string
itself.
