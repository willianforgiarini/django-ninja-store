from ninja import Router
from clientes.schemas import ClienteSchemas
from clientes.services import criar_clientes, buscar_clientes, criar_cliente, atualiza_cliente, deletar_cliente, buscar_cliente_id


router = Router()


@router.post('/post_clientes', description='Endpoint com script para criação de 10 clientes no banco de dados para realizar teste')
def post_clientes(request):
    return criar_clientes()


@router.get('/clientes', description='Endpoint para buscar todos os clientes')
def get_clientes(request):
    return buscar_clientes()


@router.post('/cliente', description='Endpoint para criar um cliente')
def post_cliente(request, cliente: ClienteSchemas):
    return criar_cliente(cliente.nome, cliente.senha, cliente.contato)


@router.put('/cliente/{id_cliente}', description='Endpoint para atualizar um cliente pelo seu id')
def put_cliente(request, id_cliente: int, cliente: ClienteSchemas):
    return atualiza_cliente(id_cliente, cliente.nome, cliente.senha, cliente.contato)


@router.delete('/cliente/{id_cliente}', description='Endpoint para deletar um cliente pelo seu id')
def delete_cliente(request, id_cliente: int):
    return deletar_cliente(id_cliente)


@router.get('/cliente/{id_cliente}', description='Endpoint para buscar um cliente pelo seu id')
def get_cliente_id(request, id_cliente: int):
    return buscar_cliente_id(id_cliente)