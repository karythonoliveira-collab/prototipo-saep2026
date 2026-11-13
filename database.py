import sqlite3

conexao = sqlite3.connect("banco.db")
cursor = conexao.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        quantidade INTEGER NOT NULL DEFAULT 0,
        preco REAL NOT NULL
    )
""")
cursor.execute("""
    CREATE VIEW IF NOT EXISTS vw_produtos_estoque AS
    SELECT
        id,
        nome,
        quantidade,
        preco,
        CASE
            WHEN quantidade = 0 THEN 'Sem estoque'
            WHEN quantidade <= 5 THEN 'Estoque baixo'
            ELSE 'Normal'
        END AS situacao
    FROM produtos
""")    
conexao.commit()
conexao.close()

print("Banco criado com sucesso!")