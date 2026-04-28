from fastapi import APIRouter
from .service import DisciplinaService
from .schemas import DisciplinaCreate

router = APIRouter(prefix="/disciplinas", tags=["Disciplinas"])

@router.get("/")
def listar():
    return DisciplinaService.listar_disciplinas()

@router.post("/")
def criar(data: DisciplinaCreate):
    return DisciplinaService.criar_disciplina(data.dict())