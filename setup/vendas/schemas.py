from pydantic import BaseModel
from datetime import date


class VendaSchemas(BaseModel):
    data_venda: date
    id_vendedor: int
    id_cliente: int
    id_instrumento: int
    quantidade: int
