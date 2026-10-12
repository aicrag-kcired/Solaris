
# ==========================================================
# SOLARIS IA - ASSISTENTE VIRTUAL COMPLETA
# Projeto Solaris
# Python + FastAPI
#
# Funciona sem APIs pagas.
# Compatível com o app.js que já está funcionando.
#
# Rota principal:
# POST /api/ia/perguntar
#
# Entrada:
# {"mensagem": "Como faço login?", "contexto": null}
#
# Saída:
# {
#   "resposta": "...",
#   "assunto": "login",
#   "tipo": "conhecimento",
#   "sugestoes": ["...", "...", "..."],
#   "pagina": "conta"
# }
# ==========================================================

import re
import unicodedata
from difflib import SequenceMatcher
from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel, Field


router = APIRouter(
    prefix="/api/ia",
    tags=["Solaris IA"]
)


class Pergunta(BaseModel):
    mensagem: str = Field(
        ...,
        min_length=1,
        max_length=500
    )
    contexto: Optional[str] = None


# ==========================================================
# TRATAMENTO DAS PERGUNTAS
# ==========================================================

def normalizar(texto):
    texto = str(texto or "").lower().strip()

    texto = unicodedata.normalize("NFKD", texto)

    texto = "".join(
        letra for letra in texto
        if not unicodedata.combining(letra)
    )

    texto = re.sub(r"[^a-z0-9\s]", " ", texto)

    return " ".join(texto.split())


STOPWORDS = {
    "a", "o", "as", "os", "um", "uma",
    "de", "do", "da", "dos", "das",
    "e", "ou", "em", "no", "na",
    "nos", "nas", "para", "por",
    "com", "que", "qual", "quais",
    "como", "onde", "quando", "quanto",
    "eu", "voce", "voces", "me",
    "meu", "minha", "seu", "sua",
    "ele", "ela", "isso", "isto",
    "esse", "essa", "tem", "ter",
    "ser", "fazer", "faz", "posso",
    "quero", "queria", "preciso",
    "pode", "poderia", "sobre",
    "aqui", "ai", "la", "site",
    "solaris", "favor", "porfavor",
    "pra", "pro", "ta", "tipo"
}


def palavras(texto):
    return {
        p for p in normalizar(texto).split()
        if p not in STOPWORDS and len(p) > 2
    }


def semelhanca(a, b):
    return SequenceMatcher(None, a, b).ratio()


def palavras_parecidas(a, b):
    if a == b:
        return True

    if min(len(a), len(b)) < 4:
        return False

    return semelhanca(a, b) >= 0.84


def sobreposicao(a, b):
    """
    Compara palavras importantes e aceita
    pequenos erros de digitação.
    """
    pa = palavras(a)
    pb = palavras(b)

    if not pa or not pb:
        return 0

    usadas = set()
    iguais = 0

    for palavra_a in pa:
        for palavra_b in pb:
            if palavra_b in usadas:
                continue

            if palavras_parecidas(palavra_a, palavra_b):
                iguais += 1
                usadas.add(palavra_b)
                break

    cobertura = iguais / len(pb)
    precisao = iguais / len(pa)

    return cobertura * 0.65 + precisao * 0.35


# ==========================================================
# BASE DE CONHECIMENTO
# ==========================================================

BASE = {}


def adicionar(
    codigo,
    titulo,
    exemplos,
    resposta,
    pagina=None,
    categoria="geral"
):
    BASE[codigo] = {
        "titulo": titulo,
        "exemplos": [
            normalizar(x)
            for x in exemplos.split("|")
        ],
        "resposta": resposta.strip(),
        "pagina": pagina,
        "categoria": categoria
    }


# ==========================================================
# PROJETO SOLARIS
# ==========================================================

adicionar(
    "projeto",
    "O que é o Solaris",
    "o que e o solaris|o que e o projeto solaris|"
    "me apresente o solaris|sobre o projeto|"
    "me explique o projeto|quem sao voces|"
    "o que voces fazem|para que serve o solaris",
    """
🌻 O Solaris é um projeto escolar que reúne
tecnologia, programação e energia solar.

Nossa plataforma possui uma loja demonstrativa,
um simulador educativo, informações sobre energia
solar e esta assistente virtual.

O projeto também explora um protótipo de
acompanhamento solar desenvolvido por estudantes.
""",
    "sobre",
    "projeto"
)

adicionar(
    "objetivo",
    "Objetivo do Solaris",
    "qual o objetivo do projeto|objetivo do solaris|"
    "qual a finalidade|qual a missao|"
    "porque criaram o solaris|o que querem alcançar",
    """
☀️ Nosso objetivo é aprender na prática e
mostrar como tecnologia e sustentabilidade
podem trabalhar juntas.

Queremos apresentar uma plataforma educativa
e explorar um protótipo relacionado à
captação de energia solar.
""",
    "sobre",
    "projeto"
)

adicionar(
    "equipe",
    "Equipe Solaris",
    "quem criou o solaris|quem desenvolveu o projeto|"
    "quem faz parte da equipe|integrantes do projeto|"
    "quem sao os criadores|equipe do solaris",
    """
👥 O Solaris é desenvolvido por estudantes.

O trabalho envolve programação,
desenvolvimento de sistemas e mecânica.

Os nomes e funções dos integrantes devem
ser consultados na apresentação oficial
do projeto.
""",
    "sobre",
    "projeto"
)

adicionar(
    "tracker",
    "Rastreador solar",
    "o que e rastreador solar|o que e tracker|"
    "painel que acompanha o sol|painel que gira|"
    "rastreamento solar|painel movel|"
    "prototipo do solaris|como funciona o tracker",
    """
🌞 Um rastreador solar é um mecanismo que
ajusta a posição de um painel para acompanhar
o movimento aparente do Sol.

A ideia é melhorar a orientação do painel
durante o dia.

O Solaris explora esse conceito em um
protótipo escolar. Os resultados reais
dependem de testes e medições.
""",
    "sobre",
    "projeto"
)

adicionar(
    "diferencial",
    "Diferencial do Solaris",
    "qual o diferencial|o que tem de diferente|"
    "qual a inovacao|porque o projeto e especial|"
    "o que torna o solaris unico",
    """
🚀 O diferencial do Solaris é combinar
uma plataforma digital educativa com
o estudo de um protótipo solar.

O visitante pode aprender sobre energia,
explorar produtos demonstrativos, utilizar
o simulador e conversar comigo.
""",
    "sobre",
    "projeto"
)

adicionar(
    "backend",
    "Backend do projeto",
    "o que e backend|como funciona o backend|"
    "backend do solaris|qual linguagem do servidor|"
    "servidor python|como funciona a api",
    """
💻 O backend é a parte do sistema responsável
por processar dados e executar regras.

No Solaris utilizamos Python e FastAPI.

O backend atende recursos como autenticação,
simulação e respostas da assistente virtual.
""",
    None,
    "projeto"
)

adicionar(
    "frontend",
    "Frontend do projeto",
    "o que e frontend|frontend do solaris|"
    "como fizeram o site|quais linguagens do site|"
    "html css javascript|como funciona a interface",
    """
🖥️ O frontend é a parte visual do site.

O Solaris utiliza HTML, CSS e JavaScript
para apresentar as páginas e permitir
a interação dos visitantes.
""",
    None,
    "projeto"
)

# ==========================================================
# CONTA, LOGIN E CADASTRO
# ==========================================================

adicionar(
    "login_erro",
    "Erro no login",
    "nao consigo fazer login|nao consigo entrar|"
    "login nao funciona|erro no login|"
    "senha incorreta|email incorreto|"
    "acesso negado|nao entra na minha conta",
    """
⚠️ Se você não consegue entrar:

1. Confira o e-mail informado.
2. Verifique se a senha foi digitada corretamente.
3. Confira sua conexão com a internet.
4. Atualize a página e tente novamente.

Se o erro continuar, procure a equipe
responsável pelo Solaris.

Nunca envie sua senha pelo chat.
""",
    "conta",
    "conta"
)

adicionar(
    "login",
    "Como fazer login",
    "como fazer login|quero fazer login|"
    "como entrar na conta|onde fica o login|"
    "acessar minha conta|entrar no solaris|"
    "fazer login com email|entrar com senha",
    """
🔐 Para fazer login no Solaris:

1. Abra a página Minha Conta.
2. Escolha a opção Entrar.
3. Digite seu e-mail.
4. Digite sua senha.
5. Clique em Entrar na conta.

Use o botão abaixo para abrir a página.
""",
    "conta",
    "conta"
)

adicionar(
    "cadastro",
    "Criar uma conta",
    "como criar conta|como fazer cadastro|"
    "quero me cadastrar|registrar usuario|"
    "criar usuario|nao tenho conta|"
    "primeiro acesso|fazer uma conta",
    """
🌻 Para criar uma conta:

1. Abra Minha Conta.
2. Selecione Criar Conta.
3. Preencha os dados solicitados.
4. Escolha uma senha segura.
5. Confirme o cadastro.

Depois você poderá acessar sua conta.
""",
    "conta",
    "conta"
)

adicionar(
    "senha",
    "Esqueci a senha",
    "esqueci minha senha|perdi a senha|"
    "recuperar senha|redefinir senha|"
    "esqueci a senha do login|"
    "nao lembro minha senha|trocar senha",
    """
🔑 A recuperação automática de senha
ainda não está disponível nesta versão
do Solaris.

Se precisar recuperar o acesso,
procure a equipe responsável.

Por segurança, nunca compartilhe
sua senha comigo ou com outras pessoas.
""",
    "conta",
    "conta"
)

adicionar(
    "logout",
    "Sair da conta",
    "como sair da conta|como fazer logout|"
    "desconectar conta|encerrar sessao|"
    "deslogar|sair do perfil",
    """
🚪 Para sair:

1. Abra Minha Conta.
2. Clique em Sair da conta.

Isso encerra sua sessão no site.
""",
    "conta",
    "conta"
)

adicionar(
    "dados",
    "Dados da conta",
    "editar perfil|alterar email|"
    "mudar nome|atualizar cadastro|"
    "excluir minha conta|apagar minha conta|"
    "mudar dados pessoais",
    """
👤 A interface atual ainda não oferece
todas as opções de edição ou exclusão
de dados da conta.

Para solicitar ajuda com seus dados,
procure a equipe responsável pelo projeto.

Não compartilhe informações pessoais
sensíveis pelo chat.
""",
    "conta",
    "conta"
)

# ==========================================================
# LOJA E CARRINHO
# ==========================================================

adicionar(
    "loja",
    "Loja Solaris",
    "como funciona a loja|abrir loja|"
    "quero ver produtos|catalogo de produtos|"
    "onde ficam os produtos|o que vende|"
    "mostrar loja|produtos disponiveis",
    """
🛒 A Loja Solaris apresenta produtos
demonstrativos relacionados à energia solar.

Você pode explorar a vitrine,
pesquisar produtos e testar o carrinho.

Os preços são fictícios.
Não realizamos vendas reais.
""",
    "loja",
    "loja"
)

adicionar(
    "comprar",
    "Como comprar",
    "como comprar|quero comprar|"
    "fazer uma compra|finalizar compra|"
    "como fazer pedido|comprar painel|"
    "comprar produto|adquirir produto",
    """
🛍️ A loja do Solaris ainda é demonstrativa.

Você pode selecionar produtos e adicioná-los
ao carrinho, mas não é possível concluir
uma compra real.

Não existe checkout com pagamento nesta versão.
""",
    "loja",
    "loja"
)

adicionar(
    "carrinho",
    "Carrinho",
    "como usar carrinho|adicionar ao carrinho|"
    "colocar produto no carrinho|abrir carrinho|"
    "ver meus produtos|onde fica o carrinho|"
    "guardar produto",
    """
🛒 Para usar o carrinho:

1. Entre na Loja.
2. Escolha um produto.
3. Clique em Adicionar ao carrinho.
4. Abra a página Carrinho.

O carrinho é demonstrativo.
""",
    "carrinho",
    "loja"
)

adicionar(
    "remover",
    "Remover produto",
    "remover produto do carrinho|"
    "tirar item do carrinho|"
    "excluir produto do carrinho|"
    "diminuir quantidade|"
    "aumentar quantidade|"
    "mudar quantidade",
    """
➕ No carrinho, utilize os botões
de aumentar e diminuir quantidade.

Ao diminuir a quantidade até zero,
o produto é removido.

Nenhuma compra real será realizada.
""",
    "carrinho",
    "loja"
)

adicionar(
    "precos",
    "Preços",
    "quanto custa o painel|"
    "qual o preco dos produtos|"
    "precos sao reais|"
    "valor dos paineis|"
    "quanto custa um produto|"
    "precos da loja",
    """
💰 Os preços exibidos na Loja Solaris
são fictícios e servem apenas para
demonstrar o funcionamento do site.

Eles não são ofertas ou orçamentos reais.
""",
    "loja",
    "loja"
)

adicionar(
    "pagamento",
    "Pagamento",
    "aceita pix|aceita cartao|"
    "formas de pagamento|"
    "como pagar|posso parcelar|"
    "aceita boleto|pagamento",
    """
💳 A Loja Solaris não processa
pagamentos reais.

Pix, cartão, boleto e parcelamento
não estão disponíveis nesta versão.
""",
    "loja",
    "loja"
)

adicionar(
    "frete",
    "Frete e entrega",
    "quanto custa o frete|"
    "faz entrega|prazo de entrega|"
    "quando chega o produto|"
    "envio de produtos|"
    "entrega na minha cidade",
    """
📦 Como a loja é demonstrativa,
não existem entregas reais.

Também não há cálculo de frete
ou previsão de envio.
""",
    "loja",
    "loja"
)

adicionar(
    "estoque",
    "Estoque",
    "tem em estoque|produto disponivel|"
    "acabou estoque|quando chega estoque|"
    "tem painel para vender|"
    "disponibilidade do produto",
    """
📦 O Solaris não possui estoque
comercial confirmado.

Os produtos da loja são exemplos
utilizados na demonstração do sistema.
""",
    "loja",
    "loja"
)

adicionar(
    "pedidos",
    "Pedidos",
    "onde esta meu pedido|"
    "acompanhar pedido|historico de compras|"
    "meus pedidos|rastrear compra|"
    "status do pedido",
    """
📋 Ainda não há acompanhamento
de pedidos reais no Solaris.

A loja não realiza vendas nesta versão.
""",
    "conta",
    "loja"
)

adicionar(
    "garantia",
    "Garantia",
    "qual a garantia|"
    "produto tem garantia|"
    "garantia do painel|"
    "quanto tempo de garantia",
    """
🛡️ Como os produtos são demonstrativos,
não existem condições comerciais
de garantia definidas.

Em compras reais, a garantia depende
do fabricante e do vendedor.
""",
    "loja",
    "loja"
)

# ==========================================================
# SIMULADOR
# ==========================================================

adicionar(
    "simulador",
    "Como usar o simulador",
    "como usar simulador|abrir simulador|"
    "fazer simulacao|calcular economia|"
    "simular conta de luz|"
    "como funciona o simulador|"
    "onde calculo economia",
    """
📊 Para utilizar o simulador:

1. Abra a página Simulador.
2. Informe o valor mensal da sua conta.
3. Clique em Calcular estimativa.
4. Confira o resultado.

A simulação é educativa e simplificada.
""",
    "simulador",
    "simulador"
)

adicionar(
    "economia",
    "Economia solar",
    "quanto posso economizar|"
    "energia solar economiza|"
    "economia na conta de luz|"
    "reduzir conta de energia|"
    "economia mensal|economia anual",
    """
💰 A energia solar pode reduzir
os gastos com eletricidade.

A economia real depende de consumo,
geração, tarifas e regras locais.

O simulador Solaris utiliza uma hipótese
simplificada de redução de 80%.

Isso não é uma garantia de economia.
""",
    "simulador",
    "simulador"
)

adicionar(
    "percentual",
    "Percentual de 80%",
    "porque 80 por cento|"
    "por que usa 80|"
    "economia de 80 por cento|"
    "simulador garante 80|"
    "percentual do simulador",
    """
📈 O percentual de 80% é uma
hipótese fixa para fins educativos.

Ele não representa um resultado
garantido para instalações reais.

Uma estimativa técnica exigiria
dados adicionais sobre consumo,
localização, tarifas e equipamentos.
""",
    "simulador",
    "simulador"
)

adicionar(
    "retorno",
    "Retorno do investimento",
    "tempo de retorno|"
    "quando se paga|"
    "payback solar|"
    "retorno do investimento|"
    "em quantos anos recupero dinheiro|"
    "vale a pena investir",
    """
📉 O retorno do investimento depende
do custo de instalação, geração,
consumo e tarifas de energia.

O simulador atual não calcula
um prazo real de retorno financeiro.
""",
    "simulador",
    "simulador"
)

# ==========================================================
# ENERGIA SOLAR
# ==========================================================

adicionar(
    "energia_solar",
    "Energia solar",
    "o que e energia solar|"
    "como funciona energia solar|"
    "explique energia solar|"
    "energia fotovoltaica|"
    "energia do sol|"
    "como o sol gera eletricidade",
    """
☀️ A energia solar utiliza
a radiação emitida pelo Sol.

Nos sistemas fotovoltaicos,
os painéis transformam a luz
em eletricidade.

Essa eletricidade pode ser utilizada
em casas, empresas e outros locais.
""",
    None,
    "energia"
)

adicionar(
    "painel",
    "Painel solar",
    "o que e painel solar|"
    "como funciona painel solar|"
    "o que e placa solar|"
    "modulo fotovoltaico|"
    "como painel gera energia|"
    "para que serve painel",
    """
🔆 O painel solar fotovoltaico
possui células que convertem
a luz solar em eletricidade.

A eletricidade gerada é inicialmente
em corrente contínua.

Em muitos sistemas, um inversor
realiza a conversão para corrente
alternada.
""",
    None,
    "energia"
)

adicionar(
    "inversor",
    "Inversor solar",
    "o que e inversor|"
    "para que serve inversor|"
    "como funciona inversor|"
    "inversor fotovoltaico|"
    "corrente continua e alternada|"
    "funcao do inversor",
    """
⚡ O inversor converte a corrente
contínua dos painéis em corrente
alternada compatível com a instalação.

Dependendo do equipamento,
ele também pode monitorar a geração.
""",
    None,
    "energia"
)

adicionar(
    "bateria",
    "Bateria solar",
    "o que e bateria solar|"
    "precisa de bateria|"
    "armazenar energia solar|"
    "como guardar energia|"
    "bateria fotovoltaica|"
    "energia armazenada",
    """
🔋 As baterias armazenam energia
para utilização posterior.

Nem todo sistema solar precisa
de baterias.

A necessidade depende do tipo
de instalação e do objetivo
do sistema.
""",
    None,
    "energia"
)

adicionar(
    "noite",
    "Energia solar à noite",
    "funciona a noite|"
    "painel gera energia de noite|"
    "energia solar no escuro|"
    "como funciona sem sol|"
    "energia durante a noite",
    """
🌙 Painéis fotovoltaicos comuns
não produzem energia significativa
durante a noite.

A eletricidade pode vir da rede
ou de baterias, dependendo
do sistema instalado.
""",
    None,
    "energia"
)

adicionar(
    "chuva",
    "Energia solar na chuva",
    "funciona na chuva|"
    "painel funciona chovendo|"
    "energia solar na chuva|"
    "funciona nublado|"
    "dia nublado|"
    "painel sem sol direto",
    """
🌧️ Sim!

Os painéis podem produzir energia
em dias nublados ou chuvosos.

Porém, a geração geralmente é menor
do que em dias com boa iluminação.
""",
    None,
    "energia"
)

adicionar(
    "calor",
    "Temperatura dos painéis",
    "painel precisa de calor|"
    "quanto mais quente melhor|"
    "energia solar no frio|"
    "frio atrapalha painel|"
    "temperatura do painel",
    """
🌡️ Os painéis fotovoltaicos
precisam principalmente de luz,
não de calor.

Temperaturas muito altas podem
reduzir a eficiência de muitos módulos.
""",
    None,
    "energia"
)

adicionar(
    "sombra",
    "Sombra nos painéis",
    "sombra atrapalha|"
    "painel na sombra|"
    "arvore faz sombra|"
    "sombreamento solar|"
    "placa precisa de sol",
    """
🌳 O sombreamento pode reduzir
a produção de energia elétrica.

Por isso, a posição dos painéis
deve ser avaliada antes
da instalação.
""",
    None,
    "energia"
)

adicionar(
    "instalacao",
    "Instalação solar",
    "como instalar painel|"
    "quem instala energia solar|"
    "instalacao fotovoltaica|"
    "posso instalar sozinho|"
    "colocar placa no telhado|"
    "requisitos de instalacao",
    """
🏠 A instalação exige avaliação
da estrutura, sombreamento,
equipamentos e projeto elétrico.

Por envolver eletricidade e
trabalho em altura, deve ser
planejada e executada por
profissionais qualificados.

O Solaris não oferece
instalação comercial.
""",
    None,
    "energia"
)

adicionar(
    "manutencao",
    "Manutenção solar",
    "painel precisa de manutencao|"
    "como limpar painel|"
    "limpeza de placa solar|"
    "manutencao fotovoltaica|"
    "cuidados com painel",
    """
🧽 Os sistemas solares precisam
de inspeção e manutenção conforme
as orientações do fabricante.

Evite subir em telhados ou
manipular partes elétricas.

Procure profissionais qualificados
para serviços que envolvam riscos.
""",
    None,
    "energia"
)

adicionar(
    "durabilidade",
    "Vida útil",
    "quanto dura painel|"
    "vida util painel solar|"
    "durabilidade da placa|"
    "quantos anos dura painel|"
    "painel estraga rapido",
    """
⏳ Muitos painéis fotovoltaicos
são projetados para operar
por décadas.

A durabilidade depende
do fabricante, das condições
de uso e da manutenção.
""",
    None,
    "energia"
)

adicionar(
    "eficiencia",
    "Eficiência solar",
    "o que e eficiencia solar|"
    "eficiencia do painel|"
    "rendimento solar|"
    "qual painel produz mais|"
    "painel mais eficiente",
    """
📈 A eficiência indica a parcela
da energia solar recebida que
o painel consegue converter
em eletricidade.

A geração também depende
de iluminação, temperatura
e instalação.
""",
    None,
    "energia"
)

adicionar(
    "potencia",
    "Potência e energia",
    "o que e watt|"
    "o que e wp|"
    "potencia do painel|"
    "quantos watts produz|"
    "diferenca entre w e kwh|"
    "o que significa kwh",
    """
⚡ Watt (W) é uma unidade
de potência.

Wp representa a potência nominal
de um painel sob condições
padronizadas de teste.

kWh é uma unidade de energia,
usada para medir consumo
e geração ao longo do tempo.
""",
    None,
    "energia"
)

adicionar(
    "tipos",
    "Tipos de sistemas solares",
    "o que e on grid|"
    "o que e off grid|"
    "sistema hibrido|"
    "tipos de sistemas solares|"
    "sistema ligado na rede|"
    "sistema fora da rede",
    """
🔌 Existem diferentes sistemas:

• On-grid: conectado à rede elétrica.
• Off-grid: independente da rede.
• Híbrido: combina características
de diferentes configurações.

Cada um possui necessidades
e aplicações próprias.
""",
    None,
    "energia"
)

adicionar(
    "sustentabilidade",
    "Meio ambiente",
    "energia solar e sustentavel|"
    "beneficios ambientais|"
    "energia limpa|"
    "ajuda o meio ambiente|"
    "energia renovavel|"
    "energia solar polui",
    """
🌱 A energia solar é renovável
e pode ajudar a reduzir emissões
relacionadas à geração elétrica.

Entretanto, a fabricação
e o descarte dos equipamentos
também geram impactos ambientais.
""",
    None,
    "energia"
)

adicionar(
    "seguranca",
    "Segurança solar",
    "energia solar e perigosa|"
    "risco de choque|"
    "painel pode dar choque|"
    "risco de incendio solar|"
    "seguranca eletrica",
    """
⚠️ Sistemas solares envolvem
eletricidade e exigem cuidados.

Nunca manipule cabos,
conectores ou equipamentos
energizados sem qualificação.

Instalações e manutenções devem
seguir as normas aplicáveis.
""",
    None,
    "energia"
)

# ==========================================================
# NAVEGAÇÃO E SUPORTE
# ==========================================================

adicionar(
    "navegacao",
    "Como usar o site",
    "como usar o site|"
    "quais paginas existem|"
    "como navegar|"
    "o que tem no site|"
    "me mostre as funcoes|"
    "onde encontro as paginas",
    """
🧭 O Solaris possui:

🏠 Início — apresentação.
🌻 Sobre — informações do projeto.
🛒 Loja — produtos demonstrativos.
📊 Simulador — estimativa educativa.
🤖 Solaris IA — atendimento virtual.
🔐 Minha Conta — login e cadastro.
🛍️ Carrinho — itens selecionados.

Você pode acessar essas páginas
pelo menu do site.
""",
    "inicio",
    "suporte"
)

adicionar(
    "erro_site",
    "Problemas no site",
    "site nao funciona|"
    "pagina em branco|"
    "site travou|"
    "botao nao funciona|"
    "erro na pagina|"
    "pagina nao carrega",
    """
🛠️ Se alguma página não funcionar:

1. Atualize o navegador.
2. Confira a conexão.
3. Tente abrir a página novamente.
4. Anote a mensagem de erro.

Se o problema continuar,
informe à equipe do projeto.
""",
    "inicio",
    "suporte"
)

adicionar(
    "atendimento",
    "Atendimento humano",
    "falar com atendente|"
    "atendimento humano|"
    "falar com suporte|"
    "contato da equipe|"
    "telefone do solaris|"
    "whatsapp do solaris",
    """
👥 Sou a assistente virtual do Solaris.

Ainda não tenho um canal oficial
de atendimento humano confirmado
para informar.

Você pode procurar a equipe
responsável pelo projeto na escola.
""",
    None,
    "suporte"
)

adicionar(
    "privacidade",
    "Privacidade",
    "politica de privacidade|"
    "meus dados estao seguros|"
    "o que fazem com meus dados|"
    "seguranca dos dados|"
    "dados pessoais",
    """
🔒 Não compartilhe senhas,
documentos ou informações
pessoais sensíveis pelo chat.

Para conhecer os procedimentos
de armazenamento e tratamento
de dados do Solaris, consulte
a equipe responsável.
""",
    None,
    "suporte"
)

adicionar(
    "gratis",
    "O Solaris é gratuito",
    "solaris e gratis|"
    "precisa pagar para usar|"
    "chat e gratuito|"
    "ia e paga|"
    "custa usar o site",
    """
🌻 A navegação e a assistente
educativa do Solaris não exigem
pagamento nesta versão.

A loja também é demonstrativa
e não realiza vendas reais.
""",
    None,
    "suporte"
)

adicionar(
    "capacidades",
    "O que a IA consegue fazer",
    "o que voce sabe|"
    "o que posso perguntar|"
    "quais perguntas responde|"
    "como pode me ajudar|"
    "suas funcionalidades|"
    "o que voce consegue fazer",
    """
🤖 Posso ajudar com:

🌻 Projeto Solaris.
☀️ Energia solar.
🔐 Login e cadastro.
🛒 Loja e carrinho.
📊 Simulador.
🧭 Navegação no site.
🛠️ Problemas comuns.

Também consigo reconhecer
diferentes formas de perguntar
e recomendar páginas do site.
""",
    None,
    "suporte"
)

adicionar(
    "identidade",
    "Quem é a Solaris IA",
    "quem e voce|"
    "voce e uma inteligencia artificial|"
    "como voce funciona|"
    "voce usa chatgpt|"
    "voce usa openai|"
    "qual modelo de ia",
    """
🤖 Sou a Solaris IA, uma assistente
virtual desenvolvida para o projeto.

Funciono com Python e uma base
de conhecimento organizada.

Reconheço perguntas semelhantes,
mantenho um contexto básico
e ajudo na navegação.

Não sou um modelo generativo
como o ChatGPT.
""",
    None,
    "suporte"
)

# ==========================================================
# CONVERSAS SIMPLES
# ==========================================================

adicionar(
    "saudacao",
    "Saudação",
    "oi|ola|opa|salve|"
    "bom dia|boa tarde|boa noite|"
    "e ai|tudo bem",
    """
Opa! 🌻☀️

Seja bem-vindo ao Solaris!

Sou sua assistente virtual.

Posso ajudar com energia solar,
login, loja, simulador e
informações sobre o projeto.

O que você gostaria de saber?
""",
    None,
    "conversa"
)

adicionar(
    "agradecimento",
    "Agradecimento",
    "obrigado|obrigada|valeu|"
    "muito obrigado|vlw|"
    "agradecido",
    """
Por nada! 😄🌻

Sempre que precisar de ajuda
com o Solaris, estarei aqui!
""",
    None,
    "conversa"
)

adicionar(
    "despedida",
    "Despedida",
    "tchau|ate mais|"
    "falou|ate logo|"
    "adeus|fui",
    """
Até mais! ☀️🌻

Obrigado por conhecer
o projeto Solaris!
""",
    None,
    "conversa"
)

adicionar(
    "elogio",
    "Elogio",
    "parabens|"
    "gostei do projeto|"
    "site bonito|"
    "muito legal|"
    "projeto incrivel|"
    "site maravilhoso",
    """
Aaaa, obrigado! 😄🌻

A equipe Solaris está
trabalhando para criar
uma experiência cada vez melhor!
""",
    None,
    "conversa"
)


# ==========================================================
# MOTOR DE RECONHECIMENTO
# ==========================================================

def calcular_pontuacao(pergunta, exemplo):
    pergunta = normalizar(pergunta)
    exemplo = normalizar(exemplo)

    if not pergunta or not exemplo:
        return 0

    if pergunta == exemplo:
        return 100

    # Frase completa presente na pergunta.
    if len(exemplo) >= 8 and exemplo in pergunta:
        return 92 + min(len(exemplo) / 100, 3)

    # Semelhança de frases.
    frase = semelhanca(pergunta, exemplo)

    # Semelhança de palavras.
    termos = sobreposicao(pergunta, exemplo)

    # Para evitar que uma palavra genérica
    # seja confundida com qualquer assunto.
    if not palavras(pergunta) or not palavras(exemplo):
        if frase >= 0.90:
            return frase * 90
        return 0

    if termos < 0.34:
        return 0

    return max(
        termos * 80,
        (termos * 0.65 + frase * 0.35) * 85
    )


def identificar_assunto(pergunta):
    resultados = []

    for codigo, assunto in BASE.items():
        melhor = max(
            calcular_pontuacao(pergunta, exemplo)
            for exemplo in assunto["exemplos"]
        )

        resultados.append((melhor, codigo))

    resultados.sort(reverse=True)

    pontuacao, codigo = resultados[0]

    # Limite de confiança:
    # abaixo dele, a IA não inventa resposta.
    if pontuacao < 56:
        return None

    # Evita aceitar resultados muito fracos
    # quando dois assuntos parecem iguais.
    if len(resultados) > 1:
        segundo = resultados[1][0]

        if (
            pontuacao < 70
            and pontuacao - segundo < 4
        ):
            return None

    return codigo


# ==========================================================
# CONTEXTO
# ==========================================================

CONTINUACOES = {
    "explique melhor",
    "me explica melhor",
    "pode explicar melhor",
    "nao entendi",
    "nao compreendi",
    "pode detalhar",
    "fala mais",
    "fale mais",
    "continue",
    "como assim",
    "me de um exemplo",
    "e depois",
    "e como funciona",
    "como faco isso",
    "quero saber mais",
    "mais detalhes"
}


def e_continuacao(texto):
    texto = normalizar(texto)

    return (
        texto in CONTINUACOES
        or texto.startswith("fale mais sobre isso")
        or texto.startswith("me explica isso")
        or texto.startswith("pode explicar isso")
    )


def resposta_detalhada(codigo):
    assunto = BASE[codigo]

    texto = assunto["resposta"]

    pagina = assunto["pagina"]

    if pagina:
        texto += (
            "\n\n🧭 Você também pode acessar "
            "a página correspondente pelo "
            "botão que aparece abaixo."
        )

    texto += (
        "\n\nSe quiser, faça uma pergunta "
        "mais específica sobre esse tema. 🌻"
    )

    return texto


# ==========================================================
# SUGESTÕES DE PERGUNTAS
# ==========================================================

SUGESTOES = {
    "projeto": [
        "Qual o objetivo do Solaris?",
        "O que é o rastreador solar?",
        "Como o site foi feito?"
    ],
    "login": [
        "Como criar uma conta?",
        "Esqueci minha senha",
        "Não consigo entrar"
    ],
    "cadastro": [
        "Como fazer login?",
        "Esqueci minha senha",
        "Como sair da conta?"
    ],
    "loja": [
        "Como comprar?",
        "Como usar o carrinho?",
        "Os preços são reais?"
    ],
    "simulador": [
        "Quanto posso economizar?",
        "Por que usa 80%?",
        "Qual o retorno do investimento?"
    ],
    "energia_solar": [
        "Como funciona um painel solar?",
        "O que faz um inversor?",
        "Painel funciona na chuva?"
    ],
    "painel": [
        "Painel funciona à noite?",
        "O que faz um inversor?",
        "Quanto dura um painel solar?"
    ],
    "tracker": [
        "Qual o objetivo do Solaris?",
        "O que é energia solar?",
        "Qual o diferencial do projeto?"
    ]
}

SUGESTOES_CATEGORIA = {
    "conta": [
        "Como fazer login?",
        "Como criar uma conta?",
        "Esqueci minha senha"
    ],
    "loja": [
        "Como usar o carrinho?",
        "Como funciona a loja?",
        "Quais formas de pagamento?"
    ],
    "energia": [
        "Como funciona a energia solar?",
        "O que faz um inversor?",
        "Painel funciona na chuva?"
    ],
    "simulador": [
        "Como usar o simulador?",
        "Quanto posso economizar?",
        "Por que usa 80%?"
    ],
    "projeto": [
        "O que é o projeto Solaris?",
        "Qual o objetivo do Solaris?",
        "O que é o rastreador solar?"
    ],
    "suporte": [
        "Como usar o site?",
        "Como fazer login?",
        "O que posso perguntar?"
    ]
}

SUGESTOES_PADRAO = [
    "Como funciona a energia solar?",
    "Como fazer login?",
    "Como usar o simulador?"
]


def sugestoes_para(codigo):
    if codigo in SUGESTOES:
        return SUGESTOES[codigo]

    categoria = BASE[codigo]["categoria"]

    return SUGESTOES_CATEGORIA.get(
        categoria,
        SUGESTOES_PADRAO
    )


# ==========================================================
# MOTOR DE RESPOSTAS
# ==========================================================

def responder(mensagem, contexto=None):
    texto = normalizar(mensagem)

    if not texto:
        return {
            "resposta": (
                "🌻 Digite uma pergunta "
                "para começarmos!"
            ),
            "assunto": None,
            "tipo": "ajuda",
            "sugestoes": SUGESTOES_PADRAO,
            "pagina": None
        }

    # Continuação de conversa anterior.
    if (
        contexto in BASE
        and e_continuacao(texto)
    ):
        return {
            "resposta": resposta_detalhada(contexto),
            "assunto": contexto,
            "tipo": "continuidade",
            "sugestoes": sugestoes_para(contexto),
            "pagina": BASE[contexto]["pagina"]
        }

    # Reconhecimento da pergunta.
    codigo = identificar_assunto(texto)

    if codigo:
        assunto = BASE[codigo]

        return {
            "resposta": assunto["resposta"],
            "assunto": codigo,
            "tipo": "conhecimento",
            "sugestoes": sugestoes_para(codigo),
            "pagina": assunto["pagina"]
        }

    # Resposta segura quando não reconhece.
    return {
        "resposta": (
            "🤔 Ainda não encontrei uma resposta "
            "confiável para essa pergunta.\n\n"
            "Posso ajudar com o projeto Solaris, "
            "energia solar, login, cadastro, loja, "
            "carrinho, simulador e navegação.\n\n"
            "Tente perguntar de outra forma "
            "ou escolha uma sugestão! 🌻"
        ),
        "assunto": None,
        "tipo": "nao_encontrado",
        "sugestoes": SUGESTOES_PADRAO,
        "pagina": None
    }


# ==========================================================
# API FASTAPI
# ==========================================================

@router.post("/perguntar")
def perguntar(dados: Pergunta):
    return responder(
        mensagem=dados.mensagem,
        contexto=dados.contexto
    )


@router.get("/status")
def status():
    return {
        "nome": "Solaris IA",
        "status": "online",
        "tipo": "assistente baseada em conhecimento",
        "assuntos": len(BASE),
        "api_paga": False,
        "navegacao_inteligente": True,
        "contexto_basico": True
    }


# ==========================================================
# FIM
# ==========================================================
