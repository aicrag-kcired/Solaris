
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from database import Base, engine
import models

from routes.clientes import router as clientes_router
from routes.simulacoes import router as simulacoes_router
from routes.cadastros import router as cadastros_router
from routes.servicos import router as servicos_router
from routes.auth import router as auth_router
from routes.site_auth import router as site_auth_router
from routes import solaris_ia

from calculos import router as simulador_publico_router


app = FastAPI(
    title="Solaris API",
    version="0.6.0",
    description="API do projeto Solaris com assistente virtual."
)


# ==========================================
# BANCO DE DADOS
# ==========================================

@app.on_event("startup")
def criar_tabelas():
    Base.metadata.create_all(bind=engine)


# ==========================================
# ROTAS DO BACKEND
# ==========================================

app.include_router(
    clientes_router,
    tags=["Clientes"]
)

app.include_router(
    simulacoes_router,
    tags=["Simulações"]
)

app.include_router(cadastros_router)
app.include_router(servicos_router)
app.include_router(auth_router)
app.include_router(site_auth_router)


# ==========================================
# SIMULADOR PÚBLICO
# ==========================================

app.include_router(
    simulador_publico_router
)


# ==========================================
# SOLARIS IA 2.0
# ==========================================

app.include_router(
    solaris_ia.router
)


# ==========================================
# SISTEMA
# ==========================================

@app.get("/", tags=["Sistema"])
def inicio():
    return {
        "mensagem": "Solaris funcionando!",
        "versao": "0.6.0",
        "ia": "Solaris IA 2.0"
    }


@app.get("/saude", tags=["Sistema"])
def saude():
    return {
        "status": "online"
    }


# ==========================================
# FRONTEND DO SOLARIS
# ==========================================

frontend_dir = (
    Path(__file__).resolve().parent.parent / "frontend"
)

app.mount(
    "/site",
    StaticFiles(
        directory=frontend_dir,
        html=True
    ),
    name="frontend"
)
