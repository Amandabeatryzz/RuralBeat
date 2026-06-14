from pydantic import BaseModel
from typing import Optional


class DisciplinaOut(BaseModel):
    id: int
    codigo: str
    nome: str
    periodo: Optional[int]
    carga_horaria: int
    obrigatoria: int


class ProgressoCreate(BaseModel):
    disciplina_id: int
    status: str  # CURSANDO | APROVADO | REPROVADO | TRANCADO


class ProgressoUpdate(BaseModel):
    status: str


class ProgressoOut(BaseModel):
    id: int
    user_id: int
    disciplina_id: int
    status: str
    disciplina: Optional[DisciplinaOut] = None