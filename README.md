# Práctica Integral — Caso 1: Adquisición de Medicamentos a Demanda

**Asignatura:** Extracción de Conocimiento en Bases de Datos (Unidad II)  
**Programa:** Ingeniería en Gestión de Desarrollo de Software (UTEQ)  
**Equipo:** 1  
**Docente:** BRANDON EFREN VENEGAS OLVERA  
**Dataset:** INPRFM — Adquisición de medicamentos demanda (2025)  
**Fuente:** [datos.gob.mx](https://www.datos.gob.mx/dataset/adquisicion_medicamentos_demanda)

---

## 1. Objetivo

Analizar un entorno de datos real, complejo y con imperfecciones de origen, aplicando destrezas de diagnóstico, estructuración multidimensional (esquema estrella Kimball) y preparación formal de entregables analíticos.

---

## 2. Estructura del Repositorio

```
practica5_modelado_dimensional/
├── notebooks/
│   └── eda_y_limpieza_contrataciones.ipynb   <- EDA, limpieza Regex, split Train/Test
├── database/
│   ├── esquema_estrella_postgres.sql           <- DDL del esquema estrella
│   └── carga_dimensiones_hechos.py             <- Pipeline E-L-T (carga a PostgreSQL)
├── data/
│   ├── adquisicion_medicamentos.csv            <- Dataset crudo original
│   ├── dim_*.csv                               <- Dimensiones limpias
│   ├── fct_adquisiciones.csv                   <- Tabla de hechos
│   ├── train_dataset.csv                       <- 75% estratificado
│   └── test_dataset.csv                        <- 25% estratificado
└── docs/
    └── Reporte_Tecnico_Practica5.pdf             <- Entregable principal (REQUERIDO)
```

---

## 3. Infraestructura

| Componente | Versión | Rol |
|---|---|---|
| Python | 3.12 | Limpieza, generación de dimensiones y particionamiento |
| PostgreSQL | 17 | Motor analítico (almacenamiento dimensional) |
| Pandas | >=2.0 | Manipulación de datos tabulares |
| SQLAlchemy | >=2.0 | ORM para carga masiva a PostgreSQL |
| scikit-learn | >=1.3 | Particionamiento estratificado Train/Test |
| python-dotenv | >=1.0 | Gestión de credenciales |

---

## 4. Ejecución

### Paso 1 — Crear entorno virtual

```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### Paso 2 — Ejecutar notebook de EDA

Abrir `notebooks/eda_y_limpieza_contrataciones.ipynb` en Jupyter/VS Code y ejecutar todas las celdas. Este notebook:

- Diagnostica calidad del dataset crudo (nulos, duplicados, formatos rotos).
- Aplica limpieza textual avanzada con **expresiones regulares** (Regex).
- Normaliza tipos de datos (fechas ISO, numéricos flotantes).
- Descompone la tabla plana en **dimensiones y hechos** (esquema estrella).
- Genera la **variable target predictiva** (`target_costo_alto`: 1 si el monto total supera el percentil 75, es decir, $466.81).
- Exporta el **particionamiento estratificado 75/25** (`train_dataset.csv`, `test_dataset.csv`).

### Paso 3 — Crear esquema estrella en PostgreSQL

```powershell
psql -U postgres -d uteq_data_mining -f database\esquema_estrella_postgres.sql
```

### Paso 4 — Cargar dimensiones y hechos

```powershell
cd database
python carga_dimensiones_hechos.py
```

---

## 5. Reglas de Negocio Aplicadas

| Regla | Implementación |
|---|---|
| **Limpieza Regex** | Eliminación de caracteres corruptos, espacios múltiples, homologación a mayúsculas. |
| **Normalización de fechas** | Conversión de `dd/mm/yyyy` a tipo `DATE` ISO 8601. |
| **Tipado numérico** | Conversión de montos con comas a `NUMERIC(12,2)`. |
| **Surrogate Keys** | Identificadores artificiales (`*_sk`) autoincrementales en cada dimensión. |
| **Integridad referencial** | Llaves foráneas entre `fct_adquisiciones` y todas las dimensiones. |
| **Target predictivo** | Variable binaria `target_costo_alto` (1 si total > percentil 75 = $466.81) para detectar adquisiciones anómalamente costosas. |

---

## 6. Esquema Estrella (Modelo Dimensional)

```
                    ┌─────────────────┐
                    │   dim_tiempo    │
                    │  (tiempo_sk)    │
                    └────────┬────────┘
                             │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
┌───────▼──────┐    ┌──────────▼──────────┐   ┌────▼─────┐
│ dim_medicamento│    │   fct_adquisiciones │   │dim_proveedor│
│(medicamento_sk)│    │                     │   │(proveedor_sk)│
└──────────────┘    │  cantidad           │   └──────────┘
                    │  precio_unitario    │
┌──────────────┐    │  total              │   ┌──────────────┐
│dim_institucion│    │  target_adjudic... │   │dim_contratacion│
│(institucion_sk)│   └──────────┬──────────┘   │(contratacion_sk)│
└──────────────┘               │             └──────────────┘
                               │
                    ┌──────────┴──────────┐
                    │   dim_contratacion  │
                    │  (contratacion_sk)  │
                    └─────────────────────┘
```

---

## 7. Validación del Particionamiento

El split 75/25 se genera con `train_test_split(..., stratify=y)` garantizando que la proporción de adjudicaciones directas se conserve idénticamente en ambos conjuntos.

---

## 8. Autores

- **Marco Antonio Gómez Olvera** — [@MarkG777](https://github.com/MarkG777)

---

*Documento generado para la Práctica Integral de la Unidad Temática II — Preparación de los Datos.*
