from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
from datetime import datetime


class TipoMaterial(str, Enum):
    LINK = "LINK"
    LIVRO = "LIVRO"
    ANOTACAO = "ANOTACAO"
    PDF = "PDF"


class MaterialCreate(BaseModel):
    disciplina_id: int
    titulo: str
    descricao: Optional[str] = None
    link: str
    tipo: TipoMaterial = TipoMaterial.LINK


class MaterialUpdate(BaseModel):
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    link: Optional[str] = None
    tipo: Optional[TipoMaterial] = None


class MaterialOut(BaseModel):
    id: int
    disciplina_id: int
    titulo: str
    descricao: Optional[str]
    link: str
    tipo: str = "LINK"
    user_id: Optional[int] = None


# ── Infinite Canvas ───────────────────────────────────────────────────────────

class TipoNoCanvas(str, Enum):
    TEXTO = "TEXTO"
    CODIGO = "CODIGO"
    ARQUIVO = "ARQUIVO"


class ViewportUpdate(BaseModel):
    viewport_x: float = 0
    viewport_y: float = 0
    zoom: float = Field(default=1, ge=0.1, le=4)


class NoCanvasCreate(BaseModel):
    tipo: TipoNoCanvas
    titulo: Optional[str] = None
    conteudo: Optional[str] = None
    pos_x: float = 0
    pos_y: float = 0
    largura: float = Field(default=280, ge=120, le=800)
    altura: float = Field(default=180, ge=80, le=600)
    material_id: Optional[int] = None
    meta_json: Optional[str] = None
    z_index: int = 0


class NoCanvasUpdate(BaseModel):
    titulo: Optional[str] = None
    conteudo: Optional[str] = None
    pos_x: Optional[float] = None
    pos_y: Optional[float] = None
    largura: Optional[float] = Field(default=None, ge=120, le=800)
    altura: Optional[float] = Field(default=None, ge=80, le=600)
    material_id: Optional[int] = None
    meta_json: Optional[str] = None
    z_index: Optional[int] = None


class NoCanvasOut(BaseModel):
    id: int
    workspace_id: int
    tipo: str
    titulo: Optional[str]
    conteudo: Optional[str]
    pos_x: float
    pos_y: float
    largura: float
    altura: float
    material_id: Optional[int]
    meta_json: Optional[str]
    z_index: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class CanvasWorkspaceOut(BaseModel):
    id: int
    user_id: int
    disciplina_id: int
    viewport_x: float
    viewport_y: float
    zoom: float
    nos: list[NoCanvasOut] = []
    updated_at: Optional[str] = None
