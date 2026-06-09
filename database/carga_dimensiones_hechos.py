#!/usr/bin/env python3
"""
Pipeline de Carga Dimensional (E-L-T)
Caso 1: Adquisicion de Medicamentos a Demanda
Equipo 1 — Extraccion de Conocimiento en Bases de Datos

Este script lee los CSVs limpios producidos por el notebook de EDA
y los persiste en PostgreSQL bajo el esquema estrella definido
en esquema_estrella_postgres.sql.
"""

import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

DB_URI = os.getenv("DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/uteq_data_mining")
engine = create_engine(DB_URI)

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

def load_csv(name):
    path = os.path.join(DATA_DIR, name)
    return pd.read_csv(path, encoding='utf-8')

print("[1/6] Cargando dimensiones desde CSV...")

dim_tiempo = load_csv('dim_tiempo.csv')
dim_medicamento = load_csv('dim_medicamento.csv')
dim_proveedor = load_csv('dim_proveedor.csv')
dim_institucion = load_csv('dim_institucion.csv')
dim_contratacion = load_csv('dim_contratacion.csv')
fct = load_csv('fct_adquisiciones.csv')

print("[2/6] Cargando dim_tiempo...")
dim_tiempo.to_sql('dim_tiempo', engine, schema='ecbd_caso1', if_exists='append', index=False)

print("[3/6] Cargando dim_medicamento...")
dim_medicamento.to_sql('dim_medicamento', engine, schema='ecbd_caso1', if_exists='append', index=False)

print("[4/6] Cargando dim_proveedor...")
dim_proveedor.to_sql('dim_proveedor', engine, schema='ecbd_caso1', if_exists='append', index=False)

print("[5/6] Cargando dim_institucion...")
dim_institucion.to_sql('dim_institucion', engine, schema='ecbd_caso1', if_exists='append', index=False)

print("[6/6] Cargando dim_contratacion y fct_adquisiciones...")
dim_contratacion.to_sql('dim_contratacion', engine, schema='ecbd_caso1', if_exists='append', index=False)
fct.to_sql('fct_adquisiciones', engine, schema='ecbd_caso1', if_exists='append', index=False)

print("[OK] Pipeline de carga completado. Esquema ecbd_caso1 poblado.")
