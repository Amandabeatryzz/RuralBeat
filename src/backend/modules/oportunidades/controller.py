from fastapi import APIRouter, Depends

from database.connection import get_db
from security import get_current_admin
from modules.oportunidades import service
from modules.oportunidades.schemas import OportunidadeCreate, OportunidadeUpdate, OportunidadeOut

router = APIRouter(prefix="/api/oportunidades", tags=["Oportunidades"])


@router.get("/", response_model=list[OportunidadeOut])
def list_oportunidades():
    with get_db() as db:
        return service.list_oportunidades(db)


@router.post("/", response_model=OportunidadeOut, status_code=201)
def create(body: OportunidadeCreate, _=Depends(get_current_admin)):
    with get_db() as db:
        return service.create_oportunidade(db, body.model_dump())


@router.put("/{op_id}", response_model=OportunidadeOut)
def update(op_id: int, body: OportunidadeUpdate, _=Depends(get_current_admin)):
    with get_db() as db:
        return service.update_oportunidade(db, op_id, body.model_dump())


@router.delete("/{op_id}", status_code=204)
def delete(op_id: int, _=Depends(get_current_admin)):
    with get_db() as db:
        service.delete_oportunidade(db, op_id)