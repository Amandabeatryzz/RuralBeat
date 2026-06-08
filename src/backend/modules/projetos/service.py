from fastapi import HTTPException
from modules.projetos import repository


def list_projetos(db):
    return repository.list_all(db)


def list_meus_projetos(db, user_id):
    return repository.list_by_user(db, user_id)


def create_projeto(db, user_id, body: dict):
    return repository.create(db, user_id, body["titulo"], body.get("descricao"), body.get("github_link"))


def update_projeto(db, projeto_id: int, user_id: int, fields: dict):
    projeto = repository.find_by_id(db, projeto_id)
    if not projeto:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")
    if projeto["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Sem permissão para editar este projeto")
    return repository.update(db, projeto_id, {k: v for k, v in fields.items() if v is not None})


def delete_projeto(db, projeto_id: int, user_id: int, is_admin: bool = False):
    projeto = repository.find_by_id(db, projeto_id)
    if not projeto:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")
    if not is_admin and projeto["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Sem permissão para excluir este projeto")
    repository.delete(db, projeto_id)