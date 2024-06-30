from ninja import NinjaAPI
from vendedores.ninja import router as vendedores
from clientes.ninja import router as clientes
from instrumentos.ninja import router as instrumentos
from vendas.ninja import router as vendas
from auth.ninja import router as auth
from ninja.security import HttpBearer
from django.db import connections


api = NinjaAPI()

class AuthBearer(HttpBearer):
    try:
        def authenticate(self, request, token):
            """ Função de autenticação para verificar se o token passado existe no banco de dados"""
            with connections['store'].cursor() as cursor:
                sql = f""" SELECT token FROM vendedores UNION SELECT token FROM clientes"""
                cursor.execute(sql)

                list_token = []

                for row in cursor.fetchall():
                    data = row[0]
                    list_token.append(data)

                if token in list_token:
                    return token
            
    except Exception as e:
        raise e


api.add_router('', vendedores, auth=AuthBearer())
api.add_router('', clientes, auth=AuthBearer())
api.add_router('', instrumentos, auth=AuthBearer())
api.add_router('', vendas, auth=AuthBearer())
api.add_router('', auth)
    