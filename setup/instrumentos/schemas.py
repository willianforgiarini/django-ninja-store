from pydantic import BaseModel


class InstrumentoSchemas(BaseModel):
    tipo: str
    modelo: str
    preco: float
    quantidade: int
    