# Genera diagramas.html (4 diagramas SVG + portada) para el PDF del proyecto.
from html import escape as E

INK = "#111827"; MUTED = "#4B5563"; LINE = "#374151"
C = {
    "src":  ("#F3F4F6", "#6B7280"),
    "ssis": ("#FFF4E5", "#C2410C"),
    "sql":  ("#EAF2FB", "#1D4ED8"),
    "sqlin":("#FFFFFF", "#1D4ED8"),
    "ssas": ("#ECFDF5", "#047857"),
    "fact": ("#DBEAFE", "#1E3A8A"),
    "err":  ("#FEF2F2", "#B91C1C"),
    "val":  ("#F9FAFB", "#6B7280"),
}

def rect(x, y, w, h, kind, rx=8, sw=1.6, dash=None):
    f, s = C[kind]
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{f}" stroke="{s}" stroke-width="{sw}"{d}/>'

def text(x, y, s, size=12, weight=400, anchor="start", fill=INK, italic=False):
    st = ' font-style="italic"' if italic else ""
    return (f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" '
            f'text-anchor="{anchor}" fill="{fill}"{st}>{E(s)}</text>')

def lines(x, y, arr, size=11, lh=None, anchor="start", fill=MUTED, weight=400):
    lh = lh or size * 1.35
    return "".join(text(x, y + i * lh, s, size, weight, anchor, fill) for i, s in enumerate(arr))

def arrow(pts, color=LINE, sw=1.8, dash=None):
    d = " ".join(("M" if i == 0 else "L") + f"{x},{y}" for i, (x, y) in enumerate(pts))
    ds = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{sw}"{ds} marker-end="url(#ah)"/>'

def badge(cx, cy, n, color="#111827"):
    return (f'<circle cx="{cx}" cy="{cy}" r="11" fill="{color}"/>'
            + text(cx, cy + 4, str(n), 11.5, 700, "middle", "#fff"))

DEFS = ('<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
        'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#374151"/></marker></defs>')

def svg(w, h, body):
    return (f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" '
            f'font-family="Inter, DejaVu Sans, sans-serif">{DEFS}{body}</svg>')

# ---------------------------------------------------------------- Diagrama 1
def d1():
    b = []
    b.append(f'<rect x="6" y="6" width="988" height="468" rx="12" fill="none" stroke="#9CA3AF" stroke-width="1.2" stroke-dasharray="6 5"/>')
    b.append(text(20, 28, "Equipo PEGASUSPLUS (Windows) — toda la solución se ejecuta en esta computadora", 11.5, 600, fill=MUTED))
    # Fuentes
    b.append(rect(20, 50, 170, 404, "src"))
    b.append(text(105, 74, "Fuentes de datos", 13.5, 700, "middle"))
    b.append(text(105, 92, "Carpeta «Famous Paintings»", 10.5, 400, "middle", MUTED))
    b.append(text(105, 106, "8 archivos CSV (UTF-8)", 10.5, 400, "middle", MUTED))
    files = ["artist.csv", "canvas_size.csv", "image_link.csv", "museum.csv",
             "museum_hours.csv", "product_size.csv", "subject.csv", "work.csv"]
    for i, f in enumerate(files):
        y = 120 + i * 40
        b.append(f'<rect x="34" y="{y}" width="142" height="30" rx="5" fill="#fff" stroke="#9CA3AF"/>')
        b.append(text(105, y + 19.5, f, 11.5, 500, "middle"))
    # SSIS
    b.append(rect(245, 50, 185, 404, "ssis"))
    b.append(text(337, 74, "SSIS", 15, 700, "middle", "#9A3412"))
    b.append(text(337, 91, "SQL Server Integration Services", 10.5, 500, "middle", MUTED))
    b.append(text(337, 105, "Visual Studio 2022", 10.5, 400, "middle", MUTED))
    b.append(f'<rect x="258" y="120" width="159" height="320" rx="6" fill="#fff" stroke="#EA9A6A"/>')
    b.append(text(337, 140, "Proyecto SSIS_FamousPaintings", 10.5, 600, "middle"))
    b.append(text(337, 156, "ETL_FamousPaintings.dtsx", 11, 700, "middle", "#9A3412"))
    items = [("Conexiones", ["8 de archivo plano", "(CSV_artist … CSV_work)", "1 OLE DB a", "PEGASUSPLUS.", "DW_FamousPaintings"]),
             ("11 tareas", ["1 flujo de datos:", "DFT Cargar staging", "10 tareas Execute SQL:", "limpieza, 6 dimensiones,", "errores y tabla de hechos"])]
    y = 182
    for title, arr in items:
        b.append(text(270, y, title, 11, 700))
        b.append(lines(270, y + 17, arr, 10.5, 14.5))
        y += 17 + len(arr) * 14.5 + 22
    # SQL Server
    b.append(rect(485, 50, 240, 404, "sql"))
    b.append(text(605, 74, "SQL Server 2019", 15, 700, "middle", "#1E3A8A"))
    b.append(text(605, 91, "Motor de base de datos (Developer)", 10.5, 500, "middle", MUTED))
    b.append(text(605, 105, "Administrado con SSMS", 10.5, 400, "middle", MUTED))
    b.append(f'<rect x="498" y="120" width="214" height="290" rx="6" fill="#fff" stroke="#93B4E8"/>')
    b.append(text(605, 140, "Base DW_FamousPaintings", 12, 700, "middle"))
    b.append(f'<rect x="512" y="152" width="186" height="92" rx="6" fill="#F8FAFC" stroke="#93B4E8" stroke-dasharray="4 3"/>')
    b.append(text(605, 171, "Esquema stg (preparación)", 11, 700, "middle"))
    b.append(lines(605, 188, ["8 tablas, una por CSV,", "con columnas de texto", "+ stg.ErroresPrecio"], 10.5, 14.5, "middle"))
    b.append(f'<rect x="512" y="300" width="186" height="98" rx="6" fill="#DBEAFE" stroke="#1D4ED8"/>')
    b.append(text(605, 319, "Esquema dbo (modelo estrella)", 11, 700, "middle"))
    b.append(lines(605, 336, ["Fact_PrecioObra", "+ 6 dimensiones", "(Obra, Artista, Museo,", "Tamano, Estilo, Tema)"], 10.5, 14.5, "middle", INK))
    b.append(arrow([(605, 244), (605, 298)]))
    b.append(badge(605, 271, 2))
    b.append(text(605, 428, "Scripts ejecutados en SSMS:", 9.8, 600, "middle", MUTED))
    b.append(text(605, 442, "01_Crear_DW y 02_Validacion_DW", 9.8, 400, "middle", MUTED))
    # SSAS
    b.append(rect(775, 50, 205, 262, "ssas"))
    b.append(text(877, 74, "SSAS 2019", 15, 700, "middle", "#065F46"))
    b.append(text(877, 91, "Analysis Services · modo Tabular", 10.5, 500, "middle", MUTED))
    b.append(text(877, 105, "Nivel de compatibilidad 1500", 10.5, 400, "middle", MUTED))
    b.append(f'<rect x="788" y="120" width="179" height="178" rx="6" fill="#fff" stroke="#6EC6A4"/>')
    b.append(text(877, 140, "Base SSAS_FamousPaintings", 11, 700, "middle"))
    b.append(lines(800, 160, ["• 7 tablas (1 hecho + 6 dim.)", "• 6 relaciones (1 a muchos)", "• 8 medidas DAX: Ofertas,", "   Obras, precios promedio,", "   mínimo, máximo, descuento", "   promedio y % Descuento", "• Desplegada y procesada"], 10.3, 15, fill=INK))
    # Consulta
    b.append(rect(775, 350, 205, 104, "val"))
    b.append(text(877, 372, "Consulta y análisis", 12.5, 700, "middle"))
    b.append(lines(877, 391, ["SSMS → Analysis Services:", "Examinar y consultas DAX", "(03_Prueba_DAX_SSAS.dax)"], 10.5, 14.5, "middle"))
    # Flechas principales
    b.append(arrow([(190, 252), (243, 252)])); b.append(badge(216, 252, 1))
    b.append(arrow([(430, 198), (510, 198)])); b.append(badge(458, 198, 1))
    b.append(arrow([(430, 330), (468, 330), (468, 271), (590, 271)], dash="5 4"));
    b.append(arrow([(698, 349), (750, 349), (750, 210), (773, 210)])); b.append(badge(750, 280, 3))
    b.append(arrow([(877, 312), (877, 348)])); b.append(badge(905, 330, 4))
    return svg(1000, 480, "".join(b))

# ---------------------------------------------------------------- Diagrama 2
RH, HH = 18, 42
def table(x, y, w, name, count, cols, kind):
    f, s = C[kind]
    h = HH + RH * len(cols) + 6
    o = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="#fff" stroke="{s}" stroke-width="1.7"/>',
         f'<path d="M{x},{y+HH} L{x},{y+7} Q{x},{y} {x+7},{y} L{x+w-7},{y} Q{x+w},{y} {x+w},{y+7} L{x+w},{y+HH} Z" fill="{f}" stroke="{s}" stroke-width="1.7"/>',
         text(x + 10, y + 18, name, 13, 700, fill=s if kind != "fact" else "#1E3A8A"),
         text(x + 10, y + 34, count, 10.5, 500, fill=MUTED)]
    for i, (k, c, t) in enumerate(cols):
        cy = y + HH + 3 + i * RH
        if i % 2: o.append(f'<rect x="{x+1}" y="{cy}" width="{w-2}" height="{RH}" fill="#F9FAFB"/>')
        if k:
            col = {"PK": "#1D4ED8", "FK": "#C2410C", "UQ": "#6B7280", "PK FK": "#7C3AED"}[k]
            bw = 34 if k == "PK FK" else 21
            o.append(f'<rect x="{x+8}" y="{cy+3.5}" width="{bw}" height="11" rx="2.5" fill="{col}"/>')
            o.append(text(x + 8 + bw / 2, cy + 12, k, 7.8, 700, "middle", "#fff"))
        o.append(text(x + 46, cy + 13, c, 11, 600 if k and "PK" in k else 400))
        o.append(text(x + w - 9, cy + 13, t, 9.5, 400, "end", MUTED))
    return "".join(o), h

def rowy(y, i): return y + HH + 3 + i * RH + RH / 2

def d2():
    b = []
    W = 232
    dims = {
        "Obra": (40, 18, "Dim_Obra", "14 716 filas", [("PK","ObraKey","INT"),("UQ","work_id","INT"),("","NombreObra","NVARCHAR(300)"),("","UrlImagen","NVARCHAR(1000)")]),
        "Artista": (40, 150, "Dim_Artista", "421 filas", [("PK","ArtistaKey","INT"),("UQ","artist_id","INT"),("","NombreCompleto","NVARCHAR(200)"),("","Nombre","NVARCHAR(100)"),("","Apellido","NVARCHAR(100)"),("","Nacionalidad","NVARCHAR(100)"),("","EstiloArtista","NVARCHAR(100)"),("","Nacimiento","INT"),("","Muerte","INT")]),
        "Museo": (40, 374, "Dim_Museo", "58 filas (incluye «Sin museo»)", [("PK","MuseoKey","INT"),("UQ","museum_id","INT"),("","NombreMuseo","NVARCHAR(200)"),("","Ciudad","NVARCHAR(100)"),("","Estado","NVARCHAR(100)"),("","Pais","NVARCHAR(100)"),("","DiasAbiertoSemana","INT")]),
        "Tamano": (728, 40, "Dim_Tamano", "200 filas", [("PK","TamanoKey","INT"),("UQ","size_id","INT"),("","Ancho","INT"),("","Alto","INT"),("","Etiqueta","NVARCHAR(200)")]),
        "Estilo": (728, 236, "Dim_Estilo", "24 filas (incluye «Sin estilo»)", [("PK","EstiloKey","INT"),("UQ","Estilo","NVARCHAR(100)")]),
        "Tema": (728, 404, "Dim_Tema", "152 filas (incluye «Sin tema»)", [("PK","TemaKey","INT"),("UQ","Tema","NVARCHAR(300)")]),
    }
    fx, fy, fw = 384, 150, 232
    fcols = [("PK FK","ObraKey","INT"),("FK","ArtistaKey","INT"),("FK","MuseoKey","INT"),("PK FK","TamanoKey","INT"),
             ("FK","EstiloKey","INT"),("FK","TemaKey","INT"),("","PrecioVenta","DECIMAL(10,2)"),("","PrecioRegular","DECIMAL(10,2)"),("","Descuento","DECIMAL(10,2)")]
    # líneas primero (debajo de las tablas)
    left = [("Obra", 0, 356), ("Artista", 1, 330), ("Museo", 2, 304)]
    right = [("Tamano", 3, 644), ("Estilo", 4, 672), ("Tema", 5, 700)]
    rel = []
    for nm, r, mx in left:
        x, y, *_ = dims[nm]; y0 = rowy(fy, r); y1 = rowy(y, 0)
        rel.append(f'<path d="M{fx},{y0} L{mx},{y0} L{mx},{y1} L{x+W},{y1}" fill="none" stroke="{LINE}" stroke-width="1.6"/>')
        rel.append(text(fx - 7, y0 - 4, "N", 10, 700, "end", "#C2410C"))
        rel.append(text(x + W + 6, y1 - 4, "1", 10, 700, "start", "#1D4ED8"))
    for nm, r, mx in right:
        x, y, *_ = dims[nm]; y0 = rowy(fy, r); y1 = rowy(y, 0)
        rel.append(f'<path d="M{fx+fw},{y0} L{mx},{y0} L{mx},{y1} L{x},{y1}" fill="none" stroke="{LINE}" stroke-width="1.6"/>')
        rel.append(text(fx + fw + 7, y0 - 4, "N", 10, 700, "start", "#C2410C"))
        rel.append(text(x - 6, y1 - 4, "1", 10, 700, "end", "#1D4ED8"))
    b += rel
    for nm, (x, y, n, cnt, cols) in dims.items():
        t, _ = table(x, y, W, n, cnt, cols, "sql"); b.append(t)
    t, fh = table(fx, fy, fw, "Fact_PrecioObra", "Tabla de hechos · 109 332 filas", fcols, "fact"); b.append(t)
    # Nota de grano y medidas
    gy = fy + fh + 16
    b.append(f'<rect x="{fx}" y="{gy}" width="{fw}" height="116" rx="7" fill="#FFFBEB" stroke="#D97706"/>')
    b.append(text(fx + 10, gy + 18, "Grano de la tabla de hechos", 11, 700, fill="#92400E"))
    b.append(lines(fx + 10, gy + 35, ["Una fila = una obra ofrecida en un", "tamaño de lienzo, con su precio.", "PK compuesta (ObraKey, TamanoKey).", "Medidas: PrecioVenta, PrecioRegular", "y Descuento = Regular − Venta."], 10.3, 14.5, fill=INK))
    # Leyenda
    lx, ly = 384, 22
    b.append(text(lx, ly, "Leyenda", 10.5, 700, fill=MUTED))
    for i, (k, desc) in enumerate([("PK", "clave primaria"), ("FK", "clave foránea"), ("UQ", "código original, único")]):
        col = {"PK": "#1D4ED8", "FK": "#C2410C", "UQ": "#6B7280"}[k]
        yy = ly + 10 + i * 17
        b.append(f'<rect x="{lx}" y="{yy}" width="21" height="11" rx="2.5" fill="{col}"/>')
        b.append(text(lx + 10.5, yy + 8.5, k, 7.8, 700, "middle", "#fff"))
        b.append(text(lx + 28, yy + 9.5, desc, 10, 400, fill=MUTED))
    b.append(text(lx, ly + 72, "1 — N: un registro de la dimensión", 10, 400, fill=MUTED))
    b.append(text(lx, ly + 86, "se relaciona con muchas filas del hecho", 10, 400, fill=MUTED))
    return svg(1000, 560, "".join(b))

# ---------------------------------------------------------------- Diagrama 3
def task(x, y, w, h, n, name, desc, kind="ssis", dash=None, fs=10.2):
    o = [rect(x, y, w, h, kind, 7, 1.6, dash)]
    if n is not None:
        o.append(badge(x + 16, y + 17, n, "#9A3412" if kind == "ssis" else "#6B7280"))
        o.append(text(x + 33, y + 21.5, name, 11, 700))
    else:
        o.append(text(x + 12, y + 21.5, name, 11, 700))
    o.append(lines(x + 12, y + 41, desc, fs, fs * 1.38, fill=INK))
    return "".join(o)

def d3():
    b = []
    X0 = 140; FW = 850
    rows = [(14, "Extracción y", "preparación", ""), (176, "Transformación", "y carga de", "dimensiones"), (338, "Errores, hechos", "y validación", "")]
    RHh = 128
    for y, a, c, d in rows:
        b.append(f'<rect x="8" y="{y}" width="984" height="{RHh+20}" rx="10" fill="#FAFAFA" stroke="#E5E7EB"/>')
        b.append(lines(20, y + (58 if d else 64), [a, c, d] if d else [a, c], 11.5, 16, fill=MUTED, weight=700))
    bh = 108
    # Fila 1
    w1, g1 = 262, 32
    r1 = [(1, "SQL Limpiar staging", ["Vacía las 9 tablas stg (TRUNCATE)", "para poder re-ejecutar el paquete", "sin duplicar datos."]),
          (2, "DFT Cargar staging", ["Flujo de datos: 8 orígenes de archivo", "plano (CSV) → 8 destinos OLE DB", "(stg.artist … stg.work)."]),
          (3, "SQL Limpiar DW", ["Vacía Fact_PrecioObra y las", "6 dimensiones; reinicia las claves", "sustitutas (IDENTITY) en 1."])]
    for i, (n, nm, d) in enumerate(r1):
        x = X0 + i * (w1 + g1); b.append(task(x, 24, w1, bh, n, nm, d))
        if i: b.append(arrow([(x - g1, 78), (x - 2, 78)]))
    # Fila 2
    w2, g2 = 131, 12.8
    r2 = [(4, "SQL Dim_Artista", ["artist → 421 filas.", "Quita espacios;", "años a número."]),
          (5, "SQL Dim_Museo", ["museum + horas.", "Corrige ciudad, país", "y «Thusday»; agrega", "«Sin museo» → 58."]),
          (6, "SQL Dim_Tamano", ["canvas_size → 200.", "Alto vacío = NULL", "(lado largo)."]),
          (7, "SQL Dim_Estilo", ["Estilos de work", "+ «Sin estilo»", "→ 24 filas."]),
          (8, "SQL Dim_Tema", ["Temas de cada obra", "unidos con « / »", "+ «Sin tema» → 152."]),
          (9, "SQL Dim_Obra", ["work sin duplicados", "+ URL de image_link", "→ 14 716 filas."])]
    for i, (n, nm, d) in enumerate(r2):
        x = X0 + i * (w2 + g2); b.append(task(x, 186, w2, bh, n, nm, d, fs=9.8))
        if i: b.append(arrow([(x - g2, 240), (x - 1, 240)]))
    # Fila 3
    r3 = [(10, "SQL Registrar errores", ["Precios cuyo size_id no existe en", "canvas_size → stg.ErroresPrecio", "(328 filas, con su motivo)."]),
          (11, "SQL Cargar Fact_PrecioObra", ["Busca la clave de las 6 dimensiones,", "calcula Descuento e inserta", "109 332 filas."])]
    for i, (n, nm, d) in enumerate(r3):
        x = X0 + i * (w1 + g1); b.append(task(x, 348, w1, bh, n, nm, d))
        if i: b.append(arrow([(x - g1, 402), (x - 2, 402)]))
    xv = X0 + 2 * (w1 + g1)
    b.append(task(xv, 348, w1, bh, None, "Validación (fuera del paquete)", ["02_Validacion_DW.sql en SSMS:", "conteos esperados, 0 duplicados", "y 0 claves foráneas huérfanas."], "val", "5 4"))
    b.append(arrow([(xv - g1, 402), (xv - 2, 402)], dash="5 4"))
    # Conectores entre filas
    x3 = X0 + 2 * (w1 + g1) + w1 / 2
    b.append(arrow([(x3, 132), (x3, 158), (X0 + w2 / 2, 158), (X0 + w2 / 2, 184)]))
    x9 = X0 + 5 * (w2 + g2) + w2 / 2
    b.append(arrow([(x9, 294), (x9, 320), (X0 + w1 / 2, 320), (X0 + w1 / 2, 346)]))
    b.append(text(990, 497, "Flechas continuas: restricciones de precedencia «éxito» del paquete ETL_FamousPaintings.dtsx (11 tareas).", 10, 400, "end", MUTED))
    return svg(1000, 505, "".join(b))

# ---------------------------------------------------------------- Diagrama 4
def d4():
    b = []
    step, y0, bh = 52, 40, 34
    src = [("artist.csv", "421"), ("museum.csv", "57"), ("museum_hours.csv", "351"), ("canvas_size.csv", "200"),
           ("work.csv", "14 776"), ("image_link.csv", "14 775"), ("subject.csv", "6 771"), ("product_size.csv", "110 347")]
    stg = ["stg.artist", "stg.museum", "stg.museum_hours", "stg.canvas_size", "stg.work", "stg.image_link", "stg.subject", "stg.product_size"]
    Y = lambda r: y0 + r * step
    b.append(text(110, 22, "Archivo CSV (filas)", 12, 700, "middle", MUTED))
    b.append(text(420, 22, "Tabla de preparación", 12, 700, "middle", MUTED))
    b.append(text(810, 22, "Destino en el modelo (filas)", 12, 700, "middle", MUTED))
    for i, ((f, n), s) in enumerate(zip(src, stg)):
        y = Y(i)
        b.append(rect(20, y, 180, bh, "src", 6, 1.3))
        b.append(text(32, y + 21.5, f, 11.5, 600)); b.append(text(190, y + 21.5, n, 11, 500, "end", MUTED))
        b.append(rect(340, y, 160, bh, "sqlin", 6, 1.3, "4 3"))
        b.append(text(420, y + 21.5, s, 11.2, 500, "middle"))
        b.append(arrow([(200, y + bh / 2), (338, y + bh / 2)], color="#9CA3AF", sw=1.4))
    b.append(text(269, Y(7) + bh + 16, "SSIS: DFT Cargar staging", 10, 600, "middle", "#9A3412"))
    dest = [("Dim_Artista", "421", 0, "sql"), ("Dim_Museo", "58", 1.5, "sql"), ("Dim_Tamano", "200", 3, "sql"),
            ("Dim_Estilo", "24", 4, "sql"), ("Dim_Obra", "14 716", 5, "sql"), ("Dim_Tema", "152", 6, "sql"),
            ("Fact_PrecioObra", "109 332", 7, "fact"), ("stg.ErroresPrecio", "328", 8, "err")]
    DX, DW = 700, 220
    pos = {}
    for nm, n, r, k in dest:
        y = Y(r); pos[nm] = y + bh / 2
        b.append(rect(DX, y, DW, bh, k, 6, 1.5))
        b.append(text(DX + 12, y + 21.5, nm, 11.5, 700)); b.append(text(DX + DW - 10, y + 21.5, n, 11, 600, "end", MUTED))
    def link(r_src, dst, dash=None, color=LINE, mx=600):
        ys = Y(r_src) + bh / 2; yd = pos[dst]
        b.append(arrow([(500, ys), (mx, ys), (mx, yd), (DX - 2, yd)], color=color, sw=1.5, dash=dash))
    link(0, "Dim_Artista", mx=560)
    link(1, "Dim_Museo", mx=560); link(2, "Dim_Museo", mx=560)
    link(3, "Dim_Tamano", mx=560)
    link(4, "Dim_Estilo", mx=560); link(4, "Dim_Obra", mx=580); link(5, "Dim_Obra", mx=580)
    link(6, "Dim_Tema", mx=560)
    link(7, "Fact_PrecioObra", mx=560); link(7, "stg.ErroresPrecio", mx=560, color="#B91C1C")
    # búsquedas de claves para el hecho
    for r, mx in [(4, 640), (6, 660)]:
        ys = Y(r) + bh / 2
        b.append(arrow([(500, ys + 6), (mx, ys + 6), (mx, pos["Fact_PrecioObra"] - 6), (DX - 2, pos["Fact_PrecioObra"] - 6)], color="#9CA3AF", sw=1.3, dash="4 3"))
    b.append(text(990, Y(8) + bh + 26, "Línea discontinua gris: datos que se usan para buscar las claves de la tabla de hechos (artista, museo, estilo y tema de cada obra).", 9.8, 400, "end", MUTED))
    b.append(text(600, Y(8) + bh + 8, "SSIS: tareas Execute SQL", 10, 600, "middle", "#9A3412"))
    return svg(1000, Y(8) + bh + 40, "".join(b))

# ---------------------------------------------------------------- Página
pages = [
    ("Diagrama 1. Arquitectura general de la solución", d1(),
     ["<b>Qué muestra:</b> el recorrido de los datos y la herramienta responsable de cada paso. "
      "<b>①</b> SSIS lee los 8 archivos CSV y los copia tal cual en el esquema <i>stg</i> de la base DW_FamousPaintings. "
      "<b>②</b> Las tareas Execute SQL del mismo paquete limpian los datos y cargan el modelo estrella del esquema <i>dbo</i> "
      "(la flecha discontinua indica que SSIS dirige ese paso, que se ejecuta dentro de SQL Server). "
      "<b>③</b> SSAS en modo Tabular lee el esquema dbo y al procesarse guarda una copia optimizada para el análisis. "
      "<b>④</b> Las consultas se hacen sobre SSAS desde SSMS (Examinar o DAX)."]),
    ("Diagrama 2. Modelo dimensional en estrella", d2(),
     ["<b>Qué muestra:</b> la tabla de hechos <b>Fact_PrecioObra</b> en el centro y sus <b>seis dimensiones</b>, con las columnas reales de "
      "01_Crear_DW_FamousPaintings.sql. Cada dimensión tiene una clave sustituta (…Key, número automático) como clave primaria "
      "y conserva el código original del CSV (work_id, artist_id…) para rastrear el dato. La tabla de hechos guarda una clave foránea "
      "hacia cada dimensión y las tres medidas de precio. El mismo modelo, con las mismas seis relaciones 1 a N, se implementó en SSAS. "
      "Los precios son de catálogo y no indican moneda."]),
    ("Diagrama 3. Proceso ETL implementado en SSIS", d3(),
     ["<b>Qué muestra:</b> las 11 tareas del paquete ETL_FamousPaintings.dtsx en el orden en que se ejecutan. "
      "Primero se <b>extraen</b> los CSV a las tablas stg (tareas 1–2); luego se vacía el modelo para poder repetir la carga (3); "
      "se <b>transforman</b> los datos y se <b>cargan</b> las dimensiones (4–9); los precios con tamaño inválido se registran como "
      "errores en lugar de borrarse (10); y al final se carga la tabla de hechos, que necesita las claves de las dimensiones (11). "
      "La <b>validación</b> se ejecuta después, en SSMS, con el script 02_Validacion_DW.sql."]),
    ("Diagrama 4. De los archivos de origen a las tablas del modelo", d4(),
     ["<b>Qué muestra:</b> de qué archivo sale cada tabla del modelo. No hay una dimensión por archivo: museum y museum_hours forman Dim_Museo; "
      "work alimenta Dim_Obra y Dim_Estilo; image_link solo aporta la URL de la imagen; y product_size es la fuente de la tabla de hechos. "
      "Las diferencias de filas se explican por las reglas de limpieza: 60 obras repetidas en work.csv, los miembros «Sin museo», «Sin estilo» y «Sin tema», "
      "los temas múltiples de una obra unidos en una sola etiqueta, y 328 precios con tamaño inválido enviados a stg.ErroresPrecio."]),
]

css = """
@page { size: 11in 8.5in; margin: 0; }
* { box-sizing: border-box; }
body { margin: 0; font-family: Inter, 'DejaVu Sans', sans-serif; color: #111827; }
.page { width: 11in; height: 8.5in; padding: 0.42in 0.55in 0.35in; position: relative; page-break-after: always; overflow: hidden; }
.page:last-child { page-break-after: auto; }
h2 { font-size: 19px; margin: 0 0 4px; color: #111827; }
.rule { height: 3px; width: 64px; background: #1D4ED8; margin-bottom: 12px; border-radius: 2px; }
.fig { display: flex; justify-content: center; align-items: center; height: 5.6in; }
.fig svg { max-width: 100%; max-height: 100%; }
.cap { font-size: 12.3px; line-height: 1.5; color: #1F2937; margin-top: 10px; border-top: 1px solid #E5E7EB; padding-top: 9px; }
.foot { position: absolute; bottom: 0.22in; left: 0.55in; right: 0.55in; font-size: 9.5px; color: #6B7280; display: flex; justify-content: space-between; }
.cover { display: flex; flex-direction: column; justify-content: center; padding: 0.9in 1in; }
.cover .band { position: absolute; left: 0; top: 0; bottom: 0; width: 0.32in; background: linear-gradient(#C2410C 0 33%, #1D4ED8 33% 66%, #047857 66%); }
.cover .k { font-size: 13px; letter-spacing: .14em; text-transform: uppercase; color: #6B7280; font-weight: 600; }
.cover h1 { font-size: 40px; line-height: 1.15; margin: 12px 0 14px; }
.cover .sub { font-size: 16px; color: #374151; margin-bottom: 34px; }
.cover table { border-collapse: collapse; font-size: 13.5px; }
.cover td { padding: 6px 18px 6px 0; vertical-align: top; }
.cover td:first-child { color: #6B7280; font-weight: 600; white-space: nowrap; }
.cover ol { margin: 0; padding-left: 18px; }
"""

out = [f"<!doctype html><html lang='es'><head><meta charset='utf-8'><title>Diagramas DW Famous Paintings</title><style>{css}</style></head><body>"]
out.append("""<section class="page cover"><div class="band"></div>
<div class="k">Proyecto final · Data Warehouse</div>
<h1>Diagramas del Data Warehouse<br>Famous Paintings</h1>
<div class="sub">SQL Server 2019 · SQL Server Integration Services (SSIS) · SQL Server Analysis Services (SSAS) Tabular</div>
<table>
<tr><td>Contenido</td><td><ol>
<li>Arquitectura general de la solución</li>
<li>Modelo dimensional en estrella (1 tabla de hechos + 6 dimensiones)</li>
<li>Proceso ETL implementado en SSIS</li>
<li>De los archivos de origen a las tablas del modelo</li></ol></td></tr>
<tr><td>Fuente</td><td>8 archivos CSV de la carpeta «Famous Paintings»</td></tr>
<tr><td>Implementación</td><td>Base DW_FamousPaintings · paquete ETL_FamousPaintings.dtsx · modelo SSAS_FamousPaintings</td></tr>
<tr><td>Fecha</td><td>Octubre de 2026</td></tr>
</table>
<p style="margin-top:30px;font-size:11.5px;color:#6B7280;max-width:7.6in">Documento complementario. Los diagramas se elaboraron a partir de los archivos reales del proyecto
(scripts SQL, paquete SSIS y modelo SSAS); los conteos de filas son los obtenidos con el script de validación.</p>
</section>""")
for i, (t, s, cap) in enumerate(pages, start=2):
    out.append(f'<section class="page"><h2>{t}</h2><div class="rule"></div><div class="fig">{s}</div>'
               f'<div class="cap">{"".join(cap)}</div>'
               f'<div class="foot"><span>Diagramas del Data Warehouse Famous Paintings</span><span>Página {i}</span></div></section>')
out.append("</body></html>")
open("/home/claude/diagramas/diagramas.html", "w", encoding="utf-8").write("".join(out))
print("ok")
