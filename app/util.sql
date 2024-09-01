DO $$ DECLARE
    r RECORD;
BEGIN
    FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP
        EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE';
    END LOOP;
END $$;


-- Verifique se há registros existentes nas tabelas
SELECT * FROM estacoes;
SELECT * FROM cursos;
SELECT * FROM estacoes_cursos;
