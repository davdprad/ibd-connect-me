CREATE DATABASE connect_me;

USE connect_me;

CREATE TABLE usuario (
    user_id VARCHAR(255) PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    foto VARCHAR(255),
    localizacao VARCHAR(255),
    biografia TEXT,
    data_nasc DATE NOT NULL
);

CREATE TABLE grupo (
    grupo_id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    biografia TEXT,
    user_id_criou VARCHAR(255) NOT NULL,
    data_criacao TIMESTAMP NOT NULL,
    FOREIGN KEY (user_id_criou) REFERENCES usuario(user_id)
);

CREATE TABLE usuario_grupo (
    user_id VARCHAR(255),
    grupo_id INT,
    data_ingresso DATE NOT NULL,
    PRIMARY KEY (user_id, grupo_id),
    FOREIGN KEY (user_id) REFERENCES usuario(user_id),
    FOREIGN KEY (grupo_id) REFERENCES grupo(grupo_id)
);

CREATE TABLE post_u (
    post_id INT AUTO_INCREMENT PRIMARY KEY,
    tipo_midia VARCHAR(50) NOT NULL,
    conteudo TEXT NOT NULL,
    user_id_postou VARCHAR(255) NOT NULL,
    data_post DATE NOT NULL,
    FOREIGN KEY (user_id_postou) REFERENCES usuario(user_id)
);

CREATE TABLE post_g (
    post_id INT AUTO_INCREMENT PRIMARY KEY,
    tipo_midia VARCHAR(50) NOT NULL,
    conteudo TEXT NOT NULL,
    user_id_postou VARCHAR(255) NOT NULL,
    grupo_id INT NOT NULL,
    data_post DATE NOT NULL,
    FOREIGN KEY (user_id_postou, grupo_id) REFERENCES usuario_grupo(user_id, grupo_id)
);

CREATE TABLE mensagem_u (
    mensagem_id INT AUTO_INCREMENT PRIMARY KEY,
    conteudo TEXT NOT NULL,
    user_id_envia VARCHAR(255) NOT NULL,
    user_id_recebe VARCHAR(255) NOT NULL,
    data_envio TIMESTAMP NOT NULL,
    data_recebimento TIMESTAMP,
    FOREIGN KEY (user_id_envia) REFERENCES usuario(user_id),
    FOREIGN KEY (user_id_recebe) REFERENCES usuario(user_id)
);

CREATE TABLE mensagem_g (
    mensagem_id INT AUTO_INCREMENT PRIMARY KEY,
    conteudo TEXT NOT NULL,
    user_id_envia VARCHAR(255) NOT NULL,
    user_id_recebe VARCHAR(255) NOT NULL,
    grupo_id INT NOT NULL,
    data_envio TIMESTAMP NOT NULL,
    data_recebimento TIMESTAMP,
    FOREIGN KEY (user_id_envia, grupo_id) REFERENCES usuario_grupo(user_id, grupo_id),
    FOREIGN KEY (user_id_recebe, grupo_id) REFERENCES usuario_grupo(user_id, grupo_id)
);

CREATE TABLE comentario_u (
    comentario_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(255),
    post_id INT,
    conteudo TEXT NOT NULL,
    data_postagem TIMESTAMP NOT NULL,
    FOREIGN KEY (user_id) REFERENCES usuario(user_id),
    FOREIGN KEY (post_id) REFERENCES post_u(post_id)
);

CREATE TABLE comentario_g (
    comentario_id INT AUTO_INCREMENT PRIMARY KEY,
    conteudo TEXT NOT NULL,
    user_id VARCHAR(255) NOT NULL,
    post_id INT NOT NULL,
    grupo_id INT NOT NULL,
    data_postagem TIMESTAMP NOT NULL,
    FOREIGN KEY (user_id, grupo_id) REFERENCES usuario_grupo(user_id, grupo_id),
    FOREIGN KEY (post_id) REFERENCES post_g(post_id)
);

CREATE TABLE curtida_u (
    user_id VARCHAR(255),
    post_id INT,
    data_curtida TIMESTAMP NOT NULL,
    PRIMARY KEY (user_id, post_id),
    FOREIGN KEY (user_id) REFERENCES usuario(user_id),
    FOREIGN KEY (post_id) REFERENCES post_u(post_id)
);

CREATE TABLE curtida_g (
    user_id VARCHAR(255),
    post_id INT,
    data_curtida TIMESTAMP NOT NULL,
    PRIMARY KEY (user_id, post_id),
    FOREIGN KEY (user_id) REFERENCES usuario(user_id),
    FOREIGN KEY (post_id) REFERENCES post_g(post_id)
);

CREATE TABLE conexao (
    user_id_1 VARCHAR(255),
    user_id_2 VARCHAR(255),
    data_amizade TIMESTAMP NOT NULL,
    PRIMARY KEY (user_id_1, user_id_2),
    FOREIGN KEY (user_id_1) REFERENCES usuario(user_id),
    FOREIGN KEY (user_id_2) REFERENCES usuario(user_id)
);

CREATE TABLE tema (
    tema_id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL
);

CREATE TABLE interesse_tema (
    user_id VARCHAR(255),
    tema_id INT,
    PRIMARY KEY (user_id, tema_id),
    FOREIGN KEY (user_id) REFERENCES usuario(user_id),
    FOREIGN KEY (tema_id) REFERENCES tema(tema_id)
);

CREATE TABLE grupo_tema (
    grupo_id INT,
    tema_id INT,
    PRIMARY KEY (grupo_id, tema_id),
    FOREIGN KEY (grupo_id) REFERENCES grupo(grupo_id),
    FOREIGN KEY (tema_id) REFERENCES tema(tema_id)
);
