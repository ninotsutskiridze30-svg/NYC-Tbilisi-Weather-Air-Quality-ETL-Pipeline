import sys
from datetime import datetime
from pathlib import Path

from airflow import DAG
from airflow.operators.python import PythonOperator


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from pipeline import run_pipeline


default_args = {
    "owner": "weather-etl",
    "retries": 1,
}


with DAG(
    dag_id="weather_etl_daily",
    description="Extract, transform, and load daily weather and air quality data.",
    default_args=default_args,
    start_date=datetime(2026, 1, 1),
    schedule="0 6 * * *",
    catchup=False,
    tags=["weather", "air-quality", "etl"],
) as dag:
    run_weather_etl = PythonOperator(
        task_id="run_weather_etl",
        python_callable=run_pipeline,
    )
