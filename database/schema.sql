CREATE TABLE disciplinas (
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

CREATE INDEX idx_disciplinas_periodo ON disciplinas(periodo);
-- =========================
-- 1º PERÍODO
-- =========================
INSERT INTO disciplinas (codigo, nome, periodo, carga_horaria) VALUES
('14734', 'Sustentabilidade em Sistemas de Informação', 1, 60);
('14708', 'Fundamentos Matemáticos para Sistemas de Informação I', 1, 60);
('14733', 'Projeto Interdisciplinar para Sistemas de Informação I', 1, 60);
('14709', 'Princípios de Programação', 1, 60);
('4109', 'Introdução à Administração', 1, 60);

-- =========================
-- 2º PERÍODO
-- =========================
INSERT INTO disciplinas (codigo, nome, periodo, carga_horaria) VALUES
('4162', 'Fundamentos de Sistemas de Informação II', 2, 60);
('14378', 'Projeto Interdisciplinar de Sistemas de Informação II', 2, 60);
('14737', 'Fundamentos Matemáticos para Sistemas de Informação II', 2, 60);
('14735', 'Elementos de Sistemas Computacionais', 2, 60);
('14736', 'Fundamentos de Problemas Computacionais I', 2, 60);

-- =========================
-- 3º PERÍODO
-- =========================
INSERT INTO disciplinas (codigo, nome, periodo, carga_horaria) VALUES
('14340', 'Engenharia para Sistemas de Informação I', 3, 60);
('14341', ' Introdução ao Armazenamento e Análise de Dados', 3, 60);
('14342', 'Projeto Interdisciplinar para Sistemas de Informação III', 3, 60);
('14379', 'Desenvolvimento de Sistemas de Informação', 3, 60);

-- =========================
-- 4º PERÍODO
-- =========================
INSERT INTO disciplinas (codigo, nome, periodo, carga_horaria) VALUES
('14344', 'Princípios de Software Básico', 4, 60);
('14346', 'Projeto Interdisciplinar de Sistemas de Informação IV', 4, 60);
('14343', 'Fundamentos de Problemas Computacionais II', 4, 60);
('14345', 'Sistemas de Informação na Internet', 4, 60);

-- =========================
-- 5º PERÍODO
-- =========================
INSERT INTO disciplinas (codigo, nome, periodo, carga_horaria) VALUES
('14347', 'Engenharia para Sistemas de Informação II', 5, 60);
('14348', 'Projeto de Desenvolvimento Tecnológico para o Mundo I', 5, 60);
('06299', 'Segurança e Auditoria de Sistemas', 5, 60);
('4249', 'Empreendedorismo e Inovação', 5, 60);


-- =========================
-- 6º PERÍODO
-- =========================
INSERT INTO disciplinas (codigo, nome, periodo, carga_horaria) VALUES
('14352', 'Engenharia para Sistemas de Informação III', 6, 60);
('14351 ', 'Modelagem de Dados', 6, 60);
('14350', 'Projeto de Desenvolvimento Tecnológico para o Mundo II', 6, 60);
('6507', 'Cálculo N1', 6, 60);

-- =========================
-- 7º PERÍODO
-- =========================
INSERT INTO disciplinas (codigo, nome, periodo, carga_horaria) VALUES
('14353', 'Estatística Aplicada à Análise de Dados', 7, 60);
('14354', 'Paradigmas de Programação', 7, 60);
('14355', 'Sistemas de Apoio à Decisão', 7, 60);
('14361', 'Princípios da Teoria da Computação', 7, 60);

-- =========================
-- 8º PERÍODO
-- =========================
INSERT INTO disciplinas (codigo, nome, periodo, carga_horaria) VALUES
('4203', 'Fundamentos de Estratégia Competitiva', 8, 60);
('14356', 'Projeto de Soluções Complexas II', 8, 60);
('14357', 'Infraestrutura de Software', 8, 60);
('4231', 'Gestão do Conhecimento', 8, 60);

-- =========================
-- 9º PERÍODO
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
('14024', 'Tópicos Avançados em Inteligência Artificial', 60);
