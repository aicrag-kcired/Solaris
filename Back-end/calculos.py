
from fastapi import APIRouter
from pydantic import BaseModel, Field


# Fórmula de economia do Solaris
def calcular_economia(valor_conta):
    percentual = 0.80

    economia_mensal = round(valor_conta * percentual, 2)
    economia_anual = round(economia_mensal * 12, 2)

    return {
        "economia_estimada": economia_mensal,
        "valor_economia_mensal": economia_mensal,
        "valor_economia_anual": economia_anual,
        "percentual_economia_primeiro_mes": 80.0
    }


# Dados necessários para a simulação pública
class SimulacaoPublicaEntrada(BaseModel):
    valor_conta_energia: float = Field(
        gt=0,
        le=1000000,
        description="Valor mensal da conta de energia em reais"
    )


router = APIRouter(
    prefix="/simulador",
    tags=["Simulador público"]
)


@router.post("/calcular")
def simular_economia(dados: SimulacaoPublicaEntrada):
    resultado = calcular_economia(
        dados.valor_conta_energia
    )

    return {
        "valor_conta_energia": dados.valor_conta_energia,
        **resultado,
        "aviso": (
            "Esta é uma estimativa simplificada. "
            "A economia real depende do projeto solar, "
            "das tarifas e das condições de instalação."
        )
    }
