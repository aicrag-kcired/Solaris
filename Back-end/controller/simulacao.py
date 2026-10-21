
from fastapi import APIRouter, HTTPException, Response, status
from database import supabase
from models.simulacao import SimulacaoEntrada, SimulacaoSaida

router = APIRouter(prefix="/simulacoes", tags=["Simulações"])


@router.post("", response_model=SimulacaoSaida, status_code=201)
def cadastrar_simulacao(dados: SimulacaoEntrada):
    resposta = supabase.table("simulacao").insert(
        dados.model_dump(mode="json")
    ).execute()
    if not resposta.data:
        raise HTTPException(502, "O Supabase não retornou a simulação.")
    return resposta.data[0]


@router.get("", response_model=list[SimulacaoSaida])
def listar_simulacoes():
    resposta = supabase.table("simulacao").select("*").order(
        "id_simulacao"
    ).execute()
    return resposta.data


@router.get("/{id_simulacao}", response_model=SimulacaoSaida)
def consultar_simulacao(id_simulacao: int):
    resposta = supabase.table("simulacao").select("*").eq(
        "id_simulacao", id_simulacao
    ).execute()
    if not resposta.data:
        raise HTTPException(404, "Simulação não encontrada.")
    return resposta.data[0]


@router.put("/{id_simulacao}", response_model=SimulacaoSaida)
def atualizar_simulacao(id_simulacao: int, dados: SimulacaoEntrada):
    resposta = supabase.table("simulacao").update(
        dados.model_dump(mode="json")
    ).eq("id_simulacao", id_simulacao).execute()
    if not resposta.data:
        raise HTTPException(404, "Simulação não encontrada.")
    return resposta.data[0]


@router.delete("/{id_simulacao}", status_code=204)
def excluir_simulacao(id_simulacao: int):
    resposta = supabase.table("simulacao").delete().eq(
        "id_simulacao", id_simulacao
    ).execute()
    if not resposta.data:
        raise HTTPException(404, "Simulação não encontrada.")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
