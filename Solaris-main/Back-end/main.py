from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controller.clientes import router as clientes_router
from controller.chatbot import router as chatbot_router
from controller.financiamento import router as financiamento_router
from controller.instalacao import router as instalacao_router
from controller.ordem_servico import router as ordem_servico_router
from controller.pagamento import router as pagamento_router
from controller.paineis import router as paineis_router
from controller.relatorio import router as relatorio_router
from controller.simulacao import router as simulacao_router
from controller.tecnico import router as tecnico_router

app = FastAPI(title="Solaris API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(clientes_router)
app.include_router(chatbot_router)
app.include_router(financiamento_router)
app.include_router(instalacao_router)
app.include_router(ordem_servico_router)
app.include_router(pagamento_router)
app.include_router(paineis_router)
app.include_router(relatorio_router)
app.include_router(simulacao_router)
app.include_router(tecnico_router)

@app.get("/")
def raiz():
    return {"mensagem": "API Solaris funcionando!"}