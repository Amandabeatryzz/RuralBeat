import sqlite3
from typing import Optional


def list_by_disciplina(db: sqlite3.Connection, disciplina_id: int) -> list:
    return [dict(r) for r in db.execute(
        "SELECT * FROM materiais WHERE disciplina_id = ? ORDER BY titulo", (disciplina_id,)
    ).fetchall()]


def find_by_id(db: sqlite3.Connection, material_id: int) -> Optional[dict]:
    row = db.execute("SELECT * FROM materiais WHERE id = ?", (material_id,)).fetchone()
    return dict(row) if row else None


def create(db: sqlite3.Connection, disciplina_id: int, titulo: str, descricao: Optional[str], link: str) -> dict:
    cursor = db.execute(
        "INSERT INTO materiais (disciplina_id, titulo, descricao, link) VALUES (?, ?, ?, ?)",
        (disciplina_id, titulo, descricao, link),
    )
    return find_by_id(db, cursor.lastrowid)


def update(db: sqlite3.Connection, material_id: int, fields: dict) -> Optional[dict]:
    if not fields:
        return find_by_id(db, material_id)
    sets = ", ".join(f"{k} = ?" for k in fields)
    db.execute(f"UPDATE materiais SET {sets} WHERE id = ?", list(fields.values()) + [material_id])
    return find_by_id(db, material_id)


def delete(db: sqlite3.Connection, material_id: int) -> bool:
    return db.execute("DELETE FROM materiais WHERE id = ?", (material_id,)).rowcount > 0