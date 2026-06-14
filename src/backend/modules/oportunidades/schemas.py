from pydantic import BaseModel
from typing import Optional


class OportunidadeCreate(BaseModel):
    titulo: str
    descricao: Optional[str] = None
    empresa: Optional[str] = None
    link: Optional[str] = None


class OportunidadeUpdate(BaseModel):
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    empresa: Optional[str] = None
    link: Optional[str] = None


class OportunidadeOut(BaseModel):
    id: int
    titulo: str
    descricao: Optional[str]
    empresa: Optional[str]
    link: Optional[str]