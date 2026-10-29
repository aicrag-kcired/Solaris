
import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from httpx import RequestError
from postgrest.exceptions import APIError

from controller.clientes import router as clientes_router
from controller.tecnico import router as tecnico_router
from controller.simulacao import router as simulacao_router
from controller.financiamento import router as financiamento_router
from controller.pagamento import router as pagamento_router
from controller.relatorio import router as relatorio_router
from controller.paineis import router as paineis_router
from controller.instalacao import router as instalacao_router
from controller.chatbot import router as chatbot_router

logger = logging.getLogger("uvicorn.error")

app = FastAPI(
    title="Solaris - API",
    description="Backend do Solaris com FastAPI e Supabase por HTTPS."
)

import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from httpx import RequestError
from postgrest.exceptions import APIError
from controller.clientes import router

logger = logging.getLogger("uvicorn.error")
app = FastAPI(
    title="Mercearia - API de Clientes",
    description="CRUD de clientes com Supabase por HTTPS.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:3000",
        "http://localhost:3000",
    ],
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type"],
)

app.include_router(router)

@app.exception_handler(APIError)
async def tratar_erro_supabase(request: Request, erro: APIError):
    logger.error("Erro na operação do Supabase: %s", erro)
    return JSONResponse(
        status_code=502,
        content={"detail": (
            "O Supabase recusou a operação. "
            "Confira a mensagem no terminal."
        )},
    )

@app.exception_handler(RequestError)
async def tratar_erro_rede(request: Request, erro: RequestError):
    logger.error("Falha de comunicação: %s", type(erro).__name__)
    return JSONResponse(
        status_code=503,
        content={"detail": (
            "Não foi possível acessar o Supabase. "
            "Verifique a conexão com a internet."
        )},
    )


app.include_router(clientes_router)
app.include_router(tecnico_router)
app.include_router(simulacao_router)
app.include_router(financiamento_router)
app.include_router(pagamento_router)
app.include_router(relatorio_router)
app.include_router(paineis_router)
app.include_router(instalacao_router)
app.include_router(chatbot_router)


@app.exception_handler(APIError)
async def tratar_erro_supabase(request: Request, erro: APIError):
    logger.error("Erro na operação do Supabase: %s", erro)
    return JSONResponse(
        status_code=502,
        content={
            "detail": (
                "O Supabase recusou a operação. "
                "Confira a mensagem no terminal."
            )
        },
    )


@app.exception_handler(RequestError)
async def tratar_erro_rede(request: Request, erro: RequestError):
    logger.error("Falha de comunicação: %s", type(erro).__name__)
    return JSONResponse(
        status_code=503,
        content={
            "detail": (
                "Não foi possível acessar o Supabase. "
                "Verifique a conexão com a internet."
            )
        },
    )
