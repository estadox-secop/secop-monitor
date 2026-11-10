import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "database", "historial.db")

if os.path.exists(DB_PATH):
    os.remove(DB_PATH)
    print("✓ historial.db eliminado.")
else:
    print("No existe historial.db todavía.")