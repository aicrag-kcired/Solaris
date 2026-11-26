from datetime import date
from decimal import Decimal
from pydantic import BaseModel, Field


class InstalacaoEntrada(BaseModel):
    tecnico_responsavel: str = Field(min_length=1, max_length=100)
    custo_instalacao: Decimal = Field(ge=0)
    status_instalacao: str = Field(min_length=1, max_length=30)
    data_instalacao: date
    id_tecnico: int = Field(gt=0)


class InstalacaoSaida(InstalacaoEntrada):
    id_instalacao: int
