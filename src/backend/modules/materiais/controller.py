from fastapi import APIRouter, Depends

from database.connection import get_db
from security import get_current_user, get_current_admin
from modules.materiais import service
from modules.materiais.schemas import (
    MaterialCreate,
    MaterialUpdate,
    MaterialOut,
    CanvasWorkspaceOut,
    ViewportUpdate,
    NoCanvasCreate,
    NoCanvasUpdate,
    NoCanvasOut,
)

router = APIRouter(prefix="/api/materiais", tags=["Materiais"])


# ── Materiais (referências / PDFs) ────────────────────────────────────────────

@router.get("/disciplina/{disciplina_id}", response_model=list[MaterialOut])
def list_materiais(disciplina_id: int, _=Depends(get_current_user)):
    with get_db() as db:
        return service.list_materiais(db, disciplina_id)


@router.post("/", response_model=MaterialOut, status_code=201)
def create_material(body: MaterialCreate, _=Depends(get_current_admin)):
    with get_db() as db:
        return service.create_material(
            db, body.disciplina_id, body.titulo, body.descricao, body.link, body.tipo.value
        )


@router.put("/{material_id}", response_model=MaterialOut)
def update_material(material_id: int, body: MaterialUpdate, _=Depends(get_current_admin)):
    with get_db() as db:
        return service.update_material(db, material_id, body.model_dump())


@router.delete("/{material_id}", status_code=204)
def delete_material(material_id: int, _=Depends(get_current_admin)):
    with get_db() as db:
        service.delete_material(db, material_id)


# ── Infinite Canvas Workspace ─────────────────────────────────────────────────

@router.get("/canvas/disciplina/{disciplina_id}", response_model=CanvasWorkspaceOut)
def get_canvas(disciplina_id: int, current_user: dict = Depends(get_current_user)):
    """Carrega o workspace completo (viewport + nós) do usuário para a disciplina."""
    with get_db() as db:
        return service.get_canvas(db, current_user["id"], disciplina_id)


@router.patch("/canvas/disciplina/{disciplina_id}/viewport", response_model=CanvasWorkspaceOut)
def save_viewport(
    disciplina_id: int,
    body: ViewportUpdate,
    current_user: dict = Depends(get_current_user),
):
    """Persiste posição e zoom da câmera do canvas."""
    with get_db() as db:
        return service.update_viewport(
            db,
            current_user["id"],
            disciplina_id,
            body.viewport_x,
            body.viewport_y,
            body.zoom,
        )


@router.post("/canvas/disciplina/{disciplina_id}/nos", response_model=NoCanvasOut, status_code=201)
def create_canvas_node(
    disciplina_id: int,
    body: NoCanvasCreate,
    current_user: dict = Depends(get_current_user),
):
    """Cria um nó no canvas (Texto, Código ou Arquivo)."""
    with get_db() as db:
        return service.create_node(db, current_user["id"], disciplina_id, body.model_dump())


@router.put("/canvas/nos/{node_id}", response_model=NoCanvasOut)
def update_canvas_node(
    node_id: int,
    body: NoCanvasUpdate,
    current_user: dict = Depends(get_current_user),
):
    """Atualiza posição, conteúdo ou metadados de um nó."""
    with get_db() as db:
        return service.update_node(db, current_user["id"], node_id, body.model_dump())


@router.delete("/canvas/nos/{node_id}", status_code=204)
def delete_canvas_node(node_id: int, current_user: dict = Depends(get_current_user)):
    with get_db() as db:
        service.delete_node(db, current_user["id"], node_id)
