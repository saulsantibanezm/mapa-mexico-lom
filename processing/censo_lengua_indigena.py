#!/usr/bin/env python3
"""
processing/censo_lengua_indigena.py
------------------------------------
Genera data/processed/indicadores_lom.csv con 3 columnas por municipio:
  - familia_dominante
  - total_hablantes
  - num_lom_distintas

Lee el CSV en chunks para no reventar RAM en máquinas con poca memoria disponible.

Ejecutar:
    python processing/censo_lengua_indigena.py
"""

import os
import pandas as pd

RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")
CHUNK_SIZE = 300_000

FAMILIAS_POR_RANGO = [
    (100, 200, "Álgica"), (200, 300, "Yuto-nahua"), (300, 400, "Cochimí-yumana"),
    (400, 500, "Seri"), (500, 600, "Oto-mangue"), (600, 700, "Maya"),
    (700, 800, "Totonaco-tepehua"), (800, 900, "Tarasca"), (900, 1000, "Mixe-zoque"),
    (1000, 1100, "Chontal-oaxaca"), (1100, 1200, "Huave"),
]


def clasificar_familia(clave: int) -> str:
    for lo, hi, nombre in FAMILIAS_POR_RANGO:
        if lo <= clave < hi:
            return nombre
    return "Otras / no especificado"


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    columnas = ["ENT", "MUN", "EDAD", "QDIALECT_INALI", "HLENGUA", "FACTOR"]

    acumulado = None  # sumas parciales por (ENT, MUN, QDIALECT_INALI)

    print("Procesando Personas00.CSV en chunks de", CHUNK_SIZE, "filas...")
    lector = pd.read_csv(
        os.path.join(RAW_DIR, "Personas00.CSV"),
        usecols=columnas,
        chunksize=CHUNK_SIZE,
    )

    total_filas = 0
    for i, chunk in enumerate(lector):
        universo = chunk[(chunk["EDAD"] >= 3) & (chunk["EDAD"] <= 130) & (chunk["HLENGUA"] == 1)]
        if universo.empty:
            continue
        parcial = (
            universo.groupby(["ENT", "MUN", "QDIALECT_INALI"])["FACTOR"]
            .sum()
            .reset_index()
        )
        acumulado = parcial if acumulado is None else pd.concat([acumulado, parcial])
        total_filas += len(chunk)
        if i % 10 == 0:
            print(f"  ...{total_filas:,} filas leídas")

    print("Consolidando sumas parciales...")
    por_lengua = (
        acumulado.groupby(["ENT", "MUN", "QDIALECT_INALI"])["FACTOR"]
        .sum()
        .reset_index()
        .rename(columns={"FACTOR": "hablantes_lengua"})
    )
    por_lengua["familia"] = por_lengua["QDIALECT_INALI"].apply(clasificar_familia)

    total_hablantes = (
        por_lengua.groupby(["ENT", "MUN"])["hablantes_lengua"]
        .sum()
        .reset_index()
        .rename(columns={"hablantes_lengua": "total_hablantes"})
    )
    num_lom = (
        por_lengua.groupby(["ENT", "MUN"])["QDIALECT_INALI"]
        .nunique()
        .reset_index()
        .rename(columns={"QDIALECT_INALI": "num_lom_distintas"})
    )
    por_familia = por_lengua.groupby(["ENT", "MUN", "familia"])["hablantes_lengua"].sum().reset_index()
    familia_dominante = (
        por_familia.loc[por_familia.groupby(["ENT", "MUN"])["hablantes_lengua"].idxmax()]
        [["ENT", "MUN", "familia"]]
        .rename(columns={"familia": "familia_dominante"})
    )

    resultado = (
        total_hablantes
        .merge(num_lom, on=["ENT", "MUN"], how="left")
        .merge(familia_dominante, on=["ENT", "MUN"], how="left")
    )

    out_path = os.path.join(OUT_DIR, "indicadores_lom.csv")
    resultado.to_csv(out_path, index=False)
    print(f"Listo: {out_path} ({len(resultado)} municipios)")


if __name__ == "__main__":
    main()
