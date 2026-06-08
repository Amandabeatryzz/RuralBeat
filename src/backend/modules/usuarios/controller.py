from fastapi import APIRouter, Depends

from database.connection import get_db
from security import get_current_user
from modules.usuarios import service
from modules.usuarios.schemas import UserCreate, UserUpdate, UserOut, LoginRequest, TokenOut

router = APIRouter(prefix="/api/usuarios", tags=["Usuários"])


@router.post("/registro", response_model=UserOut, status_code=201)
def register(body: UserCreate):
    with get_db() as db:
        return service.register(db, body.nome, body.email, body.senha)


@router.post("/login", response_model=TokenOut)
def login(body: LoginRequest):
    with get_db() as db:
        return service.login(db, body.email, body.senha)


@router.get("/me", response_model=UserOut)
def me(current_user: dict = Depends(get_current_user)):
    return current_user


@router.put("/me", response_model=UserOut)
def update_me(body: UserUpdate, current_user: dict = Depends(get_current_user)):
    with get_db() as db:
        return service.update_profile(db, current_user["id"], body.model_dump())


@router.delete("/me", status_code=204)
def delete_me(current_user: dict = Depends(get_current_user)):
    with get_db() as db:
        service.delete_account(db, current_user["id"])