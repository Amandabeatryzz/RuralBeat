import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database.init_db import init_db
from modules.usuarios.controller import router as usuarios_router
from modules.disciplinas.controller import router as disciplinas_router
from modules.materiais.controller import router as materiais_router
from modules.eventos.controller import router as eventos_router
from modules.projetos.controller import router as projetos_router
from modules.oportunidades.controller import router as oportunidades_router

init_db()

app = FastAPI(
    title="RuralBeat API",
    description="Plataforma de apoio à trajetória acadêmica e desenvolvimento profissional",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:3000",
        "http://localhost:3000",
        "null",  # abre direto como arquivo no browser
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(usuarios_router)
app.include_router(disciplinas_router)
app.include_router(materiais_router)
app.include_router(eventos_router)
app.include_router(projetos_router)
app.include_router(oportunidades_router)


@app.get("/", tags=["Health"])
def health():
    return {"status": "ok", "app": "RuralBeat API"}