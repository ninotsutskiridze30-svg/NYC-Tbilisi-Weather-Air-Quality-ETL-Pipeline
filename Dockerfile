FROM apache/airflow:2.11.2-python3.11
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir "apache-airflow==2.11.2" -r /tmp/requirements.txt && pip check
