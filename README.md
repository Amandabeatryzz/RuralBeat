RuralBeat
📌 Sobre o Projeto

O RuralBeat é um sistema acadêmico desenvolvido em Python
O sistema permite o gerenciamento de disciplinas e usuários, aplicando conceitos reais de backend como arquitetura em camadas, validação de dados e persistência.

🎯 Problema

A organização acadêmica manual dificulta o controle de disciplinas, períodos e progresso do aluno.

💡 Solução

O sistema oferece:

Gerenciamento de disciplinas
Organização por período
Cadastro e login de usuários
API para integração com aplicações web ou mobile
🧱 Arquitetura
CLI / API (FastAPI)
        ↓
   Controller (Router)
        ↓
     Service
        ↓
   Repository
        ↓
     Database (SQLite)
🔍 Camadas
CLI / API → Interface com usuário
Controller (Router) → Define endpoints da API
Service → Regras de negócio
Repository → Comunicação com banco
Database → Persistência dos dados

✔ Separação de responsabilidades
✔ Reuso de código entre CLI e API
✔ Facilidade de escalabilidade

⚙️ Tecnologias
Python 3.x
SQLite (sqlite3)
FastAPI
Uvicorn
Pydantic
Regex (validação CLI)
Git e GitHub
🚀 Funcionalidades
👤 Usuários
Cadastro
Login
Validação de email
Validação de senha
Bloqueio de email duplicado
📚 Disciplinas
Criar disciplina
Listar disciplinas
Filtrar por período
🌐 API REST (FastAPI)
📌 Estrutura
router.py → define endpoints
schemas.py → validação com Pydantic
service.py → regras de negócio
🔗 Endpoints
📥 Listar disciplinas
GET /disciplinas/
➕ Criar disciplina
POST /disciplinas/

Exemplo JSON:

{
  "codigo": "12345",
  "nome": "Nova Disciplina",
  "periodo": 1,
  "carga_horaria": 60
}
📦 Instalação
1. Clonar o repositório
git clone https://github.com/ArtRaWs/RuralBeat.git
cd RuralBeat
2. Criar ambiente virtual
python -m venv venv
3. Ativar ambiente

Windows:

venv\Scripts\activate

Linux/Mac:

source venv/bin/activate
4. Instalar dependências
pip install fastapi uvicorn pydantic
▶️ Execução
🗄️ Inicializar banco de dados
python -m src.backend.database.init_db
🖥️ Rodar CLI
python -m src.backend.modules.disciplinas.main_cli
🌐 Rodar API

Crie um arquivo main.py:

from fastapi import FastAPI
from src.backend.modules.disciplinas.controller import router as disciplinas_router

app = FastAPI(title="RuralBeat API")

app.include_router(disciplinas_router)

Execute:

uvicorn src.backend.main:app --reload
📊 Documentação automática

Após rodar a API:

Swagger:
http://127.0.0.1:8000/docs
Redoc:
http://127.0.0.1:8000/redoc
🧠 Fluxo do Sistema
Usuário acessa CLI ou API
Dados são validados (regex ou Pydantic)
Service processa regras
Repository acessa banco
Retorno ao usuário
📁 Estrutura do Projeto
src/backend/
├── config.py
├── database/
│   ├── connection.py
│   ├── init_db.py
│   ├── schema.sql
│   └── migrations.sql
└── modules/
    ├── disciplinas/
    │   ├── main_cli.py
    │   ├── router.py
    │   ├── service.py
    │   ├── repository.py
    │   └── schemas.py
    └── usuario/
        ├── user_service.py
        └── user_repository.py

    Há o front-end também
⚠️ Desafios
Integração entre CLI e API
Organização em arquitetura modular
Validação de dados
Sincronização do banco SQLite
Problemas de importação no Python
🔐 Segurança
Validação de email com regex
Validação de senha
Prevenção de duplicidade
Uso de parâmetros SQL (evita SQL Injection)
📈 Melhorias Futuras
Autenticação JWT
Criptografia de senha (bcrypt)
Interface web
Sistema de progresso do aluno
Hackathon


👨‍💻 Autores

Arthur Ricardo da Silva
Amanda Beatryz

📄 Licença

MIT License
