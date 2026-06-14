import sqlite3
from typing import Optional


def find_by_email(db: sqlite3.Connection, email: str) -> Optional[dict]:
    row = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    return dict(row) if row else None
# A função find_by_email busca um usuário específico pelo seu email. Se o usuário for encontrado, ele é retornado como um dicionário; caso contrário, a função retorna None.

def find_by_id(db: sqlite3.Connection, user_id: int) -> Optional[dict]:
    row = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    return dict(row) if row else None


def create(db: sqlite3.Connection, nome: str, email: str, senha_hash: str) -> dict:
    cursor = db.execute(
        "INSERT INTO users (nome, email, senha) VALUES (?, ?, ?)",
        (nome, email, senha_hash),
    )
    return find_by_id(db, cursor.lastrowid)


def update(db: sqlite3.Connection, user_id: int, fields: dict) -> Optional[dict]:
    if not fields:
        return find_by_id(db, user_id)
    sets = ", ".join(f"{k} = ?" for k in fields)
    values = list(fields.values()) + [user_id]
    db.execute(f"UPDATE users SET {sets} WHERE id = ?", values)
    return find_by_id(db, user_id)


def delete(db: sqlite3.Connection, user_id: int) -> bool:
    cursor = db.execute("DELETE FROM users WHERE id = ?", (user_id,))
    return cursor.rowcount > 0