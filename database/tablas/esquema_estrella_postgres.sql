-- =====================================================
-- ESQUEMA ESTRELLA: Adquisicion de Medicamentos a Demanda
-- Caso 1 — INPRFM 2025
-- Motor: PostgreSQL 17
-- =====================================================

DROP SCHEMA IF EXISTS ecbd_caso1 CASCADE;
CREATE SCHEMA ecbd_caso1;

-- -----------------------------------------------------
-- 1. DIMENSION: TIEMPO
-- -----------------------------------------------------
CREATE TABLE ecbd_caso1.dim_tiempo (
    tiempo_sk       SERIAL PRIMARY KEY,
    fecha           DATE NOT NULL UNIQUE,
    anio            INTEGER NOT NULL,
    mes             INTEGER NOT NULL CHECK (mes BETWEEN 1 AND 12),
    dia             INTEGER NOT NULL CHECK (dia BETWEEN 1 AND 31),
    trimestre       INTEGER NOT NULL CHECK (trimestre BETWEEN 1 AND 4),
    nombre_mes      VARCHAR(20) GENERATED ALWAYS AS (
        CASE mes
            WHEN 1 THEN 'Enero' WHEN 2 THEN 'Febrero' WHEN 3 THEN 'Marzo'
            WHEN 4 THEN 'Abril' WHEN 5 THEN 'Mayo' WHEN 6 THEN 'Junio'
            WHEN 7 THEN 'Julio' WHEN 8 THEN 'Agosto' WHEN 9 THEN 'Septiembre'
            WHEN 10 THEN 'Octubre' WHEN 11 THEN 'Noviembre' WHEN 12 THEN 'Diciembre'
        END
    ) STORED
);

-- -----------------------------------------------------
-- 2. DIMENSION: MEDICAMENTO
-- -----------------------------------------------------
CREATE TABLE ecbd_caso1.dim_medicamento (
    medicamento_sk  SERIAL PRIMARY KEY,
    nombre_comercial VARCHAR(200) NOT NULL,
    sustancia_activa VARCHAR(200) NOT NULL,
    forma_farmaceutica VARCHAR(100),
    concentracion    VARCHAR(100),
    presentacion     VARCHAR(100),
    UNIQUE (nombre_comercial, sustancia_activa, forma_farmaceutica, concentracion, presentacion)
);

-- -----------------------------------------------------
-- 3. DIMENSION: PROVEEDOR
-- -----------------------------------------------------
CREATE TABLE ecbd_caso1.dim_proveedor (
    proveedor_sk    SERIAL PRIMARY KEY,
    nombre_proveedor VARCHAR(250) NOT NULL,
    rfc             VARCHAR(13),
    UNIQUE (nombre_proveedor, rfc)
);

-- -----------------------------------------------------
-- 4. DIMENSION: INSTITUCION (CLUES)
-- -----------------------------------------------------
CREATE TABLE ecbd_caso1.dim_institucion (
    institucion_sk  SERIAL PRIMARY KEY,
    clues           VARCHAR(50) NOT NULL UNIQUE
);

-- -----------------------------------------------------
-- 5. DIMENSION: CONTRATACION
-- -----------------------------------------------------
CREATE TABLE ecbd_caso1.dim_contratacion (
    contratacion_sk SERIAL PRIMARY KEY,
    tipo_adquisicion VARCHAR(100) NOT NULL,
    origen_recurso   VARCHAR(200),
    UNIQUE (tipo_adquisicion, origen_recurso)
);

-- -----------------------------------------------------
-- 6. TABLA DE HECHOS: ADQUISICIONES
-- -----------------------------------------------------
CREATE TABLE ecbd_caso1.fct_adquisiciones (
    fact_id         BIGSERIAL PRIMARY KEY,
    tiempo_sk       INTEGER NOT NULL REFERENCES ecbd_caso1.dim_tiempo(tiempo_sk),
    medicamento_sk  INTEGER NOT NULL REFERENCES ecbd_caso1.dim_medicamento(medicamento_sk),
    proveedor_sk    INTEGER NOT NULL REFERENCES ecbd_caso1.dim_proveedor(proveedor_sk),
    institucion_sk  INTEGER NOT NULL REFERENCES ecbd_caso1.dim_institucion(institucion_sk),
    contratacion_sk INTEGER NOT NULL REFERENCES ecbd_caso1.dim_contratacion(contratacion_sk),
    cantidad        NUMERIC(12,2) NOT NULL CHECK (cantidad >= 0),
    precio_unitario NUMERIC(12,2) NOT NULL CHECK (precio_unitario >= 0),
    total           NUMERIC(12,2) NOT NULL CHECK (total >= 0),
    target_adjudicacion_directa INTEGER NOT NULL CHECK (target_adjudicacion_directa IN (0,1))
);

-- -----------------------------------------------------
-- 7. INDICES PARA RENDIMIENTO ANALITICO
-- -----------------------------------------------------
CREATE INDEX idx_fct_tiempo ON ecbd_caso1.fct_adquisiciones(tiempo_sk);
CREATE INDEX idx_fct_medicamento ON ecbd_caso1.fct_adquisiciones(medicamento_sk);
CREATE INDEX idx_fct_proveedor ON ecbd_caso1.fct_adquisiciones(proveedor_sk);
CREATE INDEX idx_fct_contratacion ON ecbd_caso1.fct_adquisiciones(contratacion_sk);

-- =====================================================
-- FIN DEL SCRIPT DDL
-- =====================================================
