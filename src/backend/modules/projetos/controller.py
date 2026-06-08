from fastapi import APIRouter, Depends

from database.connection import get_db
from security import get_current_user
from modules.projetos import service
from modules.projetos.schemas import ProjetoCreate, ProjetoUpdate, ProjetoOut

router = APIRouter(prefix="/api/projetos", tags=["Projetos"])


@router.get("/", response_model=list[ProjetoOut])
def list_projetos():
    with get_db() as db:
        return service.list_projetos(db)


@router.get("/me", response_model=list[ProjetoOut])
def meus_projetos(current_user: dict = Depends(get_current_user)):
    with get_db() as db:
        return service.list_meus_projetos(db, current_user["id"])


@router.post("/", response_model=ProjetoOut, status_code=201)
def create_projeto(body: ProjetoCreate, current_user: dict = Depends(get_current_user)):
    with get_db() as db:
        return service.create_projeto(db, current_user["id"], body.model_dump())


@router.put("/{projeto_id}", response_model=ProjetoOut)
def update_projeto(projeto_id: int, body: ProjetoUpdate, current_user: dict = Depends(get_current_user)):
    with get_db() as db:
        return service.update_projeto(db, projeto_id, current_user["id"], body.model_dump())


@router.delete("/{projeto_id}", status_code=204)
def delete_projeto(projeto_id: int, current_user: dict = Depends(get_current_user)):
    with get_db() as db:
        is_admin = current_user.get("nivel", 0) >= 2
        service.delete_projeto(db, projeto_id, current_user["id"], is_admin)