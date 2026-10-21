
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field, EmailStr, field_validator


class ClienteEntrada(BaseModel):
    nome_cliente: str = Field(min_length=1, max_length=50)
    cpf_cliente: str = Field(min_length=1, max_length=14)
    rg_cliente: str = Field(min_length=1, max_length=20)
    numero_cliente: str = Field(min_length=1, max_length=15)
    email_cliente: str = Field(min_length=1, max_length=100)
    endereco_cliente: str = Field(min_length=1, max_length=150)
    tipo_imovel_cliente: str = Field(min_length=1, max_length=30)
    renda_mensal_cliente: Decimal = Field(
        ge=0, max_digits=10, decimal_places=2
    )

    @field_validator("nome_cliente")
    @classmethod
    def validar_nome(cls, valor: str) -> str:
        valor = valor.strip()
        if not valor:
            raise ValueError("O nome do cliente não pode ficar vazio.")
        return valor


class ClienteSaida(ClienteEntrada):
    id_cliente: int
    data_de_cadastro_cliente: datetime
