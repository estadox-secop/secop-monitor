import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "historial.db")


def inicializar():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS vistos (
            id_del_proceso TEXT PRIMARY KEY,
            fecha_registro TEXT DEFAULT (datetime('now'))
        )
    """)
    con.commit()
    con.close()


def es_nuevo(id_proceso):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("SELECT 1 FROM vistos WHERE id_del_proceso = ?", (id_proceso,))
    resultado = cur.fetchone()
    con.close()
    return resultado is None


def marcar_visto(id_proceso):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("INSERT OR IGNORE INTO vistos (id_del_proceso) VALUES (?)", (id_proceso,))
    con.commit()
    con.close()


def filtrar_nuevos(procesos):
    return [p for p in procesos if es_nuevo(p.get("id_del_proceso"))]


def marcar_todos_vistos(procesos):
    for p in procesos:
        marcar_visto(p.get("id_del_proceso"))