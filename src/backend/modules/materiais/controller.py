from fastapi import APIRouter, Depends

from database.connection import get_db
from security import get_current_user, get_current_admin
from modules.materiais import service
from modules.materiais.schemas import MaterialCreate, MaterialUpdate, MaterialOut

router = APIRouter(prefix="/api/materiais", tags=["Materiais"])


@router.get("/disciplina/{disciplina_id}", response_model=list[MaterialOut])
def list_materiais(disciplina_id: int, _=Depends(get_current_user)):
    with get_db() as db:
        return service.list_materiais(db, disciplina_id)


@router.post("/", response_model=MaterialOut, status_code=201)
def create_material(body: MaterialCreate, _=Depends(get_current_admin)):
    with get_db() as db:
        return service.create_material(db, body.disciplina_id, body.titulo, body.descricao, body.link)


@router.put("/{material_id}", response_model=MaterialOut)
def update_material(material_id: int, body: MaterialUpdate, _=Depends(get_current_admin)):
    with get_db() as db:
        return service.update_material(db, material_id, body.model_dump())


@router.delete("/{material_id}", status_code=204)
def delete_material(material_id: int, _=Depends(get_current_admin)):
    with get_db() as db:
        service.delete_material(db, material_id)