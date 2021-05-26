from pyhive import hive
conn = hive.Connection(host="localhost") #, port=PORT, username="YOU")

print(conn)

#cursor = hive.connect('localhost').cursor()
#cursor.execute('select * from modelos.diabetes;')
#print (cursor.fetchall())

