import sqlite3
from fastapi import HTTPException
from modules.materiais import repository


def list_materiais(db: sqlite3.Connection, disciplina_id: int):
    return repository.list_by_disciplina(db, disciplina_id)


def create_material(db: sqlite3.Connection, disciplina_id: int, titulo: str, descricao, link: str):
    return repository.create(db, disciplina_id, titulo, descricao, link)


def update_material(db: sqlite3.Connection, material_id: int, fields: dict):
    if not repository.find_by_id(db, material_id):
        raise HTTPException(status_code=404, detail="Material não encontrado")
    return repository.update(db, material_id, {k: v for k, v in fields.items() if v is not None})


def delete_material(db: sqlite3.Connection, material_id: int):
    if not repository.delete(db, material_id):
        raise HTTPException(status_code=404, detail="Material não encontrado")