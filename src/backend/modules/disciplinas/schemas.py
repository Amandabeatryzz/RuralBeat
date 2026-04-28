from pydantic import BaseModel

class DisciplinaCreate(BaseModel):
    codigo: str
    nome: str
    periodo: int
    carga_horaria: int = 60