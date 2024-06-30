CREATE DATABASE store;

\c store

CREATE TYPE periodo AS ENUM ('Matutino', 'Vespertino', 'Noturno');

CREATE TABLE IF NOT EXISTS vendedores(
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    senha VARCHAR(255) NOT NULL,
    turno periodo NOT NULL,
    token varchar(255) NULL,
    salt VARCHAR(255) NULL
);

CREATE TABLE IF NOT EXISTS clientes(
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    senha VARCHAR(255) NOT NULL,
    contato VARCHAR(255) NOT NULL,
    token VARCHAR(255) NULL,
    salt VARCHAR(255) NULL
);

CREATE TABLE IF NOT EXISTS instrumentos(
    id SERIAL PRIMARY KEY,
    tipo VARCHAR(255) NOT NULL,
    modelo VARCHAR(255) NOT NULL,
    preco DECIMAL(7,2),
    quantidade INT4
);

CREATE TABLE IF NOT EXISTS vendas(
    id SERIAL PRIMARY KEY,
    data_venda DATE NOT NULL,
    id_vendedor SMALLINT NOT NULL,
    id_cliente SMALLINT NOT NULL,
    id_instrumento SMALLINT NOT NULL,
    quantidade INT4 NOT NULL,
    CONSTRAINT vendedor_fkey FOREIGN KEY (id_vendedor) REFERENCES vendedores(id),
    CONSTRAINT cliente_fkey FOREIGN KEY (id_cliente) REFERENCES clientes(id),
    CONSTRAINT instrumento_fkey FOREIGN KEY (id_instrumento) REFERENCES instrumentos(id)
);

-- Função para o endpoint filtrar vendas

CREATE OR REPLACE FUNCTION filtrar_vendas(entidade VARCHAR, valor VARCHAR)
 RETURNS TABLE(id INTEGER, data_venda DATE, vendedor VARCHAR, tipo_instrumento VARCHAR, modelo_instrumento VARCHAR, cliente VARCHAR, preco_instrumento NUMERIC, quantidade INTEGER)
 LANGUAGE plpgsql
AS $function$
DECLARE
	campo VARCHAR;
BEGIN
	
	IF entidade = 'vendedor' THEN
    -- Verifica se o valor pode ser convertido para um número inteiro, se sim, o campo recebe o id, fazendo a busca pelo id, se for VARCHAR, o campo recebe nome, fazendo a busca pelo nome
    BEGIN
        PERFORM valor::INT;
        campo := 'v.id';
    EXCEPTION WHEN others THEN
        campo := 'v.nome';
    END;

	ELSIF entidade = 'instrumento' THEN
    	campo := 'i.tipo';

    -- Verifica se o valor pode ser convertido para um número
	ELSIF entidade = 'cliente' THEN
    BEGIN
        PERFORM valor::INT;
        campo:= 'c.id';
    EXCEPTION WHEN others THEN
    	campo := 'c.nome';
    END;

    ELSIF entidade = 'data' then
    	campo := 'vd.data_venda';

	ELSE
    	RAISE EXCEPTION 'Entidade inválida: %', entidade;
	END IF;

	
    RETURN QUERY EXECUTE format('
        SELECT
			vd.id,
            vd.data_venda,
            v.nome AS vendedores,
            i.tipo AS tipo_instrumento,
            i.modelo AS modelo_instrumento,
            c.nome AS cliente,
            i.preco AS preco_instrumento,
			vd.quantidade
        FROM
            vendas vd
            JOIN vendedores v ON vd.id_vendedor = v.id
            JOIN instrumentos i ON vd.id_instrumento = i.id
            JOIN clientes c ON vd.id_cliente = c.id
        WHERE %s = %L
        ORDER BY
            vd.data_venda DESC', campo, valor);
END;
$function$
;

-- Função com um TRIGGER para quando for realizado uma venda, dependendo da quantidade que for passada, automaticamente na tabela intrumento o campo quantidade é modificado

CREATE OR REPLACE FUNCTION venda_instrumento()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
	declare
		qnt_atual INTEGER default 0;
	begin
		select quantidade into qnt_atual from instrumentos where id = new.id_instrumento;
		
		IF qnt_atual < 1 THEN
			raise exception 'Falta desse instrumento no estoque!';
		
		ELSIF qnt_atual < new.quantidade THEN
			raise exception 'Não possuimos essa quantidade no estoque!';
		
		ELSE
			update instrumentos set quantidade = (qnt_atual - new.quantidade) where id = new.id_instrumento;

			return new;
		END IF;

	END;
	
$function$
;

-- TRIGGER para realizar antes de um insert em venda, executando a função a cima, verificando se possui o intrumento no estoque

CREATE TRIGGER venda_instrumento_qnt
    BEFORE INSERT ON vendas 
    FOR EACH ROW EXECUTE FUNCTION venda_instrumento()