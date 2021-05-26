#Objeto que instacia um DAG
from airflow import DAG
#Operadores, sao as tarefas do DAG, pode ser bash
from airflow.operators.bash_operator import BashOperator
# ou python
from airflow.operators.python_operator import PythonOperator
# Função utilitária de data
from airflow.utils.dates import days_ago
from datetime import timedelta

#Argumentos gerais do DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(2),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1
}

#DAG
dag = DAG(
    'airWF',
    default_args=default_args,
    description='A simple tutorial DAG22'#, #,
    # define intervalos regulares para executar o DAG
    #schedule_interval=timedelta(days=1)
)

#Tarefas do DAG
#t1, t2 e t3 sao tarefas desse workflow

t1 = BashOperator(
    task_id='print_date',
    bash_command='date',
    dag=dag
)

t2 = BashOperator(
    task_id='pwd',
    depends_on_past=False,
    bash_command='pwd',
    retries=3,
    dag=dag
)

t3 = BashOperator(
    task_id='print_host',
    depends_on_past=False,
    bash_command='hostname',
    dag=dag
)

#sequencia de tarefas - primeiro a t1, depois t2 e t3 ao mesmo tempo
#t1 >> [t2, t3] 
t1 >> t2 >> t3 
