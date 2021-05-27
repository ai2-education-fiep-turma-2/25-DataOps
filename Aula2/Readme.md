# Airflow (https://airflow.apache.org/)
* Ferramenta para DATAops

* Instalacao https://airflow.apache.org/docs/stable/installation.html

```
conda install airflow
```


* Configurando base do Airflow

```
export AIRFLOW_HOME=~/airflowDB
airflow initdb
```

* Ajuste no arquivo de configuração $AIRFLOW_HOME/airflow.cfg
```
cookie_samesite=lax
```

* Colocando airflow em produção
  * web server
```
  airflow webserver -p 8891
```
  * scheduler
```
  airflow scheduler

* Criando um script para AirFlow (DAG - Directed Acyclic Graph)


Definindo um script airflow 

Instanciando objetos:

```
#Objeto que instacia um DAG
from airflow import DAG
#Operadores, sao as tarefas do DAG, pode ser bash
from airflow.operators.bash_operator import BashOperator
# ou python
from airflow.operators.python_operator import PythonOperator
# Função utilitária de data
from airflow.utils.dates import days_ago
```

Configuracoes de inicializacao de um DAG

```
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
```

Construindo um DAG
```
dag = DAG(
    'tutorial2',
    default_args=default_args,
    description='A simple tutorial DAG22' #,
    # define intervalos regulares para executar o DAG
    #schedule_interval=timedelta(days=1),
)
```

Opcoes para intervalo de tempo da execução do DAG
```
    #schedule_interval=timedelta(days=1)
```

* Tarefas do DAG

```
#t1, t2 e t3 sao tarefas desse workflow
t1 = BashOperator(
    task_id='print_date',
    bash_command='date',
    dag=dag,
)

t2 = BashOperator(
    task_id='sleep',
    depends_on_past=False,
    bash_command='sleep 5',
    retries=3,
    dag=dag,
)

t3 = BashOperator(
    task_id='templated',
    depends_on_past=False,
    bash_command=templated_command,
    params={'my_param': 'Parameter I passed in'},
    dag=dag,
)
```

Sequencia de execução das tarefas
Uma após a outra
```
t1 >> t2 >> t3 
```

T2 e t3 em paralelo após t1
```
t1 >> [t2, t3] 
```

* Preparando dados para sprint Sicoob

* Criando operadores python

* Sequencia de transformação de dados

* Depois de desenvolvido o DAG deve ser copiado para a pasta de DAGs do airflow: AIRFLOW_HOME

* Utilitários do AirFlow para manipular o DAG:
```
#print list of DAGs
airflow list_dags

# mostra tarefas de um DAG especifico
airflow list_tasks tutorialteste

# mostra hierarquia de tarefas de um DAG
airflow list_tasks tutorialteste --tree
```

* Executando tarefas de um DAG
```
airflow test tutorialteste pwd 2015-01-01
airflow test tutorialteste print_date 2015-01-01
airflow test tutorialteste print_host 2015-01-01

```
* Backfill: executa o DAG completo considerando as dependencias.Permite acompanhar o progresso da execucao na interface gráfica
* Por Padrão o DAG é executado uma vez por dia, se passar um intervalor com 3 dias o DAG sera executado 3 vezes

```
airflow backfill tutorialteste -s 2015-06-01 -e 2015-06-07
```

## Exemplo de workflow com operadores em python (WFAuto.py)
  * Preparação e treino do modelo em duas tarefas

## Acessando resultados de consulta no hive pelo python
```
pip install pyhive
```

* Exemplo de client python para hive: hivePython.py

```
from pyhive import hive
import pandas as pd

PORT=10000
conn = hive.Connection(host="127.0.0.1", port=PORT, username="silvio")

print(conn)

dataframe = pd.read_sql("select * from modelos.diabetes", conn)
print(dataframe.describe())
```

## Criando dataset Hive a partir do problema Olist (https://www.kaggle.com/olistbr/brazilian-ecommerce)

* copiando arquivos para o HDFS

```
hadoop fs -put /home/silvio/dataset/olist/*.csv /home/silvio/hiveW/warehouse/
```

* criação do dataset

```
CREATE TABLE IF NOT EXISTS customers ( 
customer_id STRING,
customer_unique_id STRING,
customer_zip_code_prefix INT,
customer_city STRING,
customer_state STRING
) ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' STORED AS TEXTFILE;


CREATE TABLE IF NOT EXISTS pedidos ( 
order_id STRING,
customer_id STRING,
order_status  STRING,
order_purchase_timestamp  STRING,
order_approved_at  STRING,
order_delivered_carrier_date  STRING,
order_delivered_customer_date  STRING,
order_estimated_delivery_date  STRING
) ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' STORED AS TEXTFILE;


CREATE TABLE IF NOT EXISTS itens_pedidos ( 
order_id STRING,
order_item_id STRING,
product_id STRING,
seller_id STRING,
shipping_limit_date STRING,
price STRING,
freight_value STRING
) ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' STORED AS TEXTFILE;

```

* carregamento dos dados

```
LOAD DATA LOCAL INPATH '/home/silvio/hiveW/warehouse/olist_customers_dataset.csv' INTO TABLE olist.customers; 
LOAD DATA LOCAL INPATH '/home/silvio/hiveW/warehouse//olist_orders_dataset.csv' INTO TABLE olist.pedidos;
LOAD DATA LOCAL INPATH '/home/silvio/hiveW/warehouse/olist_order_items_dataset.csv' INTO TABLE olist.itens_pedidos;
```

* criando tabela nova para relatório unificando dados de cliente e pedidos
```
create table pedido_cliente_join(order_id string, customer_unique_id string, order_purchase_timestamp string, customer_state string);
```

* select com join
```
select  pedidos.order_id, customers.customer_unique_id, pedidos.order_purchase_timestamp, customers.customer_state from customers LEFT OUTER JOIN pedidos on (customers.customer_id = pedidos.customer_id);
```

* atualizando tabela de relatório
```
INSERT OVERWRITE TABLE pedido_cliente_join  select  pedidos.order_id, customers.customer_unique_id, pedidos.order_purchase_timestamp, customers.customer_state from customers LEFT OUTER JOIN pedidos on (customers.customer_id = pedidos.customer_id);
```
