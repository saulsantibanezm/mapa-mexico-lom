"""
main.py – Backend del Mapa de México
--------------------------------------
Ejecutar:  uvicorn main:app --reload
Requiere:  pip install fastapi uvicorn jinja2

La aplicación lee TODO desde municipios.db.
Para actualizar datos, sólo modifica el CSV y vuelve a ejecutar create_db.py.
"""

import sqlite3
import os
from typing import Optional

from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# ──────────────────────────────────────────────
DB_PATH = os.path.join(os.path.dirname(__file__), "municipios.db")
# ──────────────────────────────────────────────

app = FastAPI(title="Mapa de México", version="2.0")
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))


# ── Helpers ───────────────────────────────────

def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def row_to_dict(row: sqlite3.Row) -> dict:
    return dict(row)


# ── Página principal ─────────────────────────

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# ── API: Estados ──────────────────────────────

@app.get("/api/estados")
async def get_estados():
    """Devuelve todos los estados ordenados alfabéticamente."""
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT id, nombre, lat, lon FROM estados ORDER BY nombre"
        ).fetchall()
    return [row_to_dict(r) for r in rows]


@app.get("/api/estados/{estado_id}")
async def get_estado(estado_id: int):
    """Devuelve un estado por su id."""
    with get_conn() as conn:
        row = conn.execute(
            "SELECT id, nombre, lat, lon FROM estados WHERE id = ?", (estado_id,)
        ).fetchone()
    if not row:
        return {"error": "Estado no encontrado"}
    return row_to_dict(row)


# ── API: Municipios ───────────────────────────

@app.get("/api/municipios/{estado_id}")
async def get_municipios(estado_id: int):
    """Devuelve todos los municipios de un estado, ordenados alfabéticamente."""
    with get_conn() as conn:
        rows = conn.execute(
            """SELECT id, clave_municipio, nombre, lat, lon
               FROM municipios
               WHERE estado_id = ?
               ORDER BY nombre""",
            (estado_id,)
        ).fetchall()
    return [row_to_dict(r) for r in rows]


@app.get("/api/municipios/detalle/{municipio_id}")
async def get_municipio(municipio_id: int):
    """Devuelve un municipio por su id, incluyendo el nombre del estado."""
    with get_conn() as conn:
        row = conn.execute(
            """SELECT m.id, m.clave_municipio, m.nombre, m.lat, m.lon,
                      e.id AS estado_id, e.nombre AS estado_nombre
               FROM municipios m
               JOIN estados e ON e.id = m.estado_id
               WHERE m.id = ?""",
            (municipio_id,)
        ).fetchone()
    if not row:
        return {"error": "Municipio no encontrado"}
    return row_to_dict(row)


# ── API: Búsqueda con autocompletado ──────────

@app.get("/api/buscar")
async def buscar(
    q: str = Query("", min_length=0),
    limite: int = Query(20, ge=1, le=50)
):
    """
    Busca estados y municipios por nombre (LIKE).
    Devuelve hasta `limite` resultados combinados:
      - primero estados que coincidan
      - luego municipios que coincidan
    """
    if len(q.strip()) < 2:
        return []

    term = f"%{q.strip()}%"
    resultados = []

    with get_conn() as conn:
        # Buscar en estados
        estados = conn.execute(
            """SELECT id, nombre, lat, lon,
                      'estado' AS tipo, 'Estado' AS subtitulo
               FROM estados
               WHERE nombre LIKE ? COLLATE NOCASE
               LIMIT 5""",
            (term,)
        ).fetchall()
        resultados.extend([row_to_dict(r) for r in estados])

        # Buscar en municipios
        municipios = conn.execute(
            """SELECT m.id, m.nombre, m.lat, m.lon,
                      'municipio' AS tipo, e.nombre AS subtitulo
               FROM municipios m
               JOIN estados e ON e.id = m.estado_id
               WHERE m.nombre LIKE ? COLLATE NOCASE
               ORDER BY m.nombre
               LIMIT ?""",
            (term, limite)
        ).fetchall()
        resultados.extend([row_to_dict(r) for r in municipios])

    return resultados


# ── API: Info de la base de datos ─────────────

@app.get("/api/info")
async def info():
    """Estadísticas de la base de datos."""
    with get_conn() as conn:
        n_estados   = conn.execute("SELECT COUNT(*) FROM estados").fetchone()[0]
        n_municipios = conn.execute("SELECT COUNT(*) FROM municipios").fetchone()[0]
        por_estado  = conn.execute(
            """SELECT e.nombre, COUNT(m.id) AS total
               FROM estados e
               LEFT JOIN municipios m ON m.estado_id = e.id
               GROUP BY e.id
               ORDER BY total DESC"""
        ).fetchall()
    return {
        "total_estados": n_estados,
        "total_municipios": n_municipios,
        "municipios_por_estado": [row_to_dict(r) for r in por_estado]
    }


# ── API: Indicadores LOM ──────────────────────

INDICADORES_VALIDOS = {"total_hablantes", "num_lom_distintas", "familia_dominante"}


@app.get("/api/indicadores/{municipio_id}")
async def get_indicadores(municipio_id: int):
    """Devuelve los 3 indicadores de lenguas indígenas para un municipio."""
    with get_conn() as conn:
        row = conn.execute(
            """SELECT m.nombre, e.nombre AS estado,
                      i.total_hablantes, i.num_lom_distintas, i.familia_dominante
               FROM indicadores_lom i
               JOIN municipios m ON m.id = i.municipio_id
               JOIN estados e ON e.id = m.estado_id
               WHERE i.municipio_id = ?""",
            (municipio_id,)
        ).fetchone()
    if not row:
        return {"sin_datos": True, "municipio_id": municipio_id}
    return row_to_dict(row)


@app.get("/api/mapa/{indicador}")
async def get_mapa_indicador(indicador: str):
    """
    Devuelve todos los municipios con su valor para el indicador solicitado.
    indicador: total_hablantes | num_lom_distintas | familia_dominante
    """
    if indicador not in INDICADORES_VALIDOS:
        return {"error": f"Indicador inválido. Opciones: {sorted(INDICADORES_VALIDOS)}"}

    with get_conn() as conn:
        rows = conn.execute(
            f"""SELECT m.id, m.nombre, m.lat, m.lon,
                       e.nombre AS estado, i.{indicador} AS valor
                FROM indicadores_lom i
                JOIN municipios m ON m.id = i.municipio_id
                JOIN estados e ON e.id = m.estado_id""",
        ).fetchall()
    return [row_to_dict(r) for r in rows]
