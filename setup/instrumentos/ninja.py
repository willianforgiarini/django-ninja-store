from ninja import Router
from instrumentos.schemas import InstrumentoSchemas
from instrumentos.services import criar_instrumentos, buscar_instrumentos, criar_instrumento, atualiza_instrumento, deletar_instrumento, buscar_instrumento_id


router = Router()


@router.post('/post_instrumentos', description='Endpoint com script para criação de 10 instrumentos no banco de dados para realizar testes')
def post_instrumentos(request):
    return criar_instrumentos()


@router.get('/instrumentos', description='Endpoint para buscar todos os instrumentos')
def get_instrumento(request):
    return buscar_instrumentos()


@router.post('/instrumento', description='Endpoint para criar um instrumento')
def post_instrumento(request, instrumento: InstrumentoSchemas):
    return criar_instrumento(instrumento.tipo, instrumento.modelo, instrumento.preco, instrumento.quantidade)


@router.put('/instrumento/{id_instrumento}', description='Endpoint para atualizar um instrumento pelo seu id')
def put_instrumento(request,id_instrumento: int, instrumento: InstrumentoSchemas):
    return atualiza_instrumento(id_instrumento, instrumento.tipo, instrumento.modelo, instrumento.preco, instrumento.quantidade)


@router.delete('/instrumento/{id_instrumento}', description='Endpoint para deletar um intrumento pelo seu id')
def delete_instrumento(request, id_instrumento: int):
    return deletar_instrumento(id_instrumento)


@router.get('/instrumento/{id_instrumento}', description='Endpoint para buscar um intrumento pelo seu id')
def get_instrumento_id(request, id_instrumento: int):
    return buscar_instrumento_id(id_instrumento)
