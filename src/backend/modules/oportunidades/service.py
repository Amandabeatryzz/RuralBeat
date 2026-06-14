from fastapi import HTTPException
from modules.oportunidades import repository


def list_oportunidades(db):
    return repository.list_all(db)


def create_oportunidade(db, data: dict):
    return repository.create(db, data)


def update_oportunidade(db, op_id: int, fields: dict):
    if not repository.find_by_id(db, op_id):
        raise HTTPException(status_code=404, detail="Oportunidade não encontrada")
    return repository.update(db, op_id, {k: v for k, v in fields.items() if v is not None})


def delete_oportunidade(db, op_id: int):
    if not repository.delete(db, op_id):
        raise HTTPException(status_code=404, detail="Oportunidade não encontrada")