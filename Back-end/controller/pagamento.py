
from fastapi import APIRouter, HTTPException, Response, status
from database import supabase
from models.pagamento import PagamentoEntrada, PagamentoSaida

router = APIRouter(prefix="/pagamentos", tags=["Pagamentos"])


@router.post("", response_model=PagamentoSaida, status_code=201)
def cadastrar_pagamento(dados: PagamentoEntrada):
    resposta = supabase.table("pagamento").insert(
        dados.model_dump(mode="json")
    ).execute()
    if not resposta.data:
        raise HTTPException(502, "O Supabase não retornou o pagamento.")
    return resposta.data[0]


@router.get("", response_model=list[PagamentoSaida])
def listar_pagamentos():
    resposta = supabase.table("pagamento").select("*").order(
        "id_pagamento"
    ).execute()
    return resposta.data


@router.get("/{id_pagamento}", response_model=PagamentoSaida)
def consultar_pagamento(id_pagamento: int):
    resposta = supabase.table("pagamento").select("*").eq(
        "id_pagamento", id_pagamento
    ).execute()
    if not resposta.data:
        raise HTTPException(404, "Pagamento não encontrado.")
    return resposta.data[0]


@router.put("/{id_pagamento}", response_model=PagamentoSaida)
def atualizar_pagamento(id_pagamento: int, dados: PagamentoEntrada):
    resposta = supabase.table("pagamento").update(
        dados.model_dump(mode="json")
    ).eq("id_pagamento", id_pagamento).execute()
    if not resposta.data:
        raise HTTPException(404, "Pagamento não encontrado.")
    return resposta.data[0]


@router.delete("/{id_pagamento}", status_code=204)
def excluir_pagamento(id_pagamento: int):
    resposta = supabase.table("pagamento").delete().eq(
        "id_pagamento", id_pagamento
    ).execute()
    if not resposta.data:
        raise HTTPException(404, "Pagamento não encontrado.")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
