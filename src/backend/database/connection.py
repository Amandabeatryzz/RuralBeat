import sqlite3
import os
from contextlib import contextmanager 
# A função get_connection é responsável por estabelecer uma conexão com o banco de dados SQLite. 
# Ela garante que o diretório para o banco de dados exista, conecta-se ao banco de dados usando o caminho definido em DB_PATH, configura a fábrica de linhas para retornar dicionários e ativa as chaves estrangeiras.

# Caminho absoluto para o banco, independente de onde o uvicorn é chamado
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "database", "ruralbeat.db")

def get_connection() -> sqlite3.Connection:
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

@contextmanager 
def get_db():
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback() # Se ocorrer qualquer exceção durante as operações com o banco de dados, a transação é revertida para garantir a integridade dos dados. A exceção é então propagada para ser tratada em outro lugar, se necessário.
        raise
    finally:
        conn.close()
