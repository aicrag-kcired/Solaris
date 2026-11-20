// Controles da página de acessibilidade e do tema.
const botoesAcess = document.querySelectorAll('[data-chave]');
const botoesTema = document.querySelectorAll('[data-tema]');
const botaoRestaurar = document.querySelector('#botao-restaurar');

function atualizarBotoes() {
  const config = lerAcessibilidade();
  botoesAcess.forEach(botao => {
    const ativo = config[botao.dataset.chave] === botao.dataset.valor;
    botao.setAttribute('aria-pressed', String(ativo));
    botao.classList.toggle('botao-principal', ativo);
    botao.classList.toggle('botao-secundario', !ativo);
  });
}

function atualizarTema() {
  const atual = document.documentElement.dataset.theme === 'dark' ? 'dark' : 'light';
  botoesTema.forEach(botao => {
    const ativo = botao.dataset.tema === atual;
    botao.setAttribute('aria-pressed', String(ativo));
    botao.classList.toggle('botao-principal', ativo);
    botao.classList.toggle('botao-secundario', !ativo);
  });
}

botoesAcess.forEach(botao => {
  botao.addEventListener('click', () => {
    salvarAcessibilidade(botao.dataset.chave, botao.dataset.valor);
    atualizarBotoes();
  });
});

botoesTema.forEach(botao => {
  botao.addEventListener('click', () => {
    aplicarTema(botao.dataset.tema === 'dark');
    atualizarTema();
  });
});

botaoRestaurar.addEventListener('click', () => {
  localStorage.removeItem(CHAVE_ACESS);
  aplicarAcessibilidade();
  aplicarTema(false);
  atualizarBotoes();
  atualizarTema();
});

atualizarBotoes();
atualizarTema();