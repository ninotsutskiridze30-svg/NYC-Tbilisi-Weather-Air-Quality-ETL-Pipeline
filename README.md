# NYC & Tbilisi Weather + Air Quality ETL Pipeline

An automated data pipeline that extracts daily weather and air quality data
for two cities from the Open-Meteo API, transforms it with Python/pandas,
and loads it into a PostgreSQL database — orchestrated by Apache Airflow
and fully containerized with Docker.

---

## What problem this solves

Weather and air quality data arrives as raw hourly API responses with
missing values, inconsistent units, and no historical storage. This
pipeline solves that by cleaning, aggregating, and persisting the data
daily into a structured database — making it queryable, auditable, and
ready for analysis.

---

## Architecture

![ETL Pipeline Architecture](docs/architecture.png)

| Layer | Tool |
|-------|------|
| Extraction | Python `requests` → Open-Meteo REST API |
| Transformation | `pandas` — null handling, unit conversion, daily aggregation |
| Loading | `psycopg2` — UPSERT into PostgreSQL |
| Orchestration | Apache Airflow (DAG runs daily at 06:00 UTC) |
| Infrastructure | Docker Compose (Airflow + PostgreSQL in containers) |

---

## Cities tracked

| City | Latitude | Longitude | Timezone |
|------|----------|-----------|----------|
| Tbilisi, Georgia | 41.7151 | 44.8271 | Asia/Tbilisi |
| New York, USA | 40.7128 | -74.0060 | America/New_York |

---

## Project structure

weather-etl-pipeline/
├── dags/
│   └── weather_dag.py        # Airflow DAG definition
├── src/
│   ├── extract.py            # Pull data from Open-Meteo APIs
│   ├── transform.py          # Clean and aggregate with pandas
│   └── load.py               # Write to PostgreSQL
├── sql/
│   └── schema.sql            # Table definitions (run once on setup)
├── tests/
│   └── test_transform.py     # Unit tests for transform logic
├── data/
│   └── sample_output.csv     # Example of what lands in the DB
├── docs/
│   └── architecture.png      # Pipeline diagram
├── docker-compose.yml        # Spins up Airflow + PostgreSQL
├── requirements.txt
└── README.md

---

## How to run it

### Prerequisites
- Docker Desktop installed and running
- Git

### Steps

```bash
# 1. Clone the repo
git clone https://github.com/ninotsutskiridze30-svg/weather-etl-pipeline.git
cd weather-etl-pipeline

# 2. Start the containers (Airflow + PostgreSQL)
docker-compose up -d

# 3. Wait ~60 seconds for Airflow to initialise, then open the UI
# http://localhost:8080  (user: airflow / password: airflow)

# 4. Enable the DAG called "weather_etl_daily" in the Airflow UI
#    It will run automatically at 06:00 UTC every day.
#    To trigger it immediately: click the ▶ button next to the DAG.

# 5. Query the results
docker exec -it <postgres-container-name> psql -U airflow -d airflow
SELECT * FROM daily_weather ORDER BY date DESC LIMIT 10;
```

---

## Sample output

| date | city | temp_avg_c | humidity_avg_pct | pm2_5_avg | european_aqi_avg |
|------|------|-----------|-----------------|-----------|-----------------|
| 2024-06-28 | Tbilisi | 26.4 | 52.1 | 8.3 | 21.0 |
| 2024-06-28 | New York | 24.1 | 68.3 | 14.7 | 35.0 |

*(Screenshot of actual output table goes here once you run the pipeline)*

---

## Key engineering decisions

**Idempotent loads** — the `UNIQUE(location_id, date)` constraint means
re-running the pipeline for a day that already has data performs an UPSERT
instead of creating duplicates. Safe to retry.

**Separation of concerns** — extract, transform, and load are independent
modules. Each can be tested and replaced without touching the others.

**Past-day logic** — the pipeline pulls `past_days=1` from Open-Meteo,
meaning it always fetches yesterday's *complete* data rather than today's
partial data. Reliable and consistent.

---

## Data source

Weather and air quality data provided by [Open-Meteo](https://open-meteo.com/)
under the [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) licence.
Free for non-commercial use — no API key required.