from ninja import Router
from vendas.schemas import VendaSchemas
from vendas.services import criar_vendas, buscar_vendas, filtrar_vendas, criar_venda


router = Router()


@router.post('/post_vendas', description='Endpoint para criação de vendas no banco de dados para realizar testes')
# Para esse endpoint funcionar, é preciso realizar os endpoints para criar vendedores, clientes e instrumentos
def post_vendas(request):
    return criar_vendas()


@router.get('/vendas', description='Endpoint para buscar todas as vendas')
def get_vendas(request):
    return buscar_vendas()


@router.get('/vendas/{tipo}/{valor}', description='Endpoint para filtrar vendas')
# Esse endpoint usa a função filtrar_vendas(varchar, varchar) criado no bancos de dados
# O parametro {tipo} sera o campo usado na função e o parametro {valor} sera o valor do campo para realizar o filtro na função

# Exemplos para testar o endpoint:
# /vendas/vendedor/Maria Oliveira - busca pelo nome - /vendas/vendedor/2 - busca pelo ID -- busca todos as vendas feita pelo vendedor
# /vendas/cliente/Ana Silva -- /vendas/cliente/1 -- buscar todas as vendas do cliente
# /vendas/instrumento/guitarra -- /vendas/instrumento/bateria -- buscar todas as vendas de um instrumento especifico
# /vendas/data/2023-10-31 -- busca todas as vendas de uma data especifica
def get_filtrar_vendas(request, tipo, valor):
    return filtrar_vendas(tipo, valor)


@router.post('/venda', description='Endpoint para criar uma venda')
def post_venda(request, venda: VendaSchemas):
    return criar_venda(venda.data_venda, venda.id_vendedor, venda.id_cliente, venda.id_instrumento, venda.quantidade)
