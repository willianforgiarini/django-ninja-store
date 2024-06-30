from pydantic import BaseModel


class VendedorSchemas(BaseModel):
    nome: str
    senha: str
    turno: str