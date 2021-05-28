## mlflow

* Instalar mlflow
```
conda install -c conda-forge mlflow=1.8.0
```

* Iniciando mlflow
```
mlflow server -p 8893 -h 0.0.0.0  --backend-store-uri 'file:///opt/' &
```

* rodar treino e salvar métricas
```
export MLFLOW_TRACKING_URI=http://127.0.0.1:8893
python train.py 0.2 0.4
```

* abrir na interface web a página http://localhost::8893

