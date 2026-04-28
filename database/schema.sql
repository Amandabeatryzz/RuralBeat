CREATE TABLE disciplinas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT UNIQUE NOT NULL,
    nome TEXT NOT NULL,
    periodo INTEGER NOT NULL CHECK (periodo BETWEEN 1 AND 10),
    carga_horaria INTEGER NOT NULL,
    obrigatoria INTEGER NOT NULL DEFAULT 1
);

CREATE INDEX idx_disciplinas_periodo ON disciplinas(periodo);
-- =========================
-- 1º PERÍODO
-- =========================
INSERT INTO disciplinas (codigo, nome, periodo, carga_horaria) VALUES
('06438', 'Cálculo a Uma Variável', 1, 60),
('06236', 'Introdução à Programação', 1, 90),
('06274', 'Laboratório de Informática', 1, 30),
('06203', 'Matemática Discreta', 1, 60),
('04166', 'Teoria Geral da Administração', 1, 60);

-- =========================
-- 2º PERÍODO
-- =========================
INSERT INTO disciplinas (codigo, nome, periodo, carga_horaria) VALUES
('06214', 'Algoritmos e Estruturas de Dados', 2, 60),
('06439', 'Cálculo a Várias Variáveis', 2, 60),
('04162', 'Fundamentos de Sistemas de Informação', 2, 60),
('06239', 'Introdução à Teoria da Computação', 2, 60),
('06283', 'Laboratório de Programação', 2, 60);

-- =========================
-- 3º PERÍODO
-- =========================
INSERT INTO disciplinas (codigo, nome, periodo, carga_horaria) VALUES
('06287', 'Fundamentos de Engenharia de Software', 3, 60),
('06309', 'Física para Computação', 3, 60),
('04106', 'Introdução à Economia', 3, 60),
('06286', 'Modelagem e Programação Orientada a Objetos', 3, 60),
('06418', 'Álgebra Vetorial e Linear para Computação', 3, 60);

-- =========================
-- 4º PERÍODO
-- =========================
INSERT INTO disciplinas (codigo, nome, periodo, carga_horaria) VALUES
('04163', 'Administração Financeira', 4, 60),
('06243', 'Estatística Exploratória I', 4, 60),
('06288', 'Fundamentos de Banco de Dados', 4, 60),
('06289', 'Processo de Desenvolvimento de Software', 4, 60),
('05345', 'Psicologia Aplicada às Organizações', 4, 60);

-- =========================
-- 5º PERÍODO
-- =========================
INSERT INTO disciplinas (codigo, nome, periodo, carga_horaria) VALUES
('14310', 'Análise e Projeto de Sistemas de Informação', 5, 60),
('06296', 'Gerência de Projetos de Software', 5, 60),
('06246', 'Infraestrutura de Hardware', 5, 60),
('06295', 'Metodologia de Expressão Técnica e Científica', 5, 60),
('06297', 'Projeto de Banco de Dados', 5, 60);

-- =========================
-- 6º PERÍODO
-- =========================
INSERT INTO disciplinas (codigo, nome, periodo, carga_horaria) VALUES
('04195', 'Empreendedorismo e Legislação', 6, 60),
('06298', 'Projeto de Sistemas Distribuídos', 6, 60),
('06249', 'Redes e Sistemas Internet', 6, 60);

-- =========================
-- 7º PERÍODO
-- =========================
INSERT INTO disciplinas (codigo, nome, periodo, carga_horaria) VALUES
('06253', 'Interfaces Homem-Máquina', 7, 60),
('06252', 'Paradigmas de Programação', 7, 60),
('04236', 'Sistemas de Apoio à Decisão', 7, 60);

-- =========================
-- 8º PERÍODO
-- =========================
INSERT INTO disciplinas (codigo, nome, periodo, carga_horaria) VALUES
('04202', 'Análise Organizacional de Processos', 8, 60),
('06258', 'Aspectos Filosóficos e Sociológicos da Informática', 8, 60),
('06259', 'Infraestrutura de Software', 8, 60);

-- =========================
-- 9º PERÍODO
-- =========================
INSERT INTO disciplinas (codigo, nome, periodo, carga_horaria) VALUES
('04203', 'Fundamentos de Estratégia Competitiva', 9, 60),
('06299', 'Segurança e Auditoria de Sistemas de Informação', 9, 60);

-- =========================
-- 10º PERÍODO
-- =========================
INSERT INTO disciplinas (codigo, nome, periodo, carga_horaria) VALUES
('04208', 'Educação Física A', 10, 30),
('14308', 'Projeto de Conclusão - Sistemas de Informação', 10, 420);