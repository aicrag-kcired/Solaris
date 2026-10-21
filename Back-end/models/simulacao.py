from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field


class SimulacaoEntrada(BaseModel):
    consumo_energia: Decimal = Field(ge=0)
    valor_conta_energia: Decimal = Field(ge=0)
    economia_estimada: Decimal = Field(ge=0)
    financiamento: Decimal = Field(ge=0)
    id_cliente: int = Field(gt=0)
    valor_economia_mensal: Decimal = Field(ge=0)
    valor_economia_anual: Decimal = Field(ge=0)
    percentual_economia_primeiro_mes: Decimal = Field(ge=0)


class SimulacaoSaida(SimulacaoEntrada):
    id_simulacao: int
    data_simulacao: datetime
