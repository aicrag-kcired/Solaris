
import os
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import APIRouter, HTTPException, Request, Response
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database import engine
from models import Usuario
from routes.auth import CadastroEntrada, LoginEntrada, password_hash

router = APIRouter(prefix="/api/auth", tags=["Conta do site"])

COOKIE_NAME = "solaris_session"
TEMPO_SESSAO = 3600


def criar_sessao(response: Response, usuario: Usuario):
    chave = os.getenv("JWT_SECRET_KEY")

    if not chave:
        raise HTTPException(
            status_code=503,
            detail="Autenticacao nao configurada"
        )

    expiracao = datetime.now(timezone.utc) + timedelta(hours=1)

    token = jwt.encode(
        {
            "sub": str(usuario.id_usuario),
            "exp": expiracao
        },
        chave,
        algorithm="HS256"
    )

    response.set_cookie(
        key=COOKIE_NAME,
        value=token,
        httponly=True,
        secure=False,  # Apenas para desenvolvimento local
        samesite="lax",
        max_age=TEMPO_SESSAO,
        path="/"
    )


def dados_publicos(usuario: Usuario):
    return {
        "nome": usuario.nome,
        "email": usuario.email
    }


@router.post("/cadastro", status_code=201)
def cadastrar(dados: CadastroEntrada, response: Response):
    email = str(dados.email).lower()

    with Session(engine) as db:
        existente = db.scalar(
            select(Usuario).where(Usuario.email == email)
        )

        if existente:
            raise HTTPException(
                status_code=409,
                detail="Este e-mail ja esta cadastrado"
            )

        usuario = Usuario(
            nome=dados.nome.strip(),
            email=email,
            senha_hash=password_hash.hash(dados.senha),
            tipo_usuario="cliente"
        )

        db.add(usuario)

        try:
            db.commit()
            db.refresh(usuario)
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=409,
                detail="Este e-mail ja esta cadastrado"
            )

        criar_sessao(response, usuario)

        return dados_publicos(usuario)


@router.post("/login")
def login(dados: LoginEntrada, response: Response):
    email = str(dados.email).lower()

    with Session(engine) as db:
        usuario = db.scalar(
            select(Usuario).where(Usuario.email == email)
        )

        if not usuario or not password_hash.verify(
            dados.senha,
            usuario.senha_hash
        ):
            raise HTTPException(
                status_code=401,
                detail="E-mail ou senha incorretos"
            )

        criar_sessao(response, usuario)

        return dados_publicos(usuario)


@router.get("/eu")
def minha_conta(request: Request):
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

    with Session(engine) as db:
        usuario = db.get(Usuario, id_usuario)

        if not usuario:
            raise HTTPException(
                status_code=401,
                detail="Usuario nao encontrado"
            )

        return dados_publicos(usuario)


@router.post("/sair")
def sair(response: Response):
    response.delete_cookie(
        key=COOKIE_NAME,
        path="/"
    )

    return {
        "mensagem": "Voce saiu da conta"
    }
