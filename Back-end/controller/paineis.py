
from fastapi import APIRouter, HTTPException, Response, status
from database import supabase
from models.paineis import PainelEntrada, PainelSaida

router = APIRouter(prefix="/paineis", tags=["Painéis"])


@router.post("", response_model=PainelSaida, status_code=201)
def cadastrar_painel(dados: PainelEntrada):
    resposta = supabase.table("paineis").insert(
        dados.model_dump(mode="json")
    ).execute()
    if not resposta.data:
        raise HTTPException(502, "O Supabase não retornou o painel.")
    return resposta.data[0]


@router.get("", response_model=list[PainelSaida])
def listar_paineis():
    resposta = supabase.table("paineis").select("*").order(
        "id_paineis"
    ).execute()
    return resposta.data


@router.get("/{id_paineis}", response_model=PainelSaida)
def consultar_painel(id_paineis: int):
    resposta = supabase.table("paineis").select("*").eq(
        "id_paineis", id_paineis
    ).execute()
    if not resposta.data:
        raise HTTPException(404, "Painel não encontrado.")
    return resposta.data[0]


@router.put("/{id_paineis}", response_model=PainelSaida)
def atualizar_painel(id_paineis: int, dados: PainelEntrada):
    resposta = supabase.table("paineis").update(
        dados.model_dump(mode="json")
    ).eq("id_paineis", id_paineis).execute()
    if not resposta.data:
        raise HTTPException(404, "Painel não encontrado.")
    return resposta.data[0]


@router.delete("/{id_paineis}", status_code=204)
def excluir_painel(id_paineis: int):
    resposta = supabase.table("paineis").delete().eq(
        "id_paineis", id_paineis
    ).execute()
    if not resposta.data:
        raise HTTPException(404, "Painel não encontrado.")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
