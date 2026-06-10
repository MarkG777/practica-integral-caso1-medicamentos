#!/usr/bin/env python3
"""
Generador de Evidencias Visuales del Pipeline en PostgreSQL.
Consulta en vivo el esquema ecbd_caso1 y renderiza capturas legibles
(estilo cliente SQL) que demuestran la creacion y poblacion de las tablas.
"""
import os
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

DB_URI = os.getenv("DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/uteq_data_mining")
engine = create_engine(DB_URI)

OUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'docs', 'evidencias')
os.makedirs(OUT_DIR, exist_ok=True)

HEADER = '#1A5276'
ROW_A = '#FFFFFF'
ROW_B = '#EAF2F8'


def render_table(df, title, subtitle, filename, col_widths=None, fontsize=9):
    n_rows, n_cols = df.shape
    fig_h = max(2.4, 0.42 * (n_rows + 2) + 1.4)
    fig_w = max(8, 1.6 * n_cols)
    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    ax.axis('off')

    # Reservar espacio superior para titulo + subtitulo
    top_frac = 1 - (0.85 / fig_h)
    plt.subplots_adjust(top=top_frac, bottom=0.06, left=0.04, right=0.96)

    # Titulo y subtitulo estilo cliente SQL (posiciones fijas en pulgadas)
    fig.text(0.02, 1 - (0.32 / fig_h), title, fontsize=13, fontweight='bold', color=HEADER, ha='left', va='top')
    fig.text(0.02, 1 - (0.62 / fig_h), subtitle, fontsize=9, color='#566573', ha='left', va='top')

    tbl = ax.table(
        cellText=df.values,
        colLabels=df.columns,
        cellLoc='left',
        loc='center',
        colWidths=col_widths,
    )
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(fontsize)
    tbl.scale(1, 1.4)

    for (r, c), cell in tbl.get_celld().items():
        cell.set_edgecolor('#AEB6BF')
        cell.set_linewidth(0.4)
        if r == 0:
            cell.set_facecolor(HEADER)
            cell.set_text_props(color='white', fontweight='bold')
        else:
            cell.set_facecolor(ROW_A if r % 2 else ROW_B)

    out = os.path.join(OUT_DIR, filename)
    fig.text(0.02, 0.01, 'Motor: PostgreSQL 17  |  Base: uteq_data_mining  |  Esquema: ecbd_caso1',
             fontsize=7.5, color='#85929E')
    plt.savefig(out, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print('[OK]', out)


# === EVIDENCIA 1: Tablas creadas y pobladas (conteo de registros) ===
q_counts = """
SELECT 'dim_tiempo' AS "Tabla", COUNT(*) AS "Registros" FROM ecbd_caso1.dim_tiempo
UNION ALL SELECT 'dim_medicamento', COUNT(*) FROM ecbd_caso1.dim_medicamento
UNION ALL SELECT 'dim_proveedor', COUNT(*) FROM ecbd_caso1.dim_proveedor
UNION ALL SELECT 'dim_institucion', COUNT(*) FROM ecbd_caso1.dim_institucion
UNION ALL SELECT 'dim_contratacion', COUNT(*) FROM ecbd_caso1.dim_contratacion
UNION ALL SELECT 'fct_adquisiciones', COUNT(*) FROM ecbd_caso1.fct_adquisiciones;
"""
df_counts = pd.read_sql(q_counts, engine)
render_table(
    df_counts,
    'Evidencia 1 - Creacion y Poblacion de Tablas',
    'Conteo de registros por tabla del esquema estrella (consulta SELECT COUNT(*) en vivo).',
    'evidencia_1_conteos.png',
    col_widths=[0.55, 0.45],
)

# === EVIDENCIA 2: Estructura de la tabla de hechos ===
q_struct = """
SELECT column_name AS "Columna",
       data_type AS "Tipo de Dato",
       CASE WHEN is_nullable='NO' THEN 'NOT NULL' ELSE 'NULL' END AS "Restriccion"
FROM information_schema.columns
WHERE table_schema='ecbd_caso1' AND table_name='fct_adquisiciones'
ORDER BY ordinal_position;
"""
df_struct = pd.read_sql(q_struct, engine)
render_table(
    df_struct,
    'Evidencia 2 - Estructura de la Tabla de Hechos',
    'Definicion de columnas de ecbd_caso1.fct_adquisiciones (llaves foraneas + medidas + target).',
    'evidencia_2_estructura_hechos.png',
    col_widths=[0.4, 0.35, 0.25],
)

# === EVIDENCIA 3: Muestra de datos poblados con JOIN dimensional ===
q_sample = """
SELECT f.fact_id AS "ID",
       t.fecha AS "Fecha",
       LEFT(m.nombre_comercial, 22) AS "Medicamento",
       LEFT(p.nombre_proveedor, 20) AS "Proveedor",
       f.cantidad AS "Cant.",
       f.total AS "Total",
       f.target_costo_alto AS "Costo Alto"
FROM ecbd_caso1.fct_adquisiciones f
JOIN ecbd_caso1.dim_tiempo t ON f.tiempo_sk = t.tiempo_sk
JOIN ecbd_caso1.dim_medicamento m ON f.medicamento_sk = m.medicamento_sk
JOIN ecbd_caso1.dim_proveedor p ON f.proveedor_sk = p.proveedor_sk
ORDER BY f.total DESC
LIMIT 12;
"""
df_sample = pd.read_sql(q_sample, engine)
df_sample['Fecha'] = pd.to_datetime(df_sample['Fecha']).dt.strftime('%Y-%m-%d')
render_table(
    df_sample,
    'Evidencia 3 - Datos Poblados (JOIN Dimensional)',
    'Top 12 adquisiciones por monto, uniendo la tabla de hechos con sus dimensiones.',
    'evidencia_3_muestra_join.png',
    col_widths=[0.07, 0.13, 0.25, 0.23, 0.09, 0.12, 0.11],
    fontsize=8.5,
)

print('Evidencias generadas en:', OUT_DIR)
