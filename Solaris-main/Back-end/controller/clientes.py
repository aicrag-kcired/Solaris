from fastapi import APIRouter, HTTPException, Response, status
from passlib.context import CryptContext
from database import supabase
from models.clientes import ClienteEntrada, ClienteSaida, ClienteLogin

router = APIRouter(prefix="/clientes", tags=["Clientes"])

# Configuração do criptografador de senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# POST: cadastrar cliente
@router.post(
    "",
    response_model=ClienteSaida,
    status_code=status.HTTP_201_CREATED
)
def cadastrar_cliente(dados: ClienteEntrada):
    conteudo = dados.model_dump(mode="json")

    # Criptografa a senha antes de salvar no banco
    conteudo["senha"] = pwd_context.hash(conteudo["senha"])

    resposta = (
        supabase.table("clientes")
        .insert(conteudo)
        .execute()
    )

    if not resposta.data:
        raise HTTPException(
            status_code=502,
            detail="O Supabase não retornou o cliente cadastrado."
        )

    return resposta.data[0]


# POST: login do cliente
@router.post("/login")
def login_cliente(dados: ClienteLogin):
    # Busca o cliente pelo e-mail
    resposta = (
        supabase.table("clientes")
        .select("*")
        .eq("email_cliente", dados.email_cliente)
        .execute()
    )

    if not resposta.data:
        raise HTTPException(
            status_code=401,
            detail="E-mail ou senha inválidos."
        )

    cliente = resposta.data[0]

    # Verifica se a senha digitada bate com a criptografada no banco
    if not pwd_context.verify(dados.senha, cliente["senha"]):
        raise HTTPException(
            status_code=401,
            detail="E-mail ou senha inválidos."
        )

    # Remove a senha da resposta por segurança
    cliente.pop("senha", None)
    
    return cliente


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
        raise HTTPException(
            status_code=404,
            detail="Cliente não encontrado."
        )

    return resposta.data[0]


# PUT: atualizar um cliente
@router.put("/{id_cliente}", response_model=ClienteSaida)
def atualizar_cliente(id_cliente: int, dados: ClienteEntrada):
    conteudo = dados.model_dump(mode="json")

    # Criptografa a nova senha ao atualizar
    conteudo["senha"] = pwd_context.hash(conteudo["senha"])

    resposta = (
        supabase.table("clientes")
        .update(conteudo)
        .eq("id_cliente", id_cliente)
        .execute()
    )

    if not resposta.data:
        raise HTTPException(
            status_code=404,
            detail="Cliente não encontrado."
        )

    return resposta.data[0]


# DELETE: excluir um cliente
@router.delete(
    "/{id_cliente}",
    status_code=status.HTTP_204_NO_CONTENT
)
def excluir_cliente(id_cliente: int):

    # Verificar se o cliente existe
    cliente = (
        supabase.table("clientes")
        .select("id_cliente")
        .eq("id_cliente", id_cliente)
        .execute()
    )

    if not cliente.data:
        raise HTTPException(
            status_code=404,
            detail="Cliente não encontrado."
        )

    # Verificar se o cliente possui ordens de serviço
    ordens = (
        supabase.table("ordens_servico")
        .select("id_ordem_servico")
        .eq("id_cliente", id_cliente)
        .limit(1)
        .execute()
    )

    if ordens.data:
        raise HTTPException(
            status_code=409,
            detail=(
                "Não é possível excluir este cliente "
                "porque ele possui ordens de serviço."
            )
        )

    # Excluir cliente caso não tenha ordens vinculadas
    resposta = (
        supabase.table("clientes")
        .delete()
        .eq("id_cliente", id_cliente)
        .execute()
    )

    if not resposta.data:
        raise HTTPException(
            status_code=404,
            detail="Cliente não encontrado."
        )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )