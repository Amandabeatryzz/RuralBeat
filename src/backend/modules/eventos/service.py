import sqlite3
from fastapi import HTTPException
from modules.eventos import repository


def list_eventos(db, tipo=None):
    return repository.list_all(db, tipo)


def get_evento(db, evento_id):
    e = repository.find_by_id(db, evento_id)
    if not e:
        raise HTTPException(status_code=404, detail="Evento não encontrado")
    return e


def create_evento(db, data: dict):
    return repository.create(db, data)


def update_evento(db, evento_id: int, fields: dict):
    if not repository.find_by_id(db, evento_id):
        raise HTTPException(status_code=404, detail="Evento não encontrado")
    return repository.update(db, evento_id, {k: v for k, v in fields.items() if v is not None})


def delete_evento(db, evento_id: int):
    if not repository.delete(db, evento_id):
        raise HTTPException(status_code=404, detail="Evento não encontrado")


def inscrever(db: sqlite3.Connection, user_id: int, evento_id: int):
    if not repository.find_by_id(db, evento_id):
        raise HTTPException(status_code=404, detail="Evento não encontrado")
    if repository.inscricao_exists(db, user_id, evento_id):
        raise HTTPException(status_code=409, detail="Já inscrito neste evento")
    return repository.inscrever(db, user_id, evento_id)


def cancelar_inscricao(db: sqlite3.Connection, user_id: int, evento_id: int):
    if not repository.cancelar_inscricao(db, user_id, evento_id):
        raise HTTPException(status_code=404, detail="Inscrição não encontrada")


def minhas_inscricoes(db: sqlite3.Connection, user_id: int):
    return repository.list_inscricoes_user(db, user_id)