import sqlite3
from fastapi import HTTPException

from modules.disciplinas import repository

VALID_STATUS = {"CURSANDO", "APROVADO", "REPROVADO", "TRANCADO"}


def list_disciplinas(db: sqlite3.Connection, periodo=None, obrigatoria=None):
    return repository.list_all(db, periodo, obrigatoria)


def get_disciplina(db: sqlite3.Connection, disciplina_id: int):
    d = repository.find_by_id(db, disciplina_id)
    if not d:
        raise HTTPException(status_code=404, detail="Disciplina não encontrada")
    return d


def get_progresso(db: sqlite3.Connection, user_id: int):
    return repository.get_progresso(db, user_id)


def set_progresso(db: sqlite3.Connection, user_id: int, disciplina_id: int, status: str):
    if status not in VALID_STATUS:
        raise HTTPException(status_code=422, detail=f"Status inválido. Use: {VALID_STATUS}")
    if not repository.find_by_id(db, disciplina_id):
        raise HTTPException(status_code=404, detail="Disciplina não encontrada")
    return repository.upsert_progresso(db, user_id, disciplina_id, status)


def remove_progresso(db: sqlite3.Connection, user_id: int, disciplina_id: int):
    if not repository.delete_progresso(db, user_id, disciplina_id):
        raise HTTPException(status_code=404, detail="Progresso não encontrado")