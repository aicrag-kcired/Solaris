from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field


class PagamentoEntrada(BaseModel):
    entidade_documento: str = Field(min_length=1, max_length=100)
    valor_pago: Decimal = Field(ge=0)


class PagamentoSaida(PagamentoEntrada):
    id_pagamento: int
    data_pagamento: datetime
