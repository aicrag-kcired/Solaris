// ======================= MENU LATERAL =======================
document.addEventListener('DOMContentLoaded', () => {
  const botaoMenu   = document.getElementById('botao-menu');
  const menuLateral = document.getElementById('menu-lateral');

  if (!botaoMenu || !menuLateral) return;

  botaoMenu.addEventListener('click', () => {
    const aberto = botaoMenu.getAttribute('aria-expanded') === 'true';
    botaoMenu.setAttribute('aria-expanded', String(!aberto));
    menuLateral.hidden = aberto;
  });

  // Fecha ao clicar fora
  document.addEventListener('click', (e) => {
    if (menuLateral.hidden) return;
    if (menuLateral.contains(e.target) || botaoMenu.contains(e.target)) return;
    botaoMenu.setAttribute('aria-expanded', 'false');
    menuLateral.hidden = true;
  });

  // Fecha com ESC
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && !menuLateral.hidden) {
      botaoMenu.setAttribute('aria-expanded', 'false');
      menuLateral.hidden = true;
      botaoMenu.focus();
    }
  });
});