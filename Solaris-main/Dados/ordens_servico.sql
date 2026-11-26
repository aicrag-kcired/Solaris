
-- Solaris: tabela de ordens de serviço
-- Criação segura, sem apagar tabelas existentes.

CREATE TABLE IF NOT EXISTS public.ordens_servico (
    id_ordem_servico SERIAL PRIMARY KEY,

    id_cliente INTEGER NOT NULL
        REFERENCES public.clientes(id_cliente)
        ON DELETE RESTRICT,

    descricao TEXT,

    status VARCHAR(30) NOT NULL DEFAULT 'Pendente',

    data_ordem_servico TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
