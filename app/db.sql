-- Tabela de Estações
CREATE TABLE estacoes (
    id SERIAL PRIMARY KEY,  -- Identificador único da estação
    localizacao TEXT NOT NULL,  -- Localização da estação
    nome VARCHAR(100) NOT NULL,  -- Nome da estação
    descricao TEXT,  -- Descrição opcional da estação
    cep VARCHAR(10) NOT NULL,  -- Código Postal (CEP)
    iframe_mapa TEXT,  -- URL do iframe do mapa para a estação
    fotos VARCHAR(255),  -- URL da imagem associada à estação
    contatos TEXT,  -- Informações de contato adicionais
    CONSTRAINT nome_unico_localizacao UNIQUE (nome, localizacao),  -- Nome único dentro de uma localização
    CONSTRAINT chk_cep CHECK (cep ~ '^\d{5}-\d{3}$')  -- Validação básica do formato do CEP
);

-- Tabela de Cursos
CREATE TABLE cursos (
    id SERIAL PRIMARY KEY,  -- Identificador único do curso
    nome VARCHAR(100) NOT NULL UNIQUE,  -- Nome do curso (único)
    descricao TEXT,  -- Descrição opcional do curso
    carga_horaria INT NOT NULL CHECK (carga_horaria > 0),  -- Carga horária deve ser maior que zero
    nome_professor VARCHAR(100)  -- Nome do professor responsável (não obrigatório)
);

-- Tabela de Estações-Cursos
CREATE TABLE estacoes_cursos (
    estacao_id INT NOT NULL REFERENCES estacoes(id) ON DELETE CASCADE,  -- Referência à estação
    curso_id INT NOT NULL REFERENCES cursos(id) ON DELETE CASCADE,  -- Referência ao curso
    PRIMARY KEY (estacao_id, curso_id)  -- Chave primária composta
);
