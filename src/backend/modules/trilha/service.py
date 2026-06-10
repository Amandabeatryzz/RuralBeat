import sqlite3
from fastapi import HTTPException, status
from typing import Optional

from modules.trilha import repository


# ── Trilha (grafo) ───────────────────────────────────────────────────────────

def get_trilha(db: sqlite3.Connection, user_id: int) -> dict:
    """
    Monta o grafo completo da trilha acadêmica para o usuário.

    Retorna:
      nos    → lista de NodoTrilha com status do aluno e flag desbloqueada
      arestas → lista de {source, target} representando pré-requisitos
    """
    disciplinas = repository.list_disciplinas(db)
    pre_reqs    = repository.list_pre_requisitos(db)
    progresso   = repository.list_progresso_usuario(db, user_id)

    # índices para lookup O(1)
    status_map = {p["disciplina_id"]: p["status"] for p in progresso}
    # pre_reqs_map: disciplina_id → [pre_requisito_ids]
    pre_reqs_map: dict[int, list[int]] = {}
    for pr in pre_reqs:
        pre_reqs_map.setdefault(pr["disciplina_id"], []).append(pr["pre_requisito_id"])

    nos = []
    for d in disciplinas:
        prereqs_ids = pre_reqs_map.get(d["id"], [])
        # disciplina está desbloqueada se todos os pré-requisitos foram aprovados
        desbloqueada = all(
            status_map.get(pid) == "APROVADO" for pid in prereqs_ids
        )
        nos.append({
            "disciplina":    d,
            "status":        status_map.get(d["id"]),
            "pre_requisitos": prereqs_ids,
            "desbloqueada":  desbloqueada,
        })

    arestas = [
        {"source": pr["pre_requisito_id"], "target": pr["disciplina_id"]}
        for pr in pre_reqs
    ]

    return {"nos": nos, "arestas": arestas}


# ── Pré-requisitos (admin) ───────────────────────────────────────────────────

def add_pre_requisito(db: sqlite3.Connection, disciplina_id: int, pre_requisito_id: int) -> dict:
    if disciplina_id == pre_requisito_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uma disciplina não pode ser pré-requisito de si mesma",
        )
    d  = repository.find_disciplina_by_id(db, disciplina_id)
    pr = repository.find_disciplina_by_id(db, pre_requisito_id)
    if not d or not pr:
        raise HTTPException(status_code=404, detail="Disciplina não encontrada")

    # verificação simples de ciclo: o candidato a pré-requisito não pode já depender de disciplina_id
    _assert_no_cycle(db, root=disciplina_id, candidate=pre_requisito_id)

    return repository.add_pre_requisito(db, disciplina_id, pre_requisito_id)


def remove_pre_requisito(db: sqlite3.Connection, disciplina_id: int, pre_requisito_id: int):
    removed = repository.remove_pre_requisito(db, disciplina_id, pre_requisito_id)
    if not removed:
        raise HTTPException(status_code=404, detail="Pré-requisito não encontrado")


def _assert_no_cycle(db: sqlite3.Connection, root: int, candidate: int):
    """BFS: garante que 'root' não é alcançável a partir de 'candidate' pelo grafo de pré-requisitos."""
    pre_reqs = repository.list_pre_requisitos(db)
    # grafo: disciplina → pré-requisitos dela
    grafo: dict[int, list[int]] = {}
    for pr in pre_reqs:
        grafo.setdefault(pr["disciplina_id"], []).append(pr["pre_requisito_id"])

    visited = set()
    queue   = [candidate]
    while queue:
        node = queue.pop()
        if node == root:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Adicionar este pré-requisito criaria um ciclo no grafo",
            )
        if node in visited:
            continue
        visited.add(node)
        queue.extend(grafo.get(node, []))


# ── Progresso do aluno ───────────────────────────────────────────────────────

def list_progresso(db: sqlite3.Connection, user_id: int) -> list:
    return repository.list_progresso_usuario(db, user_id)


def upsert_progresso(db: sqlite3.Connection, user_id: int, disciplina_id: int, status_val: str) -> dict:
    disciplina = repository.find_disciplina_by_id(db, disciplina_id)
    if not disciplina:
        raise HTTPException(status_code=404, detail="Disciplina não encontrada")

    # valida se está desbloqueada antes de marcar qualquer status
    pre_reqs = repository.list_pre_requisitos_de(db, disciplina_id)
    for pr in pre_reqs:
        pr_status = repository.find_progresso(db, user_id, pr["pre_requisito_id"])
        if not pr_status or pr_status["status"] != "APROVADO":
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Pré-requisito (id={pr['pre_requisito_id']}) ainda não foi aprovado",
            )

    return repository.upsert_progresso(db, user_id, disciplina_id, status_val)


def delete_progresso(db: sqlite3.Connection, user_id: int, disciplina_id: int):
    removed = repository.delete_progresso(db, user_id, disciplina_id)
    if not removed:
        raise HTTPException(status_code=404, detail="Progresso não encontrado")