from pydantic import BaseModel
from typing import Optional
from enum import Enum
 
 # Schemas para materiais de estudo, usados para validação e documentação da API
class TipoMaterial(str, Enum):
    LINK     = "LINK"
    LIVRO    = "LIVRO"
    ANOTACAO = "ANOTACAO"
 
 # Os modelos MaterialCreate, MaterialUpdate e MaterialOut são usados para criar, atualizar e representar materiais de estudo na API. 
 # O campo "tipo" é do tipo TipoMaterial, que é um Enum que define os tipos de materiais disponíveis (LINK, LIVRO, ANOTACAO).
 # O campo "user_id" em MaterialOut indica se o material é pessoal do aluno (preenchido) ou público do professor (None).
class MaterialCreate(BaseModel):
    disciplina_id: int
    titulo:        str
    descricao:     Optional[str]        = None
    link:          str
    tipo:          TipoMaterial         = TipoMaterial.LINK
 
 
class MaterialUpdate(BaseModel):
    titulo:    Optional[str]         = None
    descricao: Optional[str]         = None
    link:      Optional[str]         = None
    tipo:      Optional[TipoMaterial] = None
 
 
class MaterialOut(BaseModel):
    id:            int
    disciplina_id: int
    titulo:        str
    descricao:     Optional[str]
    link:          str
    tipo:          str
    # user_id preenchido = material pessoal do aluno; None = material público do professor
    user_id:       Optional[int] = None