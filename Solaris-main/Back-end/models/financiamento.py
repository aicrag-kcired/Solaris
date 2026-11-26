from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field


class FinanciamentoEntrada(BaseModel):
    valor_financiamento: Decimal = Field(ge=0)
    status_financiamento: str = Field(min_length=1, max_length=30)


class FinanciamentoSaida(FinanciamentoEntrada):
    id_financiamento: int
    data_financiamento: datetime
