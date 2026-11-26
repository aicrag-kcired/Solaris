from decimal import Decimal
from pydantic import BaseModel, Field


class RelatorioEntrada(BaseModel):
    total_simulacao: int = Field(ge=0)
    status_relatorio: str = Field(min_length=1, max_length=30)
    historico: str = Field(min_length=1)
    total_pago: Decimal = Field(ge=0)


class RelatorioSaida(RelatorioEntrada):
    id_relatorio: int
