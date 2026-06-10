\pset border 2
\pset pager off
\echo '======================================================================='
\echo '  MUESTRA DE DATOS POBLADOS  -  JOIN DIMENSIONAL  (Top 10 por monto)'
\echo '======================================================================='
SELECT f.fact_id AS id,
       t.fecha,
       LEFT(m.nombre_comercial,18) AS medicamento,
       LEFT(p.nombre_proveedor,16) AS proveedor,
       f.cantidad,
       f.total,
       f.target_costo_alto AS costo_alto
FROM ecbd_caso1.fct_adquisiciones f
JOIN ecbd_caso1.dim_tiempo t        ON f.tiempo_sk = t.tiempo_sk
JOIN ecbd_caso1.dim_medicamento m   ON f.medicamento_sk = m.medicamento_sk
JOIN ecbd_caso1.dim_proveedor p     ON f.proveedor_sk = p.proveedor_sk
ORDER BY f.total DESC
LIMIT 10;
