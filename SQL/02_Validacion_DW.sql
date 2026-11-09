/* =====================================================================
   PROYECTO: Data Warehouse Famous Paintings
   SCRIPT 02: Validación de la carga realizada por el paquete SSIS
   DÓNDE SE EJECUTA: SSMS -> Motor de base de datos -> New Query -> F5
   Cada consulta muestra el valor OBTENIDO y el ESPERADO (calculado en la
   etapa de análisis directamente desde los archivos CSV).
   ===================================================================== */
USE DW_FamousPaintings;
GO

/* 1. Estructura: exactamente 1 tabla de hechos y 6 dimensiones en dbo */
SELECT SUM(CASE WHEN name LIKE 'Fact[_]%' THEN 1 ELSE 0 END) AS TablasHechos,      -- esperado 1
       SUM(CASE WHEN name LIKE 'Dim[_]%'  THEN 1 ELSE 0 END) AS TablasDimension   -- esperado 6
FROM sys.tables
WHERE schema_id = SCHEMA_ID('dbo');

/* 2. Extracción: filas en staging vs filas de los CSV */
SELECT 'stg.artist' AS Tabla, COUNT(*) AS Obtenido, 421 AS Esperado FROM stg.artist
UNION ALL SELECT 'stg.canvas_size',  COUNT(*), 200    FROM stg.canvas_size
UNION ALL SELECT 'stg.image_link',   COUNT(*), 14775  FROM stg.image_link
UNION ALL SELECT 'stg.museum',       COUNT(*), 57     FROM stg.museum
UNION ALL SELECT 'stg.museum_hours', COUNT(*), 351    FROM stg.museum_hours
UNION ALL SELECT 'stg.product_size', COUNT(*), 110347 FROM stg.product_size
UNION ALL SELECT 'stg.subject',      COUNT(*), 6771   FROM stg.subject
UNION ALL SELECT 'stg.work',         COUNT(*), 14776  FROM stg.work;

/* 3. Carga: filas del modelo estrella */
SELECT 'Dim_Obra' AS Tabla, COUNT(*) AS Obtenido, 14716 AS Esperado, 'obras únicas (sin 60 duplicados)' AS Nota FROM dbo.Dim_Obra
UNION ALL SELECT 'Dim_Artista', COUNT(*), 421,    'artistas'                         FROM dbo.Dim_Artista
UNION ALL SELECT 'Dim_Museo',   COUNT(*), 58,     '57 museos + "Sin museo"'          FROM dbo.Dim_Museo
UNION ALL SELECT 'Dim_Tamano',  COUNT(*), 200,    'tamaños de lienzo'                FROM dbo.Dim_Tamano
UNION ALL SELECT 'Dim_Estilo',  COUNT(*), 24,     '23 estilos + "Sin estilo"'        FROM dbo.Dim_Estilo
UNION ALL SELECT 'Dim_Tema',    COUNT(*), 152,    '151 combinaciones + "Sin tema"'   FROM dbo.Dim_Tema
UNION ALL SELECT 'Fact_PrecioObra', COUNT(*), 109332, '110347 - 687 duplicados - 328 errores' FROM dbo.Fact_PrecioObra
UNION ALL SELECT 'stg.ErroresPrecio', COUNT(*), 328, 'filas con tamaño inválido'    FROM stg.ErroresPrecio;

/* 4. Duplicados: no debe haber dos filas con la misma obra y el mismo tamaño (grano) */
SELECT COUNT(*) AS GruposDuplicados   -- esperado 0
FROM (SELECT ObraKey, TamanoKey FROM dbo.Fact_PrecioObra
      GROUP BY ObraKey, TamanoKey HAVING COUNT(*) > 1) d;

/* 5. Integridad referencial: claves foráneas sin correspondencia (todas deben ser 0) */
SELECT
  (SELECT COUNT(*) FROM dbo.Fact_PrecioObra f LEFT JOIN dbo.Dim_Obra    d ON d.ObraKey    = f.ObraKey    WHERE d.ObraKey    IS NULL) AS SinObra,
  (SELECT COUNT(*) FROM dbo.Fact_PrecioObra f LEFT JOIN dbo.Dim_Artista d ON d.ArtistaKey = f.ArtistaKey WHERE d.ArtistaKey IS NULL) AS SinArtista,
  (SELECT COUNT(*) FROM dbo.Fact_PrecioObra f LEFT JOIN dbo.Dim_Museo   d ON d.MuseoKey   = f.MuseoKey   WHERE d.MuseoKey   IS NULL) AS SinMuseo,
  (SELECT COUNT(*) FROM dbo.Fact_PrecioObra f LEFT JOIN dbo.Dim_Tamano  d ON d.TamanoKey  = f.TamanoKey  WHERE d.TamanoKey  IS NULL) AS SinTamano,
  (SELECT COUNT(*) FROM dbo.Fact_PrecioObra f LEFT JOIN dbo.Dim_Estilo  d ON d.EstiloKey  = f.EstiloKey  WHERE d.EstiloKey  IS NULL) AS SinEstilo,
  (SELECT COUNT(*) FROM dbo.Fact_PrecioObra f LEFT JOIN dbo.Dim_Tema    d ON d.TemaKey    = f.TemaKey    WHERE d.TemaKey    IS NULL) AS SinTema;

/* 6. Reglas de limpieza aplicadas */
SELECT COUNT(*) AS PaisesUnitedKingdom FROM dbo.Dim_Museo WHERE Pais = 'United Kingdom';      -- esperado 0
SELECT COUNT(*) AS CiudadesNumericas   FROM dbo.Dim_Museo WHERE TRY_CAST(Ciudad AS INT) IS NOT NULL; -- esperado 0
SELECT MAX(DiasAbiertoSemana) AS MaxDiasAbiertos FROM dbo.Dim_Museo;                          -- esperado 7 (sin "Thusday")
SELECT COUNT(*) AS DescuentosNegativos FROM dbo.Fact_PrecioObra WHERE Descuento < 0;          -- esperado 0
SELECT Motivo, COUNT(*) AS Filas FROM stg.ErroresPrecio GROUP BY Motivo;

/* 7. Consultas analíticas de ejemplo (las mismas que se probarán en SSAS) */
-- Precio promedio de venta y número de ofertas por estilo
SELECT TOP 10 e.Estilo, COUNT(*) AS Ofertas, CAST(AVG(f.PrecioVenta) AS DECIMAL(10,2)) AS PrecioVentaPromedio
FROM dbo.Fact_PrecioObra f JOIN dbo.Dim_Estilo e ON e.EstiloKey = f.EstiloKey
GROUP BY e.Estilo ORDER BY Ofertas DESC;

-- Obras distintas y descuento promedio por nacionalidad del artista
SELECT a.Nacionalidad, COUNT(DISTINCT f.ObraKey) AS Obras, CAST(AVG(f.Descuento) AS DECIMAL(10,2)) AS DescuentoPromedio
FROM dbo.Fact_PrecioObra f JOIN dbo.Dim_Artista a ON a.ArtistaKey = f.ArtistaKey
GROUP BY a.Nacionalidad ORDER BY Obras DESC;

-- Ofertas por país del museo
SELECT m.Pais, COUNT(*) AS Ofertas
FROM dbo.Fact_PrecioObra f JOIN dbo.Dim_Museo m ON m.MuseoKey = f.MuseoKey
GROUP BY m.Pais ORDER BY Ofertas DESC;
GO
