#Objeto que instacia um DAG
from airflow import DAG
#Operadores, sao as tarefas do DAG, pode ser bash
from airflow.operators.bash_operator import BashOperator
# ou python
from airflow.operators.python_operator import PythonOperator
# Função utilitária de data
from airflow.utils.dates import days_ago
from airflow.operators import PythonOperator
from datetime import timedelta

import pandas as pd
import numpy as np 
from numpy import vstack
import matplotlib.pyplot as plt

import sklearn
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, mean_squared_error

from math import sqrt

import tensorflow as tf
import tensorflow.keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import to_categorical

from pickle import dump

import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder

DATASET='/home/silvio/dataset/'

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
    'Auto-WF',
    default_args=default_args,
    description='Auto-WF'#, #,
    # define intervalos regulares para executar o DAG
    #schedule_interval=timedelta(days=1)
)

def preparar():
    df = pd.read_csv(DATASET+'Auto2.csv') 
    df.describe()

    le = LabelEncoder()
    df['originL']= le.fit_transform(df['origin'])

    df=df.drop(columns = ['name','origin'])
    df.to_csv(DATASET+'auto_final.csv')

def treinar():
    df = pd.read_csv(DATASET+'auto_final.csv') 

    target = df[['mpg']] 
    predictors = df[['cylinders','displacement','horsepower','weight','acceleration','year','originL']]

    X = predictors.values
    y = target.values

    sc2 = StandardScaler()
    X = sc2.fit_transform(X)
    dump(sc2, open(DATASET+'scaler.pkl', 'wb'))

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=40)
    print(X_train.shape); 
    print(X_test.shape)

    model = Sequential()
    model.add(Dense(64, activation='relu', input_dim=X.shape[1]))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(1, activation='relu'))

    optimizer = tf.keras.optimizers.RMSprop()

    model.compile(loss='mse', optimizer=optimizer, metrics=['mae', 'mse'])

    model.fit(X_train, y_train, epochs=200, validation_split=0.3)
    model.save(DATASET+'autoModel.h5')

    version='1'

prep = PythonOperator(task_id='preparar', python_callable=preparar, dag=dag,)
treino = PythonOperator(task_id='treinar', python_callable=treinar , dag=dag ,)

#Tarefas do DAG
#t1, t2 e t3 sao tarefas desse workflow

#sequencia de tarefas - primeiro a t1, depois t2 e t3 ao mesmo tempo
#t1 >> [t2, t3] 
prep >> treino