from ninja import Router
from auth.schemas import LoginSchemas
from vendedores.schemas import VendedorSchemas
from vendedores.services import criar_vendedor
from auth.services import create_token


router = Router()

@router.post('/login', description='Endpoint que gera um token para poder acessar todos os outros endpoint da API')
# O endpoint cria um token a partir da senha passada armazenando o token no banco de dados
# No body do endpoint é preciso passar o tipo, nome e senha, o tipo seria vendedores ou clientes
# Mesmo que o token fiquei salvo no banco de dados, se o usuário fizer o login novamente, outro token é gerado, atualizando no banco de dados
def login_token(request, login: LoginSchemas):
    return create_token(login.tipo, login.nome, login.senha)


@router.post('/login/create', description='Endpoint para criar um primeiro usuário como vendedor e gerar um token para poder acessar todos os endpoints da API')
def create_vendedor(request, vendedor: VendedorSchemas):
    return criar_vendedor(vendedor.nome, vendedor.senha, vendedor.turno)
