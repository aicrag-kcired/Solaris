from fastapi import APIRouter, HTTPException, Response, status
from database import supabase
from models.clientes import ClienteEntrada, ClienteSaida

router = APIRouter(prefix="/clientes", tags=["Clientes"])

# POST: cadastrar cliente
@router.post("", response_model=ClienteSaida,
             status_code=status.HTTP_201_CREATED)
def cadastrar_cliente(dados: ClienteEntrada):
    conteudo = dados.model_dump(mode="json")
    resposta = (
        supabase.table("clientes")
        .insert(conteudo)
        .execute()
    )
    if not resposta.data:
        raise HTTPException(
            status_code=502,
            detail="O Supabase não retornou o cliente cadastrado.",
        )
    return resposta.data[0]

# GET: listar clientes
@router.get("", response_model=list[ClienteSaida])
def listar_clientes():
    resposta = (
        supabase.table("clientes")
        .select("*")
        .order("id_cliente")
        .execute()
    )
    return resposta.data
# GET: consultar um cliente pelo ID
@router.get("/{id_cliente}", response_model=ClienteSaida)
def consultar_cliente(id_cliente: int):
    resposta = (
        supabase.table("clientes")
        .select("*")
        .eq("id_cliente", id_cliente)
        .execute()
    )
    if not resposta.data:
        raise HTTPException(404, "Cliente não encontrado.")
    return resposta.data[0]


# PUT: atualizar um cliente
@router.put("/{id_cliente}", response_model=ClienteSaida)
def atualizar_cliente(id_cliente: int, dados: ClienteEntrada):
    conteudo = dados.model_dump(mode="json")
    resposta = (
        supabase.table("clientes")
        .update(conteudo)
        .eq("id_cliente", id_cliente)
        .execute()
    )
    if not resposta.data:
        raise HTTPException(404, "Cliente não encontrado.")
    return resposta.data[0]


# DELETE: excluir um cliente
@router.delete("/{id_cliente}",
               status_code=status.HTTP_204_NO_CONTENT)
def excluir_cliente(id_cliente: int):
    resposta = (
        supabase.table("clientes")
        .delete()
        .eq("id_cliente", id_cliente)
        .execute()
    )
    if not resposta.data:
        raise HTTPException(404, "Cliente não encontrado.")
    return Response(status_code=status.HTTP_204_NO_CONTENT)