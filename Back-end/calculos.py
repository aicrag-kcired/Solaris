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