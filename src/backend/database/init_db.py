import sqlite3
import os
from config import settings

def init_db():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DB_PATH  = os.path.join(BASE_DIR, "database", "ruralbeat.db")
    SCHEMA   = os.path.join(BASE_DIR, "database", "schema.sql")

    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")

    if os.path.exists(SCHEMA):
        with open(SCHEMA, "r", encoding="utf-8") as f:
            sql = f.read()
        try:
            conn.executescript(sql)
            print(f"✅ Schema executado: {SCHEMA}")
        except sqlite3.OperationalError as e:
            print(f"⚠️  Schema já existente, ignorando: {e}")
    else:
        print(f"⚠️  Schema não encontrado: {SCHEMA}")

    conn.commit()
    conn.close()
    print("✅ Banco inicializado com sucesso!")

if __name__ == "__main__":
    init_db()
