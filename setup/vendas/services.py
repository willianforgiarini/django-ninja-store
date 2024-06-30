from django.db import connections


def criar_vendas():
    """ Função para crias vendas, usando os clientes e vendedores criados nos endpoints de teste
        /post_clientes
        /post_vendedores
    """
    try:
        with connections['store'].cursor() as cursor:
            sql = """INSERT INTO vendas (data_venda, id_vendedor, id_cliente, id_instrumento, quantidade) VALUES
                -- Compras de Ana Silva
                ('2022-01-15', 2, 1, 1, 1),
                ('2022-05-20', 3, 1, 2, 1),
                ('2023-07-18', 4, 1, 3, 1),
                ('2023-11-25', 2, 1, 4, 1),
                ('2024-03-10', 3, 1, 5, 1),
                -- Compras de Bruno Costa
                ('2022-02-22', 3, 2, 6, 1),
                ('2022-06-12', 4, 2, 7, 1),
                ('2023-08-30', 2, 2, 8, 1),
                ('2023-12-01', 3, 2, 9, 1),
                -- Compras de Carla Pereira
                ('2022-03-05', 4, 3, 10, 1),
                ('2022-07-19', 2, 3, 1, 1),
                ('2023-09-11', 3, 3, 2, 1),
                ('2024-01-07', 4, 3, 3, 1),
                -- Compras de Daniela Oliveira
                ('2022-04-20', 2, 4, 4, 1),
                ('2022-08-22', 3, 4, 5, 1),
                ('2023-10-15', 4, 4, 6, 1),
                ('2024-02-28', 2, 4, 7, 1),
                ('2024-04-15', 3, 4, 8, 1),
                -- Compras de Eduardo Souza
                ('2022-05-11', 3, 5, 9, 1),
                ('2022-09-14', 4, 5, 10, 1),
                ('2023-11-27', 2, 5, 1, 1),
                ('2024-03-22', 3, 5, 2, 1),
                -- Compras de Fernanda Lima
                ('2022-06-25', 2, 6, 3, 1),
                ('2022-10-18', 3, 6, 4, 1),
                ('2023-12-05', 4, 6, 5, 1),
                ('2024-04-01', 2, 6, 6, 1),
                -- Compras de Gustavo Mendes
                ('2022-07-08', 3, 7, 7, 1),
                ('2022-11-22', 4, 7, 8, 1),
                ('2023-12-30', 2, 7, 9, 1),
                ('2024-04-12', 3, 7, 10, 1),
                -- Compras de Helena Barbosa
                ('2022-08-15', 4, 8, 1, 1),
                ('2022-12-20', 2, 8, 2, 1),
                ('2023-10-25', 3, 8, 3, 1),
                ('2024-02-05', 4, 8, 4, 1),
                -- Compras de Igor Santos
                ('2022-09-10', 2, 9, 5, 1),
                ('2023-01-15', 3, 9, 6, 1),
                ('2023-09-18', 4, 9, 7, 1),
                ('2024-01-20', 2, 9, 8, 1),
                -- Compras de Juliana Almeida
                ('2022-10-28', 3, 10, 9, 1),
                ('2023-02-14', 4, 10, 10, 1),
                ('2023-10-31', 2, 10, 1, 1),
                ('2024-03-03', 3, 10, 2, 1),
                ('2024-05-10', 4, 10, 3, 1);
            """
            cursor.execute(sql)

            if cursor.rowcount > 0:
                return {"message": "Vendas criadas com sucesso"}

    except Exception as e:
        raise e
    

def buscar_vendas():
    """ Busca todas as vendas no banco de dados"""
    try:
        with connections['store'].cursor() as cursor:
            sql = """ SELECT vd.id, vd.data_venda , v.nome, i.tipo, i.modelo, c.nome, i.preco, vd.quantidade
                FROM vendas vd
                JOIN vendedores v ON vd.id_vendedor = v.id
                JOIN instrumentos i ON vd.id_instrumento = i.id 
                JOIN clientes c ON vd.id_cliente = c.id
                ORDER BY vd.data_venda DESC
            """
            cursor.execute(sql)

            vendas = []

            if cursor.rowcount > 0:
                for row in cursor.fetchall():
                    venda = {
                        "id": row[0],
                        "data_venda": row[1],
                        "vendedor": row[2],
                        "tipo_instrumento": row[3],
                        "modelo": row[4],
                        "cliente": row[5],
                        "valor": row[6],
                        "quantidade": row[7]
                    }
                    vendas.append(venda)
                
                return vendas
            
    except Exception as e:
        raise e


def filtrar_vendas(tipo, valor):
    """ Função para filtrar as vendas """
    try:
        with connections['store'].cursor() as cursor:
            sql = f""" SELECT * FROM filtrar_vendas('{tipo}', '{valor}'); """
            cursor.execute(sql)

            vendas = []

            if cursor.rowcount > 0:
                qnt = 0
                tot_preco = 0

                for row in cursor.fetchall():
                    venda = {
                        "id": row[0],
                        "data_venda": row[1],
                        "vendedor": row[2],
                        "tipo_instrumento": row[3],
                        "modelo": row[4],
                        "cliente": row[5],
                        "valor": row[6],
                        "quantidade": row[7]
                    }
                    preco_qnt = row[6] * row[7]
                    qnt += row[7]
                    tot_preco += preco_qnt
                    vendas.append(venda)

                # Dependendo do tipo que for passado na função, retorna uma mensagem diferente, com um relatório de quantidade de vendas e o valor total
                if tipo == 'vendedor':
                    if qnt == 1:
                        message = f'Vendedor(a) {row[2]} fez {qnt} venda de R${tot_preco}'
                    else:
                        message = f'Vendedor(a) {row[2]} fez {qnt} vendas, totalizando R${tot_preco}'
                
                elif tipo == 'cliente':
                    if qnt == 1:
                        message = f'Cliente {row[5]} fez {qnt} compra de R${tot_preco}'
                    else:
                        message = f'Cliente {row[5]} fez {qnt} compras, totalizando R${tot_preco}'

                elif tipo == 'instrumento':
                    if qnt == 1:
                        message = f'Instrumento {row[3]} teve {qnt} venda de R${tot_preco}'
                    else:
                        message = f'Instrumento {row[3]} teve {qnt} vendas, totalizando R${tot_preco}'

                else:
                    if qnt == 1:
                        message = f'Na data {row[1]} teve {qnt} venda de R${tot_preco}'
                    else:
                        message = f'Na data {row[1]}, foram feitas {qnt} vendas, totalizando R${tot_preco}'

                return {
                    "message": message,
                    "vendas": vendas
                }

    except Exception as e:
        raise e
    

def criar_venda(data, id_vendedor, id_cliente, id_instrumento, quantidade):
    """ Função para criar uma venda """
    try:
        with connections['store'].cursor() as cursor:
            sql = f""" INSERT INTO vendas (data_venda, id_vendedor, id_cliente, id_instrumento, quantidade) 
                VALUES ('{data}', {id_vendedor}, {id_cliente}, {id_instrumento}, {quantidade}) RETURNING id ;
            """
            cursor.execute(sql)

            id = cursor.fetchone()[0]

            return {
                "message": "Venda cadastrada com sucesso",
                "id": id,
                "data_venda": data,
                "id_vendedor": id_vendedor,
                "id_cliente": id_cliente,
                "id_instrumento": id_instrumento,
                "quantidade": quantidade
            }

    except Exception as e:
        raise e
      