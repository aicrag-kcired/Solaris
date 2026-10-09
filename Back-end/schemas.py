from pydantic import BaseModel
from datetime import datetime


class ClienteSchema(BaseModel):
    nome_cliente: str
    cpf_cliente: str
    rg_cliente: int
    numero_cliente: str
    email_cliente: str
    endereco_cliente: str
    tipo_imovel_cliente: str
    renda_mensal_cliente: float
    data_de_cadastro_cliente: datetime


class SimulacaoSchema(BaseModel):
    id_cliente: int
    consumo_energia: float
    valor_conta_energia: float
    economia_estimada: float
    data_simulacao: datetime
    financiamento: float
    id_usuario: str
    valor_economia_mensal: float
    valor_economia_anual: float
    percentual_economia_primeiro_mes: float