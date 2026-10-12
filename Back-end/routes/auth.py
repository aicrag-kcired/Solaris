import os
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr, Field
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database import engine
from models import Usuario


router = APIRouter(prefix="/auth", tags=["Autenticacao"])

password_hash = PasswordHash.recommended()


class CadastroEntrada(BaseModel):
    nome: str = Field(min_length=2, max_length=100)
    email: EmailStr
    senha: str = Field(min_length=8, max_length=128)


class LoginEntrada(BaseModel):
    email: EmailStr
    senha: str


@router.post("/cadastro", status_code=201)
def cadastrar(dados: CadastroEntrada):
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

        return {
            "mensagem": "Conta criada com sucesso",
            "id_usuario": usuario.id_usuario,
            "nome": usuario.nome
        }


@router.post("/login")
def login(dados: LoginEntrada):
    email = str(dados.email).lower()

    with Session(engine) as db:
        usuario = db.scalar(
            select(Usuario).where(Usuario.email == email)
        )

        if not usuario or not password_hash.verify(
            dados.senha, usuario.senha_hash
        ):
            raise HTTPException(
                status_code=401,
                detail="E-mail ou senha incorretos"
            )

        chave = os.getenv("JWT_SECRET_KEY")

        if not chave:
            raise HTTPException(
                status_code=503,
                detail="Autenticacao ainda nao configurada"
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

        return {
            "access_token": token,
            "token_type": "bearer"
        }