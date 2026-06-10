from fastapi import APIRouter, Depends, status as http_status
from typing import List

from database.connection import get_db
from security import get_current_user, get_current_admin
from modules.trilha import service, repository
from modules.trilha.schemas import (
    TrilhaOut,
    ProgressoUpdate,
    ProgressoOut,
    PreRequisitoCreate,
    PreRequisitoOut,
    DisciplinaOut,
)

router = APIRouter(prefix="/api/trilha", tags=["Trilha Acadêmica"])


# ── Grafo da Trilha ──────────────────────────────────────────────────────────

@router.get("/", response_model=TrilhaOut)
def get_trilha(current_user: dict = Depends(get_current_user)):
    """
    Retorna o grafo completo da trilha acadêmica do usuário autenticado.
    Cada nó contém a disciplina, o status do aluno e se está desbloqueada.
    As arestas representam relações de pré-requisito (source → target).
    """
    with get_db() as db:
        return service.get_trilha(db, current_user["id"])


# ── Disciplinas (leitura) ────────────────────────────────────────────────────

@router.get("/disciplinas", response_model=List[DisciplinaOut])
def list_disciplinas(
    obrigatoria: int | None = None,
    current_user: dict = Depends(get_current_user),
):
    """Lista todas as disciplinas. Filtre por ?obrigatoria=1 ou ?obrigatoria=0."""
    with get_db() as db:
        return repository.list_disciplinas(db, obrigatoria)


# ── Progresso do Aluno ───────────────────────────────────────────────────────

@router.get("/progresso", response_model=List[ProgressoOut])
def get_progresso(current_user: dict = Depends(get_current_user)):
    """Retorna todo o progresso acadêmico do usuário autenticado."""
    with get_db() as db:
        return service.list_progresso(db, current_user["id"])


@router.put("/progresso/{disciplina_id}", response_model=ProgressoOut)
def upsert_progresso(
    disciplina_id: int,
    body: ProgressoUpdate,
    current_user: dict = Depends(get_current_user),
):
    """
    Cria ou atualiza o status de uma disciplina.
    Statuses válidos: CURSANDO | APROVADO | REPROVADO | TRANCADO
    Retorna 422 se algum pré-requisito ainda não foi APROVADO.
    """
    with get_db() as db:
        return service.upsert_progresso(db, current_user["id"], disciplina_id, body.status)


@router.delete("/progresso/{disciplina_id}", status_code=http_status.HTTP_204_NO_CONTENT)
def delete_progresso(
    disciplina_id: int,
    current_user: dict = Depends(get_current_user),
):
    """Remove o registro de progresso de uma disciplina."""
    with get_db() as db:
        service.delete_progresso(db, current_user["id"], disciplina_id)


# ── Pré-requisitos (somente admin / nível 2+) ────────────────────────────────

@router.get("/pre-requisitos", response_model=List[PreRequisitoOut])
def list_pre_requisitos(current_user: dict = Depends(get_current_user)):
    """Lista todas as relações de pré-requisito cadastradas."""
    with get_db() as db:
        repository.ensure_prerequisitos_table(db)
        return repository.list_pre_requisitos(db)


@router.post(
    "/pre-requisitos",
    response_model=PreRequisitoOut,
    status_code=http_status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_admin)],
)
def add_pre_requisito(body: PreRequisitoCreate):
    """
    Adiciona uma relação de pré-requisito (admin).
    - disciplina_id    → a disciplina que EXIGE o pré-requisito
    - pre_requisito_id → a disciplina que PRECISA ser aprovada antes
    Detecta e bloqueia ciclos automaticamente.
    """
    with get_db() as db:
        return service.add_pre_requisito(db, body.disciplina_id, body.pre_requisito_id)


@router.delete(
    "/pre-requisitos/{disciplina_id}/{pre_requisito_id}",
    status_code=http_status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_admin)],
)
def remove_pre_requisito(disciplina_id: int, pre_requisito_id: int):
    """Remove uma relação de pré-requisito (admin)."""
    with get_db() as db:
        service.remove_pre_requisito(db, disciplina_id, pre_requisito_id)