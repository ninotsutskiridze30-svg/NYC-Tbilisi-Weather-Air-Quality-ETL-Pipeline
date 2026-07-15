import pandas as pd


def _round_number(value, digits=2):
    if pd.isna(value):
        return None
    return round(float(value), digits)


def _hourly_to_dataframe(hourly_data):
    df = pd.DataFrame(hourly_data)
    df["time"] = pd.to_datetime(df["time"])
    df["date"] = df["time"].dt.date
    return df


def transform_daily(raw_data):
    weather_df = _hourly_to_dataframe(raw_data["weather"]["hourly"])
    air_quality_df = _hourly_to_dataframe(raw_data["air_quality"]["hourly"])

    hourly_df = weather_df.merge(
        air_quality_df,
        on=["time", "date"],
        how="inner",
    )

    complete_dates = hourly_df.groupby("date").filter(lambda group: len(group) == 24)
    if complete_dates.empty:
        raise ValueError("No complete 24-hour day found in extracted data.")

    target_date = complete_dates["date"].min()
    daily_df = complete_dates[complete_dates["date"] == target_date]

    return {
        "name": raw_data["name"],
        "latitude": raw_data["latitude"],
        "longitude": raw_data["longitude"],
        "timezone": raw_data["timezone"],
        "date": target_date,
        "temp_avg_c": _round_number(daily_df["temperature_2m"].mean()),
        "temp_min_c": _round_number(daily_df["temperature_2m"].min()),
        "temp_max_c": _round_number(daily_df["temperature_2m"].max()),
        "humidity_avg_pct": _round_number(daily_df["relative_humidity_2m"].mean()),
        "precipitation_sum_mm": _round_number(daily_df["precipitation"].sum()),
        "wind_speed_avg_kmh": _round_number(daily_df["wind_speed_10m"].mean()),
        "pm10_avg": _round_number(daily_df["pm10"].mean()),
        "pm2_5_avg": _round_number(daily_df["pm2_5"].mean()),
        "carbon_monoxide_avg": _round_number(daily_df["carbon_monoxide"].mean()),
        "ozone_avg": _round_number(daily_df["ozone"].mean()),
        "european_aqi_avg": _round_number(daily_df["european_aqi"].mean(), 1),
    }
