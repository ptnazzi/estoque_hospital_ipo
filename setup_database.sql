-- =====================================================
-- SISTEMA STOKE - CONFIGURAÇÃO COMPLETA DO BANCO DE DADOS
-- =====================================================
-- Execute este script no pgAdmin4 como superusuário (postgres)
-- Este script cria todas as tabelas necessárias para o sistema

-- 1. Criar tabela de usuários (se não existir)
CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    nome_completo VARCHAR(100) NOT NULL,
    tipo VARCHAR(20) NOT NULL DEFAULT 'user' CHECK (tipo IN ('user', 'admin')),
    ativo BOOLEAN NOT NULL DEFAULT true,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ultimo_login TIMESTAMP
);

-- 2. Criar tabela de logs de acesso
CREATE TABLE IF NOT EXISTS logs_acesso (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER,
    username VARCHAR(50),
    nome_completo VARCHAR(100),
    tipo_acesso VARCHAR(20),
    data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(45)
);

-- 3. Criar tabela de histórico de exclusões
CREATE TABLE IF NOT EXISTS historico_exclusoes (
    id SERIAL PRIMARY KEY,
    produto_id INTEGER,
    nome_produto VARCHAR(100),
    quantidade INTEGER,
    descricao TEXT,
    status VARCHAR(50),
    usuario_id INTEGER,
    username VARCHAR(50),
    nome_completo VARCHAR(100),
    data_exclusao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Conceder permissões para estoque_ti
GRANT ALL PRIVILEGES ON TABLE usuarios TO estoque_ti;
GRANT ALL PRIVILEGES ON TABLE logs_acesso TO estoque_ti;
GRANT ALL PRIVILEGES ON TABLE historico_exclusoes TO estoque_ti;
GRANT USAGE, SELECT ON SEQUENCE usuarios_id_seq TO estoque_ti;
GRANT USAGE, SELECT ON SEQUENCE logs_acesso_id_seq TO estoque_ti;
GRANT USAGE, SELECT ON SEQUENCE historico_exclusoes_id_seq TO estoque_ti;
-- 4. Criar tabela de histórico de edições
CREATE TABLE IF NOT EXISTS historico_edicoes (
    id SERIAL PRIMARY KEY,
    produto_id INTEGER,
    nome_antigo VARCHAR(100),
    quantidade_antiga INTEGER,
    descricao_antiga TEXT,
    status_antigo VARCHAR(50),
    nome_novo VARCHAR(100),
    quantidade_nova INTEGER,
    descricao_nova TEXT,
    status_novo VARCHAR(50),
    usuario_id INTEGER,
    username VARCHAR(50),
    nome_completo VARCHAR(100),
    data_edicao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

GRANT ALL PRIVILEGES ON TABLE historico_edicoes TO estoque_ti;
GRANT USAGE, SELECT ON SEQUENCE historico_edicoes_id_seq TO estoque_ti;


-- 5. Inserir usuários padrão (se não existirem)
INSERT INTO usuarios (username, password, nome_completo, tipo, ativo) 
VALUES ('admin', 'admin123', 'Administrador do Sistema', 'admin', true)
ON CONFLICT (username) DO NOTHING;

INSERT INTO usuarios (username, password, nome_completo, tipo, ativo) 
VALUES ('usuario', 'user123', 'Usuário Padrão', 'user', true)
ON CONFLICT (username) DO NOTHING;

-- 6. Inserir dados de teste para logs
INSERT INTO logs_acesso (usuario_id, username, nome_completo, tipo_acesso, ip_address)
VALUES 
(1, 'admin', 'Administrador do Sistema', 'login', '127.0.0.1'),
(2, 'usuario', 'Usuário Padrão', 'login', '127.0.0.1'),
(1, 'admin', 'Administrador do Sistema', 'logout', '127.0.0.1')
ON CONFLICT DO NOTHING;

-- 7. Inserir dados de teste para histórico
INSERT INTO historico_exclusoes (produto_id, nome_produto, quantidade, descricao, status, usuario_id, username, nome_completo)
VALUES 
(1, 'Mouse Logitech', 5, 'Mouse sem fio', 'Disponível', 1, 'admin', 'Administrador do Sistema'),
(2, 'Teclado Microsoft', 3, 'Teclado ergonômico', 'Em uso', 2, 'usuario', 'Usuário Padrão')
ON CONFLICT DO NOTHING;

-- 8. Verificar se tudo foi criado corretamente
SELECT '=== TABELAS CRIADAS ===' as status;
SELECT table_name FROM information_schema.tables WHERE table_name IN ('usuarios', 'logs_acesso', 'historico_exclusoes');

SELECT '=== USUÁRIOS CADASTRADOS ===' as status;
SELECT id, username, nome_completo, tipo, ativo FROM usuarios;

SELECT '=== LOGS DE ACESSO ===' as status;
SELECT id, username, tipo_acesso, data_hora FROM logs_acesso;

SELECT '=== HISTÓRICO DE EXCLUSÕES ===' as status;
SELECT id, nome_produto, username, data_exclusao FROM historico_exclusoes; 