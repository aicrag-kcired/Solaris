from fastapi import APIRouter, HTTPException, Response, status
from database import supabase
from models.ordem_servico import OrdemServicoEntrada, OrdemServicoSaida

router = APIRouter(prefix="/ordens_servico", tags=["Ordens de serviço"])
COLUNAS = "id_ordem_servico, data_ordem_servico, id_cliente, cliente:clientes(nome_cliente)"


def validar_cliente(id_cliente: int):
    resultado = (supabase.table("clientes")
                 .select("id_cliente, nome_cliente")
                 .eq("id_cliente", id_cliente).execute())
    if not resultado.data:
        raise HTTPException(400, "Cliente não encontrado. Consulte GET /clientes.")


def preparar_saida(registro: dict):
    cliente = registro.get("cliente")
    if not cliente:
        raise HTTPException(502, "Não foi possível consultar o cliente vinculado.")
    return {
        "id_ordem_servico": registro["id_ordem_servico"],
        "data_ordem_servico": registro["data_ordem_servico"],
        "id_cliente": registro["id_cliente"],
        "nome_cliente": cliente["nome_cliente"],
    }


def buscar_ordem(id_ordem_servico: int):
    resultado = (supabase.table("ordens_servico").select(COLUNAS)
                 .eq("id_ordem_servico", id_ordem_servico).execute())
    if not resultado.data:
        raise HTTPException(404, "Ordem de serviço não encontrada.")
    return preparar_saida(resultado.data[0])


@router.post("", response_model=OrdemServicoSaida, status_code=201)
def cadastrar_ordem(dados: OrdemServicoEntrada):
    validar_cliente(dados.id_cliente)
    resultado = (supabase.table("ordens_servico")
                 .insert(dados.model_dump(mode="json")).execute())
    if not resultado.data:
        raise HTTPException(502, "O Supabase não retornou a ordem cadastrada. Confira a listagem antes de repetir.")
    return buscar_ordem(resultado.data[0]["id_ordem_servico"])


@router.get("", response_model=list[OrdemServicoSaida])
def listar_ordens():
    resultado = (supabase.table("ordens_servico").select(COLUNAS)
                 .order("id_ordem_servico").execute())
    return [preparar_saida(item) for item in resultado.data]


@router.get("/{id_ordem_servico}", response_model=OrdemServicoSaida)
def consultar_ordem(id_ordem_servico: int):
    return buscar_ordem(id_ordem_servico)


@router.put("/{id_ordem_servico}", response_model=OrdemServicoSaida)
def atualizar_ordem(id_ordem_servico: int, dados: OrdemServicoEntrada):
    buscar_ordem(id_ordem_servico)
    validar_cliente(dados.id_cliente)
    resultado = (supabase.table("ordens_servico")
                 .update(dados.model_dump(mode="json"))
                 .eq("id_ordem_servico", id_ordem_servico).execute())
    if not resultado.data:
        raise HTTPException(404, "Ordem de serviço não encontrada.")
    return buscar_ordem(id_ordem_servico)


@router.delete("/{id_ordem_servico}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_ordem(id_ordem_servico: int):
    resultado = (supabase.table("ordens_servico").delete()
                 .eq("id_ordem_servico", id_ordem_servico).execute())
    if not resultado.data:
        raise HTTPException(404, "Ordem de serviço não encontrada.")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
