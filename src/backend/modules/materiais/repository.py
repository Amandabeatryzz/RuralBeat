import sqlite3
from typing import Optional


CANVAS_DDL = """
CREATE TABLE IF NOT EXISTS canvas_workspaces (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    disciplina_id INTEGER NOT NULL,
    viewport_x REAL NOT NULL DEFAULT 0,
    viewport_y REAL NOT NULL DEFAULT 0,
    zoom REAL NOT NULL DEFAULT 1,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, disciplina_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (disciplina_id) REFERENCES disciplinas(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS canvas_nodes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    workspace_id INTEGER NOT NULL,
    tipo TEXT NOT NULL CHECK (tipo IN ('TEXTO','CODIGO','ARQUIVO')),
    titulo TEXT,
    conteudo TEXT,
    pos_x REAL NOT NULL DEFAULT 0,
    pos_y REAL NOT NULL DEFAULT 0,
    largura REAL NOT NULL DEFAULT 280,
    altura REAL NOT NULL DEFAULT 180,
    material_id INTEGER,
    meta_json TEXT,
    z_index INTEGER NOT NULL DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (workspace_id) REFERENCES canvas_workspaces(id) ON DELETE CASCADE,
    FOREIGN KEY (material_id) REFERENCES materiais(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_canvas_nodes_workspace ON canvas_nodes(workspace_id);
"""


def ensure_canvas_tables(db: sqlite3.Connection) -> None:
    db.executescript(CANVAS_DDL)


def _row_to_dict(row) -> dict:
    return dict(row) if row else None


# ── Materiais (legado) ────────────────────────────────────────────────────────

def list_by_disciplina(db: sqlite3.Connection, disciplina_id: int) -> list:
    return [dict(r) for r in db.execute(
        "SELECT * FROM materiais WHERE disciplina_id = ? ORDER BY titulo",
        (disciplina_id,),
    ).fetchall()]


def find_by_id(db: sqlite3.Connection, material_id: int) -> Optional[dict]:
    row = db.execute("SELECT * FROM materiais WHERE id = ?", (material_id,)).fetchone()
    return dict(row) if row else None


def create(
    db: sqlite3.Connection,
    disciplina_id: int,
    titulo: str,
    descricao: Optional[str],
    link: str,
    tipo: str = "LINK",
) -> dict:
    cursor = db.execute(
        "INSERT INTO materiais (disciplina_id, titulo, descricao, link, tipo) VALUES (?, ?, ?, ?, ?)",
        (disciplina_id, titulo, descricao, link, tipo),
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


# ── Canvas Workspace ────────────────────────────────────────────────────────────

def get_or_create_workspace(db: sqlite3.Connection, user_id: int, disciplina_id: int) -> dict:
    ensure_canvas_tables(db)
    row = db.execute(
        "SELECT * FROM canvas_workspaces WHERE user_id = ? AND disciplina_id = ?",
        (user_id, disciplina_id),
    ).fetchone()
    if row:
        return dict(row)
    cursor = db.execute(
        """INSERT INTO canvas_workspaces (user_id, disciplina_id)
           VALUES (?, ?)""",
        (user_id, disciplina_id),
    )
    return dict(db.execute(
        "SELECT * FROM canvas_workspaces WHERE id = ?",
        (cursor.lastrowid,),
    ).fetchone())


def update_viewport(
    db: sqlite3.Connection,
    workspace_id: int,
    viewport_x: float,
    viewport_y: float,
    zoom: float,
) -> dict:
    db.execute(
        """UPDATE canvas_workspaces
           SET viewport_x = ?, viewport_y = ?, zoom = ?, updated_at = CURRENT_TIMESTAMP
           WHERE id = ?""",
        (viewport_x, viewport_y, zoom, workspace_id),
    )
    return dict(db.execute("SELECT * FROM canvas_workspaces WHERE id = ?", (workspace_id,)).fetchone())


def list_nodes(db: sqlite3.Connection, workspace_id: int) -> list:
    rows = db.execute(
        "SELECT * FROM canvas_nodes WHERE workspace_id = ? ORDER BY z_index, id",
        (workspace_id,),
    ).fetchall()
    return [dict(r) for r in rows]


def find_node(db: sqlite3.Connection, node_id: int) -> Optional[dict]:
    row = db.execute("SELECT * FROM canvas_nodes WHERE id = ?", (node_id,)).fetchone()
    return dict(row) if row else None


def create_node(db: sqlite3.Connection, workspace_id: int, data: dict) -> dict:
    cursor = db.execute(
        """INSERT INTO canvas_nodes
           (workspace_id, tipo, titulo, conteudo, pos_x, pos_y, largura, altura, material_id, meta_json, z_index)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            workspace_id,
            data["tipo"],
            data.get("titulo"),
            data.get("conteudo"),
            data["pos_x"],
            data["pos_y"],
            data.get("largura", 280),
            data.get("altura", 180),
            data.get("material_id"),
            data.get("meta_json"),
            data.get("z_index", 0),
        ),
    )
    return find_node(db, cursor.lastrowid)


def update_node(db: sqlite3.Connection, node_id: int, fields: dict) -> Optional[dict]:
    if not fields:
        return find_node(db, node_id)
    sets = ", ".join(f"{k} = ?" for k in fields)
    db.execute(
        f"UPDATE canvas_nodes SET {sets}, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
        list(fields.values()) + [node_id],
    )
    return find_node(db, node_id)


def delete_node(db: sqlite3.Connection, node_id: int) -> bool:
    return db.execute("DELETE FROM canvas_nodes WHERE id = ?", (node_id,)).rowcount > 0


def workspace_belongs_to_user(db: sqlite3.Connection, workspace_id: int, user_id: int) -> bool:
    row = db.execute(
        "SELECT 1 FROM canvas_workspaces WHERE id = ? AND user_id = ?",
        (workspace_id, user_id),
    ).fetchone()
    return row is not None
