import logging

from extract import fetch_all
from load import load_daily_row
from transform import transform_daily


LOCATIONS = [
    {
        "name": "Tbilisi",
        "latitude": 41.7151,
        "longitude": 44.8271,
        "timezone": "Asia/Tbilisi",
    },
    {
        "name": "New York",
        "latitude": 40.7128,
        "longitude": -74.0060,
        "timezone": "America/New_York",
    },
]


def run_pipeline(past_days=1):
    loaded_rows = []

    for location in LOCATIONS:
        raw_data = fetch_all(
            location["name"],
            location["latitude"],
            location["longitude"],
            location["timezone"],
            past_days=past_days,
        )
        daily_row = transform_daily(raw_data)
        load_daily_row(daily_row)
        loaded_rows.append(daily_row)

    return loaded_rows


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    )

    rows = run_pipeline()
    for row in rows:
        logging.info("Loaded %s for %s", row["name"], row["date"])
