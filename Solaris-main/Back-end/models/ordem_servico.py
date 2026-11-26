from datetime import date
from pydantic import BaseModel, ConfigDict, Field


class OrdemServicoEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")
    data_ordem_servico: date
    id_cliente: int = Field(gt=0)


class OrdemServicoSaida(OrdemServicoEntrada):
    id_ordem_servico: int
    nome_cliente: str
