CREATE TABLE IF NOT EXISTS locations (
    location_id   SERIAL PRIMARY KEY,
    name          VARCHAR(100) NOT NULL,
    latitude      NUMERIC(8, 4) NOT NULL,
    longitude     NUMERIC(8, 4) NOT NULL,
    timezone      VARCHAR(50) NOT NULL,
    UNIQUE (name)
);

CREATE TABLE IF NOT EXISTS daily_weather (
    id                    SERIAL PRIMARY KEY,
    location_id           INTEGER NOT NULL REFERENCES locations(location_id),
    date                  DATE NOT NULL,

    -- weather columns
    temp_avg_c            NUMERIC(5, 2),
    temp_min_c            NUMERIC(5, 2),
    temp_max_c            NUMERIC(5, 2),
    humidity_avg_pct      NUMERIC(5, 2),
    precipitation_sum_mm  NUMERIC(6, 2),
    wind_speed_avg_kmh    NUMERIC(6, 2),

    -- air quality columns
    pm10_avg              NUMERIC(6, 2),
    pm2_5_avg             NUMERIC(6, 2),
    carbon_monoxide_avg   NUMERIC(8, 2),
    ozone_avg             NUMERIC(6, 2),
    european_aqi_avg      NUMERIC(5, 1),

    -- pipeline metadata
    loaded_at             TIMESTAMP NOT NULL DEFAULT NOW(),

    UNIQUE (location_id, date)
);
CREATE INDEX IF NOT EXISTS idx_daily_weather_date
    ON daily_weather (date);

CREATE INDEX IF NOT EXISTS idx_daily_weather_location_date
    ON daily_weather (location_id, date);

INSERT INTO locations (name, latitude, longitude, timezone)
VALUES
    ('Tbilisi', 41.7151, 44.8271, 'Asia/Tbilisi'),
    ('New York', 40.7128, -74.0060, 'America/New_York')
ON CONFLICT (name) DO NOTHING;