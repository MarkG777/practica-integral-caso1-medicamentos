#!/usr/bin/env python3
"""Genera el Reporte Tecnico en PDF, incluyendo las capturas de evidencia de PostgreSQL."""
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
                                HRFlowable, Image, PageBreak)

BASE = os.path.join(os.path.dirname(__file__), '..')
EVID = os.path.join(BASE, 'docs', 'evidencias')
OUT = os.path.join(BASE, 'docs', 'Reporte_Tecnico_Practica5.pdf')

V = HexColor('#1A5276'); A = HexColor('#1C2541'); G = HexColor('#39A935')
S = getSampleStyleSheet()
S.add(ParagraphStyle('TP', parent=S['Title'], fontSize=18, textColor=A, spaceAfter=6, alignment=TA_CENTER))
S.add(ParagraphStyle('SU', parent=S['Normal'], fontSize=10, textColor=A, alignment=TA_CENTER, spaceAfter=2))
S.add(ParagraphStyle('H2', parent=S['Heading2'], fontSize=13, textColor=V, spaceBefore=14, spaceAfter=6))
S.add(ParagraphStyle('CU', parent=S['Normal'], fontSize=10.5, alignment=TA_JUSTIFY, leading=15, spaceAfter=8))
S.add(ParagraphStyle('CAP', parent=S['Normal'], fontSize=8.5, textColor=HexColor('#566573'), alignment=TA_CENTER, spaceBefore=2, spaceAfter=10))
S.add(ParagraphStyle('PI', parent=S['Normal'], fontSize=9, textColor=HexColor('#666666'), alignment=TA_CENTER))

E = []
def p(txt, st='CU'): E.append(Paragraph(txt, S[st]))
def h2(t): p(t, 'H2')

def add_image(fname, caption, max_w=15.5*cm):
    path = os.path.join(EVID, fname)
    ir = ImageReader(path)
    iw, ih = ir.getSize()
    w = max_w
    h = w * ih / iw
    E.append(Image(path, width=w, height=h))
    p(caption, 'CAP')

p('Reporte Tecnico de Ingenieria', 'TP')
p('Practica Integral — Caso 1: Adquisicion de Medicamentos a Demanda', 'SU')
E.append(Spacer(1,4))
p('Asignatura: Extraccion de Conocimiento en Bases de Datos (Unidad II)', 'SU')
p('Programa: Ingenieria en Gestion de Desarrollo de Software (UTEQ)', 'SU')
p('Docente: BRANDON EFREN VENEGAS OLVERA', 'SU')
p('Equipo: 1', 'SU')
p('Autores: Marco Antonio Gomez Olvera, Orlando Rubio Cabrera, Sandra Zoe Cabrera Velazquez, Israel Gomez Bonilla', 'SU')
p('Dataset: INPRFM — Adquisicion de medicamentos demanda (2025) | Fuente: datos.gob.mx', 'SU')
E.append(Spacer(1,8))
E.append(HRFlowable(width='100%', thickness=1.2, color=V))
E.append(Spacer(1,6))

h2('1. Fase Documental y Justificacion')
p('El dataset crudo proviene del Instituto Nacional de Psiquiatria Ramon de la Fuente Muniz (INPRFM) y contiene <b>2,171 registros</b> de adquisiciones de medicamentos del ano 2025. El diagnostico inicial revelo las siguientes imperfecciones de origen:')
p('<ul><li><b>Encoding inconsistente:</b> el archivo viene en latin-1 con caracteres corruptos en acentos.</li><li><b>Formatos de fecha no estandar:</b> dd/mm/yyyy en lugar de ISO 8601.</li><li><b>Montos con comas separadoras de miles:</b> requieren normalizacion a tipo flotante.</li><li><b>Espacios multiples y mayusculas inconsistentes:</b> en nombres de proveedores y medicamentos.</li></ul>')
p('Dado que todas las transacciones del dataset son del tipo <i>Adjudicacion Directa</i> y el origen de recursos es uniforme (<i>Recursos Federales Ramo 12</i>), se diseno una <b>variable target predictiva alternativa</b> con sentido de negocio: <code>target_costo_alto</code>, que clasifica como positiva (1) toda adquisicion cuyo monto total supere el <b>percentil 75</b> ($466.81), permitiendo identificar compras anomalamente costosas para auditoria preventiva.')

h2('2. Mapeo de Procesos E-T-L (Pandas)')
p('El pipeline de limpieza y transformacion se implemento en un notebook de Jupyter con Pandas, aplicando las siguientes reglas de negocio:')
T = Table([['Regla','Implementacion Tecnica'],['Limpieza Regex','str.replace(r\\s+) + eliminacion de caracteres no alfanumericos + homologacion a MAYUSCULAS'],['Normalizacion de fechas','pd.to_datetime(format=%d/%m/%Y) a tipo DATE ISO 8601'],['Tipado numerico','Conversion de comas a punto decimal con float(str.replace)'],['Variable target','target_costo_alto = (total > p75).astype(int) donde p75 = $466.81'],['Surrogate Keys','Autoincrementales por dimension (sk) generadas con range(1, n+1)']], colWidths=[4.5*cm,10.5*cm])
T.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),V),('TEXTCOLOR',(0,0),(-1,0),HexColor('#FFFFFF')),('FONTSIZE',(0,0),(-1,-1),8.5),('GRID',(0,0),(-1,-1),0.4,HexColor('#CCCCCC')),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('ROWBACKGROUNDS',(0,1),(-1,-1),[HexColor('#FFFFFF'),HexColor('#F0F4F0')]),('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4)]))
E.append(T); E.append(Spacer(1,8))

E.append(PageBreak())
h2('3. Evidencias del Pipeline y Modelado (PostgreSQL 17)')
p('Tras ejecutar el script DDL <code>esquema_estrella_postgres.sql</code> y el pipeline de carga <code>carga_dimensiones_hechos.py</code>, se verifico la creacion y poblacion de las 5 dimensiones y la tabla de hechos en el motor local PostgreSQL 17. Las siguientes capturas de pantalla fueron tomadas directamente desde el cliente oficial <code>psql</code> conectado a la base <code>uteq_data_mining</code>, ejecutando consultas en vivo sobre el esquema <code>ecbd_caso1</code>.')
add_image('psql_evidencia_1_tablas_conteos.png', 'Figura 1. Cliente psql: comando \\dt mostrando las 6 tablas del esquema estrella y SELECT COUNT(*) confirmando la poblacion (2,171 hechos).')
add_image('psql_evidencia_2_estructura.png', 'Figura 2. Cliente psql: comando \\d sobre fct_adquisiciones mostrando columnas, PRIMARY KEY, indices, CHECK constraints y FOREIGN KEYs.')
add_image('psql_evidencia_3_join.png', 'Figura 3. Cliente psql: consulta con JOIN dimensional uniendo la tabla de hechos con sus dimensiones (Top 10 por monto total).')

E.append(PageBreak())
h2('4. Validacion de Archivos Analiticos')
p('El particionamiento Train/Test se genero con <code>train_test_split(..., test_size=0.25, stratify=y, random_state=42)</code>. La validacion confirma que la proporcion del target se conserva identica en ambos conjuntos:')
T2 = Table([['Conjunto','Registros','Clase 0 (Costo normal)','Clase 1 (Costo alto)'],['Origen (100%)','2171','75.1%','24.9%'],['Entrenamiento (75%)','1628','75.1%','24.9%'],['Prueba (25%)','543','75.1%','24.9%']], colWidths=[4.5*cm,3.0*cm,4.3*cm,4.2*cm])
T2.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),G),('TEXTCOLOR',(0,0),(-1,0),HexColor('#FFFFFF')),('FONTSIZE',(0,0),(-1,-1),9),('GRID',(0,0),(-1,-1),0.4,HexColor('#CCCCCC')),('ALIGN',(1,0),(-1,-1),'CENTER'),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('ROWBACKGROUNDS',(0,1),(-1,-1),[HexColor('#FFFFFF'),HexColor('#F0F4F0')]),('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4)]))
E.append(T2); E.append(Spacer(1,10))

h2('5. Esquema Estrella en PostgreSQL')
p('El motor PostgreSQL 17 aloja el esquema <code>ecbd_caso1</code> con las siguientes caracteristicas de diseno:')
p('<ul><li><b>Llaves foraneas</b> desde <code>fct_adquisiciones</code> hacia las 5 dimensiones.</li><li><b>Indices analiticos</b> sobre tiempo_sk, medicamento_sk, proveedor_sk y contratacion_sk para acelerar agregaciones.</li><li><b>Restricciones de dominio:</b> CHECK (cantidad >= 0), CHECK (target_costo_alto IN (0,1)).</li><li><b>Columnas generadas:</b> nombre_mes derivado automaticamente del numero de mes.</li></ul>')

h2('6. Conclusion')
p('La practica integral demostro la capacidad de procesar datos reales del Gobierno Federal con imperfecciones estructurales, aplicar limpieza avanzada con expresiones regulares, modelar dimensionalmente bajo el estandar Kimball y generar datasets balanceados para la fase posterior de mineria de datos. El target <code>target_costo_alto</code> ofrece un problema de clasificacion binaria realista (75/25) que servira como insumo para las unidades siguientes de Regresion Logistica, Arboles de Decision y Random Forest.')

E.append(Spacer(1,14))
E.append(HRFlowable(width='100%', thickness=0.8, color=HexColor('#CCCCCC')))
E.append(Spacer(1,4))
p('UTEQ — Ingenieria en Gestion de Desarrollo de Software', 'PI')

SimpleDocTemplate(OUT, pagesize=letter, leftMargin=2*cm, rightMargin=2*cm, topMargin=1.8*cm, bottomMargin=1.8*cm).build(E)
print('[OK] PDF generado con evidencias:', OUT)
