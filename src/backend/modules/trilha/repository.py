import sqlite3
from typing import Optional, List


# - Disciplinas 

def list_disciplinas(db: sqlite3.Connection, obrigatoria: Optional[int] = None) -> List[dict]:
    query = "SELECT * FROM disciplinas"
    params = []
    if obrigatoria is not None:
        query += " WHERE obrigatoria = ?"
        params.append(obrigatoria)
    query += " ORDER BY periodo ASC NULLS LAST, codigo ASC"
    rows = db.execute(query, params).fetchall()
    return [dict(r) for r in rows]


def find_disciplina_by_id(db: sqlite3.Connection, disciplina_id: int) -> Optional[dict]:
    row = db.execute("SELECT * FROM disciplinas WHERE id = ?", (disciplina_id,)).fetchone()
    return dict(row) if row else None


# - Pré-requisitos 

def ensure_prerequisitos_table(db: sqlite3.Connection):
    """Garante que a tabela de pré-requisitos existe (migração inline)."""
    db.execute("""
        CREATE TABLE IF NOT EXISTS pre_requisitos (
            id               INTEGER PRIMARY KEY AUTOINCREMENT,
            disciplina_id    INTEGER NOT NULL,
            pre_requisito_id INTEGER NOT NULL,
            UNIQUE(disciplina_id, pre_requisito_id),
            FOREIGN KEY (disciplina_id)    REFERENCES disciplinas(id) ON DELETE CASCADE,
            FOREIGN KEY (pre_requisito_id) REFERENCES disciplinas(id) ON DELETE CASCADE
        )
    """)
    db.commit()


def list_pre_requisitos(db: sqlite3.Connection) -> List[dict]:
    ensure_prerequisitos_table(db)
    rows = db.execute("SELECT * FROM pre_requisitos").fetchall()
    return [dict(r) for r in rows]


def list_pre_requisitos_de(db: sqlite3.Connection, disciplina_id: int) -> List[dict]:
    ensure_prerequisitos_table(db)
    rows = db.execute(
        "SELECT * FROM pre_requisitos WHERE disciplina_id = ?", (disciplina_id,)
    ).fetchall()
    return [dict(r) for r in rows]


def add_pre_requisito(db: sqlite3.Connection, disciplina_id: int, pre_requisito_id: int) -> dict:
    ensure_prerequisitos_table(db)
    cursor = db.execute(
        "INSERT OR IGNORE INTO pre_requisitos (disciplina_id, pre_requisito_id) VALUES (?, ?)",
        (disciplina_id, pre_requisito_id),
    )
    db.commit()
    row = db.execute(
        "SELECT * FROM pre_requisitos WHERE disciplina_id = ? AND pre_requisito_id = ?",
        (disciplina_id, pre_requisito_id),
    ).fetchone()
    return dict(row)


def remove_pre_requisito(db: sqlite3.Connection, disciplina_id: int, pre_requisito_id: int) -> bool:
    ensure_prerequisitos_table(db)
    cursor = db.execute(
        "DELETE FROM pre_requisitos WHERE disciplina_id = ? AND pre_requisito_id = ?",
        (disciplina_id, pre_requisito_id),
    )
    db.commit()
    return cursor.rowcount > 0


# ─ Progresso Acadêmico 

def list_progresso_usuario(db: sqlite3.Connection, user_id: int) -> List[dict]:
    rows = db.execute(
        """
        SELECT pa.*, d.codigo, d.nome, d.periodo, d.carga_horaria, d.obrigatoria
        FROM progresso_academico pa
        JOIN disciplinas d ON d.id = pa.disciplina_id
        WHERE pa.user_id = ?
        """,
        (user_id,),
    ).fetchall()
    result = []
    for r in rows:
        d = dict(r)
        # monta sub-objeto disciplina para facilitar serialização
        d["disciplina"] = {
            "id": d["disciplina_id"],
            "codigo": d.pop("codigo"),
            "nome": d.pop("nome"),
            "periodo": d.pop("periodo"),
            "carga_horaria": d.pop("carga_horaria"),
            "obrigatoria": d.pop("obrigatoria"),
        }
        result.append(d)
    return result


def find_progresso(db: sqlite3.Connection, user_id: int, disciplina_id: int) -> Optional[dict]:
    row = db.execute(
        "SELECT * FROM progresso_academico WHERE user_id = ? AND disciplina_id = ?",
        (user_id, disciplina_id),
    ).fetchone()
    return dict(row) if row else None


def upsert_progresso(db: sqlite3.Connection, user_id: int, disciplina_id: int, status: str) -> dict:
    db.execute(
        """
        INSERT INTO progresso_academico (user_id, disciplina_id, status)
        VALUES (?, ?, ?)
        ON CONFLICT(user_id, disciplina_id) DO UPDATE SET status = excluded.status
        """,
        (user_id, disciplina_id, status),
    )
    db.commit()
    return find_progresso(db, user_id, disciplina_id)


def delete_progresso(db: sqlite3.Connection, user_id: int, disciplina_id: int) -> bool:
    cursor = db.execute(
        "DELETE FROM progresso_academico WHERE user_id = ? AND disciplina_id = ?",
        (user_id, disciplina_id),
    )
    db.commit()
    return cursor.rowcount > 0