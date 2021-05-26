Aula 1

## Instalação e Config do HIVE

* Download Hive 2.3.8

* configurar variáveis de ambiente
```
export HIVE_HOME="/home/silvio/hivesource/apache-hive-2.3.8-bin"
export PATH=$PATH:$HIVE_HOME/bin

export HADOOP_HOME=/home/silvio/hadoop/hadoop-3.2.2/
export PATH=$HADOOP_HOME/bin/:$PATH
```

* Trocar versão da biblioteca guava (apagar a mais antiga do diretório $HIVE/lib/:
```  
  rm -rf $HIVE/lib/guava-14.0.1.jar
  cp $HADOOP/share/hadoop/hdfs/lib/guava-27.0-jre.jar  $HIVE/lib/
```

* Criar pasta para salvar bancos de dados no haddop (HDFS)
  *  escolha um diretório de acordo com o seu file system local
```
  hdfs dfs -mkdir -p /home/silvio/hiveW/warehouse
  hdfs dfs -chmod g+w /home/silvio/hiveW/warehouse
```

* Configurar file system dos DBs
```
cd $HIVE_HOME/conf
cp hive-default.xml.template hive-site.xml
```

* Alterar path do warehouse hive-site.xml
  * busque pela opção hive.metastore.warehouse.dir
  * subsitua o valor da propriedade pelo diretório criado no passo anterior /home/silvio/hiveW/warehouse
  
  
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

* criar tabela ( informando que está armazenada com textfile)
```
create table modelos.diabetes( Pregnancies FLOAT, Glucose FLOAT ,BloodPressure FLOAT ,SkinThickness FLOAT ,Insulin FLOAT ,BMI FLOAT ,DiabetesPedigreeFunction FLOAT,Age FLOAT,Class FLOAT) ROW FORMAT DELIMITED FIELDS 
TERMINATED BY ',' STORED AS TEXTFILE;
```

* copiar csv para hdfs (terminal)

```
hadoop fs -put /home/silvio/git/25-DataOps/Aula1/pima-indians-diabetes.csv /home/silvio/hiveW/warehouse/AllstarFull.csv
```

* carregar arquivo csv para tabela (hivesql)
```
LOAD DATA LOCAL INPATH '/home/silvio/hiveW/warehouse/AllstarFull.csv' INTO TABLE modelos.diabetes;
```

* Obtendo informação sobre as tabelas
```
DESCRIBE FORMATTED modelos.diabetes;
```

* Hsql (Hive SQL)
```
select * from modelos.diabetes;
```

* Criando Partição
    * usando como parâmetro a coluna class
    
```
create table class_part(pregnancies int,age int) PARTITIONED BY(class int);
```

* Incluindo dados nas partições criadas
```
set hive.exec.dynamic.partition.mode=nonstrict;
INSERT OVERWRITE TABLE class_part PARTITION(class) SELECT pregnancies,age,class from modelos.diabetes;
```
