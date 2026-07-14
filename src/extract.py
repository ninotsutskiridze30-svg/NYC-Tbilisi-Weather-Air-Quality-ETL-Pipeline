import logging

import requests

logger = logging.getLogger(__name__)

WEATHER_URL = "https://api.open-meteo.com/v1/forecast"
AIR_QUALITY_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"

WEATHER_VARS = [
    "temperature_2m",
    "relative_humidity_2m",
    "precipitation",
    "wind_speed_10m",
]

AIR_QUALITY_VARS = [
    "pm10",
    "pm2_5",
    "carbon_monoxide",
    "ozone",
    "european_aqi",
]


def _fetch_open_meteo(url, variables, latitude, longitude, timezone, past_days):
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": ",".join(variables),
        "timezone": timezone,
        "past_days": past_days,
        "forecast_days": 1,
    }

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()

    data = response.json()
    hourly = data.get("hourly", {})
    if "time" not in hourly:
        raise ValueError(f"API response is missing hourly time data: {data}")

    return data


def fetch_weather(latitude, longitude, timezone, past_days=1):
    logger.info("Fetching weather for (%.4f, %.4f)", latitude, longitude)

    data = _fetch_open_meteo(
        WEATHER_URL,
        WEATHER_VARS,
        latitude,
        longitude,
        timezone,
        past_days,
    )
    logger.info("Weather fetch OK - %d hourly records", len(data["hourly"]["time"]))
    return data


def fetch_air_quality(latitude, longitude, timezone, past_days=1):
    logger.info("Fetching air quality for (%.4f, %.4f)", latitude, longitude)

    data = _fetch_open_meteo(
        AIR_QUALITY_URL,
        AIR_QUALITY_VARS,
        latitude,
        longitude,
        timezone,
        past_days,
    )
    logger.info("Air quality fetch OK - %d hourly records", len(data["hourly"]["time"]))
    return data


def fetch_all(name, latitude, longitude, timezone, past_days=1):
    logger.info("--- Extracting: %s ---", name)
    return {
        "name": name,
        "latitude": latitude,
        "longitude": longitude,
        "timezone": timezone,
        "weather": fetch_weather(latitude, longitude, timezone, past_days),
        "air_quality": fetch_air_quality(latitude, longitude, timezone, past_days),
    }
