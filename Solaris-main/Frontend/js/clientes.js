// Solaris - CRUD de clientes. O navegador acessa APENAS a FastAPI.
// As credenciais do Supabase ficam no arquivo .env do backend.
const API_URL = 'http://127.0.0.1:8000/clientes';

const formulario = document.querySelector('#form-cliente');
const campoId = document.querySelector('#id-cliente');
const campoNome = document.querySelector('#nome-cliente');
const campoCpf = document.querySelector('#cpf-cliente');
const campoRg = document.querySelector('#rg-cliente');
const campoTelefone = document.querySelector('#numero-cliente');
const campoEmail = document.querySelector('#email-cliente');
const campoEndereco = document.querySelector('#endereco-cliente');
const campoImovel = document.querySelector('#tipo-imovel-cliente');
const campoRenda = document.querySelector('#renda-cliente');
const mensagem = document.querySelector('#mensagem-clientes');
const lista = document.querySelector('#lista-clientes');
const total = document.querySelector('#total-clientes');
const botaoSalvar = document.querySelector('#botao-salvar-cliente');
const botaoListar = document.querySelector('#botao-listar-clientes');
const buscaId = document.querySelector('#busca-id-cliente');

function mostrarMensagem(texto, erro = false) {
  mensagem.textContent = texto;
  mensagem.className = erro ? 'mensagem erro' : 'mensagem';
  mensagem.hidden = false;
}

function moeda(valor) {
  return Number(valor).toLocaleString('pt-BR', {
    style: 'currency', currency: 'BRL'
  });
}

// Trata inclusive erros HTTP 404/422 e o DELETE 204 (sem JSON de resposta).
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
    throw new Error('Não foi possível acessar a API. Verifique se o backend está ligado e se o CORS permite a porta do frontend.');
  }
  if (resposta.status === 204 && resposta.ok) return null;

  const conteudo = await resposta.json().catch(() => null);
  if (!resposta.ok) {
    let detalhe = conteudo && conteudo.detail;
    if (Array.isArray(detalhe)) {
      detalhe = detalhe.map(item => `${(item.loc || []).join('.')}: ${item.msg}`).join(' | ');
    }
    throw new Error(typeof detalhe === 'string' ? detalhe : `Erro HTTP ${resposta.status}. Confira o terminal do backend.`);
  }
  if (conteudo === null) throw new Error('A API não retornou um JSON válido.');
  return conteudo;
}

function dadosFormulario() {
  const renda = Number(campoRenda.value);
  if (!Number.isFinite(renda) || renda < 0 || renda > 99999999.99) {
    throw new Error('Informe uma renda mensal válida.');
  }
  // As chaves são exatamente as do modelo ClienteEntrada do backend Solaris.
  return {
    nome_cliente: campoNome.value.trim(),
    cpf_cliente: campoCpf.value.trim(),
    rg_cliente: campoRg.value.trim(),
    numero_cliente: campoTelefone.value.trim(),
    email_cliente: campoEmail.value.trim(),
    endereco_cliente: campoEndereco.value.trim(),
    tipo_imovel_cliente: campoImovel.value.trim(),
    renda_mensal_cliente: renda.toFixed(2)
  };
}

function limparFormulario() {
  formulario.reset();
  campoId.value = '';
  document.querySelector('#titulo-formulario').textContent = 'Novo cliente';
  botaoSalvar.textContent = 'Cadastrar cliente';
}

function exibirClientes(clientes) {
  lista.replaceChildren();
  total.textContent = `${clientes.length} registro(s) exibido(s)`;
  if (clientes.length === 0) {
    const linha = lista.insertRow();
    const celula = linha.insertCell();
    celula.colSpan = 6;
    celula.className = 'vazio';
    celula.textContent = 'Nenhum cliente encontrado.';
    return;
  }

  for (const cliente of clientes) {
    const linha = lista.insertRow();
    const valores = [
      cliente.id_cliente,
      cliente.nome_cliente,
      cliente.email_cliente,
      cliente.tipo_imovel_cliente,
      moeda(cliente.renda_mensal_cliente)
    ];
    for (const valor of valores) linha.insertCell().textContent = String(valor ?? '');

    const acoes = linha.insertCell();
    const editar = document.createElement('button');
    editar.type = 'button';
    editar.className = 'botao botao-principal';
    editar.textContent = 'Editar';
    editar.addEventListener('click', () => editarCliente(cliente));

    const excluir = document.createElement('button');
    excluir.type = 'button';
    excluir.className = 'botao botao-secundario';
    excluir.textContent = 'Excluir';
    excluir.addEventListener('click', () => excluirCliente(cliente, excluir));
    acoes.append(editar, excluir);
  }
}

async function listarClientes() {
  const clientes = await requisicao();
  if (!Array.isArray(clientes)) throw new Error('A API retornou uma lista inválida.');
  exibirClientes(clientes);
}

function editarCliente(cliente) {
  campoId.value = cliente.id_cliente;
  campoNome.value = cliente.nome_cliente ?? '';
  campoCpf.value = cliente.cpf_cliente ?? '';
  campoRg.value = cliente.rg_cliente ?? '';
  campoTelefone.value = cliente.numero_cliente ?? '';
  campoEmail.value = cliente.email_cliente ?? '';
  campoEndereco.value = cliente.endereco_cliente ?? '';
  campoImovel.value = cliente.tipo_imovel_cliente ?? '';
  campoRenda.value = cliente.renda_mensal_cliente ?? '';
  document.querySelector('#titulo-formulario').textContent = `Editar cliente #${cliente.id_cliente}`;
  botaoSalvar.textContent = 'Salvar alterações';
  mostrarMensagem(`Editando cliente #${cliente.id_cliente}. Altere os campos e clique em Salvar alterações.`);
  document.querySelector('#titulo-formulario').scrollIntoView({ behavior: 'smooth', block: 'start' });
  campoNome.focus({ preventScroll: true });
}

async function excluirCliente(cliente, botao) {
  if (!confirm(`Excluir o cliente ${cliente.nome_cliente} (ID ${cliente.id_cliente})?`)) return;
  botao.disabled = true;
  try {
    await requisicao(`/${cliente.id_cliente}`, 'DELETE');
    if (campoId.value === String(cliente.id_cliente)) limparFormulario();
    mostrarMensagem(`Cliente #${cliente.id_cliente} excluído com sucesso.`);
    try {
      await listarClientes();
    } catch (erro) {
      mostrarMensagem(`Cliente excluído, mas não foi possível atualizar a lista: ${erro.message}`, true);
    }
  } catch (erro) {
    mostrarMensagem(erro.message, true);
  } finally {
    botao.disabled = false;
  }
}

formulario.addEventListener('submit', async evento => {
  evento.preventDefault();
  const id = campoId.value;
  let dados;
  try {
    dados = dadosFormulario();
    if (Object.values(dados).some(valor => valor === '')) {
      throw new Error('Preencha todos os campos do cliente.');
    }
  } catch (erro) {
    mostrarMensagem(erro.message, true);
    return;
  }

  botaoSalvar.disabled = true;
  try {
    const cliente = await requisicao(id ? `/${id}` : '', id ? 'PUT' : 'POST', dados);
    limparFormulario();
    mostrarMensagem(`Cliente #${cliente.id_cliente} ${id ? 'atualizado' : 'cadastrado'} com sucesso.`);
    try {
      await listarClientes();
    } catch (erro) {
      mostrarMensagem(`Registro salvo, mas a lista não foi atualizada: ${erro.message}`, true);
    }
  } catch (erro) {
    mostrarMensagem(erro.message, true);
  } finally {
    botaoSalvar.disabled = false;
  }
});

document.querySelector('#botao-limpar-cliente').addEventListener('click', () => {
  limparFormulario();
  mostrarMensagem('Formulário limpo. Nenhum registro foi apagado do banco.');
});

document.querySelector('#form-busca-cliente').addEventListener('submit', async evento => {
  evento.preventDefault();
  const id = Number(buscaId.value);
  if (!Number.isSafeInteger(id) || id <= 0) {
    mostrarMensagem('Informe um ID válido para consultar.', true);
    return;
  }
  try {
    const cliente = await requisicao(`/${id}`);
    exibirClientes([cliente]);
    mostrarMensagem(`Cliente #${id} encontrado. Clique em Editar para visualizar todos os campos.`);
  } catch (erro) {
    mostrarMensagem(erro.message, true);
  }
});

botaoListar.addEventListener('click', async () => {
  botaoListar.disabled = true;
  try {
    await listarClientes();
    mostrarMensagem('Lista atualizada com os registros do banco de dados.');
  } catch (erro) {
    mostrarMensagem(erro.message, true);
  } finally {
    botaoListar.disabled = false;
  }
});

// Mostra os registros reais assim que a página é aberta.
listarClientes().catch(erro => {
  exibirClientes([]);
  mostrarMensagem(erro.message, true);
});
