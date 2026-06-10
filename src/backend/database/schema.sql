CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    senha TEXT NOT NULL,
    nivel INTEGER DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS disciplinas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT UNIQUE NOT NULL,
    nome TEXT NOT NULL,
    periodo INTEGER CHECK (periodo BETWEEN 1 AND 10),
    carga_horaria INTEGER NOT NULL,
    obrigatoria INTEGER NOT NULL DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_disciplinas_periodo ON disciplinas(periodo);

CREATE TABLE IF NOT EXISTS progresso_academico (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    disciplina_id INTEGER NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('CURSANDO','APROVADO','REPROVADO','TRANCADO')),
    UNIQUE(user_id, disciplina_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (disciplina_id) REFERENCES disciplinas(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS materiais (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    disciplina_id INTEGER NOT NULL,
    titulo TEXT NOT NULL,
    descricao TEXT,
    link TEXT NOT NULL,
    tipo TEXT DEFAULT 'LINK' CHECK (tipo IN ('LINK','LIVRO','ANOTACAO','PDF')),
    user_id INTEGER,
    FOREIGN KEY (disciplina_id) REFERENCES disciplinas(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

-- Infinite Canvas Workspace (Materiais)
CREATE TABLE IF NOT EXISTS canvas_workspaces (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    disciplina_id INTEGER NOT NULL,
    viewport_x REAL NOT NULL DEFAULT 0,
    viewport_y REAL NOT NULL DEFAULT 0,
    zoom REAL NOT NULL DEFAULT 1,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, disciplina_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (disciplina_id) REFERENCES disciplinas(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS canvas_nodes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    workspace_id INTEGER NOT NULL,
    tipo TEXT NOT NULL CHECK (tipo IN ('TEXTO','CODIGO','ARQUIVO')),
    titulo TEXT,
    conteudo TEXT,
    pos_x REAL NOT NULL DEFAULT 0,
    pos_y REAL NOT NULL DEFAULT 0,
    largura REAL NOT NULL DEFAULT 280,
    altura REAL NOT NULL DEFAULT 180,
    material_id INTEGER,
    meta_json TEXT,
    z_index INTEGER NOT NULL DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (workspace_id) REFERENCES canvas_workspaces(id) ON DELETE CASCADE,
    FOREIGN KEY (material_id) REFERENCES materiais(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_canvas_nodes_workspace ON canvas_nodes(workspace_id);

CREATE TABLE IF NOT EXISTS eventos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    descricao TEXT,
    data_evento DATE,
    local TEXT,
    tipo TEXT NOT NULL DEFAULT 'EVENTO' CHECK (tipo IN ('EVENTO','HACKATHON'))
);

CREATE TABLE IF NOT EXISTS inscricoes_evento (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    evento_id INTEGER NOT NULL,
    UNIQUE(user_id, evento_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (evento_id) REFERENCES eventos(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS projetos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    titulo TEXT NOT NULL,
    descricao TEXT,
    github_link TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS oportunidades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    descricao TEXT,
    empresa TEXT,
    link TEXT
);

-- 1º PERÍODO
INSERT OR IGNORE INTO disciplinas (codigo, nome, periodo, carga_horaria, obrigatoria) VALUES
('14734', 'Sustentabilidade em Sistemas de Informação', 1, 60, 1),
('14708', 'Fundamentos Matemáticos para Sistemas de Informação I', 1, 60, 1),
('14733', 'Projeto Interdisciplinar para Sistemas de Informação I', 1, 60, 1),
('14709', 'Princípios de Programação', 1, 60, 1),
('4109', 'Introdução à Administração', 1, 60, 1);

-- 2º PERÍODO
INSERT OR IGNORE INTO disciplinas (codigo, nome, periodo, carga_horaria, obrigatoria) VALUES
('4162', 'Fundamentos de Sistemas de Informação II', 2, 60, 1),
('14378', 'Projeto Interdisciplinar de Sistemas de Informação II', 2, 60, 1),
('14737', 'Fundamentos Matemáticos para Sistemas de Informação II', 2, 60, 1),
('14735', 'Elementos de Sistemas Computacionais', 2, 60, 1),
('14736', 'Fundamentos de Problemas Computacionais I', 2, 60, 1);

-- 3º PERÍODO
INSERT OR IGNORE INTO disciplinas (codigo, nome, periodo, carga_horaria, obrigatoria) VALUES
('14340', 'Engenharia para Sistemas de Informação I', 3, 60, 1),
('14341', 'Introdução ao Armazenamento e Análise de Dados', 3, 60, 1),
('14342', 'Projeto Interdisciplinar para Sistemas de Informação III', 3, 60, 1),
('14379', 'Desenvolvimento de Sistemas de Informação', 3, 60, 1);

-- 4º PERÍODO
INSERT OR IGNORE INTO disciplinas (codigo, nome, periodo, carga_horaria, obrigatoria) VALUES
('14344', 'Princípios de Software Básico', 4, 60, 1),
('14346', 'Projeto Interdisciplinar de Sistemas de Informação IV', 4, 60, 1),
('14343', 'Fundamentos de Problemas Computacionais II', 4, 60, 1),
('14345', 'Sistemas de Informação na Internet', 4, 60, 1);

-- 5º PERÍODO
INSERT OR IGNORE INTO disciplinas (codigo, nome, periodo, carga_horaria, obrigatoria) VALUES
('14347', 'Engenharia para Sistemas de Informação II', 5, 60, 1),
('14348', 'Projeto de Desenvolvimento Tecnológico para o Mundo I', 5, 60, 1),
('06299', 'Segurança e Auditoria de Sistemas', 5, 60, 1),
('4249', 'Empreendedorismo e Inovação', 5, 60, 1);

-- 6º PERÍODO
INSERT OR IGNORE INTO disciplinas (codigo, nome, periodo, carga_horaria, obrigatoria) VALUES
('14352', 'Engenharia para Sistemas de Informação III', 6, 60, 1),
('14351', 'Modelagem de Dados', 6, 60, 1),
('14350', 'Projeto de Desenvolvimento Tecnológico para o Mundo II', 6, 60, 1),
('6507', 'Cálculo N1', 6, 60, 1);

-- 7º PERÍODO
INSERT OR IGNORE INTO disciplinas (codigo, nome, periodo, carga_horaria, obrigatoria) VALUES
('14353', 'Estatística Aplicada à Análise de Dados', 7, 60, 1),
('14354', 'Paradigmas de Programação', 7, 60, 1),
('14355', 'Sistemas de Apoio à Decisão', 7, 60, 1),
('14361', 'Princípios da Teoria da Computação', 7, 60, 1);

-- 8º PERÍODO
INSERT OR IGNORE INTO disciplinas (codigo, nome, periodo, carga_horaria, obrigatoria) VALUES
('4203', 'Fundamentos de Estratégia Competitiva', 8, 60, 1),
('14356', 'Projeto de Soluções Complexas II', 8, 60, 1),
('14357', 'Infraestrutura de Software', 8, 60, 1),
('4231', 'Gestão do Conhecimento', 8, 60, 1);

-- 9º PERÍODO
INSERT OR IGNORE INTO disciplinas (codigo, nome, periodo, carga_horaria, obrigatoria) VALUES
('14308', 'Projeto de Conclusão - Sistemas de Informação', 9, 420, 1);

-- OPTATIVAS
INSERT OR IGNORE INTO disciplinas (codigo, nome, periodo, carga_horaria, obrigatoria) VALUES
('04208', 'Educação Física', NULL, 60, 0),
('6277', 'Tópicos em Otimização', NULL, 60, 0),
('14705', 'Fundamentos de Criptografia', NULL, 60, 0),
('14051', 'Processamento de Imagens', NULL, 60, 0),
('14028', 'Fundamentos de Autômatos Celulares', NULL, 60, 0),
('06280', 'Modelagem Matemático-Computacional Aplicada à Epidemiologia', NULL, 60, 0),
('14011', 'Tópicos Avançados em Redes de Computadores I', NULL, 60, 0),
('14703', 'Tendências Tecnológicas em TIC', NULL, 60, 0),
('14328', 'Inovação em TIC', NULL, 60, 0),
('14024', 'Tópicos Avançados em Inteligência Artificial', NULL, 60, 0);


CREATE TABLE IF NOT EXISTS pre_requisitos (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    disciplina_id    INTEGER NOT NULL,
    pre_requisito_id INTEGER NOT NULL,
    UNIQUE(disciplina_id, pre_requisito_id),
    FOREIGN KEY (disciplina_id)    REFERENCES disciplinas(id) ON DELETE CASCADE,
    FOREIGN KEY (pre_requisito_id) REFERENCES disciplinas(id) ON DELETE CASCADE
);
 
CREATE INDEX IF NOT EXISTS idx_prereq_disciplina ON pre_requisitos(disciplina_id);
CREATE INDEX IF NOT EXISTS idx_prereq_dep        ON pre_requisitos(pre_requisito_id);
 

-- Pré-requisitos sugeridos (baseados na progressão natural do curso BSI UFRPE)
-- Ajuste conforme a grade oficial da sua instituição.
-- Os IDs abaixo assumem a ordem de INSERT do schema.sql original.
--
-- PERÍODO 1 → sem pré-requisitos
--
-- PERÍODO 2 exige aprovação no PERÍODO 1 (em disciplinas correlatas)

 
-- Fundamentos de Sistemas de Informação II (cod 4162)
-- exige: Fundamentos Matemáticos I (14708) + Princípios de Programação (14709)
INSERT OR IGNORE INTO pre_requisitos (disciplina_id, pre_requisito_id)
SELECT d.id, p.id FROM disciplinas d, disciplinas p
WHERE d.codigo = '4162' AND p.codigo = '14708';
 
INSERT OR IGNORE INTO pre_requisitos (disciplina_id, pre_requisito_id)
SELECT d.id, p.id FROM disciplinas d, disciplinas p
WHERE d.codigo = '4162' AND p.codigo = '14709';
 
-- Fundamentos Matemáticos II (14737) exige Fundamentos Matemáticos I (14708)
INSERT OR IGNORE INTO pre_requisitos (disciplina_id, pre_requisito_id)
SELECT d.id, p.id FROM disciplinas d, disciplinas p
WHERE d.codigo = '14737' AND p.codigo = '14708';
 
-- Fundamentos de Problemas Computacionais I (14736) exige Princípios de Programação (14709)
INSERT OR IGNORE INTO pre_requisitos (disciplina_id, pre_requisito_id)
SELECT d.id, p.id FROM disciplinas d, disciplinas p
WHERE d.codigo = '14736' AND p.codigo = '14709';
 
-- Elementos de Sistemas Computacionais (14735) exige Princípios de Programação (14709)
INSERT OR IGNORE INTO pre_requisitos (disciplina_id, pre_requisito_id)
SELECT d.id, p.id FROM disciplinas d, disciplinas p
WHERE d.codigo = '14735' AND p.codigo = '14709';
 
-- ── PERÍODO 3 ────────────────────────────────────────────────────────────────
 
-- Engenharia para SI I (14340) exige Fund. Problemas Computacionais I (14736)
INSERT OR IGNORE INTO pre_requisitos (disciplina_id, pre_requisito_id)
SELECT d.id, p.id FROM disciplinas d, disciplinas p
WHERE d.codigo = '14340' AND p.codigo = '14736';
 
-- Introdução ao Armazenamento e Análise de Dados (14341) exige Fund. Matemáticos II (14737)
INSERT OR IGNORE INTO pre_requisitos (disciplina_id, pre_requisito_id)
SELECT d.id, p.id FROM disciplinas d, disciplinas p
WHERE d.codigo = '14341' AND p.codigo = '14737';
 
-- Desenvolvimento de SI (14379) exige Elementos de Sist. Computacionais (14735)
INSERT OR IGNORE INTO pre_requisitos (disciplina_id, pre_requisito_id)
SELECT d.id, p.id FROM disciplinas d, disciplinas p
WHERE d.codigo = '14379' AND p.codigo = '14735';
 
-- ── PERÍODO 4 ────────────────────────────────────────────────────────────────
 
-- Fundamentos de Problemas Computacionais II (14343) exige Fundamentos de Problemas Computacionais I (14736)
INSERT OR IGNORE INTO pre_requisitos (disciplina_id, pre_requisito_id)
SELECT d.id, p.id FROM disciplinas d, disciplinas p
WHERE d.codigo = '14343' AND p.codigo = '14736';
 
-- Princípios de Software Básico (14344) exige Engenharia para SI I (14340)
INSERT OR IGNORE INTO pre_requisitos (disciplina_id, pre_requisito_id)
SELECT d.id, p.id FROM disciplinas d, disciplinas p
WHERE d.codigo = '14344' AND p.codigo = '14340';
 
-- Sistemas de Informação na Internet (14345) exige Desenvolvimento de SI (14379)
INSERT OR IGNORE INTO pre_requisitos (disciplina_id, pre_requisito_id)
SELECT d.id, p.id FROM disciplinas d, disciplinas p
WHERE d.codigo = '14345' AND p.codigo = '14379';
 
-- ── PERÍODO 5 ────────────────────────────────────────────────────────────────
 
-- Engenharia para SI II (14347) exige Princípios de Software Básico (14344)
INSERT OR IGNORE INTO pre_requisitos (disciplina_id, pre_requisito_id)
SELECT d.id, p.id FROM disciplinas d, disciplinas p
WHERE d.codigo = '14347' AND p.codigo = '14344';
 
-- Segurança e Auditoria (06299) exige Sistemas de Informação na Internet (14345)
INSERT OR IGNORE INTO pre_requisitos (disciplina_id, pre_requisito_id)
SELECT d.id, p.id FROM disciplinas d, disciplinas p
WHERE d.codigo = '06299' AND p.codigo = '14345';
 
-- ── PERÍODO 6 ────────────────────────────────────────────────────────────────
 
-- Engenharia para SI III (14352) exige Engenharia para SI II (14347)
INSERT OR IGNORE INTO pre_requisitos (disciplina_id, pre_requisito_id)
SELECT d.id, p.id FROM disciplinas d, disciplinas p
WHERE d.codigo = '14352' AND p.codigo = '14347';
 
-- Modelagem de Dados (14351) exige Introdução ao Armazenamento e Análise de Dados (14341)
INSERT OR IGNORE INTO pre_requisitos (disciplina_id, pre_requisito_id)
SELECT d.id, p.id FROM disciplinas d, disciplinas p
WHERE d.codigo = '14351' AND p.codigo = '14341';
 
-- ── PERÍODO 7 ────────────────────────────────────────────────────────────────
 
-- Estatística Aplicada (14353) exige Cálculo N1 (6507)
INSERT OR IGNORE INTO pre_requisitos (disciplina_id, pre_requisito_id)
SELECT d.id, p.id FROM disciplinas d, disciplinas p
WHERE d.codigo = '14353' AND p.codigo = '6507';
 
-- Paradigmas de Programação (14354) exige Fundamentos de Problemas Computacionais II (14343)
INSERT OR IGNORE INTO pre_requisitos (disciplina_id, pre_requisito_id)
SELECT d.id, p.id FROM disciplinas d, disciplinas p
WHERE d.codigo = '14354' AND p.codigo = '14343';
 
-- Sistemas de Apoio à Decisão (14355) exige Modelagem de Dados (14351)
INSERT OR IGNORE INTO pre_requisitos (disciplina_id, pre_requisito_id)
SELECT d.id, p.id FROM disciplinas d, disciplinas p
WHERE d.codigo = '14355' AND p.codigo = '14351';
 
-- Princípios da Teoria da Computação (14361) exige Fundamentos Matemáticos II (14737)
INSERT OR IGNORE INTO pre_requisitos (disciplina_id, pre_requisito_id)
SELECT d.id, p.id FROM disciplinas d, disciplinas p
WHERE d.codigo = '14361' AND p.codigo = '14737';
 
-- ── PERÍODO 8 ────────────────────────────────────────────────────────────────
 
-- Infraestrutura de Software (14357) exige Segurança e Auditoria (06299)
INSERT OR IGNORE INTO pre_requisitos (disciplina_id, pre_requisito_id)
SELECT d.id, p.id FROM disciplinas d, disciplinas p
WHERE d.codigo = '14357' AND p.codigo = '06299';
 
-- Projeto de Soluções Complexas II (14356) exige Engenharia para SI III (14352)
INSERT OR IGNORE INTO pre_requisitos (disciplina_id, pre_requisito_id)
SELECT d.id, p.id FROM disciplinas d, disciplinas p
WHERE d.codigo = '14356' AND p.codigo = '14352';
 
-- ── PERÍODO 9 ────────────────────────────────────────────────────────────────
 
-- TCC (14308) exige Projeto de Soluções Complexas II (14356)
INSERT OR IGNORE INTO pre_requisitos (disciplina_id, pre_requisito_id)
SELECT d.id, p.id FROM disciplinas d, disciplinas p
WHERE d.codigo = '14308' AND p.codigo = '14356';
 
-- ── OPTATIVAS (exemplos) ──────────────────────────────────────────────────────
 
-- Fundamentos de Criptografia (14705) recomenda Segurança e Auditoria (06299)
INSERT OR IGNORE INTO pre_requisitos (disciplina_id, pre_requisito_id)
SELECT d.id, p.id FROM disciplinas d, disciplinas p
WHERE d.codigo = '14705' AND p.codigo = '06299';
 
-- Tópicos Avançados em IA (14024) recomenda Estatística Aplicada (14353)
INSERT OR IGNORE INTO pre_requisitos (disciplina_id, pre_requisito_id)
SELECT d.id, p.id FROM disciplinas d, disciplinas p
WHERE d.codigo = '14024' AND p.codigo = '14353';
 
-- Processamento de Imagens (14051) recomenda Tópicos Avançados em IA (14024)
INSERT OR IGNORE INTO pre_requisitos (disciplina_id, pre_requisito_id)
SELECT d.id, p.id FROM disciplinas d, disciplinas p
WHERE d.codigo = '14051' AND p.codigo = '14024';
 

 