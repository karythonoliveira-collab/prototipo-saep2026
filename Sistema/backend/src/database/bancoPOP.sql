CREATE TABLE IF NOT EXISTS Usuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(500) NOT NULL,
    email VARCHAR(500) NOT NULL UNIQUE,
    senha VARCHAR(300) NOT NULL,
    administrador BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS Item (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(255) NOT NULL,
    quantidade REAL NOT NULL DEFAULT 0,
    validade TEXT,
    cor VARCHAR(45),
    unidade VARCHAR(6)
);

CREATE TABLE IF NOT EXISTS Log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo VARCHAR(10) NOT NULL CHECK (tipo IN ('ENTRADA', 'SAIDA')),
    dt DATETIME,
    item_id INTEGER NOT NULL,
    usuario_id INTEGER NOT NULL,
    quantidade REAL DEFAULT 0,
    FOREIGN KEY (usuario_id) REFERENCES Usuario(id),
    FOREIGN KEY (item_id) REFERENCES Item(id) ON DELETE CASCADE
);

INSERT INTO Log (id, tipo, dt, item_id, usuario_id, quantidade) VALUES
(1, 'ENTRADA', '2026-11-01 10:00:00', 1, 1, 2),
(2, 'ENTRADA', '2026-11-01 10:00:00', 2, 2, 5),
(3, 'SAIDA', '2026-11-01 10:00:00', 3, 3, 1)


INSERT INTO Usuario (id, nome, email, senha, administrador) VALUES
(1, 'Administrador', 'admin@saep.com', '123', True),
(2, 'Carlos ', 'carlos@saep.com', '123', False),
(3, 'Mariana', 'mariana@saep.com', '123', False);

INSERT INTO Item (id, nome, quantidade, validade, cor, unidade) VALUES
(1, 'Alcool', 1, '2026-12-31', 'transparente','ml'),
(2, 'veja', 2, '2027-05-15', 'azul', 'ml'),
(3, 'Água Sanitaria', 3, '2030-01-01', 'transparente', 'ml');

