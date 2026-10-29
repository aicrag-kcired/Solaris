// O navegador conversa somente com a API. Não coloque senhas ou chaves aqui.
const API_URL = 'http://127.0.0.1:8000/clientes';
// O cadastro grava de verdade na API (/clientes).
// O login ainda não tem rota no backend (a tabela de clientes não tem senha): fica em demonstração.
const LOGIN_DEMONSTRACAO = true;

const botaoLogin = document.querySelector('#botao-login');
const areaAcesso = document.querySelector('#area-acesso');
const painelLogin = document.querySelector('#painel-login');
const painelCadastro = document.querySelector('#painel-cadastro');
const formLogin = document.querySelector('#form-login');
const botaoEntrar = document.querySelector('#botao-entrar');
const formCadastro = document.querySelector('#form-cadastro');
const campoNome = document.querySelector('#nome-cliente');
const campoCpf = document.querySelector('#cpf-cliente');
const campoRg = document.querySelector('#rg-cliente');
const campoNumero = document.querySelector('#numero-cliente');
const campoEmail = document.querySelector('#email-cliente');
const campoEndereco = document.querySelector('#endereco-cliente');
const campoImovel = document.querySelector('#tipo-imovel-cliente');
const campoRenda = document.querySelector('#renda-cliente');
const botaoSalvar = document.querySelector('#botao-salvar');
const mensagem = document.querySelector('#mensagem');

function mostrarMensagem(texto, erro = false) {
  mensagem.textContent = texto;
  mensagem.className = erro ? 'mensagem erro' : 'mensagem';
  mensagem.hidden = false;
  mensagem.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Centraliza o envio e a leitura das respostas da API.
async function requisicao(caminho = '', metodo = 'GET', dados = null) {
  const opcoes = { method: metodo };
  if (dados !== null) {
    opcoes.headers = { 'Content-Type': 'application/json' };
    opcoes.body = JSON.stringify(dados);
  }
  let resposta;
  try {
    resposta = await fetch(API_URL + caminho, opcoes);
  } catch {
    throw new Error('Não foi possível acessar a API. Confira o backend e a configuração de CORS.');
  }
  if (resposta.status === 204) return null;
  const conteudo = await resposta.json();
  if (!resposta.ok) {
    let detalhe = conteudo.detail;
    if (Array.isArray(detalhe)) {
      detalhe = detalhe.map(item => `${item.loc.join('.')}: ${item.msg}`).join(' | ');
    }
    throw new Error(detalhe || 'Não foi possível concluir a operação.');
  }
  return conteudo;
}

formLogin.addEventListener('submit', async evento => {
  evento.preventDefault();
  botaoEntrar.disabled = true;
  try {
    if (!LOGIN_DEMONSTRACAO) {
      // Aqui entrará a chamada de login quando o backend tiver essa rota.
    }
    formLogin.reset();
    mostrarMensagem('Login realizado com sucesso (modo demonstração).');
  } finally {
    botaoEntrar.disabled = false;
  }
});

formCadastro.addEventListener('submit', async evento => {
  evento.preventDefault();
  const nome = campoNome.value.trim();
  if (!nome) {
    mostrarMensagem('Informe o nome do cliente.', true);
    campoNome.focus();
    return;
  }
  // Os nomes dos campos são os do modelo ClienteEntrada (Back-end/models/clientes.py).
  const dados = {
    nome_cliente: nome,
    cpf_cliente: campoCpf.value.trim(),
    rg_cliente: campoRg.value.trim(),
    numero_cliente: campoNumero.value.trim(),
    email_cliente: campoEmail.value.trim(),
    endereco_cliente: campoEndereco.value.trim(),
    tipo_imovel_cliente: campoImovel.value.trim(),
    renda_mensal_cliente: Number(campoRenda.value).toFixed(2)
  };
  botaoSalvar.disabled = true;
  try {
    await requisicao('', 'POST', dados);
    formCadastro.reset();
    mostrarMensagem('Cliente cadastrado com sucesso.');
  } catch (erro) {
    mostrarMensagem(erro.message, true);
  } finally {
    botaoSalvar.disabled = false;
  }
});

document.querySelector('#botao-limpar').addEventListener('click', () => formCadastro.reset());

// Mostra só um painel por vez: Entrar ou Cadastre-se.
function mostrarPainel(cadastro) {
  painelLogin.hidden = cadastro;
  painelCadastro.hidden = !cadastro;
  document.querySelector(cadastro ? '#nome-cliente' : '#login-email').focus({ preventScroll: true });
}

// As telas só aparecem quando o botão Login é clicado, sempre começando por "Entrar".
botaoLogin.addEventListener('click', () => {
  const abrir = areaAcesso.hidden;
  areaAcesso.hidden = !abrir;
  botaoLogin.setAttribute('aria-expanded', String(abrir));
  if (abrir) {
    mostrarPainel(false);
    areaAcesso.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
});

document.querySelector('#botao-ir-cadastro').addEventListener('click', () => mostrarPainel(true));
document.querySelector('#botao-ir-login').addEventListener('click', () => mostrarPainel(false));
