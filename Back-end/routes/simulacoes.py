from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session

from database import engine
from models import Cliente, Simulacao
from schemas import SimulacaoSchema

router = APIRouter()


@router.get("/simulacoes")
def listar_simulacoes():
    with Session(engine) as session:
        simulacoes = session.query(Simulacao).all()

        resultado = []

        for simulacao in simulacoes:
            cliente = session.get(Cliente, simulacao.id_cliente) if simulacao.id_cliente is not None else None

            resultado.append({
                "id_simulacao": simulacao.id_simulacao,
                "id_cliente": simulacao.id_cliente,
                "nome_cliente": cliente.nome_cliente if cliente else None,
                "consumo_energia": simulacao.consumo_energia,
                "valor_conta_energia": simulacao.valor_conta_energia,
                "economia_estimada": simulacao.economia_estimada,
                "data_simulacao": simulacao.data_simulacao,
                "financiamento": simulacao.financiamento,
                "id_usuario": simulacao.id_usuario,
                "valor_economia_mensal": simulacao.valor_economia_mensal,
                "valor_economia_anual": simulacao.valor_economia_anual,
                "percentual_economia_primeiro_mes": simulacao.percentual_economia_primeiro_mes
            })

        return resultado


@router.post("/simulacoes")
def cadastrar_simulacao(dados: SimulacaoSchema):
    with Session(engine) as session:
        cliente = session.get(Cliente, dados.id_cliente)

        if cliente is None:
            raise HTTPException(
                status_code=404,
                detail="Cliente não encontrado"
            )

        nova_simulacao = Simulacao(**dados.model_dump())

        session.add(nova_simulacao)
        session.commit()
        session.refresh(nova_simulacao)

        return {
            "id_simulacao": nova_simulacao.id_simulacao,
            "id_cliente": nova_simulacao.id_cliente,
            "nome_cliente": cliente.nome_cliente,
            "mensagem": "Simulação cadastrada com sucesso!"
        }