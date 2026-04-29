from fastapi import APIRouter # Importa o APIRouter do FastAPI para criar rotas específicas para o módulo de disciplinas
from .service import DisciplinaService # Importa o serviço de disciplinas para lidar com a lógica de negócios
from .schemas import DisciplinaCreate # Importa o esquema de criação de disciplina para validar os dados de entrada

router = APIRouter(prefix="/disciplinas", tags=["Disciplinas"]) # Cria um roteador com o prefixo "/disciplinas" e a tag "Disciplinas" para organizar as rotas relacionadas a disciplinas

@router.get("/") # Define uma rota GET para listar todas as disciplinas
def listar(): # Chama o serviço para listar as disciplinas e retorna o resultado
    return DisciplinaService.listar_disciplinas() # Retorna a lista de disciplinas obtida do serviço

@router.post("/") # Define uma rota POST para criar uma nova disciplina
def criar(data: DisciplinaCreate): # Recebe os dados de criação de disciplina, valida usando o esquema DisciplinaCreate e chama o serviço para criar a disciplina
    return DisciplinaService.criar_disciplina(data.dict()) #    Retorna o resultado da criação da disciplina, convertendo os dados de entrada para um dicionário antes de passar para o serviço