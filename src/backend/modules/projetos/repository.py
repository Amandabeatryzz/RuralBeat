import sqlite3
from typing import Optional


def list_all(db: sqlite3.Connection) -> list:
    return [dict(r) for r in db.execute("SELECT * FROM projetos ORDER BY created_at DESC").fetchall()]


def list_by_user(db: sqlite3.Connection, user_id: int) -> list:
    return [dict(r) for r in db.execute(
        "SELECT * FROM projetos WHERE user_id = ? ORDER BY created_at DESC", (user_id,)
    ).fetchall()]


def find_by_id(db: sqlite3.Connection, projeto_id: int) -> Optional[dict]:
    row = db.execute("SELECT * FROM projetos WHERE id = ?", (projeto_id,)).fetchone()
    return dict(row) if row else None


def create(db: sqlite3.Connection, user_id: int, titulo: str, descricao, github_link) -> dict:
    cursor = db.execute(
        "INSERT INTO projetos (user_id, titulo, descricao, github_link) VALUES (?,?,?,?)",
        (user_id, titulo, descricao, github_link),
    )
    return find_by_id(db, cursor.lastrowid)


def update(db: sqlite3.Connection, projeto_id: int, fields: dict) -> Optional[dict]:
    if not fields:
        return find_by_id(db, projeto_id)
    sets = ", ".join(f"{k} = ?" for k in fields)
    db.execute(f"UPDATE projetos SET {sets} WHERE id = ?", list(fields.values()) + [projeto_id])
    return find_by_id(db, projeto_id)


def delete(db: sqlite3.Connection, projeto_id: int) -> bool:
    return db.execute("DELETE FROM projetos WHERE id = ?", (projeto_id,)).rowcount > 0