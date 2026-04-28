from database.connection import get_connection
from config import DATABASE_PATH


def run_migrations():
    conn = get_connection()
    cursor = conn.cursor()

    with open("database/migrations.sql", "r", encoding="utf-8") as f:
        sql = f.read()

    cursor.executescript(sql)
    conn.commit()
    conn.close()

    print("✅ Banco inicializado com sucesso!")


def testar_conexao():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()

    print("\n📊 Tabelas no banco:")
    for t in tables:
        print("-", t["name"])

    conn.close()


if __name__ == "__main__":
    print("Iniciando RuralBeat Backend...\n")

    run_migrations()
    testar_conexao()