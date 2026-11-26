// ======================= ACESSIBILIDADE =======================
document.addEventListener('DOMContentLoaded', () => {
  const btnEngrenagem = document.getElementById('btn-engrenagem');
  const menuAcess     = document.getElementById('menu-acessibilidade');
  const btnTema       = document.getElementById('btn-tema');
  const botoesFonte   = document.querySelectorAll('[data-set-texto]');

  const raiz = document.documentElement;

  // ---------- Abrir / fechar painel ----------
  if (btnEngrenagem && menuAcess) {
    btnEngrenagem.addEventListener('click', () => {
      const aberto = btnEngrenagem.getAttribute('aria-expanded') === 'true';
      btnEngrenagem.setAttribute('aria-expanded', String(!aberto));
      menuAcess.hidden = aberto;
    });

    document.addEventListener('click', (e) => {
      if (menuAcess.hidden) return;
      if (menuAcess.contains(e.target) || btnEngrenagem.contains(e.target)) return;
      btnEngrenagem.setAttribute('aria-expanded', 'false');
      menuAcess.hidden = true;
    });

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && !menuAcess.hidden) {
        btnEngrenagem.setAttribute('aria-expanded', 'false');
        menuAcess.hidden = true;
        btnEngrenagem.focus();
      }
    });
  }

  // ---------- Tema claro / escuro ----------
  const aplicarTema = (tema) => {
    raiz.setAttribute('data-theme', tema);
    localStorage.setItem('solaris-tema', tema);
    if (btnTema) {
      btnTema.textContent = tema === 'dark'
        ? '☀️ Modo Claro'
        : '🌓 Modo Escuro';
    }
  };

  // Carrega tema salvo
  const temaSalvo = localStorage.getItem('solaris-tema') || 'light';
  aplicarTema(temaSalvo);

  if (btnTema) {
    btnTema.addEventListener('click', () => {
      const atual = raiz.getAttribute('data-theme') === 'dark' ? 'dark' : 'light';
      aplicarTema(atual === 'dark' ? 'light' : 'dark');
    });
  }

  // ---------- Tamanho da fonte ----------
  const aplicarFonte = (tamanho) => {
    raiz.setAttribute('data-texto', tamanho);
    localStorage.setItem('solaris-texto', tamanho);

    botoesFonte.forEach((b) => {
      b.setAttribute('aria-pressed', String(b.dataset.setTexto === tamanho));
    });
  };

  const fonteSalva = localStorage.getItem('solaris-texto') || 'normal';
  aplicarFonte(fonteSalva);

  botoesFonte.forEach((btn) => {
    btn.addEventListener('click', () => aplicarFonte(btn.dataset.setTexto));
  });
});