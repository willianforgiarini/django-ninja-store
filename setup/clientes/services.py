from django.db import connections
from ninja.errors import HttpError
import bcrypt


def criar_clientes():
    """ Função para criar 10 clientes no banco de dados para realizar testes """
    try:
        with connections['store'].cursor() as cursor:
            # Nesse insert ja é inserido um hash e um salt, a partir da senha '1234' para realizar testes
            sql = """ INSERT INTO clientes (nome, senha, contato, salt) VALUES
                ('Ana Silva', '$2b$12$tdtRQm7t/Sy1c8ieKIMZJevv51ag4JRuErg7UIDNir1Ok2kz7Xj3u', 'ana.silva@example.com', '$2b$12$tdtRQm7t/Sy1c8ieKIMZJe'),
                ('Bruno Costa', '$2b$12$tdtRQm7t/Sy1c8ieKIMZJevv51ag4JRuErg7UIDNir1Ok2kz7Xj3u', 'bruno.costa@example.com', '$2b$12$tdtRQm7t/Sy1c8ieKIMZJe'),
                ('Carla Pereira', '$2b$12$tdtRQm7t/Sy1c8ieKIMZJevv51ag4JRuErg7UIDNir1Ok2kz7Xj3u', 'carla.pereira@example.com', '$2b$12$tdtRQm7t/Sy1c8ieKIMZJe'),
                ('Daniela Oliveira', '$2b$12$tdtRQm7t/Sy1c8ieKIMZJevv51ag4JRuErg7UIDNir1Ok2kz7Xj3u', 'daniela.oliveira@example.com', '$2b$12$tdtRQm7t/Sy1c8ieKIMZJe'),
                ('Eduardo Souza', '$2b$12$tdtRQm7t/Sy1c8ieKIMZJevv51ag4JRuErg7UIDNir1Ok2kz7Xj3u', 'eduardo.souza@example.com', '$2b$12$tdtRQm7t/Sy1c8ieKIMZJe'),
                ('Fernanda Lima', '$2b$12$tdtRQm7t/Sy1c8ieKIMZJevv51ag4JRuErg7UIDNir1Ok2kz7Xj3u', 'fernanda.lima@example.com', '$2b$12$tdtRQm7t/Sy1c8ieKIMZJe'),
                ('Gustavo Mendes', '$2b$12$tdtRQm7t/Sy1c8ieKIMZJevv51ag4JRuErg7UIDNir1Ok2kz7Xj3u', 'gustavo.mendes@example.com', '$2b$12$tdtRQm7t/Sy1c8ieKIMZJe'),
                ('Helena Barbosa', '$2b$12$tdtRQm7t/Sy1c8ieKIMZJevv51ag4JRuErg7UIDNir1Ok2kz7Xj3u', 'helena.barbosa@example.com', '$2b$12$tdtRQm7t/Sy1c8ieKIMZJe'),
                ('Igor Santos', '$2b$12$tdtRQm7t/Sy1c8ieKIMZJevv51ag4JRuErg7UIDNir1Ok2kz7Xj3u', 'igor.santos@example.com', '$2b$12$tdtRQm7t/Sy1c8ieKIMZJe'),
                ('Juliana Almeida', '$2b$12$tdtRQm7t/Sy1c8ieKIMZJevv51ag4JRuErg7UIDNir1Ok2kz7Xj3u', 'juliana.almeida@example.com', '$2b$12$tdtRQm7t/Sy1c8ieKIMZJe');
            """
            cursor.execute(sql)

            if cursor.rowcount > 0:
                return {"message": "Clientes criado com sucesso"}

    except Exception as e:
        raise e
    

def buscar_clientes():
    """ Função para buscar todos os clientes do banco de dados """
    try:
        with connections['store'].cursor() as cursor:
            sql = """ SELECT * FROM clientes; """
            cursor.execute(sql)

            clientes = []

            for row in cursor.fetchall():
                cliente = {
                    "id": row[0],
                    "nome": row[1],
                    # "senha": row[2], - linha comentada para não mostra a senha do cliente no json
                    "contato": row[3]
                }
                clientes.append(cliente)

            return clientes

    except Exception as e:
        raise e
    

def criar_cliente(nome, senha, contato):
    """ Cria um novo cliente no banco de dados """
    
    # geração de um hash com a senha para armazenar no banco de dados
    salt = bcrypt.gensalt() # gera o salt
    hash = bcrypt.hashpw(senha.encode('utf-8'), salt) # gera o hash a partir da senha fornecida e o hash gerado

    # decode no hash e no salt para virarem string para serem armanezados no banco de dados
    hash_decode = hash.decode('utf-8')
    salt_decode = salt.decode('utf-8')

    try:
        with connections['store'].cursor() as cursor:
            sql = f""" INSERT INTO clientes (nome, senha, contato, salt) VALUES ('{nome}', '{hash_decode}', '{contato}', '{salt_decode}') RETURNING id; """
            cursor.execute(sql)

            id = cursor.fetchone()[0]

            return {
                "message": "Cliente criado com sucesso",
                "id": id,
                "nome": nome,
                # "senha": senha, - linha comentada para não mostra a senha do cliente no json
                "contato": contato
            }

    except Exception as e:
        raise e
    

def atualiza_cliente(id, nome, senha, contato):
    """ Atualiza um cliente pelo seu ID """

    # Ao atualizar um vendedor, seu hash também é atualizado automaticamente 
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(senha.encode('utf-8'), salt)

    hash_decode = hash.decode('utf-8')
    salt_decode = salt.decode('utf-8')

    try:
        with connections['store'].cursor() as cursor:
            sql = f""" UPDATE clientes SET nome = '{nome}', senha = '{hash_decode}', contato = '{contato}', salt = '{salt_decode}' WHERE id = {id}; """
            cursor.execute(sql)

            if cursor.rowcount > 0:
                return {
                    "message": f"Cliente {id} atualizado com sucesso"
                }
            else:
                raise HttpError(404, "Cliente não encontrado")

    except Exception as e:
        raise e
    

def deletar_cliente(id):
    """ Deleta um cliente pelo seu ID """
    try:
        with connections['store'].cursor() as cursor:
            sql = f""" DELETE FROM clientes WHERE id = {id}; """
            cursor.execute(sql)

            if cursor.rowcount > 0:
                return {
                    "message": f"Cliente {id} deletado!"
                }
            else:
                raise HttpError(404, "Cliente não encontrado")

    except Exception as e:
        raise e
    

def buscar_cliente_id(id):
    """ Busca um cliente pelo seu ID """
    try:
        with connections['store'].cursor() as cursor:
            sql = f""" SELECT * FROM clientes WHERE id = {id}; """
            cursor.execute(sql)

            if cursor.rowcount > 0:
                data = cursor.fetchone()
                return {
                    "message": "Busca realizada com sucesso",
                    "id": data[0],
                    "nome": data[1],
                    # "senha": data[2], - linha comentada para não mostra a senha do cliente no json
                    "contato": data[3]
                }
            else:
                raise HttpError(404, "Cliente não encontrado")

    except Exception as e:
        raise e
    