DROP TABLE IF EXISTS public.chatbot CASCADE;
DROP TABLE IF EXISTS public.relatorio CASCADE;
DROP TABLE IF EXISTS public.paineis CASCADE;
DROP TABLE IF EXISTS public.instalacao CASCADE;
DROP TABLE IF EXISTS public.tecnico CASCADE;
DROP TABLE IF EXISTS public.pagamento CASCADE;
DROP TABLE IF EXISTS public.financiamento CASCADE;
DROP TABLE IF EXISTS public.simulacao CASCADE;
DROP TABLE IF EXISTS public.cliente CASCADE;
 
-- ---------------------------------------------------------------------
-- TABELA: cliente
-- ---------------------------------------------------------------------
CREATE TABLE public.cliente (
    id_cliente               SERIAL PRIMARY KEY,
    nome_cliente             VARCHAR(50)  NOT NULL,
    cpf_cliente              VARCHAR(14)  NOT NULL UNIQUE,   -- ex: 000.000.000-00
    rg_cliente                VARCHAR(20)  NOT NULL UNIQUE,
    numero_cliente           VARCHAR(20)  NOT NULL UNIQUE,   -- telefone
    email_cliente            VARCHAR(100) NOT NULL UNIQUE,
    endereco_cliente         VARCHAR(150) NOT NULL,
    tipo_imovel_cliente      VARCHAR(30)  NOT NULL,
    renda_mensal_cliente     DECIMAL(10,2) NOT NULL,
    data_de_cadastro_cliente TIMESTAMPTZ  NOT NULL DEFAULT now()
);
 
-- ---------------------------------------------------------------------
-- TABELA: simulacao
-- ---------------------------------------------------------------------
CREATE TABLE public.simulacao (
    id_simulacao                     SERIAL PRIMARY KEY,
    id_cliente                       INT NOT NULL REFERENCES public.cliente(id_cliente) ON DELETE CASCADE,
    consumo_energia                  DECIMAL(10,2) NOT NULL,
    valor_conta_energia              DECIMAL(10,2) NOT NULL,
    economia_estimada                DECIMAL(10,2) NOT NULL,
    data_simulacao                   TIMESTAMPTZ NOT NULL DEFAULT now(),
    valor_financiamento_estimado     DECIMAL(10,2) NOT NULL,
    valor_economia_mensal            DECIMAL(10,2) NOT NULL,
    valor_economia_anual             DECIMAL(10,2) NOT NULL,
    percentual_economia_primeiro_mes DECIMAL(5,2)  NOT NULL
);
 
-- ---------------------------------------------------------------------
-- TABELA: financiamento
-- ---------------------------------------------------------------------
CREATE TABLE public.financiamento (
    id_financiamento     SERIAL PRIMARY KEY,
    id_simulacao         INT NOT NULL REFERENCES public.simulacao(id_simulacao) ON DELETE CASCADE,
    valor_financiamento  DECIMAL(10,2) NOT NULL,
    data_financiamento   TIMESTAMPTZ NOT NULL DEFAULT now(),
    status_financiamento VARCHAR(30) NOT NULL
);
 
-- ---------------------------------------------------------------------
-- TABELA: pagamento
-- ---------------------------------------------------------------------
CREATE TABLE public.pagamento (
    id_pagamento        SERIAL PRIMARY KEY,
    id_financiamento    INT NOT NULL REFERENCES public.financiamento(id_financiamento) ON DELETE CASCADE,
    entidade_documento  VARCHAR(100) NOT NULL,
    data_pagamento      TIMESTAMPTZ NOT NULL DEFAULT now(),
    valor_pago          DECIMAL(10,2) NOT NULL
);
 
-- ---------------------------------------------------------------------
-- TABELA: tecnico
-- ---------------------------------------------------------------------
CREATE TABLE public.tecnico (
    id_tecnico         SERIAL PRIMARY KEY,
    nome_tecnico       VARCHAR(100) NOT NULL,
    local_instalacao   VARCHAR(150) NOT NULL
);
 
-- ---------------------------------------------------------------------
-- TABELA: instalacao
-- ---------------------------------------------------------------------
CREATE TABLE public.instalacao (
    id_instalacao        SERIAL PRIMARY KEY,
    id_financiamento     INT NOT NULL REFERENCES public.financiamento(id_financiamento) ON DELETE CASCADE,
    id_tecnico           INT NOT NULL REFERENCES public.tecnico(id_tecnico) ON DELETE RESTRICT,
    tecnico_responsavel  VARCHAR(100) NOT NULL,
    custo_instalacao     DECIMAL(10,2) NOT NULL,
    status_instalacao    VARCHAR(30) NOT NULL,
    data_instalacao      DATE NOT NULL
);
 
-- ---------------------------------------------------------------------
-- TABELA: paineis
-- ---------------------------------------------------------------------
CREATE TABLE public.paineis (
    id_paineis              SERIAL PRIMARY KEY,
    id_instalacao           INT NOT NULL REFERENCES public.instalacao(id_instalacao) ON DELETE CASCADE,
    rendimento               VARCHAR(50)  NOT NULL,
    data_instalacao          DATE NOT NULL,
    data_garantia            DATE NOT NULL,
    local_instalacao         VARCHAR(150) NOT NULL,
    responsavel_instalacao   VARCHAR(100) NOT NULL
);
 
-- ---------------------------------------------------------------------
-- TABELA: relatorio
-- ---------------------------------------------------------------------
CREATE TABLE public.relatorio (
    id_relatorio      SERIAL PRIMARY KEY,
    id_cliente        INT NOT NULL REFERENCES public.cliente(id_cliente) ON DELETE CASCADE,
    total_simulacao   INT NOT NULL,
    status_relatorio  VARCHAR(20) NOT NULL,
    historico         TEXT NOT NULL,
    total_pago        DECIMAL(10,2) NOT NULL
);
 
-- ---------------------------------------------------------------------
-- TABELA: chatbot
-- ---------------------------------------------------------------------
CREATE TABLE public.chatbot (
    id_chatbot           SERIAL PRIMARY KEY,
    id_cliente           INT NOT NULL REFERENCES public.cliente(id_cliente) ON DELETE CASCADE,
    mensagem_boas_vindas TEXT NOT NULL,
    versao               VARCHAR(20) NOT NULL,
    status_ativo         BOOLEAN NOT NULL DEFAULT TRUE,
    historico            TEXT NOT NULL,
    economia_estimada    INT NOT NULL,
    perguntas_usuario    TEXT NOT NULL,
    lembrete_prazo       VARCHAR(100) NOT NULL
);
 
-- ---------------------------------------------------------------------
-- ÍNDICES ADICIONAIS ÚTEIS
-- ---------------------------------------------------------------------
CREATE INDEX idx_simulacao_cliente        ON public.simulacao(id_cliente);
CREATE INDEX idx_financiamento_simulacao  ON public.financiamento(id_simulacao);
CREATE INDEX idx_pagamento_financiamento  ON public.pagamento(id_financiamento);
CREATE INDEX idx_instalacao_financiamento ON public.instalacao(id_financiamento);
CREATE INDEX idx_instalacao_tecnico       ON public.instalacao(id_tecnico);
CREATE INDEX idx_paineis_instalacao       ON public.paineis(id_instalacao);
CREATE INDEX idx_relatorio_cliente        ON public.relatorio(id_cliente);
CREATE INDEX idx_chatbot_cliente          ON public.chatbot(id_cliente);
 
-- ---------------------------------------------------------------------
-- ROW LEVEL SECURITY (RLS)
-- O Supabase expõe suas tabelas via API REST/GraphQL automaticamente.
-- Por segurança, é altamente recomendado habilitar RLS em todas as
-- tabelas. Sem políticas (POLICY) definidas, isso bloqueia todo acesso
-- via API até que você crie regras específicas (ex: só o dono dos
-- dados pode ler/escrever, ou acesso liberado para usuários
-- autenticados). Ajuste as políticas conforme a regra de negócio.
-- ---------------------------------------------------------------------
ALTER TABLE public.cliente       ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.simulacao     ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.financiamento ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.pagamento     ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.tecnico       ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.instalacao    ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.paineis       ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.relatorio     ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.chatbot       ENABLE ROW LEVEL SECURITY;
 
-- Exemplo de política (ajuste/remova conforme necessário):
-- Libera leitura para qualquer usuário autenticado (ajuste para o seu caso):
-- CREATE POLICY "Permitir leitura autenticada" ON public.cliente
--     FOR SELECT
--     TO authenticated
--     USING (true);
 
