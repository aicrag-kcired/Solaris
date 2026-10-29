// Menu de navegação compartilhado por todas as telas.
const botaoMenu = document.querySelector('#botao-menu');
const menu = document.querySelector('#menu-lateral');

function alternarMenu(abrir) {
  menu.hidden = !abrir;
  botaoMenu.setAttribute('aria-expanded', String(abrir));
}

botaoMenu.addEventListener('click', () => alternarMenu(menu.hidden));

document.addEventListener('keydown', evento => {
  if (evento.key === 'Escape') alternarMenu(false);
});

document.addEventListener('click', evento => {
  if (!menu.hidden && !menu.contains(evento.target) && !botaoMenu.contains(evento.target)) {
    alternarMenu(false);
  }
});