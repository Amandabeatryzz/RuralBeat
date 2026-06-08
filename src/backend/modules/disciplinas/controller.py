from typing import Optional
from fastapi import APIRouter, Depends, Query

from database.connection import get_db
from security import get_current_user
from modules.disciplinas import service
from modules.disciplinas.schemas import DisciplinaOut, ProgressoCreate, ProgressoOut

router = APIRouter(prefix="/api/disciplinas", tags=["Disciplinas"])


@router.get("/", response_model=list[DisciplinaOut])
def list_disciplinas(
    periodo: Optional[int] = Query(None),
    obrigatoria: Optional[int] = Query(None),
):
    with get_db() as db:
        return service.list_disciplinas(db, periodo, obrigatoria)


@router.get("/{disciplina_id}", response_model=DisciplinaOut)
def get_disciplina(disciplina_id: int):
    with get_db() as db:
        return service.get_disciplina(db, disciplina_id)


@router.get("/progresso/me", response_model=list[ProgressoOut])
def get_my_progresso(current_user: dict = Depends(get_current_user)):
    with get_db() as db:
        return service.get_progresso(db, current_user["id"])


@router.post("/progresso", response_model=ProgressoOut, status_code=201)
def set_progresso(body: ProgressoCreate, current_user: dict = Depends(get_current_user)):
    with get_db() as db:
        return service.set_progresso(db, current_user["id"], body.disciplina_id, body.status)


@router.delete("/progresso/{disciplina_id}", status_code=204)
def remove_progresso(disciplina_id: int, current_user: dict = Depends(get_current_user)):
    with get_db() as db:
        service.remove_progresso(db, current_user["id"], disciplina_id)