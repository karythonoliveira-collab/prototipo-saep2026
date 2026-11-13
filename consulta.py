import sqlite3

conexao = sqlite3.connect("banco.db")
cursor = conexao.cursor()

cursor.execute("SELECT * FROM vw_produtos_estoque")

for produto in cursor.fetchall():
    print(produto)

conexao.close()