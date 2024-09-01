-- -------------------------------------------
-- Inserção de Dados nas Tabelas
-- -------------------------------------------

-- -------------------------------------------
-- Inserir dados na tabela de Estações
-- -------------------------------------------
INSERT INTO estacoes (localizacao, nome, descricao, cep, iframe_mapa, fotos, contatos)
VALUES 
    ('Rua da União (em frente à loja A Renovar), S/N, bairro Sol e Mar', 
     'Estação Tech Sol e Mar', 
     'Estação localizada na União de Moradores do Sol e Mar, voltada para cursos de Robótica e Informática Básica.', 
     '65066-620', 
     '<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3986.056637903178!2d-44.217878625031354!3d-2.488205597490451!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x7f69251fb2ba65f%3A0x27fed2dc2597697b!2sUni%C3%A3o%20de%20Moradores%20do%20Sol%20e%20Mar!5e0!3m2!1spt-PT!2sbr!4v1725156514901!5m2!1spt-PT!2sbr" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>', 
    
    
     'https://streetviewpixels-pa.googleapis.com/v1/thumbnail?panoid=AT605Dsyf-8d7dhqG3jpPg&cb_client=search.gws-prod.gps&w=408&h=240&yaw=285.48596&pitch=0&thumbfov=100', 
     'contato@techsolmar.com, 
      98 99999999'),



-- -------------------------------------------
-- Inserir dados na tabela de Cursos
-- -------------------------------------------
INSERT INTO cursos (nome, descricao, carga_horaria)
VALUES 
    ('Curso de Robótica e Informática Básica', 
     'Curso presencial de Robótica e Informática Básica, realizado entre 26 e 28 de agosto, e online de 2 a 6 de setembro. Aulas das 8h às 12h e das 14h às 18h.', 
     24),

    
-- -------------------------------------------
-- Inserir dados na tabela de Estações-Cursos
-- -------------------------------------------
INSERT INTO estacoes_cursos (estacao_id, curso_id)
VALUES 
    (1, 1),  -- Associa a Estação Tech Sol e Mar ao Curso de Robótica e Informática Básica
  
