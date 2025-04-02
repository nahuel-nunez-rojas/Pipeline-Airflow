from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.http.sensors.http import HttpSensor
import json
from airflow.providers.http.operators.http import HttpOperator
from airflow.operators.python_operator import PythonOperator
import pandas as pd
import os

# Function to transform and load weather data from the API
def transform_load_weather_data(task_instance):
    data = task_instance.xcom_pull(task_ids = 'extract_weather_data')
    city = data['name']
    weather_description = data['weather'][0]['description']
    temp_celsius = data['main']['temp'] - 273.15
    feels_like_celsius = data['main']['feels_like'] - 273.15
    min_temp_celsius = data['main']['temp_min'] - 273.15
    max_temp_celsius = data['main']['temp_max'] - 273.15
    pressure = data['main']['pressure']
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed']
    time_of_record = datetime.utcfromtimestamp(data['dt'] + data['timezone'])
    sunrise = datetime.utcfromtimestamp(data['sys']['sunrise'] + data['timezone'])
    sunset = datetime.utcfromtimestamp(data['sys']['sunset'] + data['timezone'])

    transformed_data = {
        'city': city,
        'weather_description': weather_description,
        'temp_celsius': temp_celsius,
        'feels_like_celsius': feels_like_celsius,
        'min_temp_celsius': min_temp_celsius,
        'max_temp_celsius': max_temp_celsius,
        'pressure': pressure,
        'humidity': humidity,
        'wind_speed': wind_speed,
        'time_of_record': time_of_record,
        'sunrise': sunrise,
        'sunset': sunset
    }

    transdormed_data_list = [transformed_data]
    df_data = pd.DataFrame(transdormed_data_list)

# Credentials for AWS S3
    aws_credentials = { "key": "ASIAYZZGTDDUL1LTAT3K",
                        "secret": "7FdXlvyr/4WVrW9rYKrVpehyRlDfGXM3I9xCrCEH",
                        "token": "FvoGZXIvYXdzEHoaDDllDwhS/ZCNm0sd/SJqbwcLSi0Fb0eCbjt7D7aVz32r+j7uXN9mt3nOvurNePOTahyFLm4JWbwg5Vixc7SlHEl+cFUuMRdcqWJLf3Ufk0oL6YAqQcPurwc2xgrDlnNJ/zIuBYvFAWl9Vc8d7Bv6+yWIVDbAQ7/riyi08LO/BjIojcITmxVUZOidgfhUuSGBRuqOOlbJMOrjYdVppiW3b52KLRRcpP3M2A=="
                        }

# Name the CSV file, which contains the current date and time
    now = datetime.now()
    dt_string = now.strftime("%d%m%Y%H%M%S")
    dt_string = 'current_weather_data_' + dt_string

# Save the DataFrame to a CSV file in local storage
    #output_dir = '/root/airflow'
    #os.makedirs(output_dir, exist_ok=True)
    #filepath = os.path.join(output_dir, dt_string + '.csv')
    #df_data.to_csv(filepath, index=False)

# Save the DataFrame to a CSV file in S3
    df_data.to_csv(f"s3://airflowweatherapi/{dt_string}.csv", index=False, storage_options=aws_credentials)

# Default configuration for the DAG in Apache Airflow
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 8),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=2)
}

# Define the DAG and its execution schedule
with DAG('weather_dag',
        default_args=default_args,
        description='A simple weather DAG',
        schedule_interval = "@daily",
        catchup = False) as dag:

# Check if the API is available
        is_weather_api_ready = HttpSensor(
        task_id='is_weather_api_ready',
        http_conn_id='weathermap_api',
        endpoint='/data/2.5/weather?id=2514256&appid=4259a8514d6bdea0f428102d0ac63426',
        )

# Task to extract data from the API
        extract_weather_data = HttpOperator(
        task_id = 'extract_weather_data',
        http_conn_id = 'weathermap_api',
        endpoint = '/data/2.5/weather?id=2514256&appid=4259a8514d6bdea0f428102d0ac63426',
        method = 'GET',
        response_filter = lambda r: json.loads(r.text),
        log_response = True
        )

        transform_load_weather_data = PythonOperator(
        task_id='transform_load_weather_data',
        python_callable=transform_load_weather_data,
        )

# Define the order of tasks
        is_weather_api_ready >> extract_weather_data >> transform_load_weather_data
        
