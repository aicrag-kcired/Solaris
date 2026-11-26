// ======================= LOGIN E CADASTRO =======================
document.addEventListener('DOMContentLoaded', () => {
    const areaAcesso       = document.getElementById('area-acesso');
    const botaoLogin       = document.getElementById('botao-login');
    const painelLogin      = document.getElementById('painel-login');
    const painelCadastro   = document.getElementById('painel-cadastro');
    const formLogin        = document.getElementById('form-login');
    const formCadastro     = document.getElementById('form-cadastro');
    const botaoIrCadastro  = document.getElementById('botao-ir-cadastro');
    const botaoIrLogin     = document.getElementById('botao-ir-login');
    const botaoLimpar      = document.getElementById('botao-limpar');
    const msgBox           = document.getElementById('mensagem');
    const inputCpf         = document.getElementById('cpf-cliente');
    const inputTel         = document.getElementById('numero-cliente');
  
    // ---------- Olhinho: mostrar / ocultar senha ----------
    document.querySelectorAll('.btn-olho').forEach((btn) => {
      btn.addEventListener('click', () => {
        const alvo = document.getElementById(btn.dataset.alvo);
        if (!alvo) return;
  
        const mostrando = alvo.type === 'text';
        alvo.type = mostrando ? 'password' : 'text';
        btn.setAttribute('aria-pressed', String(!mostrando));
        btn.setAttribute('aria-label', mostrando ? 'Mostrar senha' : 'Ocultar senha');
        btn.textContent = mostrando ? '👁️' : '🙈';
        alvo.focus();
      });
    });
  
    // ---------- Utilitário de mensagem ----------
    let msgTimer = null;
    function mostrarMensagem(texto, erro = false) {
      if (!msgBox) return;
      msgBox.textContent = texto;
      msgBox.classList.toggle('erro', erro);
      msgBox.hidden = false;
      clearTimeout(msgTimer);
      msgTimer = setTimeout(() => { msgBox.hidden = true; }, 5000);
    }
  
    // ---------- Abrir / fechar área de acesso ----------
    if (botaoLogin && areaAcesso) {
      botaoLogin.addEventListener('click', () => {
        const aberto = botaoLogin.getAttribute('aria-expanded') === 'true';
        botaoLogin.setAttribute('aria-expanded', String(!aberto));
        areaAcesso.hidden = aberto;
        if (!aberto) {
          const primeiro = painelLogin.hidden ? null : document.getElementById('login-email');
          if (primeiro) setTimeout(() => primeiro.focus(), 100);
        }
      });
    }
  
    // ---------- Alternar painéis ----------
    function mostrarLogin() {
      painelLogin.hidden = false;
      painelCadastro.hidden = true;
      const foco = document.getElementById('login-email');
      if (foco) foco.focus();
    }
  
    function mostrarCadastro() {
      painelLogin.hidden = true;
      painelCadastro.hidden = false;
      const foco = document.getElementById('nome-cliente');
      if (foco) foco.focus();
    }
  
    if (botaoIrCadastro) botaoIrCadastro.addEventListener('click', mostrarCadastro);
    if (botaoIrLogin)    botaoIrLogin.addEventListener('click', mostrarLogin);
  
    // ---------- Máscaras ----------
    function mascaraCpf(v) {
      return v.replace(/\D/g, '')
              .replace(/(\d{3})(\d)/, '$1.$2')
              .replace(/(\d{3})(\d)/, '$1.$2')
              .replace(/(\d{3})(\d{1,2})$/, '$1-$2')
              .slice(0, 14);
    }
    function mascaraTel(v) {
      return v.replace(/\D/g, '')
              .replace(/^(\d{2})(\d)/, '($1) $2')
              .replace(/(\d{5})(\d)/, '$1-$2')
              .slice(0, 15);
    }
  
    if (inputCpf) inputCpf.addEventListener('input', (e) => {
      e.target.value = mascaraCpf(e.target.value);
    });
    if (inputTel) inputTel.addEventListener('input', (e) => {
      e.target.value = mascaraTel(e.target.value);
    });
  
    // ---------- Storage ----------
    const KEY_CLIENTES = 'solaris-clientes';
    const KEY_SESSAO   = 'solaris-sessao';
  
    const lerClientes = () => {
      try { return JSON.parse(localStorage.getItem(KEY_CLIENTES)) || []; }
      catch { return []; }
    };
    const salvarClientes = (lista) =>
      localStorage.setItem(KEY_CLIENTES, JSON.stringify(lista));
  
    // ---------- Cadastro ----------
    if (formCadastro) {
      formCadastro.addEventListener('submit', (e) => {
        e.preventDefault();
  
        const dados = {
          id: Date.now(),
          nome:     document.getElementById('nome-cliente').value.trim(),
          cpf:      document.getElementById('cpf-cliente').value.trim(),
          rg:       document.getElementById('rg-cliente').value.trim(),
          telefone: document.getElementById('numero-cliente').value.trim(),
          email:    document.getElementById('email-cliente').value.trim().toLowerCase(),
          senha:    document.getElementById('senha-cliente').value,
          endereco: document.getElementById('endereco-cliente').value.trim(),
          imovel:   document.getElementById('tipo-imovel-cliente').value.trim(),
          renda:    document.getElementById('renda-cliente').value,
          criadoEm: new Date().toISOString()
        };
  
        if (dados.cpf.replace(/\D/g, '').length !== 11) {
          mostrarMensagem('CPF inválido. Informe os 11 dígitos.', true);
          return;
        }
        if (dados.senha.length < 6) {
          mostrarMensagem('A senha deve ter ao menos 6 caracteres.', true);
          return;
        }
  
        const lista = lerClientes();
        if (lista.some((c) => c.email === dados.email)) {
          mostrarMensagem('Este e-mail já está cadastrado.', true);
          return;
        }
        if (lista.some((c) => c.cpf === dados.cpf)) {
          mostrarMensagem('Este CPF já está cadastrado.', true);
          return;
        }
  
        lista.push(dados);
        salvarClientes(lista);
  
        mostrarMensagem(`Cliente "${dados.nome}" cadastrado com sucesso!`);
        formCadastro.reset();
        setTimeout(mostrarLogin, 800);
      });
    }
  
    // ---------- Limpar ----------
    if (botaoLimpar && formCadastro) {
      botaoLimpar.addEventListener('click', () => {
        formCadastro.reset();
        const primeiro = document.getElementById('nome-cliente');
        if (primeiro) primeiro.focus();
      });
    }
  
    // ---------- Login ----------
    if (formLogin) {
      formLogin.addEventListener('submit', (e) => {
        e.preventDefault();
  
        const email = document.getElementById('login-email').value.trim().toLowerCase();
        const senha = document.getElementById('login-senha').value;
  
        if (senha.length < 6) {
          mostrarMensagem('A senha deve ter ao menos 6 caracteres.', true);
          return;
        }
  
        const lista = lerClientes();
        const cliente = lista.find((c) => c.email === email);
  
        if (!cliente) {
          mostrarMensagem('E-mail não encontrado. Faça seu cadastro.', true);
          return;
        }
        if (cliente.senha !== senha) {
          mostrarMensagem('Senha incorreta.', true);
          return;
        }
  
        localStorage.setItem(KEY_SESSAO, JSON.stringify({
          id: cliente.id,
          nome: cliente.nome,
          email: cliente.email,
          logadoEm: new Date().toISOString()
        }));
  
        mostrarMensagem(`Bem-vindo(a), ${cliente.nome}! Login realizado.`);
        formLogin.reset();
  
        setTimeout(() => {
          window.location.href = './Frontend/pages/ia.html';
        }, 1400);
      });
    }
  
    // ---------- Fechar mensagem ----------
    if (msgBox) {
      msgBox.addEventListener('click', () => { msgBox.hidden = true; });
    }
  });