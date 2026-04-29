# 🌱 RuralBeat

<p align="center">
  Sistema de gestão acadêmica com CLI + API REST (FastAPI)
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue">
  <img src="https://img.shields.io/badge/FastAPI-API-green">
  <img src="https://img.shields.io/badge/SQLite-Database-lightgrey">
  <img src="https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow">
</p>

---

## 📌 Sobre o Projeto

O **RuralBeat** é um sistema acadêmico desenvolvido em Python que permite gerenciar disciplinas e usuários através de:

* 🖥️ Interface CLI (terminal)
* 🌐 API REST com FastAPI

O projeto aplica conceitos reais de desenvolvimento backend, incluindo arquitetura em camadas, validação de dados e organização modular.

---

## 🎯 Problema

A dificuldade em organizar disciplinas e acompanhar a estrutura acadêmica de forma simples e centralizada.

---

## 💡 Solução

Um sistema que permite:

* Cadastro e autenticação de usuários
* Gerenciamento de disciplinas
* Organização por período
* Integração via API para futuras aplicações web

---

## 🧱 Arquitetura

```bash id="5z9y2r"
CLI / API (FastAPI)
        ↓
   Controller (Router)
        ↓
     Service
        ↓
   Repository
        ↓
     Database (SQLite)
```

✔ Separação de responsabilidades
✔ Reutilização de código
✔ Estrutura escalável

---

## 🚀 Releases (Evolução do Projeto)

### 🔹 Versão 1.0 (VA1)

* Estrutura inicial do projeto
* Configuração do banco SQLite
* CRUD básico de disciplinas (CLI)
* Arquitetura em camadas implementada

---

### 🔹 Versão 2.0 (VA2)

* Sistema de autenticação (login/cadastro)
* Validação de email (regex)
* Validação de senha
* Bloqueio de email duplicado
* Filtro de disciplinas por período

---

### 🔹 Versão 3.0 (VA3)

* Implementação da API REST com FastAPI
* Criação de endpoints (GET / POST)
* Uso de Pydantic para validação
* Documentação automática (Swagger)
* Integração CLI + API

---

## 🔄 Fluxogramas e Planejamento

📁 Acesse os fluxogramas e a planilha do projeto:

 https://drive.google.com/drive/folders/12n1BCKfDIjs-ZURshak3fSPBVY3y9v70?usp=sharing

Conteúdo:

* Fluxogramas das funcionalidades
* PDF da planilha de acompanhamento
* Organização das releases

---

## ⚙️ Tecnologias Utilizadas

* Python 3.x
* SQLite
* FastAPI
* Uvicorn
* Pydantic
* Regex
* Git e GitHub

---

## 🌐 API REST

### 📌 Endpoints

#### 📥 Listar disciplinas

```http id="9h9x9p"
GET /disciplinas/
```

#### ➕ Criar disciplina

```http id="ik4mqh"
POST /disciplinas/
```

Exemplo:

```json id="5d0e3k"
{
  "codigo": "12345",
  "nome": "Nova Disciplina",
  "periodo": 1,
  "carga_horaria": 60
}
```

---

## 📦 Instalação

```bash id="s9r6b8"
git clone https://github.com/ArtRaWs/RuralBeat.git
cd RuralBeat
```

---

## 🧪 Ambiente

```bash id="0skzqg"
python -m venv venv
```

Ativar:

**Windows**

```bash id="g2v1fb"
venv\Scripts\activate
```

---

## 📥 Dependências

```bash id="y7m7dy"
pip install fastapi uvicorn pydantic
```

---

## ▶️ Execução

### Banco de dados

```bash id="p1r4bi"
python -m src.backend.database.init_db
```

---

### CLI

```bash id="hb7sd2"
python -m src.backend.modules.disciplinas.main_cli
```

---

### API

Crie `main.py`:

```python id="s5q3du"
from fastapi import FastAPI
from src.backend.modules.disciplinas.controller import router

app = FastAPI(title="RuralBeat API")

app.include_router(router)
```

Execute:

```bash id="n94t3w"
uvicorn src.backend.main:app --reload
```

---

## 📊 Documentação

* Swagger: http://127.0.0.1:8000/docs
* Redoc: http://127.0.0.1:8000/redoc

---

## 🔐 Segurança

* Validação de email
* Validação de senha
* Prevenção de duplicidade
* Queries seguras (anti SQL Injection)

---

## ⚠️ Desafios

* Organização em camadas
* Integração CLI + API
* Gerenciamento de banco
* Problemas de importação Python

---

## 📈 Melhorias Futuras

* Autenticação JWT
* Criptografia de senha
* Interface web
* Deploy

---

## 👨‍💻 Autores

Arthur Ricardo da Silva
Amanda 

---

## 📄 Licença

MIT License
