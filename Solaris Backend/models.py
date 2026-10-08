from sqlalchemy import Column, Integer, String, Numeric, DateTime, Date
from database import Base


class Cliente(Base):
    __tablename__ = "cliente"

    id_cliente = Column(Integer, primary_key=True, autoincrement=True)

    nome_cliente = Column(String(50), nullable=False)
    cpf_cliente = Column(Integer, nullable=False, unique=True)
    rg_cliente = Column(Integer, nullable=False, unique=True)
    numero_cliente = Column(Integer, nullable=False, unique=True)
    email_cliente = Column(String(100), nullable=False, unique=True)
    endereco_cliente = Column(String(150), nullable=False)
    tipo_imovel_cliente = Column(String(30), nullable=False)
    renda_mensal_cliente = Column(Numeric(10, 2), nullable=False)
    data_de_cadastro_cliente = Column(DateTime, nullable=False)


class Simulacao(Base):
    __tablename__ = "simulacao"

    id_simulacao = Column(Integer, primary_key=True, autoincrement=True)

    consumo_energia = Column(Numeric(10, 2), nullable=False)
    valor_conta_energia = Column(Numeric(10, 2), nullable=False)
    economia_estimada = Column(Numeric(10, 2), nullable=False)
    data_simulacao = Column(DateTime, nullable=False)
    financiamento = Column(Numeric(10, 2), nullable=False)
    id_usuario = Column(String, nullable=False, unique=True)
    valor_economia_mensal = Column(Numeric(10, 2), nullable=False)
    valor_economia_anual = Column(Numeric(10, 2), nullable=False)
    percentual_economia_primeiro_mes = Column(Numeric(10, 2), nullable=False)


class Financiamento(Base):
    __tablename__ = "financiamento"

    id_financiamento = Column(Integer, primary_key=True, autoincrement=True)

    valor_financiamento = Column(Numeric(10, 2), nullable=False)
    data_financiamento = Column(DateTime, nullable=False)
    status_financiamento = Column(String, nullable=False)


class Pagamento(Base):
    __tablename__ = "pagamento"

    id_pagamento = Column(Integer, primary_key=True, autoincrement=True)

    entidade_documento = Column(String, nullable=False)
    data_pagamento = Column(DateTime, nullable=False)
    valor_pago = Column(Numeric(10, 2), nullable=False)


class Relatorio(Base):
    __tablename__ = "relatorio"

    id_relatorio = Column(Integer, primary_key=True, autoincrement=True)

    total_simulacao = Column(String, nullable=False)
    status_relatorio = Column(String, nullable=False)
    historico = Column(String, nullable=False)
    total_pago = Column(String, nullable=False)


class Paineis(Base):
    __tablename__ = "paineis"

    id_paineis = Column(Integer, primary_key=True, autoincrement=True)

    rendimento = Column(String, nullable=False)
    data_instalacao = Column(Date, nullable=False)
    data_garantia = Column(Date, nullable=False)
    local_instalacao = Column(String, nullable=False)
    responsavel_instalacao = Column(String, nullable=False)


class Instalacao(Base):
    __tablename__ = "instalacao"

    id_instalacao = Column(Integer, primary_key=True, autoincrement=True)

    tecnico_responsavel = Column(String, nullable=False)
    custo_instalacao = Column(Numeric(10, 2), nullable=False)
    status_instalacao = Column(String, nullable=False)
    data_instalacao = Column(Date, nullable=False)
    id_tecnico = Column(Integer, nullable=False, unique=True)


class Chatbot(Base):
    __tablename__ = "chatbot"

    id_chatbot = Column(Integer, primary_key=True, autoincrement=True)

    mensagem_boas_vindas = Column(String, nullable=False)
    versao = Column(String, nullable=False)
    status_ativo = Column(String, nullable=False)
    historico = Column(String, nullable=False)
    economia_estimada = Column(Integer, nullable=False)
    perguntas_usuario = Column(String, nullable=False)
    lembrete_prazo = Column(Integer, nullable=False)


class Tecnico(Base):
    __tablename__ = "tecnico"

    id_tecnico = Column(Integer, primary_key=True, autoincrement=True)

    local_instalacao = Column(String, nullable=False)