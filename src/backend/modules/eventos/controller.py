from typing import Optional
from fastapi import APIRouter, Depends, Query # para lidar com parâmetros de consulta (query parameters) nas rotas

from database.connection import get_db
from security import get_current_user, get_current_admin # para lidar com autenticação e autorização, garantindo que apenas usuários autenticados possam acessar certas rotas e que apenas administradores possam acessar rotas de criação, atualização e exclusão de eventos
from modules.eventos import service
from modules.eventos.schemas import EventoCreate, EventoUpdate, EventoOut, InscricaoOut

router = APIRouter(prefix="/api/eventos", tags=["Eventos"])


@router.get("/", response_model=list[EventoOut])
def list_eventos(tipo: Optional[str] = Query(None)):
    with get_db() as db:
        return service.list_eventos(db, tipo)


@router.get("/hackathons", response_model=list[EventoOut])
def list_hackathons():
    with get_db() as db:
        return service.list_eventos(db, tipo="HACKATHON")


@router.get("/{evento_id}", response_model=EventoOut)
def get_evento(evento_id: int):
    with get_db() as db:
        return service.get_evento(db, evento_id)


@router.post("/", response_model=EventoOut, status_code=201)
def create_evento(body: EventoCreate, _=Depends(get_current_admin)):
    with get_db() as db:
        return service.create_evento(db, body.model_dump())


@router.put("/{evento_id}", response_model=EventoOut)
def update_evento(evento_id: int, body: EventoUpdate, _=Depends(get_current_admin)):
    with get_db() as db:
        return service.update_evento(db, evento_id, body.model_dump())


@router.delete("/{evento_id}", status_code=204)
def delete_evento(evento_id: int, _=Depends(get_current_admin)):
    with get_db() as db:
        service.delete_evento(db, evento_id)


@router.post("/{evento_id}/inscrever", response_model=InscricaoOut, status_code=201)
def inscrever(evento_id: int, current_user: dict = Depends(get_current_user)):
    with get_db() as db:
        return service.inscrever(db, current_user["id"], evento_id)


@router.delete("/{evento_id}/inscrever", status_code=204)
def cancelar(evento_id: int, current_user: dict = Depends(get_current_user)):
    with get_db() as db:
        service.cancelar_inscricao(db, current_user["id"], evento_id)


@router.get("/inscricoes/me", response_model=list[InscricaoOut])
def minhas_inscricoes(current_user: dict = Depends(get_current_user)):
    with get_db() as db:
        return service.minhas_inscricoes(db, current_user["id"])