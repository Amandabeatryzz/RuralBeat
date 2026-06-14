import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # para permitir requisições de origens diferentes (CORS)

from database.init_db import init_db # função para inicializar o banco de dados
from modules.usuarios.controller import router as usuarios_router # importação do roteador de usuários para lidar com as rotas relacionadas a usuários
from modules.disciplinas.controller import router as disciplinas_router
from modules.materiais.controller import router as materiais_router
from modules.eventos.controller import router as eventos_router
from modules.projetos.controller import router as projetos_router
from modules.oportunidades.controller import router as oportunidades_router
from modules.trilha.controller import router as trilha_router

init_db() # inicializa o banco de dados, criando as tabelas necessárias se elas ainda não existirem

app = FastAPI( # criação da aplicação FastAPI, que é o objeto principal para definir rotas e configurações da API
    title="RuralBeat API",
    description="Plataforma de apoio à trajetória acadêmica e desenvolvimento profissional",
    version="1.0.0",
)
# Configuração do CORS para permitir requisições de origens específicas, como o frontend rodando em localhost
app.add_middleware( 
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500", # permite requisições do frontend rodando em localhost na porta 5500, o que é útil durante o desenvolvimento para evitar problemas de CORS. Em produção, é recomendado restringir isso para melhorar a segurança.
        "http://localhost:5500", 
        "http://127.0.0.1:3000", 
        "http://localhost:3000",
        "null",  # abre direto como arquivo no browser
    ],
    allow_credentials=True,
    allow_methods=["*"], # permite todos os métodos HTTP (GET, POST, PUT, DELETE, etc.) para as rotas da API, o que é útil durante o desenvolvimento para evitar problemas de CORS. Em produção, é recomendado restringir isso para melhorar a segurança.
    allow_headers=["*"], # permite todos os métodos HTTP e cabeçalhos, o que é útil durante o desenvolvimento para evitar problemas de CORS. Em produção, é recomendado restringir isso para melhorar a segurança.
)

app.include_router(usuarios_router) # inclui o roteador de usuários na aplicação, o que permite que as rotas definidas no controller de usuários sejam acessíveis através da API. O roteador é responsável por lidar com as requisições relacionadas a usuários, como cadastro, login, etc.
app.include_router(disciplinas_router)
app.include_router(materiais_router)
app.include_router(eventos_router)
app.include_router(projetos_router)
app.include_router(oportunidades_router)
app.include_router(trilha_router)


@app.get("/", tags=["Health"]) # rota para verificar se a API está funcionando corretamente, retornando um status "ok" e o nome da aplicação. Essa rota pode ser usada para monitoramento e testes de saúde da API.
def health():
    return {"status": "ok", "app": "RuralBeat API"}


# 
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app", 
        host="127.0.0.1", 
        port=8000, 
        reload=True,
        # Ignora os arquivos do banco e a pasta database inteira
        reload_excludes=["*.db", "*.db-journal", "database/*"] 
    )