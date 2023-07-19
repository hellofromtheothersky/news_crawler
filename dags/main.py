from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator

import pandas as pd


default_args = {
    'owner': 'hieu_nguyen',
    'retries': 5,
    'retry_delay': timedelta(minutes=1)
}


with DAG( 
    default_args=default_args,
    dag_id='news_crawler',
    description='crawl data from various newspaper sources, and then run kakka, spark',
    start_date = datetime.now()- timedelta(days=2),
    schedule_interval='* * * * *',
    catchup=False,
) as dag:
    start = BashOperator(
        task_id='start',
        bash_command="echo START",
    )
    crawl_kenh14 = BashOperator(
        task_id='crawl_kenh14',
        bash_command="cd /opt/airflow/news_crawler/ ; python3 crawl_me.py --s kenh14 --nc 1 --nn 1 --u 1 ; cd -" ,
    )
    crawl_vtv = BashOperator(
        task_id='crawl_vtv',
        bash_command="cd /opt/airflow/news_crawler/ ; python3 crawl_me.py --s vtv --nc 1 --nn 1 --u 1 ; cd -" ,
    )
    end = BashOperator(
        task_id='end',
        bash_command="echo END",
    )

    start>>[crawl_kenh14, crawl_vtv]>>end