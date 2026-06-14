CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    codigo TEXT UNIQUE NOT NULL,
    nome TEXT NOT NULL,
    periodo INTEGER NOT NULL CHECK (periodo BETWEEN 1 AND 10),
    carga_horaria INTEGER NOT NULL,
    obrigatoria INTEGER NOT NULL DEFAULT 1);

CREATE TABLE optativas (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 codigo TEXT UNIQUE NOT NULL,
 nome TEXT NOT NULL,
 carga_horaria INTEGER NOT NULL,
);

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    nome TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    senha TEXT NOT NULL,
    nivel INTEGER DEFAULT 1);
=======
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
    FOREIGN KEY (disciplina_id) REFERENCES disciplinas(id) ON DELETE CASCADE
);

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
>>>>>>> b43bd1e25c0af18779ccb959c9d83cf57dca3a90

-- 1º PERÍODO

-- =========================
INSERT INTO disciplinas (codigo, nome, periodo, carga_horaria) VALUES
('14734', 'Sustentabilidade em Sistemas de Informação', 1, 60);
('14708', 'Fundamentos Matemáticos para Sistemas de Informação I', 1, 60);
('14733', 'Projeto Interdisciplinar para Sistemas de Informação I', 1, 60);
('14709', 'Princípios de Programação', 1, 60);
('4109', 'Introdução à Administração', 1, 60);
=======
INSERT OR IGNORE INTO disciplinas (codigo, nome, periodo, carga_horaria, obrigatoria) VALUES
('14734', 'Sustentabilidade em Sistemas de Informação', 1, 60, 1),
('14708', 'Fundamentos Matemáticos para Sistemas de Informação I', 1, 60, 1),
('14733', 'Projeto Interdisciplinar para Sistemas de Informação I', 1, 60, 1),
('14709', 'Princípios de Programação', 1, 60, 1),
('4109', 'Introdução à Administração', 1, 60, 1);
>>>>>>> b43bd1e25c0af18779ccb959c9d83cf57dca3a90

-- 2º PERÍODO
<<<<<<< HEAD
-- =========================
INSERT INTO disciplinas (codigo, nome, periodo, carga_horaria) VALUES
('4162', 'Fundamentos de Sistemas de Informação II', 2, 60);
('14378', 'Projeto Interdisciplinar de Sistemas de Informação II', 2, 60);
('14737', 'Fundamentos Matemáticos para Sistemas de Informação II', 2, 60);
('14735', 'Elementos de Sistemas Computacionais', 2, 60);
('14736', 'Fundamentos de Problemas Computacionais I', 2, 60);
=======
INSERT OR IGNORE INTO disciplinas (codigo, nome, periodo, carga_horaria, obrigatoria) VALUES
('4162', 'Fundamentos de Sistemas de Informação II', 2, 60, 1),
('14378', 'Projeto Interdisciplinar de Sistemas de Informação II', 2, 60, 1),
('14737', 'Fundamentos Matemáticos para Sistemas de Informação II', 2, 60, 1),
('14735', 'Elementos de Sistemas Computacionais', 2, 60, 1),
('14736', 'Fundamentos de Problemas Computacionais I', 2, 60, 1);
>>>>>>> b43bd1e25c0af18779ccb959c9d83cf57dca3a90

-- 3º PERÍODO
<<<<<<< HEAD
-- =========================
INSERT INTO disciplinas (codigo, nome, periodo, carga_horaria) VALUES
('14340', 'Engenharia para Sistemas de Informação I', 3, 60);
('14341', ' Introdução ao Armazenamento e Análise de Dados', 3, 60);
('14342', 'Projeto Interdisciplinar para Sistemas de Informação III', 3, 60);
('14379', 'Desenvolvimento de Sistemas de Informação', 3, 60);
=======
INSERT OR IGNORE INTO disciplinas (codigo, nome, periodo, carga_horaria, obrigatoria) VALUES
('14340', 'Engenharia para Sistemas de Informação I', 3, 60, 1),
('14341', 'Introdução ao Armazenamento e Análise de Dados', 3, 60, 1),
('14342', 'Projeto Interdisciplinar para Sistemas de Informação III', 3, 60, 1),
('14379', 'Desenvolvimento de Sistemas de Informação', 3, 60, 1);
>>>>>>> b43bd1e25c0af18779ccb959c9d83cf57dca3a90

-- 4º PERÍODO
<<<<<<< HEAD
-- =========================
INSERT INTO disciplinas (codigo, nome, periodo, carga_horaria) VALUES
('14344', 'Princípios de Software Básico', 4, 60);
('14346', 'Projeto Interdisciplinar de Sistemas de Informação IV', 4, 60);
('14343', 'Fundamentos de Problemas Computacionais II', 4, 60);
('14345', 'Sistemas de Informação na Internet', 4, 60);
=======
INSERT OR IGNORE INTO disciplinas (codigo, nome, periodo, carga_horaria, obrigatoria) VALUES
('14344', 'Princípios de Software Básico', 4, 60, 1),
('14346', 'Projeto Interdisciplinar de Sistemas de Informação IV', 4, 60, 1),
('14343', 'Fundamentos de Problemas Computacionais II', 4, 60, 1),
('14345', 'Sistemas de Informação na Internet', 4, 60, 1);
>>>>>>> b43bd1e25c0af18779ccb959c9d83cf57dca3a90

-- 5º PERÍODO
<<<<<<< HEAD
-- =========================
INSERT INTO disciplinas (codigo, nome, periodo, carga_horaria) VALUES
('14347', 'Engenharia para Sistemas de Informação II', 5, 60);
('14348', 'Projeto de Desenvolvimento Tecnológico para o Mundo I', 5, 60);
('06299', 'Segurança e Auditoria de Sistemas', 5, 60);
('4249', 'Empreendedorismo e Inovação', 5, 60);

=======
INSERT OR IGNORE INTO disciplinas (codigo, nome, periodo, carga_horaria, obrigatoria) VALUES
('14347', 'Engenharia para Sistemas de Informação II', 5, 60, 1),
('14348', 'Projeto de Desenvolvimento Tecnológico para o Mundo I', 5, 60, 1),
('06299', 'Segurança e Auditoria de Sistemas', 5, 60, 1),
('4249', 'Empreendedorismo e Inovação', 5, 60, 1);
>>>>>>> b43bd1e25c0af18779ccb959c9d83cf57dca3a90

-- 6º PERÍODO
<<<<<<< HEAD
-- =========================
INSERT INTO disciplinas (codigo, nome, periodo, carga_horaria) VALUES
('14352', 'Engenharia para Sistemas de Informação III', 6, 60);
('14351 ', 'Modelagem de Dados', 6, 60);
('14350', 'Projeto de Desenvolvimento Tecnológico para o Mundo II', 6, 60);
('6507', 'Cálculo N1', 6, 60);
=======
INSERT OR IGNORE INTO disciplinas (codigo, nome, periodo, carga_horaria, obrigatoria) VALUES
('14352', 'Engenharia para Sistemas de Informação III', 6, 60, 1),
('14351', 'Modelagem de Dados', 6, 60, 1),
('14350', 'Projeto de Desenvolvimento Tecnológico para o Mundo II', 6, 60, 1),
('6507', 'Cálculo N1', 6, 60, 1);
>>>>>>> b43bd1e25c0af18779ccb959c9d83cf57dca3a90

-- 7º PERÍODO
<<<<<<< HEAD
-- =========================
INSERT INTO disciplinas (codigo, nome, periodo, carga_horaria) VALUES
('14353', 'Estatística Aplicada à Análise de Dados', 7, 60);
('14354', 'Paradigmas de Programação', 7, 60);
('14355', 'Sistemas de Apoio à Decisão', 7, 60);
('14361', 'Princípios da Teoria da Computação', 7, 60);
=======
INSERT OR IGNORE INTO disciplinas (codigo, nome, periodo, carga_horaria, obrigatoria) VALUES
('14353', 'Estatística Aplicada à Análise de Dados', 7, 60, 1),
('14354', 'Paradigmas de Programação', 7, 60, 1),
('14355', 'Sistemas de Apoio à Decisão', 7, 60, 1),
('14361', 'Princípios da Teoria da Computação', 7, 60, 1);
>>>>>>> b43bd1e25c0af18779ccb959c9d83cf57dca3a90

-- 8º PERÍODO
<<<<<<< HEAD
-- =========================
INSERT INTO disciplinas (codigo, nome, periodo, carga_horaria) VALUES
('4203', 'Fundamentos de Estratégia Competitiva', 8, 60);
('14356', 'Projeto de Soluções Complexas II', 8, 60);
('14357', 'Infraestrutura de Software', 8, 60);
('4231', 'Gestão do Conhecimento', 8, 60);
=======
INSERT OR IGNORE INTO disciplinas (codigo, nome, periodo, carga_horaria, obrigatoria) VALUES
('4203', 'Fundamentos de Estratégia Competitiva', 8, 60, 1),
('14356', 'Projeto de Soluções Complexas II', 8, 60, 1),
('14357', 'Infraestrutura de Software', 8, 60, 1),
('4231', 'Gestão do Conhecimento', 8, 60, 1);
>>>>>>> b43bd1e25c0af18779ccb959c9d83cf57dca3a90

-- 9º PERÍODO
<<<<<<< HEAD
-- =========================
INSERT INTO disciplinas (codigo, nome, periodo, carga_horaria) VALUES
('14308', 'Projeto de Conclusão - Sistemas de Informação', 9, 420);

-- =========================
-- OPTATIVAS
-- =========================
INSERT INTO optativas (codigo, nome, carga_horaria) VALUES
('04208', 'Educação Física', 60);
('6277', 'Tópicos em Otimização', 60);
('14705', 'Fundamentos de Criptografia', 60);
('14051', 'Processamento de Imagens', 60);
('14028', ' Fundamentos de Autômatos Celulares', 60);
('06280', 'Modelagem Matemático-Computacional Aplicada à Epidemiologia', 60);
('14011', 'Tópicos Avançados em Redes de Computadores I', 60);
('14703', 'Tendências Tecnológicas em TIC', 60);
('14328', 'Inovação em TIC', 60);
('14024', 'Tópicos Avançados em Inteligência Artificial', 60);.
=======
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
>>>>>>> b43bd1e25c0af18779ccb959c9d83cf57dca3a90
