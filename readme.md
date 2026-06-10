# 🦀 RuralBeat

Plataforma de apoio à trajetória acadêmica e ao desenvolvimento profissional dos estudantes de tecnologia da UFRPE — Sistemas de Informação.

Link(Artigo): https://pt.overleaf.com/read/jdnfsshbhbgh#84f119

## 📚 Bibliotecas e dependências utilizadas

### Backend (Python)

| Biblioteca | Versão | Justificativa |
|---|---|---|
| **FastAPI** | 0.111.0 | Framework web assíncrono de alta performance para construção de APIs REST. Escolhido pela validação automática via Pydantic, geração automática de documentação OpenAPI (Swagger) e suporte nativo a tipagem Python. |
| **Uvicorn** | 0.29.0 | Servidor ASGI utilizado para executar a aplicação FastAPI. É leve, rápido e suporta hot-reload durante o desenvolvimento. |
| **Pydantic v2** | 2.7.1 | Biblioteca de validação de dados baseada em anotações de tipo Python. Utilizada para definir e validar os schemas de entrada e saída de todos os endpoints da API. |
| **pydantic-settings** | 2.14.1 | Extensão do Pydantic para gerenciamento de configurações via variáveis de ambiente e arquivo `.env`. Utilizada no `config.py` para centralizar as configurações da aplicação (SECRET_KEY, DATABASE_URL, JWT). |
| **python-jose** | 3.3.0 | Implementação de JSON Web Tokens (JWT) para Python. Utilizada no `security.py` para criação e verificação dos tokens de autenticação dos usuários. |
| **passlib + bcrypt** | 1.7.4 + 4.0.1 | Passlib é uma biblioteca de hashing de senhas; bcrypt é o algoritmo utilizado. Responsáveis por armazenar senhas de forma segura com salt automático, tornando impossível a reversão mesmo em caso de vazamento do banco. |
| **python-multipart** | 0.0.9 | Dependência do FastAPI para parsing de formulários HTML. Requerida pelo OAuth2PasswordBearer utilizado na autenticação. |
| **SQLite3** | stdlib | Banco de dados relacional embutido no Python. Escolhido pela ausência de necessidade de instalação de servidor externo, adequado para o escopo acadêmico do projeto. |

### Frontend (HTML + CSS + JavaScript puro)

| Recurso | Origem | Justificativa |
|---|---|---|
| **Syne** (fonte) | Google Fonts | Fonte display com personalidade forte, usada nos títulos e logotipo. Transmite identidade tecnológica e moderna ao projeto. |
| **DM Sans** (fonte) | Google Fonts | Fonte sans-serif otimizada para leitura em telas em tamanhos pequenos e médios. Utilizada no corpo do texto e elementos de interface. |
| **SVG inline** | Nativo | Ícones implementados diretamente como SVG inline para evitar dependências externas e garantir escalabilidade em qualquer resolução. |
| **SVG API do navegador** | Nativo | A Trilha Acadêmica utiliza `createElementNS` e curvas Bézier cúbicas para desenhar as conexões entre disciplinas dinamicamente, sem bibliotecas de diagramas externas. |

> O frontend foi desenvolvido intencionalmente sem frameworks como React, Vue ou Angular, e sem bibliotecas de UI como Bootstrap ou Tailwind, para demonstrar domínio de HTML, CSS e JavaScript puros.

---

## ⚙️ Como rodar o projeto

### Pré-requisitos

- [Python 3.11](https://www.python.org/downloads/release/python-3119/) — **obrigatório usar 3.11**. Versões 3.12+ têm incompatibilidade com o `pydantic-core` que exige compilação Rust.
- [Git](https://git-scm.com/)
- [VS Code](https://code.visualstudio.com/) com extensão [Live Server](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer)

### 1. Clonar o repositório

```bash
git clone https://github.com/seu-usuario/RuralBeat.git
cd RuralBeat
```

### 2. Configurar e rodar o backend

```bash
cd src/backend

# Criar e ativar ambiente virtual com Python 3.11
py -3.11 -m venv venv
source venv/Scripts/activate   # Windows Git Bash
# venv\Scripts\activate        # Windows PowerShell
# source venv/bin/activate     # Linux/macOS

# Instalar dependências
pip install -r requirements.txt
pip install pydantic-settings

# Se houver erro com bcrypt:
pip install bcrypt==4.0.1

# Copiar schema para o backend
cp ../../database/schema.sql database/schema.sql

# Subir o servidor
cd api
uvicorn main:app
```

Servidor em **http://localhost:8000** · Swagger em **http://localhost:8000/docs**

### 3. Rodar o frontend

1. Abra `src/frontend/` no VS Code
2. Clique com botão direito em `index.html` → **Open with Live Server**
3. Acesse **http://127.0.0.1:5500**

> ⚠️ É obrigatório abrir pelo Live Server (porta 5500). Abrir diretamente no navegador gera erros de CORS.

### 4. Variáveis de ambiente (opcional)

Crie `src/backend/.env`:

```env
DATABASE_URL=database/ruralbeat.db
SECRET_KEY=sua-chave-secreta-aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
```

---

## 🗂️ Organização dos módulos

O projeto segue arquitetura em camadas com o padrão **Controller → Service → Repository** no backend e uma SPA (Single Page Application) no frontend.

```
RuralBeat/
├── database/
│   └── schema.sql                  # Schema SQL: tabelas e seed de disciplinas
│
├── src/
│   ├── backend/
│   │   ├── config.py               # Configurações globais (JWT, DB, ambiente)
│   │   ├── security.py             # Autenticação: bcrypt, JWT, dependências FastAPI
│   │   ├── requirements.txt        # Dependências Python
│   │   ├── database/
│   │   │   ├── connection.py       # Context manager SQLite (commit/rollback automático)
│   │   │   ├── init_db.py          # Inicialização do banco ao subir o servidor
│   │   │   └── schema.sql          # Cópia do schema usada pelo backend
│   │   ├── api/
│   │   │   └── main.py             # Entrypoint FastAPI: routers, CORS, middlewares
│   │   └── modules/
│   │       ├── usuarios/           # Autenticação, cadastro e perfil
│   │       ├── disciplinas/        # Disciplinas e progresso acadêmico
│   │       ├── materiais/          # Materiais de apoio por disciplina
│   │       ├── eventos/            # Eventos, hackathons e inscrições
│   │       ├── projetos/           # Projetos publicados pela comunidade
│   │       └── oportunidades/      # Vagas, estágios e oportunidades
│   │       └── trilha/             # Organização, acadêmico
│   │       └── hackathon/           # Eventos, Equipes
│   │
│   └── frontend/
│       ├── index.html              # SPA: toda a estrutura HTML das 8 páginas
│       ├── styles.css              # Design system completo (tema dark, componentes)
│       └── script.js               # Lógica: estado global, API calls, renderização
```

### Padrão interno de cada módulo backend

Cada um dos 6 módulos segue a mesma estrutura de 4 arquivos, garantindo separação de responsabilidades:

| Arquivo | Responsabilidade |
|---|---|
| `controller.py` | Define rotas HTTP e injeta dependências (autenticação, DB) |
| `service.py` | Contém regras de negócio e validações de domínio |
| `repository.py` | Executa queries SQL diretamente no banco de dados |
| `schemas.py` | Define modelos Pydantic para validação de entrada e saída |

O controller nunca acessa o banco diretamente, e o repository nunca contém lógica de negócio.

### Regras de permissão por módulo

| Módulo | Leitura | Escrita | Admin |
|---|---|---|---|
| usuarios | — | Próprio usuário | — |
| disciplinas | Pública | JWT (progresso) | — |
| materiais | JWT | — | ✅ Criar/editar/excluir |
| eventos | Pública | JWT (inscrição) | ✅ Criar/editar/excluir |
| projetos | Pública | JWT (próprios) | ✅ Excluir qualquer |
| oportunidades | Pública | — | ✅ Criar/editar/excluir |

---

## 💡 Funcionalidade de inovação: Trilha Acadêmica Visual

A principal inovação do RuralBeat é a **Trilha Acadêmica** — uma representação visual interativa de todo o currículo do curso organizado por período, com o progresso pessoal do estudante refletido em tempo real.

### O que ela faz

A trilha exibe todas as disciplinas obrigatórias dispostas em colunas por período (1º ao 9º), conectadas por curvas Bézier que representam a progressão natural entre os semestres. Cada disciplina é um nó interativo que reflete o status acadêmico do estudante com cores distintas:

| Cor | Status |
|---|---|
| 🟢 Verde | Aprovado |
| 🔵 Azul | Cursando atualmente |
| 🔴 Vermelho | Reprovado |
| 🟡 Amarelo | Trancado |
| ⬜ Cinza | Ainda não cursada |

As conexões entre os nós também mudam de cor conforme o progresso: saindo de disciplinas aprovadas ficam verdes, de disciplinas em andamento ficam azuis — criando um "caminho iluminado" que mostra visualmente até onde o estudante chegou no curso.

### Por que é inovador

Plataformas acadêmicas convencionais apresentam o currículo como listas ou tabelas planas, sem contexto visual de progressão. A Trilha Acadêmica transforma essa informação em um **mapa de jornada personalizado**, onde o estudante consegue:

- Ver de imediato em qual semestre está e o que falta concluir
- Identificar gargalos (disciplinas reprovadas que bloqueiam o avanço)
- Ter senso de progresso e motivação ao visualizar o caminho percorrido
- Clicar em qualquer disciplina para ver detalhes e acessar materiais

### Como foi implementado

A trilha é construída inteiramente com tecnologias nativas do navegador, sem bibliotecas externas de diagramas:

- **Layout em colunas** via CSS Flexbox, uma coluna por período
- **Conexões visuais** desenhadas com a SVG API nativa (`createElementNS`), usando curvas Bézier cúbicas calculadas dinamicamente com base nas posições dos nós no DOM
- **Atualização em tempo real** — ao alterar o status de uma disciplina em qualquer parte do sistema, a trilha redesenha as conexões instantaneamente
- **Scroll horizontal** para acomodar os 9 períodos em telas menores

```javascript
// Curva Bézier conectando dois nós de períodos consecutivos
const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
path.setAttribute('d', `M${x1},${y1} C${cx1},${y1} ${cx2},${y2} ${x2},${y2}`);
path.setAttribute('stroke',
  fromStatus === 'APROVADO' ? 'rgba(34,197,94,0.3)' :
  fromStatus === 'CURSANDO' ? 'rgba(59,130,246,0.25)' :
  'rgba(255,255,255,0.05)'
);
```

---

## 🛠️ Tecnologias utilizadas (resumo)

**Backend:** Python 3.11 · FastAPI · SQLite · JWT (python-jose) · bcrypt (passlib) · Pydantic v2

**Frontend:** HTML5 · CSS3 · JavaScript ES2022 · SVG API nativa · Google Fonts (Syne + DM Sans)

**Ferramentas:** Git · VS Code · Live Server · Uvicorn

---

## 🐛 Problemas comuns

| Erro | Solução |
|---|---|
| `ModuleNotFoundError: pydantic_settings` | `pip install pydantic-settings` |
| `ValueError: password cannot be longer than 72 bytes` | `pip install bcrypt==4.0.1` |
| `sqlite3.OperationalError: unable to open database file` | Verifique se `schema.sql` está em `src/backend/database/` |
| Porta 8000 em uso | `taskkill /F /IM python.exe` (Windows) · `pkill -f uvicorn` (Linux/macOS) |
| CORS bloqueando requisições | Abra o frontend pelo Live Server na porta 5500 |
| `Failed building wheel for pydantic-core` | Use Python 3.11, não 3.12+ |

---

## 👥 Equipe

Desenvolvido por Arthur Ricardo e Amanda Beatryz - Sistemas de Informação — UFRPE / Campus Recife.

🦀 *O Crabit é o mascote do RuralBeat — um caranguejo programador que acompanha o estudante em toda a jornada acadêmica.*