document.addEventListener("DOMContentLoaded", () => {
  const html = document.documentElement;
  const btnEngrenagem = document.getElementById("btn-engrenagem");
  const menuAcess = document.getElementById("menu-acessibilidade");
  const btnTema = document.getElementById("btn-tema");
  const botoesTexto = document.querySelectorAll("[data-set-texto]");

  // 1. Abrir e fechar o menu na engrenagem
  if (btnEngrenagem && menuAcess) {
    btnEngrenagem.addEventListener("click", (e) => {
      e.stopPropagation();
      const estaOculto = menuAcess.hasAttribute("hidden");
      if (estaOculto) {
        menuAcess.removeAttribute("hidden");
        btnEngrenagem.setAttribute("aria-expanded", "true");
      } else {
        menuAcess.setAttribute("hidden", "");
        btnEngrenagem.setAttribute("aria-expanded", "false");
      }
    });

    document.addEventListener("click", (e) => {
      if (!menuAcess.contains(e.target) && !btnEngrenagem.contains(e.target)) {
        menuAcess.setAttribute("hidden", "");
        btnEngrenagem.setAttribute("aria-expanded", "false");
      }
    });
  }

  // 2. Modo Escuro (usa :root[data-theme="dark"] do seu style.css)
  const aplicarTema = (tema) => {
    if (tema === "dark") {
      html.setAttribute("data-theme", "dark");
      if (btnTema) btnTema.textContent = "☀️ Modo Claro";
    } else {
      html.removeAttribute("data-theme");
      if (btnTema) btnTema.textContent = "🌓 Modo Escuro";
    }
  };

  let temaAtual = localStorage.getItem("solaris_tema") || "light";
  aplicarTema(temaAtual);

  if (btnTema) {
    btnTema.addEventListener("click", () => {
      temaAtual = temaAtual === "dark" ? "light" : "dark";
      localStorage.setItem("solaris_tema", temaAtual);
      aplicarTema(temaAtual);
    });
  }

  // 3. Tamanho da Letra (usa html[data-texto] do seu style.css)
  const aplicarTexto = (tamanho) => {
    if (tamanho === "normal") {
      html.removeAttribute("data-texto");
    } else {
      html.setAttribute("data-texto", tamanho);
    }
    botoesTexto.forEach((btn) => {
      btn.setAttribute("aria-pressed", btn.dataset.setTexto === tamanho);
    });
  };

  let textoAtual = localStorage.getItem("solaris_texto") || "normal";
  aplicarTexto(textoAtual);

  botoesTexto.forEach((btn) => {
    btn.addEventListener("click", () => {
      textoAtual = btn.dataset.setTexto;
      localStorage.setItem("solaris_texto", textoAtual);
      aplicarTexto(textoAtual);
    });
  });
});