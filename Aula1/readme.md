Aula 1

## Instalação e Config do HIVE

* Download Hive 2.3.8
* Trocar versão da biblioteca guava:
```  
  cp $HADOOP/share/hadoop/hdfs/lib/guava-27.0-jre.jar  $HIVE/lib/
```

* Criar pasta para salvar bancos de dados no haddop (HDFS)
```
  hdfs dfs -mkdir -p /home/silvio/hiveW/warehouse
  hdfs dfs -chmod g+w home/silvio/hiveW/warehouse
```

* Configurar file system dos DBs
```
cd $HIVE_HOME/conf
cp hive-default.xml.template hive-site.xml
```

* Alterar path do warehouse hive-site.xml

* Configurar metastore

```
schematool -dbType derby -initSchema
```


## Hive ClI

* iniciar o cli
```
hive
```

* mostrar bancos de dados

```
SHOW DATABASES;
```

* criar um banco novo
```
CREATE DATABASE human_resources;
```

* Colocar banco de dados na área
```
 USE human_resources;
```

* criar tabela
```
create table modelos.diabete( Pregnancies FLOAT, Glucose FLOAT ,BloodPressure FLOAT ,SkinThickness FLOAT ,Insulin FLOAT ,BMI FLOAT ,DiabetesPedigreeFunction FLOAT,Age FLOAT,Class FLOAT) 
```

* copiar csv para hdfs (terminal)

```
hadoop fs -put /home/silvio/git/25-DataOps/Aula1/pima-indians-diabetes.csv /home/silvio/hiveW/warehouse/AllstarFull.csv
```

* carregar arquivo csv para tabela (hivesql)
```
LOAD DATA LOCAL INPATH '/home/silvio/hiveW/warehouse/AllstarFull.csv' INTO TABLE modelos.diabete;
```


