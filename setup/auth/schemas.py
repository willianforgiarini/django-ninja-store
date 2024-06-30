from pydantic import BaseModel


class LoginSchemas(BaseModel):
    tipo: str
    nome: str
    senha: str