from decimal import Decimal
from pydantic import BaseModel, Field


class ChatbotEntrada(BaseModel):
    mensagem_boas_vindas: str = Field(min_length=1)
    versao: str = Field(min_length=1, max_length=20)
    status_ativo: str = Field(min_length=1, max_length=20)
    historico: str = Field(min_length=1)
    economia_estimada: Decimal = Field(ge=0)
    perguntas_usuario: str = Field(min_length=1)
    lembrete_prazo: str = Field(min_length=1, max_length=255)


class ChatbotSaida(ChatbotEntrada):
    id_chatbot: int
