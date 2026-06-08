from pydantic import BaseModel
from typing import Optional


class MaterialCreate(BaseModel):
    disciplina_id: int
    titulo: str
    descricao: Optional[str] = None
    link: str


class MaterialUpdate(BaseModel):
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    link: Optional[str] = None


class MaterialOut(BaseModel):
    id: int
    disciplina_id: int
    titulo: str
    descricao: Optional[str]
    link: str