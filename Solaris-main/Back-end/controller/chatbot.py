
from fastapi import APIRouter, HTTPException, Response, status
from database import supabase
from models.chatbot import ChatbotEntrada, ChatbotSaida

router = APIRouter(prefix="/chatbot", tags=["Chatbot"])


@router.post("", response_model=ChatbotSaida, status_code=201)
def cadastrar_chatbot(dados: ChatbotEntrada):
    resposta = supabase.table("chatbot").insert(
        dados.model_dump(mode="json")
    ).execute()
    if not resposta.data:
        raise HTTPException(502, "O Supabase não retornou o registro.")
    return resposta.data[0]


@router.get("", response_model=list[ChatbotSaida])
def listar_chatbot():
    resposta = supabase.table("chatbot").select("*").order(
        "id_chatbot"
    ).execute()
    return resposta.data


@router.get("/{id_chatbot}", response_model=ChatbotSaida)
def consultar_chatbot(id_chatbot: int):
    resposta = supabase.table("chatbot").select("*").eq(
        "id_chatbot", id_chatbot
    ).execute()
    if not resposta.data:
        raise HTTPException(404, "Registro não encontrado.")
    return resposta.data[0]


@router.put("/{id_chatbot}", response_model=ChatbotSaida)
def atualizar_chatbot(id_chatbot: int, dados: ChatbotEntrada):
    resposta = supabase.table("chatbot").update(
        dados.model_dump(mode="json")
    ).eq("id_chatbot", id_chatbot).execute()
    if not resposta.data:
        raise HTTPException(404, "Registro não encontrado.")
    return resposta.data[0]


@router.delete("/{id_chatbot}", status_code=204)
def excluir_chatbot(id_chatbot: int):
    resposta = supabase.table("chatbot").delete().eq(
        "id_chatbot", id_chatbot
    ).execute()
    if not resposta.data:
        raise HTTPException(404, "Registro não encontrado.")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
