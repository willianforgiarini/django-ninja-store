from django.db import connections
from ninja.errors import HttpError
import jwt # biblioteca para geração do token
from datetime import datetime, timedelta
import bcrypt


def create_token(tipo, nome, senha):
    """ Função para criar o token e armazenar no banco de dados"""
    try:
        with connections['store'].cursor() as cursor:
            sql = f""" SELECT * FROM {tipo} WHERE nome = '{nome}'; """
            cursor.execute(sql)

            if cursor.rowcount > 0:

                user = cursor.fetchone()
                id = user[0] # varialvel user[0] ira conter o id do usuário!!
                hash = user[2] # varialvel user[2] ira conter o hash!!
                salt = user[5].encode('utf-8') # varialvel user[5] ira conter o salt!!

                # Criação de um hash usando a senha passada e usando o Salt que tem no banco de dados, .decode('utf-8') no final para ja transformar em string
                new_hash = bcrypt.hashpw(senha.encode('utf-8'), salt).decode('utf-8')

                
                if hash == new_hash:
                    token = jwt.encode({
                        "exp": datetime.utcnow() + timedelta(minutes=30) # utcnow() - tempo de agora, timedelta - acrescentando mais um tempo
                    }, key=f'{hash}', algorithm='HS256') # key='1234', o valor de key sera usado para gerar o token

                    sql = f""" UPDATE {tipo} SET token = '{token}' WHERE id = {id}""" # user[0] é o id do usuário do login
                    cursor.execute(sql)

                    return {"token": token}
                else:
                    return HttpError(401, "Senha inválida")
                
            else:
                raise HttpError(401, "Usuário inválido")
    
    except Exception as e:
        raise e
    