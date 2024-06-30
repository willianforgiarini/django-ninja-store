from pydantic import BaseModel


class ClienteSchemas(BaseModel):
    nome: str
    senha: str
    contato: str