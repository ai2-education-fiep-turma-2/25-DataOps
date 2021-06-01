### kafka linha de comando

## Instalação

* Baixar e descompactar https://kafka.apache.org/downloads

* Os comandos a seguir devem ser executados no diretório do Apache Kafka

## iniciando zookeeper

```
bin/zookeeper-server-start.sh config/zookeeper.properties
```

## iniciando servidor

```
bin/kafka-server-start.sh config/server.properties
```

## criando um tópico

```
bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic test
Created topic "test"
```

## listando tópicos gerados

```
bin/kafka-topics.sh --list --zookeeper localhost:2181
```

## Enviando mensagens para o tópico (Produtor)

```
bin/kafka-console-producer.sh --broker-list localhost:9092 --topic test
```

## Lendo mensagens do tópico (Consumidor)
```
bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test --from-beginning
```

## kafka-python - lib para manipular kafka no python 
```
pip install kafka-python
```

* kafka-Producer : produz mensagens
* kafka-Consumer : consome mensagens

## streams com spark

* O Spark apresenta um suporte a streams a partir de socket

* Rodando servidor de mensagens (Socket)

```
nc -lk 9999
```

* pyspark-consumer: consumidor de mensagens gerados pelo nc