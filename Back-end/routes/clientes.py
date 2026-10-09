from fastapi import APIRouter
from sqlalchemy.orm import Session
from database import engine
from models import Cliente
from schemas import ClienteSchema

router = APIRouter()


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