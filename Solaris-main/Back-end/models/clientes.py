from decimal import Decimal
from pydantic import BaseModel, Field, field_validator, EmailStr

class ClienteEntrada(BaseModel):
    nome_cliente: str = Field(min_length=1, max_length=50)
    cpf_cliente: str = Field(min_length=1, max_length=14)
    rg_cliente: str = Field(min_length=1, max_length=20)
    numero_cliente: str = Field(min_length=1, max_length=15)
    email_cliente: str = Field(min_length=1, max_length=100)
    senha: str = Field(min_length=6, description="Senha do cliente")
    endereco_cliente: str = Field(min_length=1, max_length=150)
    tipo_imovel_cliente: str = Field(min_length=1, max_length=30)
    renda_mensal_cliente: Decimal = Field(ge=0, max_digits=10, decimal_places=2)

    @field_validator("nome_cliente")
    @classmethod
    def validar_nome(cls, valor: str) -> str:
        valor = valor.strip()
        if not valor:
            raise ValueError("O nome do cliente não pode ficar vazio.")
        return valor

# A Saída não herda mais a Entrada diretamente, para não vazar a senha no JSON de resposta
class ClienteSaida(BaseModel):
    id_cliente: int
    nome_cliente: str
    cpf_cliente: str
    rg_cliente: str
    numero_cliente: str
    email_cliente: str
    endereco_cliente: str
    tipo_imovel_cliente: str
    renda_mensal_cliente: Decimal

class ClienteLogin(BaseModel):
    email_cliente: str
    senha: str