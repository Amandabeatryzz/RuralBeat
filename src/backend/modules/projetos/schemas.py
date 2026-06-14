from pydantic import BaseModel
from typing import Optional


class ProjetoCreate(BaseModel):
    titulo: str
    descricao: Optional[str] = None
    github_link: Optional[str] = None


class ProjetoUpdate(BaseModel):
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    github_link: Optional[str] = None


class ProjetoOut(BaseModel):
    id: int
    user_id: int
    titulo: str
    descricao: Optional[str]
    github_link: Optional[str]
    created_at: Optional[str]