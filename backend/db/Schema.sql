CREATE TABLE restaurante (
    id_restaurante SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    direccion VARCHAR(200) NOT NULL
);

CREATE TABLE usuario (
    id_usuario SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    id_restaurante INT NOT NULL,
    CONSTRAINT fk_usuario_restaurante FOREIGN KEY (id_restaurante) 
        REFERENCES restaurante(id_restaurante) ON DELETE CASCADE
);

CREATE TABLE cliente (
    id_cliente SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    id_restaurante INT NOT NULL,
    CONSTRAINT fk_cliente_restaurante FOREIGN KEY (id_restaurante) 
        REFERENCES restaurante(id_restaurante) ON DELETE CASCADE
);

CREATE TABLE plato (
    id_plato SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    id_restaurante INT NOT NULL,
    CONSTRAINT fk_plato_restaurante FOREIGN KEY (id_restaurante) 
        REFERENCES restaurante(id_restaurante) ON DELETE CASCADE
);

CREATE TABLE venta_plato (
    id_venta_plato SERIAL PRIMARY KEY,
    fecha DATE NOT NULL,
    cantidad_predicha INT NOT NULL,
    cantidad_normal INT NOT NULL,
    cantidad_excedente INT NOT NULL,
    cantidad_descartada INT NOT NULL,
    id_plato INT NOT NULL,
    CONSTRAINT fk_venta_plato FOREIGN KEY (id_plato) 
        REFERENCES plato(id_plato) ON DELETE CASCADE
);