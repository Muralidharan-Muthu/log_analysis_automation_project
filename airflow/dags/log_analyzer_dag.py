from airflow.providers.standard.operators.bash import BashOperator

import datetime
from airflow.sdk import DAG


with DAG(
    dag_id="log_dag",
    start_date=datetime.datetime(2025,10,26),
    schedule='0 12 * * *',
    catchup=False,
    tags=["log","DAG","analysis"],
) as dag:
    task1 = BashOperator(
        task_id='log_task',
        bash_command="sh /home/mural/log-analysis-automation/wrapperScript.sh "
    )