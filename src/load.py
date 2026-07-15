import os
from pathlib import Path

import psycopg2
from psycopg2.extras import RealDictCursor


DB_CONFIG = {
    "host": os.getenv("POSTGRES_HOST", "127.0.0.1"),
    "port": os.getenv("POSTGRES_PORT", "55432"),
    "dbname": os.getenv("POSTGRES_DB", "weather_etl"),
    "user": os.getenv("POSTGRES_USER", "weather_user"),
    "password": os.getenv("POSTGRES_PASSWORD", "weather_password"),
}

SCHEMA_PATH = Path(__file__).resolve().parents[1] / "sql" / "schema.sql"


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def initialize_database():
    schema_sql = SCHEMA_PATH.read_text(encoding="utf-8")

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(schema_sql)


def upsert_location(cursor, row):
    cursor.execute(
        """
        INSERT INTO locations (name, latitude, longitude, timezone)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (name)
        DO UPDATE SET
            latitude = EXCLUDED.latitude,
            longitude = EXCLUDED.longitude,
            timezone = EXCLUDED.timezone
        RETURNING location_id;
        """,
        (row["name"], row["latitude"], row["longitude"], row["timezone"]),
    )
    return cursor.fetchone()["location_id"]


def upsert_daily_weather(cursor, location_id, row):
    cursor.execute(
        """
        INSERT INTO daily_weather (
            location_id,
            date,
            temp_avg_c,
            temp_min_c,
            temp_max_c,
            humidity_avg_pct,
            precipitation_sum_mm,
            wind_speed_avg_kmh,
            pm10_avg,
            pm2_5_avg,
            carbon_monoxide_avg,
            ozone_avg,
            european_aqi_avg
        )
        VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
        ON CONFLICT (location_id, date)
        DO UPDATE SET
            temp_avg_c = EXCLUDED.temp_avg_c,
            temp_min_c = EXCLUDED.temp_min_c,
            temp_max_c = EXCLUDED.temp_max_c,
            humidity_avg_pct = EXCLUDED.humidity_avg_pct,
            precipitation_sum_mm = EXCLUDED.precipitation_sum_mm,
            wind_speed_avg_kmh = EXCLUDED.wind_speed_avg_kmh,
            pm10_avg = EXCLUDED.pm10_avg,
            pm2_5_avg = EXCLUDED.pm2_5_avg,
            carbon_monoxide_avg = EXCLUDED.carbon_monoxide_avg,
            ozone_avg = EXCLUDED.ozone_avg,
            european_aqi_avg = EXCLUDED.european_aqi_avg,
            loaded_at = NOW();
        """,
        (
            location_id,
            row["date"],
            row["temp_avg_c"],
            row["temp_min_c"],
            row["temp_max_c"],
            row["humidity_avg_pct"],
            row["precipitation_sum_mm"],
            row["wind_speed_avg_kmh"],
            row["pm10_avg"],
            row["pm2_5_avg"],
            row["carbon_monoxide_avg"],
            row["ozone_avg"],
            row["european_aqi_avg"],
        ),
    )


def load_daily_row(row):
    initialize_database()

    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            location_id = upsert_location(cursor, row)
            upsert_daily_weather(cursor, location_id, row)

    return row
