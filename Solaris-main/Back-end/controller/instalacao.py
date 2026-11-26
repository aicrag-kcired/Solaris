
from fastapi import APIRouter, HTTPException, Response, status
from database import supabase
from models.instalacao import InstalacaoEntrada, InstalacaoSaida

router = APIRouter(prefix="/instalacoes", tags=["Instalações"])


@router.post("", response_model=InstalacaoSaida, status_code=201)
def cadastrar_instalacao(dados: InstalacaoEntrada):
    resposta = supabase.table("instalacao").insert(
        dados.model_dump(mode="json")
    ).execute()
    if not resposta.data:
        raise HTTPException(502, "O Supabase não retornou a instalação.")
    return resposta.data[0]


@router.get("", response_model=list[InstalacaoSaida])
def listar_instalacoes():
    resposta = supabase.table("instalacao").select("*").order(
        "id_instalacao"
    ).execute()
    return resposta.data


@router.get("/{id_instalacao}", response_model=InstalacaoSaida)
def consultar_instalacao(id_instalacao: int):
    resposta = supabase.table("instalacao").select("*").eq(
        "id_instalacao", id_instalacao
    ).execute()
    if not resposta.data:
        raise HTTPException(404, "Instalação não encontrada.")
    return resposta.data[0]


@router.put("/{id_instalacao}", response_model=InstalacaoSaida)
def atualizar_instalacao(id_instalacao: int, dados: InstalacaoEntrada):
    resposta = supabase.table("instalacao").update(
        dados.model_dump(mode="json")
    ).eq("id_instalacao", id_instalacao).execute()
    if not resposta.data:
        raise HTTPException(404, "Instalação não encontrada.")
    return resposta.data[0]


@router.delete("/{id_instalacao}", status_code=204)
def excluir_instalacao(id_instalacao: int):
    resposta = supabase.table("instalacao").delete().eq(
        "id_instalacao", id_instalacao
    ).execute()
    if not resposta.data:
        raise HTTPException(404, "Instalação não encontrada.")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
