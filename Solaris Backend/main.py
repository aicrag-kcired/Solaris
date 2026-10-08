from fastapi import FastAPI
from routes.clientes import router as clientes_router

app = FastAPI()

app.include_router(clientes_router)


@app.get("/")
def inicio():
    return {"mensagem": "Solaris funcionando!"}