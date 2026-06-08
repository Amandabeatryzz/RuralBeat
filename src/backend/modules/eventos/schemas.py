from pydantic import BaseModel
from typing import Optional


class EventoCreate(BaseModel):
    titulo: str
    descricao: Optional[str] = None
    data_evento: Optional[str] = None   # ISO date: "2025-08-10"
    local: Optional[str] = None
    tipo: str = "EVENTO"                # EVENTO | HACKATHON


class EventoUpdate(BaseModel):
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    data_evento: Optional[str] = None
    local: Optional[str] = None
    tipo: Optional[str] = None


class EventoOut(BaseModel):
    id: int
    titulo: str
    descricao: Optional[str]
    data_evento: Optional[str]
    local: Optional[str]
    tipo: str


class InscricaoOut(BaseModel):
    id: int
    user_id: int
    evento_id: int