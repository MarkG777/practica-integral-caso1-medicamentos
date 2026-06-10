\pset border 2
\pset pager off
\echo '======================================================='
\echo '  ESQUEMA ecbd_caso1  -  TABLAS CREADAS (\dt)'
\echo '======================================================='
\dt ecbd_caso1.*
\echo ''
\echo '======================================================='
\echo '  CONTEO DE REGISTROS POR TABLA  (POBLACION)'
\echo '======================================================='
SELECT 'dim_tiempo' AS tabla, COUNT(*) AS registros FROM ecbd_caso1.dim_tiempo
UNION ALL SELECT 'dim_medicamento', COUNT(*) FROM ecbd_caso1.dim_medicamento
UNION ALL SELECT 'dim_proveedor', COUNT(*) FROM ecbd_caso1.dim_proveedor
UNION ALL SELECT 'dim_institucion', COUNT(*) FROM ecbd_caso1.dim_institucion
UNION ALL SELECT 'dim_contratacion', COUNT(*) FROM ecbd_caso1.dim_contratacion
UNION ALL SELECT 'fct_adquisiciones', COUNT(*) FROM ecbd_caso1.fct_adquisiciones;
