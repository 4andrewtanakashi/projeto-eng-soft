import sqlite3

database = sqlite3.connect('db.sqlite3')
cursor = database.cursor()


print('###### TABELA PROPRIEDADE ######')

cursor.execute("SELECT * FROM core_propriedade")

for linha in cursor.fetchall():
	print(linha)

print('###### TABELA RESERVA ######')

cursor.execute("SELECT * FROM core_reserva")

for linha in cursor.fetchall():
	print(linha)

print('###### TABELA PAGAMENTO ######')

cursor.execute("SELECT * FROM core_pagamento")

for linha in cursor.fetchall():
	print(linha)

database.close()
