from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.hooks.base_hook import BaseHook

connection = BaseHook.get_connection("my_postgres_2")


default_args = {
    "owner": "test_user",
    "depends_on_past": False,
    "start_date": datetime(2025, 2, 27)
}

dag = DAG('dag2', default_args=default_args, schedule_interval='0 * * * *', catchup=True,
          max_active_tasks=3, max_active_runs=2, tags=['test dag', 'test'])

extract_data_and_load_into_temp_table = BashOperator(
    task_id='task1',
    bash_command='python3 /airflow/scripts/dag2/task1.py --date {{ ds }} ' +f'--host {connection.host} --dbname {connection.schema} --user {connection.login} --jdbc_password {connection.password} --port 5432',
    dag=dag
    )



