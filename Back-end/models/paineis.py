from datetime import date
from decimal import Decimal
from pydantic import BaseModel, Field


class PainelEntrada(BaseModel):
    rendimento: Decimal = Field(ge=0)
    data_instalacao: date
    data_garantia: date
    local_instalacao: str = Field(min_length=1, max_length=150)
    responsavel_instalacao: str = Field(min_length=1, max_length=100)


class PainelSaida(PainelEntrada):
    id_paineis: int
