-- Run with psql -v ON_ERROR_STOP=1 -f /path/to/project_stats.sql.
-- A consistent snapshot keeps totals and per-city counts aligned during loads.
BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ READ ONLY;

SELECT COUNT(*) AS total_rows,
       MIN(date) AS earliest_date,
       MAX(date) AS latest_date,
       COUNT(DISTINCT date) AS distinct_dates_loaded,
       COUNT(DISTINCT location_id) AS locations_with_data
FROM daily_weather;

SELECT l.name AS city,
       COUNT(d.id) AS rows_loaded,
       MIN(d.date) AS earliest_date,
       MAX(d.date) AS latest_date
FROM locations l
LEFT JOIN daily_weather d USING (location_id)
GROUP BY l.location_id, l.name
ORDER BY l.name;

SELECT COUNT(*) AS number_of_locations FROM locations;

COMMIT;
