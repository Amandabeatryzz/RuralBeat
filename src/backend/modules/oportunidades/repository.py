import sqlite3
from typing import Optional


def list_all(db: sqlite3.Connection) -> list:
    return [dict(r) for r in db.execute("SELECT * FROM oportunidades ORDER BY titulo").fetchall()]


def find_by_id(db: sqlite3.Connection, op_id: int) -> Optional[dict]:
    row = db.execute("SELECT * FROM oportunidades WHERE id = ?", (op_id,)).fetchone()
    return dict(row) if row else None


def create(db: sqlite3.Connection, data: dict) -> dict:
    cursor = db.execute(
        "INSERT INTO oportunidades (titulo, descricao, empresa, link) VALUES (?,?,?,?)",
        (data["titulo"], data.get("descricao"), data.get("empresa"), data.get("link")),
    )
    return find_by_id(db, cursor.lastrowid)


def update(db: sqlite3.Connection, op_id: int, fields: dict) -> Optional[dict]:
    if not fields:
        return find_by_id(db, op_id)
    sets = ", ".join(f"{k} = ?" for k in fields)
    db.execute(f"UPDATE oportunidades SET {sets} WHERE id = ?", list(fields.values()) + [op_id])
    return find_by_id(db, op_id)


def delete(db: sqlite3.Connection, op_id: int) -> bool:
    return db.execute("DELETE FROM oportunidades WHERE id = ?", (op_id,)).rowcount > 0