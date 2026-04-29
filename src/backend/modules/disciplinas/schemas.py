from pydantic import BaseModel # Importa o BaseModel do Pydantic para criar modelos de dados para validação e serialização
class DisciplinaCreate(BaseModel): # Define um modelo de dados para a criação de uma disciplina, com os campos necessários e seus tipos
    codigo: str 
    nome: str
    periodo: int
    carga_horaria: int = 60