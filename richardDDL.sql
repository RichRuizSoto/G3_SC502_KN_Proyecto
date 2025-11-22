-- SE DEBE DE AJUSTAR EL USER Y PW EN .env DEPENDIENDO A SUS CREDENCIALES LOCALES


CREATE DATABASE Turismo;

CREATE TABLE tipo_usuario (
    id_tipo INT NOT NULL AUTO_INCREMENT,
    nombre_rol VARCHAR(50) NOT NULL,
    descripcion VARCHAR(255),
    PRIMARY KEY (id_tipo)
);


CREATE TABLE usuario (
    id_usuario INT NOT NULL AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(100) NOT NULL UNIQUE,
    contrasena VARCHAR(255) NOT NULL,
    id_tipo_usuario INT NOT NULL,
    telefono VARCHAR(20),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_usuario),
    FOREIGN KEY (id_tipo_usuario) REFERENCES tipo_usuario(id_tipo)
);

INSERT INTO tipo_usuario (id_tipo, nombre_rol, descripcion)
VALUES (1, 'usuario', 'Registro normal');
