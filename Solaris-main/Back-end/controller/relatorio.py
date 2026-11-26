
from fastapi import APIRouter, HTTPException, Response, status
from database import supabase
from models.relatorio import RelatorioEntrada, RelatorioSaida

router = APIRouter(prefix="/relatorios", tags=["Relatórios"])


@router.post("", response_model=RelatorioSaida, status_code=201)
def cadastrar_relatorio(dados: RelatorioEntrada):
    resposta = supabase.table("relatorio").insert(
        dados.model_dump(mode="json")
    ).execute()
    if not resposta.data:
        raise HTTPException(502, "O Supabase não retornou o relatório.")
    return resposta.data[0]


@router.get("", response_model=list[RelatorioSaida])
def listar_relatorios():
    resposta = supabase.table("relatorio").select("*").order(
        "id_relatorio"
    ).execute()
    return resposta.data


@router.get("/{id_relatorio}", response_model=RelatorioSaida)
def consultar_relatorio(id_relatorio: int):
    resposta = supabase.table("relatorio").select("*").eq(
        "id_relatorio", id_relatorio
    ).execute()
    if not resposta.data:
        raise HTTPException(404, "Relatório não encontrado.")
    return resposta.data[0]


@router.put("/{id_relatorio}", response_model=RelatorioSaida)
def atualizar_relatorio(id_relatorio: int, dados: RelatorioEntrada):
    resposta = supabase.table("relatorio").update(
        dados.model_dump(mode="json")
    ).eq("id_relatorio", id_relatorio).execute()
    if not resposta.data:
        raise HTTPException(404, "Relatório não encontrado.")
    return resposta.data[0]


@router.delete("/{id_relatorio}", status_code=204)
def excluir_relatorio(id_relatorio: int):
    resposta = supabase.table("relatorio").delete().eq(
        "id_relatorio", id_relatorio
    ).execute()
    if not resposta.data:
        raise HTTPException(404, "Relatório não encontrado.")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
