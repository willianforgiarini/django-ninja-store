from django.db import connections
from ninja.errors import HttpError


def criar_instrumentos():
    """ Função para criar 10 instrumentos no banco de dados para realizar testes"""
    try:
        with connections['store'].cursor() as cursor:
            sql = """ INSERT INTO instrumentos (tipo, modelo, preco, quantidade) VALUES
                ('guitarra', 'Fender Stratocaster', 1200.00, 10),
                ('guitarra', 'Gibson Les Paul', 2500.00, 10),
                ('bateria', 'Pearl Export', 700.00, 10),
                ('bateria', 'Yamaha Stage Custom', 850.00, 10),
                ('violão', 'Yamaha C40', 150.00, 10),
                ('violão', 'Fender CD-60', 200.00, 10),
                ('flauta', 'Yamaha YFL-222', 500.00, 10),
                ('flauta', 'Gemeinhardt 2SP', 450.00, 10),
                ('teclado', 'Casio CTK-3500', 100.00, 10),
                ('teclado', 'Yamaha PSR-E373', 150.00, 10);
            """
            cursor.execute(sql)

            if cursor.rowcount > 0:
                return {"message": "Instrumentos criados com sucesso"}

    except Exception as e:
        raise e
    

def buscar_instrumentos():
    """ Função para buscar todos os instrumentos do banco de dados """
    try:
        with connections['store'].cursor() as cursor:
            sql = """ SELECT * FROM instrumentos; """
            cursor.execute(sql)

            instrumentos = []

            for row in cursor.fetchall():
                instrumento = {
                    "id": row[0],
                    "tipo": row[1],
                    "modelo": row[2],
                    "preco": row[3],
                    "quantidade": row[4]
                }
                instrumentos.append(instrumento)

            return instrumentos

    except Exception as e:
        raise e
    

def criar_instrumento(tipo, modelo, preco, quantidade):
    """ Função para criar um instrumento """
    try:
        with connections['store'].cursor() as cursor:
            sql = f""" INSERT INTO instrumentos (tipo, modelo, preco, quantidade) VALUES ('{tipo}', '{modelo}', {preco}, {quantidade}) RETURNING id; """
            cursor.execute(sql)

            if cursor.rowcount > 0:
                id = cursor.fetchone()[0]

                return {
                    "message": f"{tipo} criado com sucesso",
                    "id": id,
                    "tipo": tipo,
                    "modelo": modelo,
                    "preco": preco,
                    "quantidade": quantidade
                }

    except Exception as e:
        raise e
    

def atualiza_instrumento(id_instrumento, tipo, modelo, preco, quantidade):
    """ Função para atualizar um instrumento """
    try:
        with connections['store'].cursor() as cursor:
            sql = f""" UPDATE instrumentos SET tipo = '{tipo}', modelo = '{modelo}', preco = {preco}, quantidade = {quantidade} WHERE id = {id_instrumento}; """
            cursor.execute(sql)

            if cursor.rowcount > 0:
                return {"message": f"Instrumento {id_instrumento} atualizado com sucesso!"}
            else:
                raise HttpError(404, "Instrumento não encontrado")

    except Exception as e:
        raise e
    

def deletar_instrumento(id_instrumento):
    """ Função para deletar um instrumento pelo seu ID """
    try:
        with connections['store'].cursor() as cursor:
            sql = f""" DELETE FROM instrumentos WHERE id = {id_instrumento}; """
            cursor.execute(sql)

            if cursor.rowcount > 0:
                return {"message": f"Instrumento {id_instrumento} foi deletado"}
            else:
                raise HttpError(404, "Instrumento não encontrado")

    except Exception as e:
        raise e
    

def buscar_instrumento_id(id_instrumento):
    """ Função para buscar um intrumento pelo seu ID """
    try:
        with connections['store'].cursor() as cursor:
            sql = f""" SELECT * FROM instrumentos WHERE id = {id_instrumento}; """
            cursor.execute(sql)

            if cursor.rowcount > 0:
                instrumento = cursor.fetchone()
                return {
                    "message": f"Busca pelo id {id_instrumento} realizada com sucesso",
                    "id": instrumento[0],
                    "tipo": instrumento[1],
                    "modelo": instrumento[2],
                    "preco": instrumento[3],
                    "quantidade": instrumento[4]
                }
            else:
                raise HttpError(404, "Instrumento não encontrado")

    except Exception as e:
        raise e
    