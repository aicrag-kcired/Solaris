
from fastapi import APIRouter, HTTPException, Response, status
from database import supabase
from models.financiamento import FinanciamentoEntrada, FinanciamentoSaida

router = APIRouter(prefix="/financiamentos", tags=["Financiamentos"])


@router.post("", response_model=FinanciamentoSaida, status_code=201)
def cadastrar_financiamento(dados: FinanciamentoEntrada):
    resposta = supabase.table("financiamento").insert(
        dados.model_dump(mode="json")
    ).execute()
    if not resposta.data:
        raise HTTPException(502, "O Supabase não retornou o financiamento.")
    return resposta.data[0]


@router.get("", response_model=list[FinanciamentoSaida])
def listar_financiamentos():
    resposta = supabase.table("financiamento").select("*").order(
        "id_financiamento"
    ).execute()
    return resposta.data


@router.get("/{id_financiamento}", response_model=FinanciamentoSaida)
def consultar_financiamento(id_financiamento: int):
    resposta = supabase.table("financiamento").select("*").eq(
        "id_financiamento", id_financiamento
    ).execute()
    if not resposta.data:
        raise HTTPException(404, "Financiamento não encontrado.")
    return resposta.data[0]


@router.put("/{id_financiamento}", response_model=FinanciamentoSaida)
def atualizar_financiamento(
    id_financiamento: int, dados: FinanciamentoEntrada
):
    resposta = supabase.table("financiamento").update(
        dados.model_dump(mode="json")
    ).eq("id_financiamento", id_financiamento).execute()
    if not resposta.data:
        raise HTTPException(404, "Financiamento não encontrado.")
    return resposta.data[0]


@router.delete("/{id_financiamento}", status_code=204)
def excluir_financiamento(id_financiamento: int):
    resposta = supabase.table("financiamento").delete().eq(
        "id_financiamento", id_financiamento
    ).execute()
    if not resposta.data:
        raise HTTPException(404, "Financiamento não encontrado.")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
