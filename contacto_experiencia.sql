-- Crear tabla contacto_experiencia
CREATE TABLE IF NOT EXISTS contacto_experiencia (
    id_contacto INT AUTO_INCREMENT PRIMARY KEY,
    id_experiencia INT NOT NULL,
    nombre_contacto VARCHAR(150) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    email VARCHAR(150) NOT NULL,
    direccion VARCHAR(255),
    horario_atencion VARCHAR(100),
    sitio_web VARCHAR(255),
    redes_sociales TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_experiencia) REFERENCES experiencia(id_experiencia) ON DELETE CASCADE,
    UNIQUE KEY unique_contacto_experiencia (id_experiencia)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
