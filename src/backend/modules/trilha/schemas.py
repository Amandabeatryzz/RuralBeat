from pydantic import BaseModel
from typing import Optional, List


class DisciplinaOut(BaseModel):
    id: int
    codigo: str
    nome: str
    periodo: Optional[int]
    carga_horaria: int
    obrigatoria: int


class PreRequisitoCreate(BaseModel):
    disciplina_id: int
    pre_requisito_id: int


class PreRequisitoOut(BaseModel):
    id: int
    disciplina_id: int
    pre_requisito_id: int


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


class NodoTrilha(BaseModel):
    """Representa um nó do grafo de trilha acadêmica."""
    disciplina: DisciplinaOut
    status: Optional[str] = None          # status do progresso do aluno (ou None se sem registro)
    pre_requisitos: List[int] = []        # lista de disciplina_id que são pré-requisitos deste nó
    desbloqueada: bool = True             # False se algum pré-requisito não foi APROVADO


class TrilhaOut(BaseModel):
    """Resposta completa do grafo de trilha."""
    nos: List[NodoTrilha]
    arestas: List[dict]                   # [{source: id, target: id}] — para renderizar linhas no frontend