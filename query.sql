-- 1. Crear la base de datos
CREATE DATABASE escuela;

-- 2. Usar la base de datos
USE escuela;

-- 3. Crear la tabla de alumnos (como la definió SQLAlchemy)
CREATE TABLE alumnos (
    matricula VARCHAR(50) PRIMARY KEY,
    nombre VARCHAR(100),
    carrera VARCHAR(100)
);

