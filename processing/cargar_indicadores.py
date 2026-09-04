#!/usr/bin/env python3
"""
processing/cargar_indicadores.py
---------------------------------
Lee data/processed/indicadores_lom.csv y lo inserta en municipios.db,
uniendo por (estado_id, clave_municipio) contra la tabla municipios existente.

Ejecutar después de censo_lengua_indigena.py:
    python processing/cargar_indicadores.py
"""

import os
import sqlite3
import pandas as pd

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "municipios.db")
CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "processed", "indicadores_lom.csv")


def main():
    df = pd.read_csv(CSV_PATH)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
        DROP TABLE IF EXISTS indicadores_lom;
        CREATE TABLE indicadores_lom (
            municipio_id      INTEGER PRIMARY KEY,
            total_hablantes   INTEGER NOT NULL,
            num_lom_distintas INTEGER NOT NULL,
            familia_dominante TEXT,
            FOREIGN KEY (municipio_id) REFERENCES municipios(id)
        );
    """)

    insertados, sin_match = 0, 0
    sin_match_lista = []
    for _, row in df.iterrows():
        r = cur.execute(
            "SELECT id FROM municipios WHERE estado_id = ? AND clave_municipio = ?",
            (int(row["ENT"]), int(row["MUN"])),
        ).fetchone()
        if r is None:
            sin_match += 1
            sin_match_lista.append((int(row["ENT"]), int(row["MUN"])))
            continue
        municipio_id = r[0]
        cur.execute(
            """INSERT INTO indicadores_lom
               (municipio_id, total_hablantes, num_lom_distintas, familia_dominante)
               VALUES (?, ?, ?, ?)""",
            (municipio_id, int(row["total_hablantes"]), int(row["num_lom_distintas"]),
             row["familia_dominante"]),
        )
        insertados += 1

    conn.commit()
    conn.close()
    print(f"Insertados: {insertados} | Sin match en municipios.db: {sin_match}")
    if sin_match_lista:
        print("Primeros 15 sin match (ENT, MUN):", sin_match_lista[:15])


if __name__ == "__main__":
    main()
