import sqlite3
from fastapi import HTTPException # para levantar exceções HTTP com códigos de status e mensagens personalizadas. Isso é útil para indicar erros específicos, como quando um evento não é encontrado ou quando um usuário já está inscrito em um evento.
from modules.eventos import repository


def list_eventos(db, tipo=None):
    return repository.list_all(db, tipo)


def get_evento(db, evento_id):
    e = repository.find_by_id(db, evento_id)
    if not e:
        raise HTTPException(status_code=404, detail="Evento não encontrado") # A função get_evento tenta recuperar um evento pelo seu ID usando a função find_by_id do repositório. Se o evento não for encontrado, ela levanta uma exceção HTTP 404 com a mensagem "Evento não encontrado". Caso contrário, o evento é retornado como um dicionário.
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
# A função cancelar_inscricao tenta cancelar a inscrição de um usuário em um evento. Se a inscrição não for encontrada, ela levanta uma exceção HTTP 404 indicando que a inscrição não existe. Caso contrário, a inscrição é cancelada com sucesso.

def minhas_inscricoes(db: sqlite3.Connection, user_id: int):
    return repository.list_inscricoes_user(db, user_id)
# A função minhas_inscricoes retorna uma lista de inscrições para um usuário específico, usando a função list_inscricoes_user do repositório. Ela recebe o ID do usuário e retorna as inscrições associadas a esse usuário.