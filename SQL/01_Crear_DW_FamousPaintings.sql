/* =====================================================================
   PROYECTO: Data Warehouse Famous Paintings
   SCRIPT 01: Creación de la base de datos, tablas de preparación,
              6 dimensiones, 1 tabla de hechos y tabla de errores.
   DÓNDE SE EJECUTA: SSMS -> conexión "Database Engine" -> New Query -> F5
   NOTA: Este script NO borra nada. Si la base ya existe, se detiene.
   ===================================================================== */

/* ---------------------------------------------------------------------
   BLOQUE 1. Crear la base de datos (solo si no existe)
   --------------------------------------------------------------------- */
IF DB_ID('DW_FamousPaintings') IS NOT NULL
BEGIN
    RAISERROR('La base DW_FamousPaintings ya existe. No se modificó nada. Para volver a crearla, elimínela primero.', 16, 1);
    SET NOEXEC ON;   -- detiene el resto del script sin borrar nada
END
GO

CREATE DATABASE DW_FamousPaintings;
GO

USE DW_FamousPaintings;
GO

/* ---------------------------------------------------------------------
   BLOQUE 2. Esquema "stg" (preparación)
   Aquí SSIS copiará los CSV tal cual vienen. Todas las columnas son de
   texto para que valores problemáticos (ej. "#VALUE!") no detengan la carga.
   Así el esquema dbo contiene SOLO el modelo estrella (1 hecho + 6 dim).
   --------------------------------------------------------------------- */
CREATE SCHEMA stg;
GO

CREATE TABLE stg.artist (
    artist_id     NVARCHAR(50),
    full_name     NVARCHAR(200),
    first_name    NVARCHAR(100),
    middle_names  NVARCHAR(100),
    last_name     NVARCHAR(100),
    nationality   NVARCHAR(100),
    style         NVARCHAR(100),
    birth         NVARCHAR(50),
    death         NVARCHAR(50)
);

CREATE TABLE stg.canvas_size (
    size_id  NVARCHAR(50),
    width    NVARCHAR(50),
    height   NVARCHAR(50),
    label    NVARCHAR(200)
);

CREATE TABLE stg.image_link (
    work_id              NVARCHAR(50),
    url                  NVARCHAR(1000),
    thumbnail_small_url  NVARCHAR(1000),
    thumbnail_large_url  NVARCHAR(1000)
);

CREATE TABLE stg.museum (
    museum_id  NVARCHAR(50),
    name       NVARCHAR(200),
    address    NVARCHAR(200),
    city       NVARCHAR(100),
    state      NVARCHAR(100),
    postal     NVARCHAR(50),
    country    NVARCHAR(100),
    phone      NVARCHAR(100),
    url        NVARCHAR(500)
);

CREATE TABLE stg.museum_hours (
    museum_id  NVARCHAR(50),
    day        NVARCHAR(50),
    [open]     NVARCHAR(50),
    [close]    NVARCHAR(50)
);

CREATE TABLE stg.product_size (
    work_id        NVARCHAR(50),
    size_id        NVARCHAR(50),
    sale_price     NVARCHAR(50),
    regular_price  NVARCHAR(50)
);

CREATE TABLE stg.subject (
    work_id  NVARCHAR(50),
    subject  NVARCHAR(100)
);

CREATE TABLE stg.work (
    work_id    NVARCHAR(50),
    name       NVARCHAR(300),
    artist_id  NVARCHAR(50),
    style      NVARCHAR(100),
    museum_id  NVARCHAR(50)
);

/* Tabla de errores: guarda las filas de precios con tamaño inválido
   (decisión A). No forma parte del modelo estrella. */
CREATE TABLE stg.ErroresPrecio (
    ErrorID        INT IDENTITY(1,1) PRIMARY KEY,
    work_id        NVARCHAR(50),
    size_id        NVARCHAR(50),
    sale_price     NVARCHAR(50),
    regular_price  NVARCHAR(50),
    Motivo         NVARCHAR(200),
    FechaRegistro  DATETIME DEFAULT GETDATE()
);
GO

/* ---------------------------------------------------------------------
   BLOQUE 3. Las 6 dimensiones (esquema dbo)
   Cada dimensión tiene:
   - una clave sustituta (xxxKey, número automático IDENTITY) = PK
   - el código original del CSV para rastrear el dato (work_id, etc.)
   --------------------------------------------------------------------- */
CREATE TABLE dbo.Dim_Obra (
    ObraKey     INT IDENTITY(1,1) NOT NULL CONSTRAINT PK_Dim_Obra PRIMARY KEY,
    work_id     INT            NOT NULL CONSTRAINT UQ_Dim_Obra_work_id UNIQUE,
    NombreObra  NVARCHAR(300)  NOT NULL,
    UrlImagen   NVARCHAR(1000) NULL
);

CREATE TABLE dbo.Dim_Artista (
    ArtistaKey      INT IDENTITY(1,1) NOT NULL CONSTRAINT PK_Dim_Artista PRIMARY KEY,
    artist_id       INT           NOT NULL CONSTRAINT UQ_Dim_Artista_artist_id UNIQUE,
    NombreCompleto  NVARCHAR(200) NOT NULL,
    Nombre          NVARCHAR(100) NULL,
    Apellido        NVARCHAR(100) NULL,
    Nacionalidad    NVARCHAR(100) NULL,
    EstiloArtista   NVARCHAR(100) NULL,
    Nacimiento      INT           NULL,
    Muerte          INT           NULL
);

CREATE TABLE dbo.Dim_Museo (
    MuseoKey           INT IDENTITY(1,1) NOT NULL CONSTRAINT PK_Dim_Museo PRIMARY KEY,
    museum_id          INT           NOT NULL CONSTRAINT UQ_Dim_Museo_museum_id UNIQUE,  -- -1 = "Sin museo"
    NombreMuseo        NVARCHAR(200) NOT NULL,
    Ciudad             NVARCHAR(100) NULL,
    Estado             NVARCHAR(100) NULL,
    Pais               NVARCHAR(100) NULL,
    DiasAbiertoSemana  INT           NULL
);

CREATE TABLE dbo.Dim_Tamano (
    TamanoKey  INT IDENTITY(1,1) NOT NULL CONSTRAINT PK_Dim_Tamano PRIMARY KEY,
    size_id    INT           NOT NULL CONSTRAINT UQ_Dim_Tamano_size_id UNIQUE,
    Ancho      INT           NULL,
    Alto       INT           NULL,   -- NULL = medida de "lado largo" (no tiene alto)
    Etiqueta   NVARCHAR(200) NOT NULL
);

CREATE TABLE dbo.Dim_Estilo (
    EstiloKey  INT IDENTITY(1,1) NOT NULL CONSTRAINT PK_Dim_Estilo PRIMARY KEY,
    Estilo     NVARCHAR(100) NOT NULL CONSTRAINT UQ_Dim_Estilo UNIQUE   -- incluye "Sin estilo"
);

CREATE TABLE dbo.Dim_Tema (
    TemaKey  INT IDENTITY(1,1) NOT NULL CONSTRAINT PK_Dim_Tema PRIMARY KEY,
    Tema     NVARCHAR(300) NOT NULL CONSTRAINT UQ_Dim_Tema UNIQUE      -- incluye "Sin tema"
);
GO

/* ---------------------------------------------------------------------
   BLOQUE 4. Tabla de hechos
   Grano: una fila por cada obra ofrecida en un tamaño de lienzo.
   Por eso la PK es (ObraKey, TamanoKey): impide filas repetidas.
   --------------------------------------------------------------------- */
CREATE TABLE dbo.Fact_PrecioObra (
    ObraKey        INT NOT NULL,
    ArtistaKey     INT NOT NULL,
    MuseoKey       INT NOT NULL,
    TamanoKey      INT NOT NULL,
    EstiloKey      INT NOT NULL,
    TemaKey        INT NOT NULL,
    PrecioVenta    DECIMAL(10,2) NOT NULL,
    PrecioRegular  DECIMAL(10,2) NOT NULL,
    Descuento      DECIMAL(10,2) NOT NULL,   -- = PrecioRegular - PrecioVenta
    CONSTRAINT PK_Fact_PrecioObra PRIMARY KEY (ObraKey, TamanoKey),
    CONSTRAINT FK_Fact_Obra    FOREIGN KEY (ObraKey)    REFERENCES dbo.Dim_Obra(ObraKey),
    CONSTRAINT FK_Fact_Artista FOREIGN KEY (ArtistaKey) REFERENCES dbo.Dim_Artista(ArtistaKey),
    CONSTRAINT FK_Fact_Museo   FOREIGN KEY (MuseoKey)   REFERENCES dbo.Dim_Museo(MuseoKey),
    CONSTRAINT FK_Fact_Tamano  FOREIGN KEY (TamanoKey)  REFERENCES dbo.Dim_Tamano(TamanoKey),
    CONSTRAINT FK_Fact_Estilo  FOREIGN KEY (EstiloKey)  REFERENCES dbo.Dim_Estilo(EstiloKey),
    CONSTRAINT FK_Fact_Tema    FOREIGN KEY (TemaKey)    REFERENCES dbo.Dim_Tema(TemaKey)
);
GO

/* ---------------------------------------------------------------------
   BLOQUE 5. Índices básicos en las claves foráneas más usadas
   (aceleran los filtros por artista, museo, estilo y tema)
   --------------------------------------------------------------------- */
CREATE INDEX IX_Fact_ArtistaKey ON dbo.Fact_PrecioObra (ArtistaKey);
CREATE INDEX IX_Fact_MuseoKey   ON dbo.Fact_PrecioObra (MuseoKey);
CREATE INDEX IX_Fact_EstiloKey  ON dbo.Fact_PrecioObra (EstiloKey);
CREATE INDEX IX_Fact_TemaKey    ON dbo.Fact_PrecioObra (TemaKey);
GO

/* ---------------------------------------------------------------------
   BLOQUE 6. Verificación: lista de tablas creadas por esquema
   Resultado esperado: 7 tablas en dbo (1 Fact + 6 Dim)
                       9 tablas en stg (8 CSV + ErroresPrecio)
   --------------------------------------------------------------------- */
SELECT s.name AS Esquema, t.name AS Tabla
FROM sys.tables t
JOIN sys.schemas s ON s.schema_id = t.schema_id
ORDER BY s.name, t.name;

SELECT COUNT(*) AS ClavesForaneasEnFact   -- esperado: 6
FROM sys.foreign_keys
WHERE parent_object_id = OBJECT_ID('dbo.Fact_PrecioObra');
GO

SET NOEXEC OFF;
GO
