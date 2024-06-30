from django.db import connections
from ninja.errors import HttpError
import bcrypt


def criar_vendedores():
    """ Função para criar 3 vendedores no banco de dados para realizar testes """
    try:
        with connections['store'].cursor() as cursor:
            # Nesse insert ja é inserido um hash e um salt a partir da senha '1234' para realizar testes
            sql_insert = """ INSERT INTO vendedores (nome, senha, turno, salt) VALUES
                ('João Silva', '$2b$12$tdtRQm7t/Sy1c8ieKIMZJevv51ag4JRuErg7UIDNir1Ok2kz7Xj3u', 'Matutino', '$2b$12$tdtRQm7t/Sy1c8ieKIMZJe'),
                ('Maria Oliveira', '$2b$12$tdtRQm7t/Sy1c8ieKIMZJevv51ag4JRuErg7UIDNir1Ok2kz7Xj3u', 'Vespertino', '$2b$12$tdtRQm7t/Sy1c8ieKIMZJe'),
                ('Carlos Pereira', '$2b$12$tdtRQm7t/Sy1c8ieKIMZJevv51ag4JRuErg7UIDNir1Ok2kz7Xj3u', 'Noturno', '$2b$12$tdtRQm7t/Sy1c8ieKIMZJe');
            """
            cursor.execute(sql_insert)

            if cursor.rowcount > 0:
                return {"message": "Vendedores criado com sucesso!"}

    except Exception as e:
        raise e
    

def buscar_vendedores():
    """ Busca todos os vendedores no banco de dados """
    try:
        with connections['store'].cursor() as cursor:
            sql = """ SELECT * FROM vendedores; """
            cursor.execute(sql)

            vendedores = []

            for row in cursor.fetchall():
                vendedor = {
                    "id": row[0],
                    "nome": row[1],
                    # "senha": row[2],
                    "turno": row[3]
                }
                vendedores.append(vendedor)

            return vendedores
    
    except Exception as e:
        raise e
    

def criar_vendedor(nome, senha, turno):
    """ Cria um vendedor no banco de dados """

    # geração de um hash com a senha para armazenar no banco de dados
    salt = bcrypt.gensalt() # gera o salt
    hash = bcrypt.hashpw(senha.encode('utf-8'), salt) # gera o hash a partir da senha fornecida e o hash gerado

    # decode no hash e no salt para virarem string para serem armanezados no banco de dados
    hash_decode = hash.decode('utf-8')
    salt_decode = salt.decode('utf-8')
        
    try:
        with connections['store'].cursor() as cursor:
            sql = f""" INSERT INTO vendedores (nome, senha, turno, salt) VALUES ('{nome}', '{hash_decode}', '{turno}', '{salt_decode}') RETURNING id; """
            cursor.execute(sql)

            id = cursor.fetchone()[0]

            return {
                "message": "Vendedor criado com sucesso",
                "id": id,
                "nome": nome,
                # "senha": hash_decode,
                "turno": turno
            }

    except Exception as e:
        raise e
    

def deletar_vendedor(vendedor_id):
    """ Deleta um vendedor filtrando pelo seu ID """
    try:
        with connections['store'].cursor() as cursor:
            sql = f""" DELETE FROM vendedores WHERE id = {vendedor_id}; """
            cursor.execute(sql)

            if cursor.rowcount > 0:
                return {"message": f"Vendedor {vendedor_id} deletado!"}
            else:
                raise HttpError(404, "Vendedor não encontrado")

    except Exception as e:
        raise e
    

def atualizar_vendedor(vendedor_id, nome, senha, turno):
    """ Atualiza um vendedor pelo seu ID """

    # Ao atualizar um vendedor, seu hash também é atualizado automaticamente
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(senha.encode('utf-8'), salt)

    hash_decode = hash.decode('utf-8')
    salt_decode = salt.decode('utf-8')

    try:
        with connections['store'].cursor() as cursor:

            sql = f""" UPDATE vendedores SET nome = '{nome}', senha = '{hash_decode}', turno = '{turno}', salt = '{salt_decode}' WHERE id = {vendedor_id}; """
            cursor.execute(sql)

            if cursor.rowcount > 0:
                return {"message": f"Vendedor {vendedor_id} atualizado!"}
            else:
                raise HttpError(404, "Vendedor não encontrado")

    except Exception as e:
        raise e
    

def buscar_vendedor_id(vendedor_id):
    """ Busca um vendedor pelo seu ID """
    try:
        with connections['store'].cursor() as cursor:
            sql = f""" SELECT * FROM vendedores WHERE id = {vendedor_id} """
            cursor.execute(sql)

            if cursor.rowcount > 0:
                v = cursor.fetchone()

                return {
                    "message": "Busca realizada com sucesso",
                    "id": v[0],
                    "nome": v[1],
                    # "senha": v[2],
                    "turno": v[3]
                }
            else:
                raise HttpError(404, "Vendedor não encontrado")

    except Exception as e:
        raise e
    

