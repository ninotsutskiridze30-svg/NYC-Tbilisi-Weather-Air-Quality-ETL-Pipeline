from datetime import datetime, timedelta

import pytest

from src.transform import transform_daily


def _hourly_times(start, hours):
    start_time = datetime.fromisoformat(start)
    return [
        (start_time + timedelta(hours=hour)).strftime("%Y-%m-%dT%H:%M")
        for hour in range(hours)
    ]


def _raw_data(hours=24):
    times = _hourly_times("2026-07-14T00:00", hours)

    return {
        "name": "Tbilisi",
        "latitude": 41.7151,
        "longitude": 44.8271,
        "timezone": "Asia/Tbilisi",
        "weather": {
            "hourly": {
                "time": times,
                "temperature_2m": list(range(hours)),
                "relative_humidity_2m": [50] * hours,
                "precipitation": [1] * hours,
                "wind_speed_10m": [10] * hours,
            }
        },
        "air_quality": {
            "hourly": {
                "time": times,
                "pm10": [20] * hours,
                "pm2_5": [5] * hours,
                "carbon_monoxide": [100] * hours,
                "ozone": [30] * hours,
                "european_aqi": [25] * hours,
            }
        },
    }


def test_transform_daily_aggregates_one_complete_day():
    row = transform_daily(_raw_data())

    assert row["name"] == "Tbilisi"
    assert row["date"].isoformat() == "2026-07-14"
    assert row["temp_avg_c"] == 11.5
    assert row["temp_min_c"] == 0.0
    assert row["temp_max_c"] == 23.0
    assert row["humidity_avg_pct"] == 50.0
    assert row["precipitation_sum_mm"] == 24.0
    assert row["wind_speed_avg_kmh"] == 10.0
    assert row["pm2_5_avg"] == 5.0
    assert row["european_aqi_avg"] == 25.0


def test_transform_daily_rejects_incomplete_day():
    with pytest.raises(ValueError, match="No complete 24-hour day"):
        transform_daily(_raw_data(hours=23))
