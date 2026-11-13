-- SQLite: as tabelas e a VIEW são criadas somente se não existirem.
CREATE TABLE IF NOT EXISTS produto (
    id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE,
    quantidade_estoque INTEGER NOT NULL DEFAULT 0 CHECK (quantidade_estoque >= 0),
    valor_unitario NUMERIC NOT NULL CHECK (valor_unitario >= 0),
    estoque_minimo INTEGER NOT NULL DEFAULT 10 CHECK (estoque_minimo >= 0),
    data_cadastro TEXT NOT NULL DEFAULT (date('now'))
);

CREATE TABLE IF NOT EXISTS movimentacao (
    id_movimentacao INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT NOT NULL CHECK (tipo IN ('ENTRADA', 'SAIDA')),
    quantidade INTEGER NOT NULL CHECK (quantidade > 0),
    id_produto INTEGER NOT NULL REFERENCES produto(id_produto) ON DELETE RESTRICT,
    datetime_movimentacao TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
);

CREATE VIEW IF NOT EXISTS vw_situacao_estoque AS
SELECT id_produto, nome, quantidade_estoque AS saldo, estoque_minimo,
       ROUND(valor_unitario * quantidade_estoque, 2) AS valor_total,
       CASE
           WHEN quantidade_estoque = 0 THEN 'Sem estoque'
           WHEN quantidade_estoque <= estoque_minimo THEN 'Baixo'
           ELSE 'Normal'
       END AS situacao
FROM produto;
