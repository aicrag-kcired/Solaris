
import os

import jwt
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from database import engine
from models import Cliente, Usuario
from schemas import ClienteSchema
from routes.site_auth import COOKIE_NAME


def exigir_administrador(request: Request):
    token = request.cookies.get(COOKIE_NAME)
    chave = os.getenv("JWT_SECRET_KEY")

    if not token or not chave:
        raise HTTPException(
            status_code=401,
            detail="Voce precisa entrar na sua conta"
        )

    try:
        dados = jwt.decode(
            token,
            chave,
            algorithms=["HS256"]
        )
        id_usuario = int(dados["sub"])

    except (jwt.PyJWTError, KeyError, ValueError, TypeError):
        raise HTTPException(
            status_code=401,
            detail="Sessao invalida ou expirada"
        )

    with Session(engine) as session:
        usuario = session.get(Usuario, id_usuario)

        if not usuario:
            raise HTTPException(
                status_code=401,
                detail="Usuario nao encontrado"
            )

        if usuario.tipo_usuario != "admin":
            raise HTTPException(
                status_code=403,
                detail="Acesso permitido apenas para administradores"
            )


router = APIRouter(
    dependencies=[Depends(exigir_administrador)]
)


@router.get("/clientes")
def listar_clientes():
    with Session(engine) as session:
        clientes = session.query(Cliente).all()
        return clientes


@router.post("/clientes")
def cadastrar_cliente(dados: ClienteSchema):
    with Session(engine) as session:
        novo_cliente = Cliente(**dados.model_dump())

        session.add(novo_cliente)
        session.commit()
        session.refresh(novo_cliente)

        return novo_cliente
