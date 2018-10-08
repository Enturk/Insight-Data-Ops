"""
Code that goes along with the Airflow located at:
http://airflow.readthedocs.org/en/latest/tutorial.html
"""
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
import os

default_args = {
    'owner': 'nazim',
    'depends_on_past': False,
    'catchup_by_default' : False,
    'start_date': datetime(2018, 10, 1),
    'email': ['nazimkaraca@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2018, 12, 1),
    # 'schedule_interval': '@weekly',
}

bashOps = """cd ~/Insight-Data-Ops/src/
./newTerraInst.sh
 """
# add after default args to thoroughly test changes:
# , schedule_interval=timedelta(minutes = 5)
dag = DAG('terraflow', default_args=default_args, schedule_interval=timedelta(minutes = 2))

# Operations
t1 = BashOperator(
    task_id='print_date',
    bash_command='date',
    dag=dag)

t2 = BashOperator(
    task_id='newTerraInst',
    bash_command=bashOps,
    dag=dag)

t2.set_upstream(t1)
