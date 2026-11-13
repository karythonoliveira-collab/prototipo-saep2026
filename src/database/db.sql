DROP DATABASE IF EXISTS database;
CREATE DATABASE database CHARACTER SET utf8 COLLATE utf8_danish_ci;
USE database;

-- DROP TABLES
DROP TABLE IF EXISTS logs CASCADE;
DROP TABLE IF EXISTS products CASCADE;

CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    description VARCHAR(100) NOT NULL,
    quantity INTEGER NOT NULL,
    value NUMERIC(10,2) NOT NULL,
    created_at DATE NOT NULL DEFAULT CURRENT_DATE
);

CREATE TABLE logs (
    id INTEGER PRIMARY KEY,
    type VARCHAR(10) NOT NULL CHECK (type IN ("entry", "exit")),
    quantity INTEGER NOT NULL,
    datetime DATETIME,
    product_id INTEGER NOT NULL REFERENCES produto(id_produto),
    user_id INTEGER NOT NULL REFERENCES user(id_user)
);

INSERT INTO products (description, quantity, value) VALUES
('Amaciante de roupas', 100, 0.50),
('Detergente', 25, 18.90),
('Sabão em pó', 40, 22.50);


INSERT INTO logs (type, quantity, product_id, user_id) VALUES
("entry", 50, 1, 1),
("exit", 10, 1, 1),
("exit", 5, 2, 1);

select * from products;

-- SQL editado para refletir as mudanças feitas via ORM no banco de dados