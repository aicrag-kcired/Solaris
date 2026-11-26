from pydantic import BaseModel, Field


class TecnicoEntrada(BaseModel):
    nome_tecnico: str = Field(min_length=1, max_length=100)
    email_tecnico: str = Field(min_length=1, max_length=100)
    telefone_tecnico: str = Field(min_length=1, max_length=20)
    local_instalacao: str = Field(min_length=1)


class TecnicoSaida(TecnicoEntrada):
    id_tecnico: int
