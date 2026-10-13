from fastapi import FastAPI
from routes.clientes import router as clientes_router
from routes.simulacoes import router as simulacoes_router
from routes.cadastros import router as cadastros_router
from routes.servicos import router as servicos_router

app = FastAPI(title="Solaris API", version="0.2.0")

app.include_router(clientes_router, tags=["Clientes"])
app.include_router(simulacoes_router, tags=["Simulações"])
app.include_router(cadastros_router)
app.include_router(servicos_router)

@app.get("/", tags=["Sistema"])
def inicio():
    return {"mensagem": "Solaris funcionando!"}

@app.get("/saude", tags=["Sistema"])
def saude():
    return {"status": "online"}
