
'use strict';

// ======================================================
// SOLARIS - APP.JS COMPLETO
// Site, loja, simulador, conta, carrinho e Solaris IA
// Voz conversada, microfone e navegação inteligente
// ======================================================

const $ = (selector, parent = document) =>
  parent.querySelector(selector);

const root = $('#conteudo');

const routes = new Set([
  'inicio',
  'sobre',
  'loja',
  'simulador',
  'ia',
  'conta',
  'carrinho'
]);

const pageNames = {
  inicio: 'Início',
  sobre: 'Sobre o projeto',
  loja: 'Loja',
  simulador: 'Simulador',
  ia: 'Solaris IA',
  conta: 'Minha Conta',
  carrinho: 'Carrinho'
};

const currency = value =>
  new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  }).format(value);

const safe = value =>
  String(value ?? '').replace(/[&<>"']/g, char => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#39;'
  }[char]));

// ======================================================
// PRODUTOS DEMONSTRATIVOS
// ======================================================

const PRODUCTS = [
  {
    id: 's480',
    name: 'Painel Solar Solaris 480',
    type: 'convencional',
    power: '480 W',
    price: 890,
    tag: 'Modelo demonstrativo',
    description:
      'Exemplo de painel fotovoltaico convencional para conhecer a loja.'
  },
  {
    id: 's620',
    name: 'Painel Solar Solaris 620',
    type: 'convencional',
    power: '620 W',
    price: 1190,
    tag: 'Linha premium • demonstração',
    description:
      'Exemplo de módulo de maior potência, sem fornecedor definido.'
  },
  {
    id: 'tracker',
    name: 'Solaris Tracker',
    type: 'rastreador',
    power: 'Protótipo',
    price: 2490,
    tag: 'Conceito escolar',
    description:
      'Conceito de painel com acompanhamento solar desenvolvido pelo projeto.'
  }
];

// ======================================================
// ESTADO
// ======================================================

let cart = readCart();
let currentUser = null;
let storeFilter = 'todos';
let storeSearch = '';
let authMode = 'login';
let toastTimer;

let chatContext = null;
let chatBusy = false;
let chatVersion = 0;

const welcomeMessage =
  'Olá! 🌻 Sou a Solaris IA, conectada ao nosso backend Python. ' +
  'Posso explicar energia solar, falar sobre o projeto ' +
  'e ajudar você a navegar pelo site.';

let messages = [
  {
    role: 'bot',
    text: welcomeMessage
  }
];

// ======================================================
// CARRINHO
// ======================================================

function readCart() {
  try {
    const data = JSON.parse(
      localStorage.getItem('solaris_demo_cart') || '{}'
    );

    if (
      !data ||
      typeof data !== 'object' ||
      Array.isArray(data)
    ) {
      return {};
    }

    return Object.fromEntries(
      Object.entries(data).filter(([id, n]) =>
        PRODUCTS.some(p => p.id === id) &&
        Number.isInteger(n) &&
        n > 0 &&
        n <= 99
      )
    );
  } catch {
    return {};
  }
}

function persistCart() {
  try {
    localStorage.setItem(
      'solaris_demo_cart',
      JSON.stringify(cart)
    );
  } catch {}

  updateCartCount();
}

function updateCartCount() {
  const badge = $('#cart-count');

  if (!badge) return;

  const count = Object.values(cart).reduce(
    (sum, n) => sum + n,
    0
  );

  badge.textContent = count;
  badge.hidden = !count;
}

function toast(text) {
  const element = $('#toast');

  if (!element) {
    console.log(text);
    return;
  }

  element.textContent = text;
  element.classList.add('show');

  clearTimeout(toastTimer);

  toastTimer = setTimeout(() => {
    element.classList.remove('show');
  }, 3400);
}

// ======================================================
// NAVEGAÇÃO
// ======================================================

function page() {
  const path = (location.hash || '#/inicio')
    .replace(/^#\/?/, '')
    .split('?')[0]
    .split('/')[0];

  return routes.has(path) ? path : 'inicio';
}

function navigate(path) {
  if (!routes.has(path)) return;

  const destination = `#/${path}`;

  if (location.hash === destination) {
    render();
  } else {
    location.hash = destination;
  }
}

function heading(kicker, title, description) {
  return `
    <div class="container page-head">
      <span class="eyebrow">${kicker}</span>
      <h1>${title}</h1>
      <p>${description}</p>
    </div>
  `;
}

// ======================================================
// PÁGINA INICIAL
// ======================================================

function home() {
  return `
    <div class="page">

      <section class="hero">
        <div class="container hero-grid">

          <div>
            <span class="eyebrow">
              ENERGIA PARA O AMANHÃ
            </span>

            <h1>
              ILUMINANDO<br>
              <em>SEU FUTURO.</em>
            </h1>

            <p>
              Energia solar, tecnologia e inovação
              reunidas em um projeto que acredita
              em um amanhã mais inteligente.
            </p>

            <div class="hero-actions">
              <a
                class="btn btn-primary"
                href="#/simulador"
              >
                Simular economia <span>↗</span>
              </a>

              <a
                class="btn btn-outline"
                href="#/sobre"
              >
                Conheça o projeto →
              </a>
            </div>
          </div>

          <div class="hero-art">
            <img
              src="assets/solar-hero.svg"
              alt="Ilustração de um painel solar com o sol ao fundo"
            >

            <div class="hero-float">
              <span class="float-icon">☀</span>

              <div>
                <strong>Energia que transforma</strong>
                <small>Descubra o universo solar</small>
              </div>
            </div>
          </div>

        </div>
      </section>

      <div class="trust-strip">
        <div class="container trust-items">
          <div>
            <span>✺</span>
            Projeto educacional inovador
          </div>

          <div>
            <span>◈</span>
            Tecnologia e sustentabilidade
          </div>

          <div>
            <span>↗</span>
            Ideias para o futuro
          </div>
        </div>
      </div>

      <section class="section">
        <div class="container banner">

          <div>
            <span class="eyebrow">
              NOSSO PROJETO
            </span>

            <h2>
              O futuro começa com uma ideia.
            </h2>

            <p>
              Uma iniciativa escolar que conecta
              desenvolvimento de sistemas e mecânica
              para explorar soluções com energia solar.
            </p>

            <a
              class="btn btn-primary"
              href="#/sobre"
            >
              Descubra nossa história ↗
            </a>
          </div>

          <div
            class="banner-art"
            aria-hidden="true"
          >
            ✺
          </div>

        </div>
      </section>

    </div>
  `;
}

// ======================================================
// SOBRE O PROJETO
// ======================================================

function about() {
  return `
    <div class="page">

      ${heading(
        'NOSSA HISTÓRIA',
        'Tecnologia com propósito<span class="text-orange">.</span>',
        'O Solaris nasceu como um projeto escolar para unir conhecimentos, criatividade e o potencial da energia solar.'
      )}

      <section
        class="section"
        style="padding-top:0"
      >
        <div class="container about-grid">

          <div>
            <span class="eyebrow">
              O QUE É O SOLARIS?
            </span>

            <h2>
              Um projeto, muitas ideias.
            </h2>

            <p>
              Estamos desenvolvendo uma plataforma
              digital para apresentar produtos,
              explicar energia solar e explorar
              simulações.
            </p>

            <p>
              Ao mesmo tempo, a equipe de mecânica
              trabalha em um protótipo de painel
              com acompanhamento da posição do sol.
            </p>

            <p>
              Nosso objetivo é aprender na prática
              e apresentar uma experiência acessível,
              moderna e educativa.
            </p>

            <div class="notice">
              <strong>Transparência:</strong>
              o protótipo, as funcionalidades
              e os resultados de desempenho
              ainda estão em desenvolvimento
              e validação.
            </div>
          </div>

          <img
            src="assets/solar-hero.svg"
            alt="Painel fotovoltaico ilustrado sob a luz do sol"
          >

        </div>
      </section>

      <section class="section section-alt">
        <div class="container">

          <span class="eyebrow">
            COMO TRABALHAMOS
          </span>

          <h2>
            Conhecimento em movimento.
          </h2>

          <div class="steps">

            <div class="step">
              <b>01</b>
              <h3>Desenvolvimento</h3>
              <p>
                Construímos a plataforma,
                o frontend e as APIs.
              </p>
            </div>

            <div class="step">
              <b>02</b>
              <h3>Protótipo</h3>
              <p>
                Exploramos um painel com
                acompanhamento solar junto
                à equipe de mecânica.
              </p>
            </div>

            <div class="step">
              <b>03</b>
              <h3>Aprendizado</h3>
              <p>
                Testamos ideias, melhoramos
                a experiência e documentamos
                os resultados.
              </p>
            </div>

          </div>
        </div>
      </section>

    </div>
  `;
}

// ======================================================
// LOJA
// ======================================================

function productCard(p) {
  return `
    <article class="product-card">

      <div class="product-img">
        <img
          src="assets/panel-card.svg"
          alt="Ilustração de painel solar"
        >

        <span class="tag">
          ${safe(p.tag)}
        </span>
      </div>

      <div class="product-info">

        <span class="eyebrow">
          ${p.type === 'rastreador'
            ? 'CONCEITO SOLARIS'
            : 'PAINEL SOLAR'}
        </span>

        <h3>${safe(p.name)}</h3>

        <p>${safe(p.description)}</p>

        <div class="product-meta">
          <div>
            <strong>
              ${currency(p.price)}
            </strong>

            <small style="display:block">
              Preço fictício para testes
            </small>
          </div>

          <small>
            ${safe(p.power)}
          </small>
        </div>

        <button
          class="btn btn-primary add-cart"
          data-id="${safe(p.id)}"
        >
          Adicionar ao carrinho +
        </button>

      </div>

    </article>
  `;
}

function filteredProducts() {
  const matches = PRODUCTS.filter(p =>
    (
      storeFilter === 'todos' ||
      p.type === storeFilter
    ) &&
    `${p.name} ${p.description}`
      .toLocaleLowerCase('pt-BR')
      .includes(
        storeSearch.toLocaleLowerCase('pt-BR')
      )
  );

  if (!matches.length) {
    return `
      <div class="empty-state">
        <h3>Nenhum produto encontrado</h3>
        <p>Tente outro termo de busca.</p>
      </div>
    `;
  }

  return matches.map(productCard).join('');
}

function store() {
  return `
    <div class="page section-alt">

      ${heading(
        'LOJA SOLARIS',
        'A energia certa para suas ideias<span class="text-orange">.</span>',
        'Conheça a vitrine demonstrativa do Solaris. Todos os produtos e preços são fictícios.'
      )}

      <section
        class="container"
        style="padding-bottom:85px"
      >

        <div class="store-toolbar">

          <div
            class="chips"
            role="group"
            aria-label="Filtrar produtos"
          >

            <button
              class="chip ${storeFilter === 'todos'
                ? 'active'
                : ''}"
              data-filter="todos"
            >
              Todos
            </button>

            <button
              class="chip ${storeFilter === 'convencional'
                ? 'active'
                : ''}"
              data-filter="convencional"
            >
              Convencionais
            </button>

            <button
              class="chip ${storeFilter === 'rastreador'
                ? 'active'
                : ''}"
              data-filter="rastreador"
            >
              Projeto Solaris
            </button>

          </div>

          <label class="search-field">
            <span aria-hidden="true">⌕</span>

            <input
              id="store-search"
              type="search"
              placeholder="Buscar produtos"
              value="${safe(storeSearch)}"
              aria-label="Buscar produtos"
            >
          </label>

        </div>

        <div
          class="product-grid"
          id="product-grid"
        >
          ${filteredProducts()}
        </div>

        <p
          class="notice"
          style="margin-top:28px"
        >
          <strong>Loja em demonstração:</strong>
          não há fornecedores, estoque,
          garantias, entrega ou pagamentos
          reais cadastrados.
        </p>

      </section>

    </div>
  `;
}

// ======================================================
// SIMULADOR
// ======================================================

function simulator() {
  return `
    <div class="page section-alt">

      ${heading(
        'SIMULADOR SOLAR',
        'Imagine sua economia<span class="text-orange">.</span>',
        'Calcule uma estimativa educativa usando a API do Solaris.'
      )}

      <section
        class="container"
        style="padding-bottom:90px"
      >

        <div class="two-col">

          <div class="panel-box">

            <span class="eyebrow">
              01 / SEUS DADOS
            </span>

            <h3>Vamos fazer as contas?</h3>

            <p>
              Digite o valor mensal da sua
              conta de luz. O servidor fará
              um cálculo ilustrativo usando
              uma hipótese fixa de 80%
              de economia.
            </p>

            <form id="simulation-form">

              <label class="field">
                Valor mensal da conta de luz (R$)

                <input
                  id="bill"
                  type="number"
                  min="1"
                  max="100000"
                  step="0.01"
                  value="350"
                  required
                >
              </label>

              <button
                type="submit"
                class="btn btn-primary"
                style="width:100%"
              >
                Calcular estimativa ↗
              </button>

              <p class="form-hint">
                Simulação simplificada:
                não considera impostos,
                tarifas mínimas, sazonalidade,
                dimensionamento ou condições
                reais de instalação.
              </p>

            </form>
          </div>

          <div
            class="panel-box"
            id="simulation-result"
            aria-live="polite"
          >

            <span class="eyebrow">
              02 / RESULTADO
            </span>

            <h3>
              Sua simulação aparecerá aqui
            </h3>

            <p>
              Informe o valor da conta
              e clique em calcular estimativa.
            </p>

          </div>

        </div>

      </section>

    </div>
  `;
}

function simulationResult(data) {
  const bill = Number(data.valor_conta_energia);
  const saved = Number(data.valor_economia_mensal);
  const annual = Number(data.valor_economia_anual);
  const percent = Number(
    data.percentual_economia_primeiro_mes
  );

  const after = Math.max(0, bill - saved);

  const afterHeight = bill > 0
    ? Math.max(
        6,
        Math.round(170 * (after / bill))
      )
    : 6;

  return `
    <span class="eyebrow">
      02 / RESULTADO DA API
    </span>

    <h3>Seu cenário estimado</h3>

    <div class="result-hero">

      <span>
        Economia mensal hipotética
      </span>

      <strong>
        ${currency(saved)}
      </strong>

      <span>
        Considerando
        ${percent.toLocaleString('pt-BR')}%
        de redução ilustrativa
      </span>

    </div>

    <div class="metric-grid">

      <div class="metric">
        <small>Economia anual</small>
        <strong>${currency(annual)}</strong>
      </div>

      <div class="metric">
        <small>Conta após economia</small>
        <strong>${currency(after)}</strong>
      </div>

    </div>

    <div class="chart-wrap">

      <strong>
        Conta mensal: antes × depois
      </strong>

      <div
        class="chart-bars"
        role="img"
        aria-label="Antes: ${currency(bill)}; depois: ${currency(after)}"
      >

        <div class="bar-col">
          <div
            class="bar before"
            style="height:170px"
          ></div>
        </div>

        <div class="bar-col">
          <div
            class="bar after"
            style="height:${afterHeight}px"
          ></div>
        </div>

      </div>

      <div class="bar-labels">
        <span>
          Antes<br>${currency(bill)}
        </span>

        <span>
          Depois<br>${currency(after)}
        </span>
      </div>

    </div>

    <p class="form-hint">
      ${safe(
        data.aviso ||
        'Esta é uma estimativa simplificada, não uma economia garantida.'
      )}
    </p>
  `;
}

// ======================================================
// SOLARIS IA - INTERFACE
// ======================================================

function ia() {
  return `
    <div class="page">

      ${heading(
        'SOLARIS IA',
        'Uma conversa que ilumina<span class="text-orange">.</span>',
        'Converse com a assistente educativa do Solaris, conectada ao backend Python.'
      )}

      <div class="container">

        <div class="chat-shell">

          <div class="chat-side">

            <h3>✳ Solaris IA</h3>

            <button
              type="button"
              class="btn btn-outline btn-small"
              id="new-chat"
            >
              + Nova conversa
            </button>

            <p class="muted-note">
              Pergunte sobre painéis,
              inversores, baterias,
              rastreadores e economia solar.
            </p>

            <small>
              API PRÓPRIA • Conversa não salva
            </small>

          </div>

          <div class="chat-main">

            <div class="chat-head">

              <div class="ai-avatar">✺</div>

              <div>
                <strong>Solaris IA</strong>

                <small id="chat-status">
                  Conectada ao backend
                </small>
              </div>

            </div>

            <div
              class="messages"
              id="messages"
              role="log"
              aria-live="polite"
              aria-label="Mensagens da conversa"
            >
              ${messagesMarkup()}
            </div>

            <div
              class="chat-suggestions"
              id="chat-suggestions"
            >
              ${suggestionsMarkup([
                'Como funciona a energia solar?',
                'O que é o projeto Solaris?',
                'Quanto economizaria com conta de R$ 300?'
              ])}
            </div>

            <form
              id="chat-form"
              class="chat-compose"
            >

              <input
                id="chat-input"
                type="text"
                maxlength="500"
                required
                autocomplete="off"
                placeholder="Pergunte sobre energia solar..."
                aria-label="Digite sua mensagem"
              >

              <button
                class="btn btn-primary"
                type="submit"
                id="chat-send"
              >
                Enviar ↗
              </button>

            </form>

          </div>

        </div>

        <p
          class="notice"
          style="margin:-55px 0 70px"
        >
          <strong>Importante:</strong>
          esta assistente utiliza uma base
          de conhecimento programada,
          não um modelo generativo.
          Não envie dados pessoais ou senhas.
        </p>

      </div>

    </div>
  `;
}

function messagesMarkup() {
  return messages.map(m => `
    <div class="message ${m.role === 'me'
      ? 'me'
      : 'bot'}">

      ${safe(m.text).replace(/\n/g, '<br>')}

      ${m.role === 'bot' && routes.has(m.pagina)
        ? `
          <div
            class="ia-actions"
            style="margin-top:12px"
          >

            <button
              type="button"
              class="btn btn-primary btn-small"
              data-ia-page="${safe(m.pagina)}"
            >
              Ir para ${safe(pageNames[m.pagina])} ↗
            </button>

          </div>
        `
        : ''}

    </div>
  `).join('');
}

function suggestionsMarkup(items) {
  return items.map(text => `
    <button
      type="button"
      class="chat-prompt"
      data-prompt="${safe(text)}"
    >
      ${safe(text)}
    </button>
  `).join('');
}

function refreshChat() {
  const box = $('#messages');

  if (box) {
    box.innerHTML = messagesMarkup();
    scrollChat();
  }

  const status = $('#chat-status');

  if (status) {
    status.textContent = chatBusy
      ? 'Pensando...'
      : 'Conectada ao backend • assistente educativa';
  }

  const input = $('#chat-input');
  const button = $('#chat-send');

  if (input) {
    input.disabled = chatBusy;
  }

  if (button) {
    button.disabled = chatBusy;

    button.textContent = chatBusy
      ? 'Respondendo...'
      : 'Enviar ↗';
  }

  document.querySelectorAll('.chat-prompt')
    .forEach(button => {
      button.disabled = chatBusy;
    });
}

function resetChat() {
  chatVersion++;
  chatContext = null;
  chatBusy = false;

  messages = [
    {
      role: 'bot',
      text: welcomeMessage
    }
  ];

  // Para a voz quando uma nova conversa começa.
  window.dispatchEvent(
    new Event('solaris:parar-voz')
  );

  render();
}

// ======================================================
// SOLARIS IA - COMUNICAÇÃO COM O BACKEND
// ======================================================

async function sendChat(text) {
  text = String(text || '')
    .trim()
    .slice(0, 500);

  if (!text || chatBusy) return;

  const version = chatVersion;

  messages.push({
    role: 'me',
    text
  });

  chatBusy = true;
  refreshChat();

  try {
    const data = await api(
      '/api/ia/perguntar',
      {
        method: 'POST',
        body: JSON.stringify({
          mensagem: text,
          contexto: chatContext
        })
      }
    );

    if (version !== chatVersion) return;

    const resposta =
      typeof data.resposta === 'string'
        ? data.resposta
        : 'Não recebi uma resposta válida do servidor.';

    // Resposta visual completa.
    messages.push({
      role: 'bot',
      text: resposta,
      pagina:
        typeof data.pagina === 'string' &&
        routes.has(data.pagina)
          ? data.pagina
          : null
    });

    chatContext = data.assunto || null;

    const suggestions = $('#chat-suggestions');

    if (
      suggestions &&
      Array.isArray(data.sugestoes)
    ) {
      suggestions.innerHTML = suggestionsMarkup(
        data.sugestoes.slice(0, 3)
      );
    }

    // Resposta falada separada da resposta visual.
    // Se o backend fornecer "fala", ela é utilizada.
    // Caso contrário, o sistema cria uma fala resumida.
    window.dispatchEvent(
      new CustomEvent('solaris:resposta', {
        detail: {
          pergunta: text,
          resposta,
          fala:
            typeof data.fala === 'string'
              ? data.fala
              : ''
        }
      })
    );

  } catch (err) {
    if (version !== chatVersion) return;

    messages.push({
      role: 'bot',
      text:
        '⚠️ Não consegui conversar com a API. ' +
        'Confira se o servidor está ligado ' +
        'e tente novamente.'
    });

    console.error('Solaris IA:', err);

  } finally {
    if (version === chatVersion) {
      chatBusy = false;
      refreshChat();

      const input = $('#chat-input');

      if (input) input.focus();
    }
  }
}

// ======================================================
// MINHA CONTA
// ======================================================

function account() {
  const file = location.protocol === 'file:';
  const logged = !!currentUser;

  const nome = logged
    ? String(currentUser.nome || 'Usuário')
    : '';

  return `
    <div class="page section-alt">

      ${heading(
        'MINHA CONTA',
        logged
          ? `Olá, ${safe(nome.split(' ')[0])}<span class="text-orange">!</span>`
          : 'Seu espaço no Solaris<span class="text-orange">.</span>',
        logged
          ? 'Acompanhe as próximas novidades da sua conta.'
          : 'Entre ou crie sua conta para começar sua jornada com o Solaris.'
      )}

      <section
        class="container"
        style="padding-bottom:90px"
      >

        ${logged
          ? `
            <div class="panel-box auth-card">

              <span class="eyebrow">
                CONTA CONECTADA
              </span>

              <h3>${safe(nome)}</h3>

              <p>
                ${safe(currentUser.email)}
              </p>

              <p class="notice">
                Pedidos, permissões de funcionários
                e painel administrativo ainda
                não foram integrados.
              </p>

              <button
                class="btn btn-dark"
                id="logout"
              >
                Sair da conta
              </button>

            </div>
          `
          : `
            <div class="panel-box auth-card">

              <div class="auth-switch">

                <button
                  class="chip ${authMode === 'login'
                    ? 'active'
                    : ''}"
                  data-auth="login"
                >
                  Entrar
                </button>

                <button
                  class="chip ${authMode === 'cadastro'
                    ? 'active'
                    : ''}"
                  data-auth="cadastro"
                >
                  Criar conta
                </button>

              </div>

              <h3>
                ${authMode === 'login'
                  ? 'Bem-vindo de volta!'
                  : 'Vamos começar?'}
              </h3>

              ${file
                ? `
                  <p class="notice">
                    Abra o site pelo servidor
                    para utilizar login e cadastro.
                  </p>
                `
                : `
                  <p class="muted-note">
                    O login usa a API local
                    do Solaris.
                  </p>
                `}

              <form id="auth-form">

                ${authMode === 'cadastro'
                  ? `
                    <label class="field">
                      Nome completo

                      <input
                        name="nome"
                        autocomplete="name"
                        minlength="2"
                        maxlength="120"
                        required
                      >
                    </label>

                    <label class="field">
                      Telefone (opcional)

                      <input
                        name="telefone"
                        autocomplete="tel"
                        maxlength="25"
                      >
                    </label>
                  `
                  : ''}

                <label class="field">
                  E-mail

                  <input
                    name="email"
                    type="email"
                    autocomplete="email"
                    required
                  >
                </label>

                <label class="field">
                  Senha

                  <input
                    name="senha"
                    type="password"
                    minlength="${authMode === 'cadastro'
                      ? 10
                      : 1}"
                    autocomplete="${authMode === 'cadastro'
                      ? 'new-password'
                      : 'current-password'}"
                    required
                  >
                </label>

                <p
                  class="error"
                  id="auth-error"
                  role="alert"
                ></p>

                <button
                  class="btn btn-primary"
                  type="submit"
                  style="width:100%"
                  ${file ? 'disabled' : ''}
                >
                  ${authMode === 'login'
                    ? 'Entrar na conta ↗'
                    : 'Criar conta ↗'}
                </button>

              </form>

              <p class="form-hint">
                Nunca envie sua senha pelo chat.
              </p>

            </div>
          `}

      </section>

    </div>
  `;
}

// ======================================================
// CARRINHO
// ======================================================

function cartPage() {
  const items = PRODUCTS.filter(
    p => cart[p.id]
  );

  const total = items.reduce(
    (sum, p) =>
      sum + p.price * cart[p.id],
    0
  );

  return `
    <div class="page section-alt">

      ${heading(
        'MEU CARRINHO',
        'Suas escolhas solares<span class="text-orange">.</span>',
        'Um carrinho de demonstração para testar a experiência da loja.'
      )}

      <section
        class="container"
        style="padding-bottom:95px"
      >

        ${items.length
          ? `
            <div class="two-col">

              <div class="panel-box">

                <h3>
                  Produtos selecionados
                </h3>

                <div class="cart-list">

                  ${items.map(p => `
                    <div class="cart-row">

                      <div>
                        <h3>
                          ${safe(p.name)}
                        </h3>

                        <p>
                          Preço fictício •
                          ${currency(p.price)}
                          cada
                        </p>
                      </div>

                      <div class="qty">

                        <button
                          data-qty="-1"
                          data-id="${safe(p.id)}"
                          aria-label="Diminuir quantidade"
                        >
                          −
                        </button>

                        <strong>
                          ${cart[p.id]}
                        </strong>

                        <button
                          data-qty="1"
                          data-id="${safe(p.id)}"
                          aria-label="Aumentar quantidade"
                        >
                          +
                        </button>

                      </div>

                    </div>
                  `).join('')}

                </div>

              </div>

              <div class="panel-box">

                <h3>Resumo do pedido</h3>

                <p>
                  ${items.reduce(
                    (sum, p) =>
                      sum + cart[p.id],
                    0
                  )}
                  item(ns) no carrinho
                </p>

                <div class="cart-total">
                  <span>Total fictício</span>
                  <strong>
                    ${currency(total)}
                  </strong>
                </div>

                <p class="notice">
                  O checkout está desativado.
                  Nenhum pagamento será realizado.
                </p>

                <button
                  class="btn btn-primary"
                  id="demo-checkout"
                  style="width:100%"
                >
                  ${currentUser
                    ? 'Checkout indisponível'
                    : 'Entrar para continuar'} ↗
                </button>

                <a
                  href="#/loja"
                  class="btn btn-outline"
                  style="width:100%;margin-top:12px"
                >
                  Continuar explorando
                </a>

              </div>

            </div>
          `
          : `
            <div class="empty-state">

              <div class="empty-icon">
                🛒
              </div>

              <h3>
                Seu carrinho está vazio
              </h3>

              <p>
                Que tal conhecer os painéis
                demonstrativos da Loja Solaris?
              </p>

              <a
                class="btn btn-primary"
                href="#/loja"
              >
                Explorar loja ↗
              </a>

            </div>
          `}

      </section>

    </div>
  `;
}

// ======================================================
// RENDERIZAÇÃO
// ======================================================

const renderers = {
  inicio: home,
  sobre: about,
  loja: store,
  simulador: simulator,
  ia,
  conta: account,
  carrinho: cartPage
};

function closeMenu() {
  document.body.classList.remove('menu-open');

  const overlay = $('#menu-overlay');
  const sidebar = $('#sidebar');
  const toggle = $('#menu-toggle');

  if (overlay) overlay.hidden = true;

  if (sidebar) {
    sidebar.classList.remove('open');
    sidebar.setAttribute(
      'aria-hidden',
      'true'
    );
    sidebar.inert = true;
  }

  if (toggle) {
    toggle.setAttribute(
      'aria-expanded',
      'false'
    );
  }
}

function openMenu() {
  document.body.classList.add('menu-open');

  const overlay = $('#menu-overlay');
  const sidebar = $('#sidebar');
  const toggle = $('#menu-toggle');

  if (overlay) overlay.hidden = false;

  if (sidebar) {
    sidebar.classList.add('open');
    sidebar.setAttribute(
      'aria-hidden',
      'false'
    );
    sidebar.inert = false;
  }

  if (toggle) {
    toggle.setAttribute(
      'aria-expanded',
      'true'
    );
  }

  $('#menu-close')?.focus();
}

function render() {
  if (!root) return;

  const p = page();

  root.innerHTML = renderers[p]();

  document.title =
    `${pageNames[p]} | Solaris`;

  document
    .querySelectorAll('[data-page]')
    .forEach(link => {
      const active =
        link.dataset.page === p;

      link.classList.toggle(
        'active',
        active
      );

      if (active) {
        link.setAttribute(
          'aria-current',
          'page'
        );
      } else {
        link.removeAttribute(
          'aria-current'
        );
      }
    });

  const accountShortcut =
    $('#account-shortcut');

  if (accountShortcut) {
    accountShortcut.textContent =
      currentUser
        ? 'Minha conta ↗'
        : 'Entrar ↗';
  }

  updateCartCount();
  closeMenu();

  window.scrollTo({
    top: 0,
    behavior: 'instant'
  });

  if (p === 'ia') {
    scrollChat();
  }
}

function scrollChat() {
  const box = $('#messages');

  if (box) {
    box.scrollTop = box.scrollHeight;
  }
}

// ======================================================
// EVENTOS DO MENU
// ======================================================

$('#menu-toggle')?.addEventListener(
  'click',
  openMenu
);

$('#menu-close')?.addEventListener(
  'click',
  closeMenu
);

$('#menu-overlay')?.addEventListener(
  'click',
  closeMenu
);

document.addEventListener('keydown', e => {
  if (
    e.key === 'Escape' &&
    $('#sidebar')?.classList.contains('open')
  ) {
    closeMenu();
    $('#menu-toggle')?.focus();
  }
});

$('#account-shortcut')?.addEventListener(
  'click',
  () => navigate('conta')
);

$('#cart-shortcut')?.addEventListener(
  'click',
  () => navigate('carrinho')
);

window.addEventListener(
  'hashchange',
  render
);

// ======================================================
// EVENTOS DOS BOTÕES
// ======================================================

document.addEventListener('click', e => {
  const target = e.target;

  if (!(target instanceof Element)) return;

  // NAVEGAÇÃO INTELIGENTE
  const irPara = target.closest(
    '[data-ia-page]'
  );

  if (
    irPara &&
    routes.has(irPara.dataset.iaPage)
  ) {
    navigate(irPara.dataset.iaPage);
    return;
  }

  // FILTROS DA LOJA
  const filter = target.closest(
    '[data-filter]'
  );

  if (filter) {
    storeFilter = filter.dataset.filter;

    document
      .querySelectorAll('[data-filter]')
      .forEach(button => {
        button.classList.toggle(
          'active',
          button === filter
        );
      });

    const grid = $('#product-grid');

    if (grid) {
      grid.innerHTML = filteredProducts();
    }
  }

  // ADICIONAR AO CARRINHO
  const add = target.closest(
    '.add-cart'
  );

  if (add) {
    const id = add.dataset.id;

    if (!PRODUCTS.some(p => p.id === id)) {
      return;
    }

    cart[id] = Math.min(
      99,
      (cart[id] || 0) + 1
    );

    persistCart();

    toast(
      'Produto demonstrativo adicionado ao carrinho!'
    );
  }

  // QUANTIDADE DO CARRINHO
  const qty = target.closest(
    '[data-qty]'
  );

  if (qty) {
    const id = qty.dataset.id;

    if (!PRODUCTS.some(p => p.id === id)) {
      return;
    }

    cart[id] = Math.max(
      0,
      Math.min(
        99,
        (cart[id] || 0) +
        Number(qty.dataset.qty)
      )
    );

    if (!cart[id]) {
      delete cart[id];
    }

    persistCart();
    render();
  }

  // LOGIN OU CADASTRO
  const mode = target.closest(
    '[data-auth]'
  );

  if (mode) {
    authMode = mode.dataset.auth;
    render();
  }

  // SUGESTÕES DA IA
  const prompt = target.closest(
    '.chat-prompt'
  );

  if (prompt) {
    void sendChat(
      prompt.dataset.prompt
    );
  }

  // NOVA CONVERSA
  if (target.closest('#new-chat')) {
    resetChat();
  }

  // CHECKOUT
  if (target.closest('#demo-checkout')) {
    if (!currentUser) {
      toast(
        'Faça login para continuar. Nenhuma compra real será realizada.'
      );

      navigate('conta');
    } else {
      toast(
        'Checkout ainda indisponível: esta loja é uma demonstração.'
      );
    }
  }

  // SAIR
  if (target.closest('#logout')) {
    void logout();
  }
});

// ======================================================
// BUSCA DA LOJA
// ======================================================

document.addEventListener('input', e => {
  if (e.target.id === 'store-search') {
    storeSearch = e.target.value;

    const grid = $('#product-grid');

    if (grid) {
      grid.innerHTML = filteredProducts();
    }
  }
});

// ======================================================
// FORMULÁRIOS
// ======================================================

document.addEventListener(
  'submit',
  async e => {

    // SIMULADOR
    if (
      e.target.id === 'simulation-form'
    ) {
      e.preventDefault();

      const bill = Number(
        $('#bill').value
      );

      if (
        !Number.isFinite(bill) ||
        bill < 1 ||
        bill > 100000
      ) {
        toast(
          'Confira o valor da conta de luz.'
        );
        return;
      }

      const btn = e.target.querySelector(
        'button[type="submit"]'
      );

      btn.disabled = true;
      btn.textContent = 'Calculando...';

      try {
        const data = await api(
          '/simulador/calcular',
          {
            method: 'POST',
            body: JSON.stringify({
              valor_conta_energia: bill
            })
          }
        );

        const result = $(
          '#simulation-result'
        );

        if (result) {
          result.innerHTML =
            simulationResult(data);
        }

        toast(
          'Cálculo recebido do servidor Solaris!'
        );

      } catch (err) {
        const result = $(
          '#simulation-result'
        );

        if (result) {
          result.innerHTML = `
            <span class="eyebrow">
              02 / RESULTADO
            </span>

            <h3>
              Não foi possível calcular
            </h3>

            <p class="error">
              ${safe(err.message)}
            </p>

            <p>
              Confira se o servidor Solaris
              está ligado e tente novamente.
            </p>
          `;
        }

      } finally {
        btn.disabled = false;
        btn.textContent =
          'Calcular estimativa ↗';
      }
    }

    // CHAT
    if (
      e.target.id === 'chat-form'
    ) {
      e.preventDefault();

      const input = $('#chat-input');

      if (!input) return;

      const text = input.value.trim();

      if (text) {
        void sendChat(text);
        input.value = '';
      }
    }

    // LOGIN E CADASTRO
    if (
      e.target.id === 'auth-form'
    ) {
      e.preventDefault();

      await submitAuth(e.target);
    }
  }
);

// ======================================================
// COMUNICAÇÃO COM O BACKEND
// ======================================================

async function api(url, options = {}) {
  const response = await fetch(url, {
    credentials: 'same-origin',
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers || {})
    }
  });

  let data = {};

  try {
    data = await response.json();
  } catch {}

  if (!response.ok) {
    throw Error(
      typeof data.detail === 'string'
        ? data.detail
        : 'Não foi possível concluir. Verifique se a API está ligada.'
    );
  }

  return data;
}

// ======================================================
// AUTENTICAÇÃO
// ======================================================

async function submitAuth(form) {
  const error = $('#auth-error');

  if (!error) return;

  error.textContent = '';

  if (location.protocol === 'file:') {
    error.textContent =
      'Abra o site pelo servidor para fazer login.';
    return;
  }

  const data = Object.fromEntries(
    new FormData(form)
  );

  const endpoint =
    authMode === 'cadastro'
      ? 'cadastro'
      : 'login';

  const btn = form.querySelector(
    'button[type="submit"]'
  );

  btn.disabled = true;

  try {
    currentUser = await api(
      `/api/auth/${endpoint}`,
      {
        method: 'POST',
        body: JSON.stringify(data)
      }
    );

    toast('Conta conectada!');
    render();

  } catch (err) {
    error.textContent = err.message;

  } finally {
    btn.disabled = false;
  }
}

async function logout() {
  try {
    await api(
      '/api/auth/sair',
      {
        method: 'POST'
      }
    );

    currentUser = null;

    toast('Você saiu da conta!');
    render();

  } catch (err) {
    toast(err.message);
  }
}

async function checkSession() {
  if (
    location.protocol === 'file:'
  ) {
    return;
  }

  try {
    currentUser = await api(
      '/api/auth/eu'
    );

    render();

  } catch {
    currentUser = null;
  }
}

// ======================================================
// INICIALIZAÇÃO
// ======================================================

if (!location.hash) {
  history.replaceState(
    null,
    '',
    '#/inicio'
  );
}

render();
void checkSession();

// ======================================================
// SOLARIS IA - VOZ NATURAL E MICROFONE
// 100% GRÁTIS
// ======================================================

(() => {
  'use strict';

  const Recognition =
    window.SpeechRecognition ||
    window.webkitSpeechRecognition;

  const temVoz =
    'speechSynthesis' in window &&
    'SpeechSynthesisUtterance' in window;

  let vozAtiva = true;
  let gravando = false;
  let reconhecimento = null;

  let ultimaFala = '';
  let ultimaResposta = '';
  let formularioAtual = null;

  // ====================================================
  // LIMPEZA DO TEXTO
  // ====================================================

  function limparTexto(texto) {
    return String(texto || '')
      .replace(
        /```[\s\S]*?```/g,
        ' '
      )
      .replace(
        /https?:\/\/[^\s]+/gi,
        ' '
      )
      .replace(
        /\[([^\]]+)\]\([^)]+\)/g,
        '$1'
      )
      .replace(
        /\p{Extended_Pictographic}/gu,
        ' '
      )
      .replace(
        /\p{Emoji_Modifier}/gu,
        ''
      )
      .replace(
        /[\uFE0E\uFE0F\u200D\u20E3]/g,
        ''
      )
      .replace(
        /[✳✺✻◈◆★☆•●▪]/g,
        ' '
      )
      .replace(
        /[*_`#~]/g,
        ''
      )
      .replace(
        /^\s*[-–—]\s+/gm,
        ''
      )
      .replace(
        /\bkWh\b/gi,
        'quilowatt-hora'
      )
      .replace(
        /\bkW\b/gi,
        'quilowatt'
      )
      .replace(
        /\bIA\b/g,
        'inteligência artificial'
      )
      .replace(
        /\s+/g,
        ' '
      )
      .trim();
  }

  // ====================================================
  // TRANSFORMAR RESPOSTA EM FALA CONVERSADA
  // ====================================================

  function montarFala(
    pergunta,
    resposta,
    falaDaAPI = ''
  ) {
    // O backend pode mandar um roteiro próprio.
    if (
      typeof falaDaAPI === 'string' &&
      falaDaAPI.trim()
    ) {
      return limparTexto(falaDaAPI);
    }

    const original = String(resposta || '');

    // Separar linhas do texto.
    const linhas = original
      .split(/\n+/)
      .map(linha => linha.trim())
      .filter(Boolean);

    // Ignorar títulos e comandos de navegação.
    const conteudo = linhas
      .filter(linha => {
        const texto = limparTexto(linha);

        if (!texto || texto.length < 9) {
          return false;
        }

        if (
          /^(saiba mais|clique aqui|acesse|ir para|sugestões|opções|veja também)/i
            .test(texto)
        ) {
          return false;
        }

        return true;
      })
      .join(' ');

    let limpo = limparTexto(
      conteudo || original
    );

    // Trocar expressões formais por linguagem comum.
    limpo = limpo
      .replace(
        /\bVocê pode observar que\b/gi,
        'Dá pra perceber que'
      )
      .replace(
        /\bÉ importante destacar que\b/gi,
        'Vale lembrar que'
      )
      .replace(
        /\bAlém disso\b/gi,
        'E tem mais'
      )
      .replace(
        /\bPortanto\b/gi,
        'Então'
      )
      .replace(
        /\bUtiliza\b/gi,
        'usa'
      )
      .replace(
        /\bUtilizam\b/gi,
        'usam'
      )
      .replace(
        /\bAdquirir\b/gi,
        'comprar'
      )
      .replace(
        /\bResidências\b/gi,
        'casas'
      )
      .replace(
        /\bDessa maneira\b/gi,
        'Assim'
      )
      .replace(
        /\bCom o objetivo de\b/gi,
        'Para'
      )
      .replace(
        /\bPor esse motivo\b/gi,
        'Por isso'
      );

    if (!limpo) return '';

    // A voz usa apenas as primeiras frases.
    // O texto completo permanece na tela.
    const frases =
      limpo.match(/[^.!?]+[.!?]?/g) ||
      [limpo];

    const escolhidas = [];

    let tamanho = 0;

    for (const parte of frases) {
      const frase = parte.trim();

      if (!frase) continue;

      if (escolhidas.length >= 3) {
        break;
      }

      if (
        tamanho + frase.length > 320 &&
        escolhidas.length > 0
      ) {
        break;
      }

      escolhidas.push(frase);
      tamanho += frase.length;
    }

    if (!escolhidas.length) {
      escolhidas.push(
        limpo.slice(0, 230)
      );
    }

    let resumo = escolhidas
      .join(' ')
      .replace(
        /\s+([,.!?])/g,
        '$1'
      )
      .trim();

    if (!/[.!?]$/.test(resumo)) {
      resumo += '.';
    }

    // Introdução diferente conforme a pergunta.
    const perguntaLimpa =
      limparTexto(pergunta).toLowerCase();

    let inicio = 'Olha só! ';

    if (
      /^(como|de que forma)\b/.test(
        perguntaLimpa
      )
    ) {
      inicio = 'Funciona assim: ';
    }

    else if (
      /^(o que|qual|quem)\b/.test(
        perguntaLimpa
      )
    ) {
      inicio = 'Boa pergunta! ';
    }

    else if (
      /^(posso|consigo|dá para|tem como)\b/
        .test(perguntaLimpa)
    ) {
      inicio = 'Vamos lá! ';
    }

    else if (
      /^(quanto|quantos)\b/.test(
        perguntaLimpa
      )
    ) {
      inicio = 'Vamos entender isso: ';
    }

    // Erros não recebem introdução animada.
    if (
      /^(não consegui|não entendi|desculpe|ocorreu um erro|erro)/i
        .test(resumo)
    ) {
      inicio = '';
    }

    return inicio + resumo;
  }

  // ====================================================
  // ESCOLHER VOZ BRASILEIRA
  // ====================================================

  function escolherVoz() {
    if (!temVoz) return null;

    const vozes =
      window.speechSynthesis.getVoices();

    const brasileiras = vozes.filter(
      voz =>
        voz.lang
          .toLowerCase()
          .replace('_', '-') === 'pt-br'
    );

    const preferencias = [
      /Microsoft Francisca.*Online/i,
      /Microsoft Antonio.*Online/i,
      /Microsoft Francisca/i,
      /Microsoft Antonio/i,
      /Google português do Brasil/i,
      /Google português/i
    ];

    for (const padrao of preferencias) {
      const encontrada = brasileiras.find(
        voz => padrao.test(voz.name)
      );

      if (encontrada) {
        return encontrada;
      }
    }

    return brasileiras[0] || null;
  }

  // ====================================================
  // FALAR
  // ====================================================

  function pararVoz() {
    if (temVoz) {
      window.speechSynthesis.cancel();
    }
  }

  function falar(texto) {
    if (
      !temVoz ||
      !vozAtiva ||
      gravando
    ) {
      return;
    }

    const mensagem = limparTexto(texto);

    if (!mensagem) return;

    pararVoz();

    const fala =
      new SpeechSynthesisUtterance(
        mensagem
      );

    fala.lang = 'pt-BR';
    fala.rate = 0.98;
    fala.pitch = 1;
    fala.volume = 1;

    const voz = escolherVoz();

    if (voz) {
      fala.voice = voz;
    }

    window.speechSynthesis.speak(fala);
  }

  // ====================================================
  // RECEBER A RESPOSTA DA IA
  // ====================================================

  window.addEventListener(
    'solaris:resposta',
    evento => {
      const dados = evento.detail || {};

      ultimaResposta = String(
        dados.resposta || ''
      );

      ultimaFala = montarFala(
        dados.pergunta || '',
        ultimaResposta,
        dados.fala || ''
      );

      falar(ultimaFala);
    }
  );

  window.addEventListener(
    'solaris:parar-voz',
    () => {
      pararVoz();

      ultimaFala = '';
      ultimaResposta = '';
    }
  );

  // ====================================================
  // MICROFONE
  // ====================================================

  function atualizarMicrofone() {
    const botao =
      document.querySelector(
        '#solaris-mic'
      );

    if (!botao) return;

    botao.textContent = gravando
      ? '🔴'
      : '🎤';

    botao.title = gravando
      ? 'Parar de ouvir'
      : 'Falar com a Solaris IA';

    botao.setAttribute(
      'aria-label',
      botao.title
    );

    botao.style.background = gravando
      ? '#ef4444'
      : '#f5b800';
  }

  function iniciarMicrofone() {
    if (!Recognition) {
      alert(
        'Reconhecimento de voz indisponível. ' +
        'Tente usar Chrome ou Edge.'
      );
      return;
    }

    if (gravando) {
      reconhecimento?.stop();
      return;
    }

    if (
      !document.querySelector(
        '#chat-input'
      )
    ) {
      return;
    }

    pararVoz();

    reconhecimento = new Recognition();

    reconhecimento.lang = 'pt-BR';
    reconhecimento.continuous = false;
    reconhecimento.interimResults = false;
    reconhecimento.maxAlternatives = 1;

    reconhecimento.onstart = () => {
      gravando = true;
      atualizarMicrofone();
    };

    reconhecimento.onresult = evento => {
      const texto =
        evento.results?.[0]?.[0]
          ?.transcript?.trim();

      const campo =
        document.querySelector(
          '#chat-input'
        );

      const formulario =
        document.querySelector(
          '#chat-form'
        );

      if (
        !texto ||
        !campo ||
        !formulario
      ) {
        return;
      }

      campo.value = texto;

      formulario.requestSubmit();
    };

    reconhecimento.onerror = evento => {
      if (
        evento.error === 'not-allowed'
      ) {
        alert(
          'Permita o acesso ao microfone ' +
          'nas configurações do navegador.'
        );
      }

      else if (
        !['no-speech', 'aborted'].includes(
          evento.error
        )
      ) {
        console.warn(
          'Microfone Solaris:',
          evento.error
        );
      }
    };

    reconhecimento.onend = () => {
      gravando = false;
      atualizarMicrofone();
    };

    try {
      reconhecimento.start();

    } catch (erro) {
      gravando = false;
      atualizarMicrofone();

      console.error(
        'Microfone Solaris:',
        erro
      );
    }
  }

  // ====================================================
  // INSTALAR BOTÕES
  // ====================================================

  function instalarBotoes() {
    const formulario =
      document.querySelector(
        '#chat-form'
      );

    if (!formulario) return;

    // BOTÃO DO MICROFONE
    if (
      !document.querySelector(
        '#solaris-mic'
      )
    ) {
      const botao =
        document.createElement(
          'button'
        );

      botao.type = 'button';
      botao.id = 'solaris-mic';
      botao.textContent = '🎤';

      botao.title =
        'Falar com a Solaris IA';

      botao.setAttribute(
        'aria-label',
        botao.title
      );

      Object.assign(
        botao.style,
        {
          border: 'none',
          borderRadius: '12px',
          padding: '10px 14px',
          background: '#f5b800',
          color: '#17200c',
          fontSize: '20px',
          cursor: 'pointer',
          flexShrink: '0'
        }
      );

      botao.addEventListener(
        'click',
        iniciarMicrofone
      );

      const enviar =
        formulario.querySelector(
          '#chat-send'
        );

      if (enviar) {
        formulario.insertBefore(
          botao,
          enviar
        );
      } else {
        formulario.appendChild(
          botao
        );
      }
    }

    const cabecalho =
      document.querySelector(
        '.chat-head'
      );

    if (!cabecalho) return;

    // BOTÃO LIGAR/DESLIGAR VOZ
    if (
      !document.querySelector(
        '#solaris-voz'
      )
    ) {
      const botao =
        document.createElement(
          'button'
        );

      botao.type = 'button';
      botao.id = 'solaris-voz';

      Object.assign(
        botao.style,
        {
          marginLeft: 'auto',
          border: '1px solid #d9d9d9',
          borderRadius: '12px',
          padding: '9px 12px',
          background: '#ffffff',
          color: '#222222',
          fontWeight: '700',
          cursor: 'pointer',
          flexShrink: '0'
        }
      );

      function atualizar() {
        botao.textContent = vozAtiva
          ? '🔊 Voz ligada'
          : '🔇 Voz desligada';

        botao.setAttribute(
          'aria-pressed',
          String(vozAtiva)
        );
      }

      botao.addEventListener(
        'click',
        () => {
          vozAtiva = !vozAtiva;

          if (!vozAtiva) {
            pararVoz();
          }

          atualizar();
        }
      );

      atualizar();

      cabecalho.appendChild(
        botao
      );
    }

    // BOTÃO REPETIR RESPOSTA
    if (
      !document.querySelector(
        '#solaris-repetir'
      )
    ) {
      const botao =
        document.createElement(
          'button'
        );

      botao.type = 'button';
      botao.id = 'solaris-repetir';
      botao.textContent = '🔁';

      botao.title =
        'Repetir última resposta';

      botao.setAttribute(
        'aria-label',
        'Repetir última resposta da Solaris'
      );

      Object.assign(
        botao.style,
        {
          border: '1px solid #d9d9d9',
          borderRadius: '12px',
          padding: '9px 12px',
          background: '#ffffff',
          color: '#222222',
          fontSize: '18px',
          cursor: 'pointer',
          flexShrink: '0'
        }
      );

      botao.addEventListener(
        'click',
        () => {
          if (!ultimaFala) {
            toast(
              'A Solaris ainda não respondeu.'
            );
            return;
          }

          if (!vozAtiva) {
            toast(
              'Ative a voz para repetir a resposta.'
            );
            return;
          }

          falar(ultimaFala);
        }
      );

      cabecalho.appendChild(
        botao
      );
    }
  }

  // ====================================================
  // FUNCIONAR APÓS MUDAR DE PÁGINA
  // ====================================================

  function verificarInterface() {
    instalarBotoes();

    const formulario =
      document.querySelector(
        '#chat-form'
      );

    if (!formulario) {
      if (formularioAtual !== null) {
        pararVoz();

        if (gravando) {
          reconhecimento?.stop();
        }
      }

      formularioAtual = null;
    } else {
      formularioAtual = formulario;
    }
  }

  const conteudo =
    document.querySelector(
      '#conteudo'
    );

  if (conteudo) {
    new MutationObserver(
      verificarInterface
    ).observe(
      conteudo,
      {
        childList: true
      }
    );
  }

  verificarInterface();

  console.log(
    'Solaris IA: voz conversada e microfone prontos!'
  );
})();
