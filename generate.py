"""
Generates spacecraft_telemetry_events.csv with 100,000 rows.
Fixed seed=42 — output is deterministic and canonical.

Stdlib only, no third-party dependencies. Writes the CSV next to this script.

Usage:
    python generate.py
"""

import csv
import hashlib
import os
import random
import uuid
from datetime import date, datetime, timedelta, time
from decimal import Decimal
from pathlib import Path

random.seed(42)

N = 100_000
OUT_CSV = Path(__file__).parent / "spacecraft_telemetry_events.csv"

SPACECRAFTS = [f"SC-{i:03d}" for i in range(1, 21)]       # 20 spacecraft
MISSIONS    = ["MISSION-ALPHA", "MISSION-BETA", "MISSION-GAMMA", "MISSION-DELTA", "MISSION-EPSILON"]
SENSOR_TYPES = ["THERMAL", "RADIATION", "POWER", "NAVIGATION", "COMMS"]
SENSOR_NAMES = {
    "THERMAL":    ["core_temp", "hull_temp", "engine_temp", "solar_panel_temp"],
    "RADIATION":  ["cosmic_ray_counter", "gamma_detector", "xray_sensor"],
    "POWER":      ["solar_output", "battery_monitor", "power_bus_voltage"],
    "NAVIGATION": ["gps_receiver", "star_tracker", "imu_sensor", "gyroscope"],
    "COMMS":      ["antenna_signal", "transponder", "uplink_receiver"],
}
SEVERITIES = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
STATUS_CODES = [0, 1, 2, 3]   # SMALLINT
TAGS_POOL = ["nominal", "anomaly", "warning", "science", "maintenance", "downlink", "uplink", "attitude"]

EPOCH = datetime(2024, 1, 1)
EPOCH_DATE = date(2024, 1, 1)
YEAR_SECONDS = 365 * 24 * 3600


def maybe(val, pct_null=0.30):
    return None if random.random() < pct_null else val


def rand_decimal(precision, scale, lo, hi):
    val = round(random.uniform(lo, hi), scale)
    return Decimal(str(val))


def rand_timestamp(lo_offset=0, hi_offset=YEAR_SECONDS):
    return EPOCH + timedelta(seconds=random.randint(lo_offset, hi_offset))


def rand_date():
    return EPOCH_DATE + timedelta(days=random.randint(0, 364))


def rand_time():
    return time(random.randint(0, 23), random.randint(0, 59), random.randint(0, 59),
                random.randint(0, 999999))


def rand_tags():
    k = random.randint(0, 3)
    return ",".join(random.sample(TAGS_POOL, k)) if k else None


def rand_json():
    return f'{{"seq":{random.randint(1,9999)},"gain":{round(random.uniform(0,1),4)},"mode":"{random.choice(["auto","manual","safe"])}"}}'


rows = []
for i in range(N):
    sc   = random.choice(SPACECRAFTS)
    mis  = random.choice(MISSIONS)
    stype = random.choice(SENSOR_TYPES)
    sname = random.choice(SENSOR_NAMES[stype])
    is_anomaly = random.random() < 0.05
    severity   = random.choices(SEVERITIES, weights=[60, 25, 10, 5])[0]
    status_code = 0 if not is_anomaly else random.choice([1, 2, 3])
    ts = rand_timestamp()
    row_id = str(uuid.UUID(int=random.getrandbits(128)))
    checksum = hashlib.sha256(f"{row_id}{i}".encode()).hexdigest()

    lat  = maybe(rand_decimal(9, 6, -90, 90))
    lon  = maybe(rand_decimal(9, 6, -180, 180))
    alt  = maybe(rand_decimal(12, 3, 200, 42000))
    vel  = maybe(rand_decimal(12, 3, 7000, 28000))
    temp = maybe(rand_decimal(8, 3, -270, 1500))
    rad  = maybe(rand_decimal(10, 5, 0, 100))
    bat  = maybe(rand_decimal(5, 2, 0, 100))
    mass = maybe(rand_decimal(10, 3, 100, 5000))

    rows.append({
        "id":                row_id,
        "spacecraft_id":     sc,
        "mission_id":        mis,
        "event_sequence":    i + 1,
        "sensor_name":       sname,
        "sensor_type":       stype,
        "reading_int":       maybe(random.randint(-32768, 32767)),
        "reading_bigint":    maybe(random.randint(-2**31, 2**31)),
        "reading_decimal":   maybe(rand_decimal(18, 6, -1e9, 1e9)),
        "reading_double":    maybe(random.gauss(0, 1e6)),
        "reading_bool":      maybe(random.choice([True, False])),
        "reading_text":      maybe(f"raw:{sname}:{round(random.uniform(-1,1),4)}"),
        "status_code":       status_code,
        "severity":          severity,
        "is_anomaly":        is_anomaly,
        "event_date":        rand_date(),
        "event_time":        maybe(rand_time(), pct_null=0.15),
        "event_timestamp":   ts,
        "received_at":       maybe(ts + timedelta(seconds=random.randint(0, 60)), pct_null=0.10),
        "latitude":          lat,
        "longitude":         lon,
        "altitude_km":       alt,
        "velocity_kmh":      vel,
        "temperature_c":     temp,
        "radiation_level":   rad,
        "battery_percent":   bat,
        "payload_mass_kg":   mass,
        "operator_notes":    maybe(f"Note from operator {random.randint(1,20)} about {sname}"),
        "raw_payload_json":  maybe(rand_json(), pct_null=0.40),
        "tags":              rand_tags(),
        "checksum":          maybe(checksum, pct_null=0.05),
        "created_at":        ts,
        "updated_at":        ts + timedelta(seconds=random.randint(0, 3600)),
        "deleted_at":        maybe(ts + timedelta(days=random.randint(1, 365)), pct_null=0.92),
    })

COLUMN_ORDER = [
    "id", "spacecraft_id", "mission_id", "event_sequence", "sensor_name", "sensor_type",
    "reading_int", "reading_bigint", "reading_decimal", "reading_double", "reading_bool",
    "reading_text", "status_code", "severity", "is_anomaly",
    "event_date", "event_time", "event_timestamp", "received_at",
    "latitude", "longitude", "altitude_km", "velocity_kmh", "temperature_c",
    "radiation_level", "battery_percent", "payload_mass_kg",
    "operator_notes", "raw_payload_json", "tags", "checksum",
    "created_at", "updated_at", "deleted_at",
]


def _to_csv_val(v):
    if v is None:
        return ''
    if isinstance(v, bool):
        return 'true' if v else 'false'
    if isinstance(v, datetime):
        return v.strftime('%Y-%m-%d %H:%M:%S')
    if isinstance(v, date):
        return v.isoformat()
    if isinstance(v, time):
        return v.strftime('%H:%M:%S')
    if isinstance(v, Decimal):
        return str(v)
    return str(v)


print(f"Writing {N} rows → {OUT_CSV}...")
with open(OUT_CSV, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
    writer.writerow(COLUMN_ORDER)
    for row in rows:
        writer.writerow([_to_csv_val(row[k]) for k in COLUMN_ORDER])

size_mb = OUT_CSV.stat().st_size / 1024 / 1024
print(f"Written {N} rows → {OUT_CSV}, {size_mb:.1f} MB")
