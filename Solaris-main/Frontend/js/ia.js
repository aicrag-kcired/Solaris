// Tela Solaris IA. Respostas de demonstração até existir a API da IA.
const conversa = document.querySelector('#conversa');
const boasVindas = document.querySelector('#boas-vindas');
const formChat = document.querySelector('#form-chat');
const textoChat = document.querySelector('#texto-chat');
const mensagem = document.querySelector('#mensagem');

function mostrarMensagem(texto, erro = false) {
  mensagem.textContent = texto;
  mensagem.className = erro ? 'mensagem erro' : 'mensagem';
  mensagem.hidden = false;
}

function adicionarMensagem(texto, autor) {
  const balao = document.createElement('div');
  balao.className = `msg ${autor}`;
  balao.textContent = texto;
  conversa.append(balao);
  conversa.scrollTop = conversa.scrollHeight;
}

function novoChat() {
  conversa.querySelectorAll('.msg').forEach(balao => balao.remove());
  boasVindas.hidden = false;
  mensagem.hidden = true;
  textoChat.value = '';
  textoChat.focus();
}

formChat.addEventListener('submit', evento => {
  evento.preventDefault();
  const texto = textoChat.value.trim();
  if (!texto) return;
  boasVindas.hidden = true;
  adicionarMensagem(texto, 'usuario');
  textoChat.value = '';
  // Aqui entrará a chamada à API da IA (fetch).
  adicionarMensagem('Modo demonstração: em breve a Solaris IA responderá sobre economia e painéis solares.', 'solaris');
});

document.querySelector('#botao-novo-chat').addEventListener('click', novoChat);

// Botões que ainda não têm função mostram um aviso.
document.querySelectorAll('[data-aviso]').forEach(botao => {
  botao.addEventListener('click', () => mostrarMensagem(botao.dataset.aviso));
});