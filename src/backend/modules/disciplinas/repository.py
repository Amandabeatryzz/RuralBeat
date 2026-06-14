import sqlite3
from typing import Optional


# ---------- disciplinas ----------

def list_all(db: sqlite3.Connection, periodo: Optional[int] = None, obrigatoria: Optional[int] = None) -> list:
    query = "SELECT * FROM disciplinas WHERE 1=1"
    params = []
    if periodo is not None:
        query += " AND periodo = ?"
        params.append(periodo)
    if obrigatoria is not None:
        query += " AND obrigatoria = ?"
        params.append(obrigatoria)
    query += " ORDER BY periodo, nome"
    return [dict(r) for r in db.execute(query, params).fetchall()]


def find_by_id(db: sqlite3.Connection, disciplina_id: int) -> Optional[dict]:
    row = db.execute("SELECT * FROM disciplinas WHERE id = ?", (disciplina_id,)).fetchone()
    return dict(row) if row else None


# ---------- progresso ----------

def get_progresso(db: sqlite3.Connection, user_id: int) -> list:
    rows = db.execute("""
        SELECT p.*, d.codigo, d.nome, d.periodo, d.carga_horaria, d.obrigatoria
        FROM progresso_academico p
        JOIN disciplinas d ON d.id = p.disciplina_id
        WHERE p.user_id = ?
        ORDER BY d.periodo, d.nome
    """, (user_id,)).fetchall()
    result = []
    for r in rows:
        r = dict(r)
        result.append({
            "id": r["id"],
            "user_id": r["user_id"],
            "disciplina_id": r["disciplina_id"],
            "status": r["status"],
            "disciplina": {
                "id": r["disciplina_id"],
                "codigo": r["codigo"],
                "nome": r["nome"],
                "periodo": r["periodo"],
                "carga_horaria": r["carga_horaria"],
                "obrigatoria": r["obrigatoria"],
            }
        })
    return result


def upsert_progresso(db: sqlite3.Connection, user_id: int, disciplina_id: int, status: str) -> dict:
    db.execute("""
        INSERT INTO progresso_academico (user_id, disciplina_id, status)
        VALUES (?, ?, ?)
        ON CONFLICT(user_id, disciplina_id) DO UPDATE SET status = excluded.status
    """, (user_id, disciplina_id, status))
    row = db.execute(
        "SELECT * FROM progresso_academico WHERE user_id = ? AND disciplina_id = ?",
        (user_id, disciplina_id)
    ).fetchone()
    return dict(row)


def delete_progresso(db: sqlite3.Connection, user_id: int, disciplina_id: int) -> bool:
    cursor = db.execute(
        "DELETE FROM progresso_academico WHERE user_id = ? AND disciplina_id = ?",
        (user_id, disciplina_id)
    )
    return cursor.rowcount > 0