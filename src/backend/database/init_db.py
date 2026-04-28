import sqlite3
import os
from src.backend.config import DATABASE_PATH

def init_db():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

    scripts = [
        os.path.join(BASE_DIR, "database", "schema.sql"),
        os.path.join(BASE_DIR, "src/backend/database/migrations.sql"),
    ]

    for path in scripts:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                cursor.executescript(f.read())
                print(f"✔ Executado: {path}")
        else:
            print(f"⚠ Arquivo não encontrado: {path}")

    conn.commit()
    conn.close()

    print("\n✅ Banco inicializado com sucesso!")

if __name__ == "__main__":
    init_db()