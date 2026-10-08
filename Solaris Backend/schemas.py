from pydantic import BaseModel
from datetime import datetime


class ClienteSchema(BaseModel):
    nome_cliente: str
    cpf_cliente: int
    rg_cliente: int
    numero_cliente: int
    email_cliente: str
    endereco_cliente: str
    tipo_imovel_cliente: str
    renda_mensal_cliente: float
    data_de_cadastro_cliente: datetime