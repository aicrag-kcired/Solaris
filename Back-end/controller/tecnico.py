
from fastapi import APIRouter, HTTPException, Response, status
from database import supabase
from models.tecnico import TecnicoEntrada, TecnicoSaida

router = APIRouter(prefix="/tecnicos", tags=["Técnicos"])


@router.post("", response_model=TecnicoSaida, status_code=201)
def cadastrar_tecnico(dados: TecnicoEntrada):
    resposta = supabase.table("tecnico").insert(
        dados.model_dump(mode="json")
    ).execute()
    if not resposta.data:
        raise HTTPException(502, "O Supabase não retornou o técnico.")
    return resposta.data[0]


@router.get("", response_model=list[TecnicoSaida])
def listar_tecnicos():
    resposta = supabase.table("tecnico").select("*").order(
        "id_tecnico"
    ).execute()
    return resposta.data


@router.get("/{id_tecnico}", response_model=TecnicoSaida)
def consultar_tecnico(id_tecnico: int):
    resposta = supabase.table("tecnico").select("*").eq(
        "id_tecnico", id_tecnico
    ).execute()
    if not resposta.data:
        raise HTTPException(404, "Técnico não encontrado.")
    return resposta.data[0]


@router.put("/{id_tecnico}", response_model=TecnicoSaida)
def atualizar_tecnico(id_tecnico: int, dados: TecnicoEntrada):
    resposta = supabase.table("tecnico").update(
        dados.model_dump(mode="json")
    ).eq("id_tecnico", id_tecnico).execute()
    if not resposta.data:
        raise HTTPException(404, "Técnico não encontrado.")
    return resposta.data[0]


@router.delete("/{id_tecnico}", status_code=204)
def excluir_tecnico(id_tecnico: int):
    resposta = supabase.table("tecnico").delete().eq(
        "id_tecnico", id_tecnico
    ).execute()
    if not resposta.data:
        raise HTTPException(404, "Técnico não encontrado.")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
