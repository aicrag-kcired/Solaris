import os
import smtplib
import ssl
from email.message import EmailMessage
from urllib.parse import urlencode
import httpx
from fastapi import APIRouter, HTTPException, Header, Depends, Query
from pydantic import BaseModel, EmailStr, Field

router = APIRouter(tags=['Serviços externos'])

class EmailPedido(BaseModel):
    destinatario: EmailStr
    assunto: str = Field(min_length=1, max_length=160)
    mensagem: str = Field(min_length=1, max_length=5000)

def chave_admin(x_api_key: str | None = Header(default=None)):
    chave = os.getenv('SOLARIS_API_KEY')
    if not chave:
        raise HTTPException(503, 'Configure SOLARIS_API_KEY no .env para habilitar o envio')
    import secrets
    if not x_api_key or not secrets.compare_digest(x_api_key, chave):
        raise HTTPException(401, 'Chave inválida')

@router.get('/localizacao/buscar')
async def buscar_localizacao(endereco: str = Query(min_length=3, max_length=200)):
    # Nominatim é serviço de terceiros; use com moderação e conforme a política do provedor.
    headers = {'User-Agent': os.getenv('SOLARIS_USER_AGENT', 'SolarisProjetoEscolar/1.0 (configure-contato@example.com)')}
    try:
        async with httpx.AsyncClient(timeout=10.0, headers=headers) as client:
            resp = await client.get('https://nominatim.openstreetmap.org/search', params={'q': endereco, 'format':'jsonv2', 'limit':5})
            resp.raise_for_status()
        return [{'nome': i['display_name'], 'latitude': float(i['lat']), 'longitude': float(i['lon'])} for i in resp.json()]
    except (httpx.HTTPError, ValueError, KeyError):
        raise HTTPException(502, 'Serviço de localização indisponível')

@router.post('/emails/enviar', dependencies=[Depends(chave_admin)])
def enviar_email(pedido: EmailPedido):
    host = os.getenv('SMTP_HOST')
    usuario = os.getenv('SMTP_USER')
    senha = os.getenv('SMTP_PASSWORD')
    remetente = os.getenv('SMTP_FROM', usuario)
    if not all([host, usuario, senha, remetente]):
        raise HTTPException(503, 'Configure SMTP_HOST, SMTP_USER, SMTP_PASSWORD e SMTP_FROM')
    mensagem = EmailMessage()
    mensagem['From'] = remetente
    mensagem['To'] = str(pedido.destinatario)
    mensagem['Subject'] = pedido.assunto
    mensagem.set_content(pedido.mensagem)
    try:
        porta = int(os.getenv('SMTP_PORT', '587'))
        with smtplib.SMTP(host, porta, timeout=15) as smtp:
            smtp.starttls(context=ssl.create_default_context())
            smtp.login(usuario, senha)
            smtp.send_message(mensagem)
    except (smtplib.SMTPException, OSError, ValueError):
        raise HTTPException(502, 'Falha ao enviar e-mail; confira a configuração SMTP')
    return {'mensagem': 'E-mail enviado ao servidor SMTP'}
