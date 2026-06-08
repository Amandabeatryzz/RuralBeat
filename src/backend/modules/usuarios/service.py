import sqlite3
from fastapi import HTTPException, status

from security import hash_password, verify_password, create_access_token
from modules.usuarios import repository


def register(db: sqlite3.Connection, nome: str, email: str, senha: str) -> dict:
    if repository.find_by_email(db, email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="E-mail já cadastrado")
    senha_hash = hash_password(senha)
    return repository.create(db, nome, email, senha_hash)


def login(db: sqlite3.Connection, email: str, senha: str) -> dict:
    user = repository.find_by_email(db, email)
    if not user or not verify_password(senha, user["senha"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")
    token = create_access_token({"sub": str(user["id"])})
    return {"access_token": token, "token_type": "bearer", "user": user}


def get_profile(db: sqlite3.Connection, user_id: int) -> dict:
    user = repository.find_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user


def update_profile(db: sqlite3.Connection, user_id: int, fields: dict) -> dict:
    return repository.update(db, user_id, {k: v for k, v in fields.items() if v is not None})


def delete_account(db: sqlite3.Connection, user_id: int):
    if not repository.delete(db, user_id):
        raise HTTPException(status_code=404, detail="Usuário não encontrado")