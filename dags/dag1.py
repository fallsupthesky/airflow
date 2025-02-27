from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator


default_args = {
    "owner": "test_user",
    "depends_on_past": False,
    "start_date": datetime(2025, 2, 26)
}

dag = DAG('dag1', default_args=default_args, schedule_interval='0 * * * *', catchup=True,
          max_active_tasks=3, max_active_runs=2, tags=['test dag', 'test'])

extract_data_and_load_into_temp_table = BashOperator(
    task_id='task1',
    bash_command='python3 /airflow/scripts/dag1/task1.py',
    dag=dag
    )