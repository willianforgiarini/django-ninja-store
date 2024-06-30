from ninja import Router
from vendedores.schemas import VendedorSchemas
from vendedores.services import criar_vendedores, buscar_vendedores, criar_vendedor, deletar_vendedor, atualizar_vendedor, buscar_vendedor_id


router = Router()


@router.post('/post_vendedores', description='Endpoint com scprit para criação de 3 vendedores no banco de dados para realizar teste')
def post_vendedores(request):
    return criar_vendedores()


@router.get('/vendedores', description='Endpoint para buscar todos os vendedores')
def get_vendedores(request):
    return buscar_vendedores()


@router.post('/vendedor', description='Endpoint para criar um vendedor')
def post_vendedor(request, vendedor: VendedorSchemas):
    return criar_vendedor(vendedor.nome, vendedor.senha, vendedor.turno)


@router.delete('/vendedor/{vendedor_id}', description='Endpoint para deletar um vendedor pelo seu id')
def delete_vendedor(request, vendedor_id: int):
    return deletar_vendedor(vendedor_id)


@router.put('/vendedor/{vendedor_id}', description='Endpoint para atualizar um vendedor pelo seu id')
def put_vendedor(request, vendedor_id: int, vendedor: VendedorSchemas):
    return atualizar_vendedor(vendedor_id, vendedor.nome, vendedor.senha, vendedor.turno)


@router.get('/vendedor/{vendedor_id}', description='Endpoint para buscar um vendedor pelo seu id')
def get_vendedor_id(request, vendedor_id: int):
    return buscar_vendedor_id(vendedor_id)
