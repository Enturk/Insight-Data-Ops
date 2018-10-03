"""
Code that goes along with the Airflow located at:
http://airflow.readthedocs.org/en/latest/tutorial.html
"""
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
import os

InsightDir = os.getcwd()

default_args = {
    'owner': 'nazim',
    'depends_on_past': False,
    'start_date': datetime(2018, 10, 1),
    'email': ['nazimkaraca@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    'end_date': datetime(2018, 12, 1),
    'schedule_interval': '@weekly',
}

dag = DAG(
    'terraflow', default_args=default_args,schedule_interval=timedelta(1))

# Operations
t1 = BashOperator(
    task_id='print_date',
    bash_command='date',
    dag=dag)

t2 = BashOperator(
    task_id='newTerraInst',
    bash_command='.' + InsightDir + '/src/newTerraInst.sh',
    dag=dag)

t2.set_upstream(t1)
