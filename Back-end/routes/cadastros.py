from fastapi import APIRouter, HTTPException, Query
from pydantic import create_model, ConfigDict
from sqlalchemy import inspect
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session
from database import engine
from models import Financiamento, Pagamento, Relatorio, Paineis, Instalacao, Chatbot, Tecnico
from datetime import date, datetime
from decimal import Decimal

router = APIRouter()

# Schemas gerados a partir das colunas atuais; não mudam o banco.
TIPOS = {int: int, str: str, Decimal: Decimal, date: date, datetime: datetime}

def schema_para(model):
    campos = {}
    for coluna in inspect(model).columns:
        if coluna.primary_key:
            continue
        tipo = coluna.type.python_type
        campos[coluna.key] = (TIPOS.get(tipo, tipo), ... if not coluna.nullable else None)
    return create_model(model.__name__ + 'Entrada', __config__=ConfigDict(extra='forbid'), **campos)

def adicionar_crud(nome, modelo, chave):
    Entrada = schema_para(modelo)

    def listar(limite: int = Query(default=100, ge=1, le=500), deslocamento: int = Query(default=0, ge=0)):
        with Session(engine) as db:
            return db.query(modelo).offset(deslocamento).limit(limite).all()

    def consultar(identificador: int):
        with Session(engine) as db:
            registro = db.get(modelo, identificador)
            if registro is None:
                raise HTTPException(404, 'Registro não encontrado')
            return registro

    def criar(dados: Entrada):
        with Session(engine) as db:
            registro = modelo(**dados.model_dump())
            db.add(registro)
            try:
                db.commit()
                db.refresh(registro)
            except IntegrityError:
                db.rollback()
                raise HTTPException(409, 'Dados duplicados ou relacionamento inválido')
            return registro

    def atualizar(identificador: int, dados: Entrada):
        with Session(engine) as db:
            registro = db.get(modelo, identificador)
            if registro is None:
                raise HTTPException(404, 'Registro não encontrado')
            for campo, valor in dados.model_dump().items():
                setattr(registro, campo, valor)
            try:
                db.commit()
                db.refresh(registro)
            except IntegrityError:
                db.rollback()
                raise HTTPException(409, 'Dados duplicados ou relacionamento inválido')
            return registro

    def apagar(identificador: int):
        with Session(engine) as db:
            registro = db.get(modelo, identificador)
            if registro is None:
                raise HTTPException(404, 'Registro não encontrado')
            db.delete(registro)
            try:
                db.commit()
            except IntegrityError:
                db.rollback()
                raise HTTPException(409, 'Registro vinculado a outros dados')
            return {'mensagem': 'Registro excluído'}

    # Nomes exclusivos para documentação OpenAPI.
    for func, sufixo in [(listar,'listar'),(consultar,'consultar'),(criar,'criar'),(atualizar,'atualizar'),(apagar,'apagar')]:
        func.__name__ = f'{sufixo}_{nome}'
    router.add_api_route(f'/{nome}', listar, methods=['GET'], tags=[nome.title()])
    router.add_api_route(f'/{nome}/{{identificador}}', consultar, methods=['GET'], tags=[nome.title()])
    router.add_api_route(f'/{nome}', criar, methods=['POST'], status_code=201, tags=[nome.title()])
    router.add_api_route(f'/{nome}/{{identificador}}', atualizar, methods=['PUT'], tags=[nome.title()])
    router.add_api_route(f'/{nome}/{{identificador}}', apagar, methods=['DELETE'], tags=[nome.title()])

for nome, modelo, chave in [
    ('financiamentos', Financiamento, 'id_financiamento'),
    ('pagamentos', Pagamento, 'id_pagamento'),
    ('relatorios', Relatorio, 'id_relatorio'),
    ('paineis', Paineis, 'id_paineis'),
    ('instalacoes', Instalacao, 'id_instalacao'),
    ('chatbots', Chatbot, 'id_chatbot'),
    ('tecnicos', Tecnico, 'id_tecnico'),
]:
    adicionar_crud(nome, modelo, chave)
