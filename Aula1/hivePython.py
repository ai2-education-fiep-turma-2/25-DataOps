from pyhive import hive
import pandas as pd

PORT=10000
conn = hive.Connection(host="127.0.0.1", port=PORT, username="silvio")

print(conn)

dataframe = pd.read_sql("select * from modelos.diabetes", conn)
print(dataframe.describe())
