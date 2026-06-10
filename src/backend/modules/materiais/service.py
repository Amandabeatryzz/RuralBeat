import sqlite3
from fastapi import HTTPException
from modules.materiais import repository


# ── Materiais (legado) ────────────────────────────────────────────────────────

def list_materiais(db: sqlite3.Connection, disciplina_id: int):
    return repository.list_by_disciplina(db, disciplina_id)


def create_material(
    db: sqlite3.Connection,
    disciplina_id: int,
    titulo: str,
    descricao,
    link: str,
    tipo: str = "LINK",
):
    return repository.create(db, disciplina_id, titulo, descricao, link, tipo)


def update_material(db: sqlite3.Connection, material_id: int, fields: dict):
    if not repository.find_by_id(db, material_id):
        raise HTTPException(status_code=404, detail="Material não encontrado")
    return repository.update(db, material_id, {k: v for k, v in fields.items() if v is not None})


def delete_material(db: sqlite3.Connection, material_id: int):
    if not repository.delete(db, material_id):
        raise HTTPException(status_code=404, detail="Material não encontrado")


# ── Canvas ────────────────────────────────────────────────────────────────────

def get_canvas(db: sqlite3.Connection, user_id: int, disciplina_id: int) -> dict:
    ws = repository.get_or_create_workspace(db, user_id, disciplina_id)
    nos = repository.list_nodes(db, ws["id"])
    return {**ws, "nos": nos}


def update_viewport(
    db: sqlite3.Connection,
    user_id: int,
    disciplina_id: int,
    viewport_x: float,
    viewport_y: float,
    zoom: float,
) -> dict:
    ws = repository.get_or_create_workspace(db, user_id, disciplina_id)
    updated = repository.update_viewport(db, ws["id"], viewport_x, viewport_y, zoom)
    nos = repository.list_nodes(db, ws["id"])
    return {**updated, "nos": nos}


def create_node(db: sqlite3.Connection, user_id: int, disciplina_id: int, data: dict) -> dict:
    ws = repository.get_or_create_workspace(db, user_id, disciplina_id)
    if data.get("material_id") and not repository.find_by_id(db, data["material_id"]):
        raise HTTPException(status_code=404, detail="Material de referência não encontrado")
    return repository.create_node(db, ws["id"], data)


def update_node(db: sqlite3.Connection, user_id: int, node_id: int, fields: dict) -> dict:
    node = repository.find_node(db, node_id)
    if not node:
        raise HTTPException(status_code=404, detail="Nó não encontrado")
    if not repository.workspace_belongs_to_user(db, node["workspace_id"], user_id):
        raise HTTPException(status_code=403, detail="Acesso negado")
    if fields.get("material_id") and not repository.find_by_id(db, fields["material_id"]):
        raise HTTPException(status_code=404, detail="Material de referência não encontrado")
    updated = repository.update_node(db, node_id, {k: v for k, v in fields.items() if v is not None})
    return updated


def delete_node(db: sqlite3.Connection, user_id: int, node_id: int):
    node = repository.find_node(db, node_id)
    if not node:
        raise HTTPException(status_code=404, detail="Nó não encontrado")
    if not repository.workspace_belongs_to_user(db, node["workspace_id"], user_id):
        raise HTTPException(status_code=403, detail="Acesso negado")
    repository.delete_node(db, node_id)
