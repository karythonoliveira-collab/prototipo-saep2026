DROP DATABASE IF EXISTS empresa;
CREATE DATABASE empresa CHARACTER SET utf8 COLLATE utf8_danish_ci;
USE empresa;

-- DROP TABLES
DROP TABLE IF EXISTS estoque;
DROP TABLE IF EXISTS usuario;
DROP TABLE IF EXISTS logs;

-- -----------------------------------------------------
-- Table usuario
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS usuario (
  id INT NOT NULL AUTO_INCREMENT,
  email VARCHAR(120) NOT NULL UNIQUE,
  senha VARCHAR(255) NOT NULL,
  nome VARCHAR(120) NOT NULL,
  is_admin TINYINT NOT NULL DEFAULT 0,
  PRIMARY KEY (id)
);

-- -----------------------------------------------------
-- Table estoque
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS estoque (
  id INT NOT NULL AUTO_INCREMENT,
  nome VARCHAR(120) NOT NULL UNIQUE,
  dt_cads DATETIME NOT NULL DEFAULT NOW(),
  preco_uni DECIMAL(10,2) NOT NULL,
  qtn INT NOT NULL,
  PRIMARY KEY (id)
);
 
-- -----------------------------------------------------
-- Table logs
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS logss (
  id INT NOT NULL AUTO_INCREMENT,
  id_usuario INT NOT NULL,
  id_estoque INT NOT NULL,
  dt_acao DATETIME NOT NULL DEFAULT now(),
  is_retirada TINYINT NOT NULL DEFAULT 0,
  PRIMARY KEY (id, id_usuario, id_estoque),

  CONSTRAINT fk_usuario_has_estoque_usuario
    FOREIGN KEY (id_usuario)
    REFERENCES usuario (id)
    ON DELETE NO CASCADE,
    
  CONSTRAINT fk_usuario_has_estoque_estoque1
    FOREIGN KEY (id_estoque)
    REFERENCES estoque (id)
    ON DELETE NO CASCADE 

);

-- -----------------------------------------------------
-- Insert usuario
-- -----------------------------------------------------
INSERT INTO usuario (email, senha, nome, is_admin) VALUES
("renato@tempo.perdio", "$argon2id$v=19$m=65536,t=3,p=4$Xdg7MBoQEY2vTl54yV+lzg$YS5Es/XYccFVzNSPC7FKbhfMhJmz6sY9f9/gkTKKTe4", "Renato Russo", 1), -- senha é 123456789
("chico@roda.viva", "$argon2id$v=19$m=65536,t=3,p=4$ZNdQIfiD2lcYs+Vg+zTp4A$CQqxqzukj7+Rs5yTffptXY0Y64q/RkdDvgyERcfVW1I", "Chico Buarque", 0), -- senha é 123456789
("rita@erva.venenosa", "$argon2id$v=19$m=65536,t=3,p=4$kWmfHnhbvM6/zsJ/vq55yg$2NthV79S8OXMDR9VPy8oBw2vDSDjhvvbXxHE3lPgApA", "Rita Lee", 0); -- senha é 123456789

-- -----------------------------------------------------
-- Insert estoque
-- -----------------------------------------------------
INSERT INTO estoque (nomes, preco_uni, qtn) VALUES
("cimento", 50.4, 3,),
("balde de tinta", 5, 20),
("fio de cobre", 9.52, 50);

-- -----------------------------------------------------
-- Insert estoque
-- -----------------------------------------------------
INSERT INTO logs (id_usuario, id_estoque, , is_retirada) VALUES
(1, 1,  1),
(2, 2,  0),
(3, 3,  1);


select id,nome,qtn,preco_uni from estoque;