/*  
configuração da URL base da API, que é usada para fazer requisições ao backend. Neste caso, a API está rodando localmente na porta 8000.
*/
const API = 'http://localhost:8000';
/* state
O objeto state é usado para armazenar o estado global da aplicação, incluindo informações sobre o usuário autenticado, as disciplinas, o progresso, os projetos, os eventos, as inscrições e as oportunidades. Ele também inclui filtros para exibir apenas disciplinas obrigatórias ou optativas, e para filtrar por período ou tipo de evento. O estado é atualizado conforme o usuário interage com a aplicação e é usado para renderizar a interface do usuário de acordo com os dados atuais.
*/
let state = {
  token: localStorage.getItem('rb_token') || null,
  user: JSON.parse(localStorage.getItem('rb_user') || 'null'),
  disciplinas: [],
  progresso: [],
  projetos: [],
  eventos: [],
  inscricoes: [],
  oportunidades: [],
  discFilter: 'all',
  periodoFilter: null,
  eventoFilter: 'all',
};


/*  API helpers */
async function api(method, path, body) {
  const opts = {
    method,
    headers: { 'Content-Type': 'application/json' },
  };
  if (state.token) opts.headers['Authorization'] = 'Bearer ' + state.token;
  if (body) opts.body = JSON.stringify(body);
  try {
    const r = await fetch(API + path, opts);
    if (r.status === 204) return null;
    const data = await r.json();
    if (!r.ok) throw new Error(data.detail || 'Erro na requisição');
    return data;
  } catch(e) {
    throw e;
  }
}

/* TOAST
 toast(msg, type) exibe uma mensagem de notificação (toast) na tela. O parâmetro msg é a mensagem a ser exibida, 
 e o parâmetro type define o tipo de notificação (por exemplo, 'success', 'error', 'info'), que afeta a aparência do toast. O toast é automaticamente removido após 3 segundos.
*/

function toast(msg, type='info') { 
  const el = document.createElement('div');
  el.className = `toast toast-${type}`;
  el.innerHTML = `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
    ${type==='success'?'<polyline points="20,6 9,17 4,12"/>'
    :type==='error'?'<circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/>'
    :'<circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><circle cx="12" cy="16" r="1" fill="currentColor"/>'}
  </svg> ${msg}`;
  document.getElementById('toast-container').appendChild(el);
  setTimeout(() => el.remove(), 3000);
}

/* MODAL */
function openModal(id) { document.getElementById(id).classList.add('open'); }
function closeModal(id) { document.getElementById(id).classList.remove('open'); }

/*  AUTH */
function toggleAuth(mode) {
  document.getElementById('form-login').style.display    = mode==='login'    ? '' : 'none';
  document.getElementById('form-register').style.display = mode==='register' ? '' : 'none';
}

async function doLogin() {
  const email = document.getElementById('login-email').value.trim();
  const senha = document.getElementById('login-senha').value;
  if (!email || !senha) return toast('Preencha e-mail e senha', 'error');
  const btn = document.getElementById('btn-login');
  btn.innerHTML = '<span class="spinner"></span>';
  btn.disabled = true;
  try {
    const data = await api('POST', '/api/usuarios/login', { email, senha });
    state.token = data.access_token;
    state.user  = data.user;
    localStorage.setItem('rb_token', state.token);
    localStorage.setItem('rb_user', JSON.stringify(state.user));
    toast('Bem-vindo de volta!', 'success');
    showApp();
  } catch(e) {
    toast(e.message, 'error');
  } finally {
    btn.innerHTML = 'Entrar';
    btn.disabled = false;
  }
}

async function doRegister() {
  const nome  = document.getElementById('reg-nome').value.trim();
  const email = document.getElementById('reg-email').value.trim();
  const senha = document.getElementById('reg-senha').value;
  if (!nome || !email || !senha) return toast('Preencha todos os campos', 'error');
  const btn = document.getElementById('btn-register');
  btn.innerHTML = '<span class="spinner"></span>';
  btn.disabled = true;
  try {
    await api('POST', '/api/usuarios/registro', { nome, email, senha });
    toast('Conta criada! Faça login.', 'success');
    toggleAuth('login');
  } catch(e) {
    toast(e.message, 'error');
  } finally {
    btn.innerHTML = 'Criar conta';
    btn.disabled = false;
  }
}

function doLogout() {
  state.token = null;
  state.user  = null;
  localStorage.removeItem('rb_token');
  localStorage.removeItem('rb_user');
  showAuth();
}

/* APP INIT */
function showAuth() {
  document.getElementById('auth-view').style.display = '';
  document.getElementById('app-view').style.display  = 'none';
}

function showApp() {
  document.getElementById('auth-view').style.display = 'none';
  document.getElementById('app-view').style.display  = '';
  updateSidebar();
  loadAll();
  navigate('dashboard');
}

function updateSidebar() {
  if (!state.user) return;
  const name = state.user.nome || 'Usuário';
  document.getElementById('sidebar-avatar').textContent = name.charAt(0).toUpperCase();
  document.getElementById('sidebar-name').textContent   = name;
  document.getElementById('sidebar-role').textContent   = state.user.nivel >= 2 ? 'Administrador' : 'Estudante';
  document.getElementById('topbar-nivel').textContent   = 'Nível ' + (state.user.nivel || 1);
  document.getElementById('dash-name').textContent      = name.split(' ')[0];
}

async function loadAll() {
  await Promise.allSettled([
    loadDisciplinas(),
    loadProjetos(),
    loadEventos(),
    loadOportunidades(),
    loadInscricoes(),
  ]);
  await loadProgresso();
  updateDashboard();
  populateDiscSelect();
  populateCanvasDiscSelect?.();
}

/* Navegação */
const pageTitles = {
  dashboard: 'Dashboard',
  disciplinas: 'Disciplinas',
  materiais: 'Materiais',
  trilha: 'Trilha Acadêmica',
  projetos: 'Projetos',
  eventos: 'Eventos',
  oportunidades: 'Oportunidades',
  perfil: 'Perfil',
};

function navigate(page) {
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
  const el = document.getElementById('page-' + page);
  if (el) {
    el.classList.add('active');
    el.classList.remove('page-fade');
    void el.offsetWidth;
    el.classList.add('page-fade');
  }
  document.querySelector(`[data-page="${page}"]`)?.classList.add('active');
  document.getElementById('topbar-title').textContent = pageTitles[page] || page;
  closeSidebar();

  if (page === 'perfil') renderPerfil();
  if (page === 'trilha' && !trilhaState.nos.length) loadTrilha();
  if (page === 'materiais') {
    populateCanvasDiscSelect?.();
    loadCanvasWorkspace?.();
  }
}

/* SIDEBAR MOBILE */
function toggleSidebar() {
  document.getElementById('sidebar').classList.toggle('open');
  document.getElementById('sidebar-overlay').classList.toggle('open');
}
function closeSidebar() {
  document.getElementById('sidebar').classList.remove('open');
  document.getElementById('sidebar-overlay').classList.remove('open');
}

/* DISCIPLINAS */
async function loadDisciplinas() {
  try {
    state.disciplinas = await api('GET', '/api/disciplinas/') || [];
  } catch(e) {
    state.disciplinas = getMockDisciplinas();
  }
  renderDiscPeriodoPills();
  renderDisc();
}

async function loadProgresso() {
  try {
    state.progresso = await api('GET', '/api/disciplinas/progresso/me') || [];
  } catch(e) {
    state.progresso = [];
  }
}

function getProgresso(discId) {
  return state.progresso.find(p => p.disciplina_id === discId);
}

function renderDiscPeriodoPills() {
  const periodos = [...new Set(state.disciplinas.filter(d => d.periodo).map(d => d.periodo))].sort((a,b)=>a-b);
  const container = document.getElementById('periodo-pills');
  container.innerHTML = `<button class="periodo-pill active" onclick="setPeriodo(null, this)">Todos os períodos</button>` +
    periodos.map(p => `<button class="periodo-pill" onclick="setPeriodo(${p}, this)">${p}º período</button>`).join('');
}

function setPeriodo(p, btn) {
  state.periodoFilter = p;
  document.querySelectorAll('.periodo-pill').forEach(el => el.classList.remove('active'));
  btn.classList.add('active');
  renderDisc();
}

function filterDisc(type) {
  state.discFilter = type;
  document.querySelectorAll('#disc-tabs .tab-btn').forEach((b,i) => {
    b.classList.toggle('active', ['all','obrigatorias','optativas'][i] === type);
  });
  renderDisc();
}

function renderDisc() {
  let list = state.disciplinas;
  if (state.discFilter === 'obrigatorias') list = list.filter(d => d.obrigatoria);
  if (state.discFilter === 'optativas')    list = list.filter(d => !d.obrigatoria);
  if (state.periodoFilter)                 list = list.filter(d => d.periodo === state.periodoFilter);

  const grid = document.getElementById('disc-grid');
  if (!list.length) {
    grid.innerHTML = '<div style="grid-column:1/-1"><div class="empty-state"><p>Nenhuma disciplina encontrada</p></div></div>';
    return;
  }
  grid.innerHTML = list.map(d => {
    const prog = getProgresso(d.id);
    const status = prog ? prog.status : null;
    const statusClass = status ? 'status-' + status : 'status-null';
    return `<div class="disc-card" onclick="openDiscModal(${d.id})">
      <div class="disc-card-top">
        <div>
          <div class="disc-name">${d.nome}</div>
          <div class="disc-code">${d.codigo} · ${d.carga_horaria}h</div>
        </div>
        ${d.periodo ? `<span class="periodo-dot">${d.periodo}</span>` : '<span class="badge-pill badge-orange">Optativa</span>'}
      </div>
      <div class="disc-footer">
        <select class="status-select ${statusClass}" onchange="setProgresso(event, ${d.id})" onclick="event.stopPropagation()">
          <option value="" ${!status?'selected':''}>Sem status</option>
          <option value="CURSANDO"  ${status==='CURSANDO' ?'selected':''}>Cursando</option>
          <option value="APROVADO"  ${status==='APROVADO' ?'selected':''}>Aprovado</option>
          <option value="REPROVADO" ${status==='REPROVADO'?'selected':''}>Reprovado</option>
          <option value="TRANCADO"  ${status==='TRANCADO' ?'selected':''}>Trancado</option>
        </select>
        <span style="font-size:12px;color:var(--gray-400)">${d.carga_horaria}h</span>
      </div>
    </div>`;
  }).join('');
}

async function setProgresso(e, discId) {
  const status = e.target.value;
  const select = e.target;
  try {
    if (!status) {
      await api('DELETE', `/api/disciplinas/progresso/${discId}`);
      state.progresso = state.progresso.filter(p => p.disciplina_id !== discId);
    } else {
      const result = await api('POST', '/api/disciplinas/progresso', { disciplina_id: discId, status });
      const idx = state.progresso.findIndex(p => p.disciplina_id === discId);
      if (idx >= 0) state.progresso[idx] = result;
      else state.progresso.push(result);
    }
    select.className = `status-select status-${status || 'null'}`;
    toast('Progresso atualizado', 'success');
    updateDashboard();
  } catch(e) {
    toast(e.message, 'error');
  }
}

function openDiscModal(discId) {
  const d = state.disciplinas.find(x => x.id === discId);
  if (!d) return;
  document.getElementById('modal-disc-title').textContent = d.nome;
  document.getElementById('modal-disc-body').innerHTML = `
    <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:16px">
      <span class="badge-pill badge-orange">${d.codigo}</span>
      ${d.periodo ? `<span class="badge-pill badge-blue">${d.periodo}º período</span>` : '<span class="badge-pill badge-orange">Optativa</span>'}
      <span class="badge-pill" style="background:var(--gray-50);color:var(--gray-600)">${d.carga_horaria}h</span>
    </div>
    <p style="font-size:14px;color:var(--gray-400);margin-bottom:16px">
      ${d.obrigatoria ? 'Disciplina obrigatória' : 'Disciplina optativa'}
    </p>
    <button class="btn btn-secondary btn-sm" onclick="navigate('materiais');closeModal('modal-disc')">Ver materiais</button>
  `;
  openModal('modal-disc');
}

/* MATERIAIS */
state.materiais        = [];
state.materiaisFilter  = 'all';

function populateDiscSelect() {
  const sel = document.getElementById('canvas-disc-select');

  if (!sel) {
    console.error('canvas-disc-select não encontrado');
    return;
  }

  sel.innerHTML =
    '<option value="">Selecione uma disciplina...</option>' +
    state.disciplinas.map(d =>
      `<option value="${d.id}">${d.nome}</option>`
    ).join('');
}

async function loadMateriais() {
  const discId = document.getElementById('canvas-discc-select').value;
  const content = document.getElementById('mat-content');
  const searchWrap = document.getElementById('mat-search-wrap');
  const addBtnWrap = document.getElementById('mat-add-btn-wrap');

  if (!discId) {
    searchWrap.style.display = 'none';
    addBtnWrap.style.display = 'none';
    content.innerHTML = `<div class="mat-empty-hero">
      <div class="mat-empty-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="40" height="40"><path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/><polyline points="13,2 13,9 20,9"/></svg></div>
      <p class="mat-empty-title">Selecione uma disciplina</p>
      <p class="mat-empty-sub">Escolha uma disciplina acima para visualizar e gerenciar seus materiais de estudo</p>
    </div>`;
    return;
  }

  searchWrap.style.display = '';
  addBtnWrap.style.display = '';
  content.innerHTML = '<div class="mat-loading"><span class="spinner" style="border-color:var(--orange);border-top-color:transparent"></span><span>Carregando materiais...</span></div>';

  try {
    const fetched = await api('GET', `/api/materiais/disciplina/${discId}`);
    state.materiais = (fetched || []).map(m => ({
      ...m,
      tipo: m.tipo || (m.link && m.link.startsWith('NOTA:') ? 'ANOTACAO' : 'LINK'),
    }));
  } catch(e) {
    state.materiais = [];
  }
  state.materiaisFilter = 'all';
  document.querySelectorAll('#mat-type-tabs .mat-type-tab').forEach((b,i)=>b.classList.toggle('active',i===0));
  document.getElementById('mat-search').value = '';
  renderMateriais();
}

function filterMatType(type, btn) {
  state.materiaisFilter = type;
  document.querySelectorAll('#mat-type-tabs .mat-type-tab').forEach(b=>b.classList.remove('active'));
  btn.classList.add('active');
  renderMateriais();
}

function filterMateriais() {
  renderMateriais();
}

function renderMateriais() {
  const content = document.getElementById('mat-content');
  const q = (document.getElementById('mat-search')?.value || '').toLowerCase();
  let list = state.materiais;
  if (state.materiaisFilter !== 'all') list = list.filter(m => (m.tipo || 'LINK') === state.materiaisFilter);
  if (q) list = list.filter(m => m.titulo.toLowerCase().includes(q) || (m.descricao||'').toLowerCase().includes(q));

  if (!state.materiais.length) {
    content.innerHTML = `<div class="mat-empty-hero">
      <div class="mat-empty-icon mat-empty-add">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="40" height="40"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
      </div>
      <p class="mat-empty-title">Nenhum material ainda</p>
      <p class="mat-empty-sub">Adicione links, livros ou anotações para esta disciplina</p>
      <button class="btn btn-primary" style="margin-top:16px" onclick="openModal('modal-material')">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" width="16" height="16"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
        Adicionar primeiro material
      </button>
    </div>`;
    return;
  }

  if (!list.length) {
    content.innerHTML = `<div class="mat-empty-hero">
      <div class="mat-empty-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="40" height="40"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg></div>
      <p class="mat-empty-title">Nenhum resultado</p>
      <p class="mat-empty-sub">Tente outro filtro ou termo de busca</p>
    </div>`;
    return;
  }

  // group by type
  const groups = { LINK: [], LIVRO: [], ANOTACAO: [] };
  list.forEach(m => { const t = m.tipo || 'LINK'; (groups[t] = groups[t]||[]).push(m); });

  const typeLabels = { LINK: 'Links', LIVRO: 'Livros', ANOTACAO: 'Anotações' };
  const typeIcons = {
    LINK: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>`,
    LIVRO: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>`,
    ANOTACAO: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>`,
  };

  let html = '';
  for (const [tipo, items] of Object.entries(groups)) {
    if (!items.length) continue;
    html += `<div class="mat-group">
      <div class="mat-group-header">
        <span class="mat-group-icon mat-gi-${tipo.toLowerCase()}">${typeIcons[tipo]}</span>
        <span class="mat-group-label">${typeLabels[tipo]}</span>
        <span class="mat-group-count">${items.length}</span>
      </div>
      <div class="mat-cards">`;

    items.forEach(m => {
      const isNota = tipo === 'ANOTACAO';
      const nota = m.link && m.link.startsWith('NOTA:') ? m.link.slice(5) : (m.nota || '');
      html += `<div class="mat-card mat-card-${tipo.toLowerCase()}" data-id="${m.id}">
        <div class="mat-card-body">
          <div class="mat-card-title">${m.titulo}</div>
          ${m.descricao ? `<div class="mat-card-desc">${m.descricao}</div>` : ''}
          ${isNota && nota ? `<div class="mat-card-nota-preview">${nota.slice(0,120)}${nota.length>120?'…':''}</div>` : ''}
          ${!isNota && m.link ? `<div class="mat-card-url">${m.link}</div>` : ''}
        </div>
        <div class="mat-card-actions">
          ${isNota
            ? `<button class="btn btn-ghost btn-sm" onclick="viewNota(${m.id})">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
                Ver
              </button>`
            : `<a href="${m.link}" target="_blank" class="btn btn-ghost btn-sm">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15,3 21,3 21,9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
                Abrir
              </a>`
          }
          <button class="btn btn-danger btn-sm mat-del-btn" onclick="deleteMaterial(${m.id})">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14"><polyline points="3,6 5,6 21,6"/><path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/><path d="M10 11v6"/><path d="M14 11v6"/><path d="M9 6V4h6v2"/></svg>
          </button>
        </div>
      </div>`;
    });

    html += `</div></div>`;
  }

  content.innerHTML = html;
}

function viewNota(id) {
  const m = state.materiais.find(x => x.id === id);
  if (!m) return;
  const nota = m.link && m.link.startsWith('NOTA:') ? m.link.slice(5) : (m.nota || '');
  document.getElementById('modal-nota-title').textContent = m.titulo;
  document.getElementById('modal-nota-content').innerHTML = nota.replace(/\n/g, '<br>');
  openModal('modal-nota');
}

async function deleteMaterial(id) {
  if (!confirm('Excluir este material?')) return;
  try {
    await api('DELETE', `/api/materiais/${id}`);
    state.materiais = state.materiais.filter(m => m.id !== id);
    renderMateriais();
    toast('Material excluído', 'success');
  } catch(e) {
    toast(e.message, 'error');
  }
}

function selectMatTipo(tipo, btn) {
  document.getElementById('mat-tipo').value = tipo;
  document.querySelectorAll('.mat-type-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  const linkGroup = document.getElementById('mat-link-group');
  const notaGroup = document.getElementById('mat-nota-group');
  const linkLabel = document.getElementById('mat-link-label');
  if (tipo === 'ANOTACAO') {
    linkGroup.style.display = 'none';
    notaGroup.style.display = '';
  } else {
    linkGroup.style.display = '';
    notaGroup.style.display = 'none';
    linkLabel.innerHTML = tipo === 'LIVRO'
      ? 'Link do livro / PDF <span style="color:var(--red)">*</span>'
      : 'URL do recurso <span style="color:var(--red)">*</span>';
  }
}

async function submitMaterial() {
  const discId = document.getElementById('canvas-discc-select').value;
  if (!discId) return toast('Selecione uma disciplina primeiro', 'error');
  const tipo   = document.getElementById('mat-tipo').value;
  const titulo = document.getElementById('mat-titulo').value.trim();
  const desc   = document.getElementById('mat-desc').value.trim();
  const link   = document.getElementById('mat-link').value.trim();
  const nota   = document.getElementById('mat-nota').value.trim();

  if (!titulo) return toast('Título obrigatório', 'error');
  if (tipo !== 'ANOTACAO' && !link) return toast('Informe o link', 'error');
  if (tipo === 'ANOTACAO' && !nota) return toast('Escreva sua anotação', 'error');

  const payload = {
    disciplina_id: Number(discId),
    titulo,
    descricao: desc || null,
    link: tipo === 'ANOTACAO' ? 'NOTA:' + nota : link,
    tipo,
  };

  try {
    const created = await api('POST', '/api/materiais/', payload);
    state.materiais.unshift({ ...created, tipo });
    renderMateriais();
    closeModal('modal-material');
    // reset form
    document.getElementById('mat-titulo').value = '';
    document.getElementById('mat-desc').value   = '';
    document.getElementById('mat-link').value   = '';
    document.getElementById('mat-nota').value   = '';
    selectMatTipo('LINK', document.querySelector('.mat-type-btn[data-tipo="LINK"]'));
    toast('Material adicionado!', 'success');
  } catch(e) {
    toast(e.message, 'error');
  }
}

/* PROJETOS */
async function loadProjetos() {
  try {
    state.projetos = await api('GET', '/api/projetos/') || [];
  } catch(e) {
    state.projetos = getMockProjetos();
  }
  renderProjetos();
}

function renderProjetos() {
  const grid = document.getElementById('project-grid');
  if (!state.projetos.length) {
    grid.innerHTML = `<div style="grid-column:1/-1"><div class="empty-state">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><polyline points="16,18 22,12 16,6"/><polyline points="8,6 2,12 8,18"/></svg>
      <p>Nenhum projeto publicado ainda</p>
    </div></div>`;
    return;
  }
  grid.innerHTML = state.projetos.map(p => `
    <div class="project-card">
      <div>
        <div class="project-title">${p.titulo}</div>
        ${p.descricao ? `<div class="project-desc">${p.descricao}</div>` : ''}
      </div>
      <div class="project-footer">
        <span class="project-author">por usuário #${p.user_id}</span>
        ${p.github_link ? `<a href="${p.github_link}" target="_blank" class="github-link">
          <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.3 3.44 9.8 8.2 11.4.6.11.82-.26.82-.57v-2c-3.34.73-4.04-1.61-4.04-1.61-.55-1.4-1.34-1.77-1.34-1.77-1.09-.74.08-.73.08-.73 1.2.09 1.84 1.24 1.84 1.24 1.07 1.83 2.8 1.3 3.49.99.1-.78.42-1.3.76-1.6-2.67-.3-5.47-1.33-5.47-5.93 0-1.31.47-2.38 1.24-3.22-.13-.3-.54-1.52.12-3.18 0 0 1.01-.32 3.3 1.23a11.5 11.5 0 0 1 3-.4c1.02 0 2.04.13 3 .4 2.28-1.55 3.29-1.23 3.29-1.23.66 1.66.25 2.88.12 3.18.77.84 1.24 1.91 1.24 3.22 0 4.61-2.81 5.63-5.48 5.92.43.37.82 1.1.82 2.22v3.29c0 .32.22.69.83.57C20.56 21.8 24 17.3 24 12c0-6.63-5.37-12-12-12z"/></svg>
          GitHub
        </a>` : ''}
      </div>
      ${p.user_id === state.user?.id ? `
        <button class="btn btn-danger btn-sm" onclick="deleteProjeto(${p.id})">Excluir</button>
      ` : ''}
    </div>
  `).join('');
}

async function submitProjeto() {
  const titulo     = document.getElementById('proj-titulo').value.trim();
  const descricao  = document.getElementById('proj-desc').value.trim();
  const githubLink = document.getElementById('proj-github').value.trim();
  if (!titulo) return toast('Título obrigatório', 'error');
  try {
    const proj = await api('POST', '/api/projetos/', { titulo, descricao, github_link: githubLink || null });
    state.projetos.unshift(proj);
    renderProjetos();
    closeModal('modal-projeto');
    document.getElementById('proj-titulo').value = '';
    document.getElementById('proj-desc').value   = '';
    document.getElementById('proj-github').value = '';
    toast('Projeto publicado!', 'success');
    updateDashboard();
  } catch(e) {
    toast(e.message, 'error');
  }
}

async function deleteProjeto(id) {
  if (!confirm('Excluir este projeto?')) return;
  try {
    await api('DELETE', `/api/projetos/${id}`);
    state.projetos = state.projetos.filter(p => p.id !== id);
    renderProjetos();
    toast('Projeto excluído', 'success');
  } catch(e) {
    toast(e.message, 'error');
  }
}

/*  EVENTOS */
async function loadEventos() {
  try {
    state.eventos = await api('GET', '/api/eventos/') || [];
  } catch(e) {
    state.eventos = getMockEventos();
  }
  renderEventos();
}

async function loadInscricoes() {
  try {
    state.inscricoes = await api('GET', '/api/eventos/inscricoes/me') || [];
  } catch(e) {
    state.inscricoes = [];
  }
}

function filterEventos(type) {
  state.eventoFilter = type;
  document.querySelectorAll('#evento-tabs .tab-btn').forEach((b,i) => {
    b.classList.toggle('active', ['all','EVENTO','HACKATHON','meus'][i] === type);
  });
  renderEventos();
}

function renderEventos() {
  let list = state.eventos;
  if (state.eventoFilter === 'EVENTO')    list = list.filter(e => e.tipo === 'EVENTO');
  if (state.eventoFilter === 'HACKATHON') list = list.filter(e => e.tipo === 'HACKATHON');
  if (state.eventoFilter === 'meus')      list = list.filter(e => state.inscricoes.some(i => i.evento_id === e.id));

  const container = document.getElementById('event-list');
  if (!list.length) {
    container.innerHTML = `<div class="empty-state">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
      <p>Nenhum evento encontrado</p>
    </div>`;
    return;
  }
  container.innerHTML = list.map(ev => {
    const d = ev.data_evento ? new Date(ev.data_evento + 'T00:00:00') : null;
    const isInscrito = state.inscricoes.some(i => i.evento_id === ev.id);
    return `<div class="event-card ${ev.tipo === 'HACKATHON' ? 'event-hackathon' : ''}">
      ${d ? `<div class="event-date-box">
        <div class="event-date-day">${d.getDate().toString().padStart(2,'0')}</div>
        <div class="event-date-mon">${d.toLocaleString('pt-BR',{month:'short'})}</div>
      </div>` : `<div class="event-date-box"><div style="font-size:11px;color:var(--orange-d)">–</div></div>`}
      <div class="event-info">
        <div class="event-title">${ev.titulo}</div>
        <div class="event-meta">
          ${ev.local ? ev.local + ' · ' : ''}
          <span class="badge-pill ${ev.tipo === 'HACKATHON' ? 'badge-orange' : 'badge-blue'}" style="padding:2px 8px;font-size:11px">${ev.tipo}</span>
        </div>
      </div>
      <button class="btn ${isInscrito ? 'btn-secondary' : 'btn-primary'} btn-sm" onclick="toggleInscricao(${ev.id}, ${isInscrito})">
        ${isInscrito ? 'Inscrito ✓' : 'Inscrever-se'}
      </button>
    </div>`;
  }).join('');
}

async function toggleInscricao(eventoId, isInscrito) {
  try {
    if (isInscrito) {
      await api('DELETE', `/api/eventos/${eventoId}/inscrever`);
      state.inscricoes = state.inscricoes.filter(i => i.evento_id !== eventoId);
      toast('Inscrição cancelada', 'info');
    } else {
      const insc = await api('POST', `/api/eventos/${eventoId}/inscrever`);
      state.inscricoes.push(insc);
      toast('Inscrição realizada!', 'success');
    }
    renderEventos();
    updateDashboard();
  } catch(e) {
    toast(e.message, 'error');
  }
}

/*  OPORTUNIDADES */
async function loadOportunidades() {
  try {
    state.oportunidades = await api('GET', '/api/oportunidades/') || [];
  } catch(e) {
    state.oportunidades = getMockOportunidades();
  }
  renderOportunidades();
}

function renderOportunidades() {
  const container = document.getElementById('opp-list');
  if (!state.oportunidades.length) {
    container.innerHTML = `<div class="empty-state">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 7V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v2"/></svg>
      <p>Nenhuma oportunidade disponível no momento</p>
    </div>`;
    return;
  }
  container.innerHTML = state.oportunidades.map(op => `
    <div class="opp-card">
      <div class="opp-company-badge">${(op.empresa || '?').charAt(0).toUpperCase()}</div>
      <div class="opp-info">
        <div class="opp-title">${op.titulo}</div>
        ${op.empresa ? `<div class="opp-company">${op.empresa}</div>` : ''}
        ${op.descricao ? `<div class="opp-company" style="margin-top:2px">${op.descricao}</div>` : ''}
      </div>
      ${op.link ? `<a href="${op.link}" target="_blank" class="btn btn-primary btn-sm">Ver vaga</a>` : ''}
    </div>
  `).join('');
}

/* PERFIL */
function renderPerfil() {
  const u = state.user;
  if (!u) return;
  document.getElementById('perfil-avatar').textContent      = u.nome.charAt(0).toUpperCase();
  document.getElementById('perfil-nome-display').textContent = u.nome;
  document.getElementById('perfil-email-display').textContent = u.email;
  document.getElementById('perfil-nome').value  = u.nome;
  document.getElementById('perfil-email').value = u.email;

  const aprovadas = state.progresso.filter(p => p.status === 'APROVADO').length;
  const cursando  = state.progresso.filter(p => p.status === 'CURSANDO').length;
  const total     = state.disciplinas.filter(d => d.obrigatoria).length;

  document.getElementById('perfil-stats').innerHTML = `
    <div style="display:flex;justify-content:space-between;align-items:center">
      <span style="font-size:13px;color:var(--gray-400)">Disciplinas aprovadas</span>
      <span style="font-size:15px;font-weight:700;color:var(--green)">${aprovadas}</span>
    </div>
    <div style="display:flex;justify-content:space-between;align-items:center">
      <span style="font-size:13px;color:var(--gray-400)">Cursando atualmente</span>
      <span style="font-size:15px;font-weight:700;color:var(--blue-m)">${cursando}</span>
    </div>
    <div style="display:flex;justify-content:space-between;align-items:center">
      <span style="font-size:13px;color:var(--gray-400)">Total de disciplinas</span>
      <span style="font-size:15px;font-weight:700;color:var(--blue)">${total}</span>
    </div>
    <div style="display:flex;justify-content:space-between;align-items:center">
      <span style="font-size:13px;color:var(--gray-400)">Projetos publicados</span>
      <span style="font-size:15px;font-weight:700;color:var(--orange)">${state.projetos.filter(p=>p.user_id===u.id).length}</span>
    </div>
    <div style="display:flex;justify-content:space-between;align-items:center">
      <span style="font-size:13px;color:var(--gray-400)">Eventos inscritos</span>
      <span style="font-size:15px;font-weight:700;color:var(--yellow)">${state.inscricoes.length}</span>
    </div>
    <div style="margin-top:8px">
      <div style="display:flex;justify-content:space-between;margin-bottom:6px">
        <span style="font-size:13px;color:var(--gray-400)">Conclusão do curso</span>
        <span style="font-size:13px;font-weight:600;color:var(--orange)">${total ? Math.round(aprovadas/total*100) : 0}%</span>
      </div>
      <div class="progress-track"><div class="progress-fill" style="width:${total ? Math.round(aprovadas/total*100) : 0}%"></div></div>
    </div>
  `;
}

async function updatePerfil() {
  const nome  = document.getElementById('perfil-nome').value.trim();
  const email = document.getElementById('perfil-email').value.trim();
  try {
    const updated = await api('PUT', '/api/usuarios/me', { nome, email });
    state.user = { ...state.user, ...updated };
    localStorage.setItem('rb_user', JSON.stringify(state.user));
    updateSidebar();
    renderPerfil();
    toast('Perfil atualizado!', 'success');
  } catch(e) {
    toast(e.message, 'error');
  }
}

/*  DASHBOARD*/
function updateDashboard() {
  const aprovadas = state.progresso.filter(p => p.status === 'APROVADO').length;
  const cursando  = state.progresso.filter(p => p.status === 'CURSANDO').length;
  const totalObrig = state.disciplinas.filter(d => d.obrigatoria).length;
  const pct = totalObrig ? Math.round(aprovadas / totalObrig * 100) : 0;
  const meusProjetos = state.projetos.filter(p => p.user_id === state.user?.id).length;

  document.getElementById('stat-aprovadas').textContent = aprovadas;
  document.getElementById('stat-cursando').textContent  = cursando;
  document.getElementById('stat-projetos').textContent  = meusProjetos;
  document.getElementById('stat-eventos').textContent   = state.inscricoes.length;
  document.getElementById('dash-progress-bar').style.width = pct + '%';
  document.getElementById('dash-pct-label').textContent  = pct + '%';
  document.getElementById('dash-progress-text').textContent = `${aprovadas} de ${totalObrig} disciplinas obrigatórias concluídas`;
  document.getElementById('dash-sub').textContent = aprovadas > 0 ? `${aprovadas} disciplinas aprovadas · ${cursando} cursando` : 'Comece registrando suas disciplinas';

  const eventosContainer = document.getElementById('dash-eventos-list');
  const proximos = state.eventos.filter(e => e.data_evento).slice(0,3);
  if (!proximos.length) {
    eventosContainer.innerHTML = '<div class="empty-state"><p>Nenhum evento próximo</p></div>';
  } else {
    eventosContainer.innerHTML = proximos.map(ev => {
      const d = new Date(ev.data_evento + 'T00:00:00');
      return `<div style="display:flex;align-items:center;gap:10px;padding:8px 0;border-bottom:1px solid var(--gray-50)">
        <div style="width:36px;text-align:center;background:var(--orange-bg);border-radius:6px;padding:4px">
          <div style="font-family:var(--font-display);font-size:14px;font-weight:800;color:var(--orange)">${d.getDate()}</div>
          <div style="font-size:10px;text-transform:uppercase;color:var(--orange-d);letter-spacing:.05em">${d.toLocaleString('pt-BR',{month:'short'})}</div>
        </div>
        <div style="flex:1;min-width:0">
          <div style="font-size:13px;font-weight:500;color:var(--blue);white-space:nowrap;overflow:hidden;text-overflow:ellipsis">${ev.titulo}</div>
          <div style="font-size:11px;color:var(--gray-400)">${ev.tipo}</div>
        </div>
      </div>`;
    }).join('');
  }
}

/* MOCK DATA (quando API offline)*/
function getMockDisciplinas() {
  return [
    {id:1,codigo:'14709',nome:'Princípios de Programação',periodo:1,carga_horaria:60,obrigatoria:1},
    {id:2,codigo:'14708',nome:'Fundamentos Matemáticos I',periodo:1,carga_horaria:60,obrigatoria:1},
    {id:3,codigo:'14734',nome:'Sustentabilidade em SI',periodo:1,carga_horaria:60,obrigatoria:1},
    {id:4,codigo:'14736',nome:'Fundamentos de Problemas Computacionais I',periodo:2,carga_horaria:60,obrigatoria:1},
    {id:5,codigo:'14737',nome:'Fundamentos Matemáticos II',periodo:2,carga_horaria:60,obrigatoria:1},
    {id:6,codigo:'14340',nome:'Engenharia para SI I',periodo:3,carga_horaria:60,obrigatoria:1},
    {id:7,codigo:'14341',nome:'Introdução ao Armazenamento e Análise de Dados',periodo:3,carga_horaria:60,obrigatoria:1},
    {id:8,codigo:'14344',nome:'Princípios de Software Básico',periodo:4,carga_horaria:60,obrigatoria:1},
    {id:9,codigo:'06299',nome:'Segurança e Auditoria de Sistemas',periodo:5,carga_horaria:60,obrigatoria:1},
    {id:10,codigo:'14705',nome:'Fundamentos de Criptografia',periodo:null,carga_horaria:60,obrigatoria:0},
    {id:11,codigo:'14024',nome:'Tópicos Avançados em IA',periodo:null,carga_horaria:60,obrigatoria:0},
  ];
}
function getMockProjetos() {
  return [
    {id:1,user_id:1,titulo:'Sistema de Gestão Acadêmica',descricao:'Plataforma web para gestão de notas e frequência.',github_link:'https://github.com',created_at:'2025-01-01'},
    {id:2,user_id:2,titulo:'App de Alertas Ambientais',descricao:'Monitoramento de queimadas com IoT e ML.',github_link:null,created_at:'2025-01-02'},
    {id:3,user_id:1,titulo:'Chatbot para Suporte TI',descricao:'Bot com NLP para triagem de chamados.',github_link:'https://github.com',created_at:'2025-01-03'},
  ];
}
function getMockEventos() {
  return [
    {id:1,titulo:'Hackathon Agro-Tech 2025',descricao:'Desafio de inovação no agronegócio',data_evento:'2025-08-15',local:'Recife, PE',tipo:'HACKATHON'},
    {id:2,titulo:'Semana de TI',descricao:'Palestras e workshops de tecnologia',data_evento:'2025-07-20',local:'Campus UFRPE',tipo:'EVENTO'},
    {id:3,titulo:'Workshop de Machine Learning',descricao:'Introdução prática a ML com Python',data_evento:'2025-07-05',local:'Online',tipo:'EVENTO'},
  ];
}
function getMockOportunidades() {
  return [
    {id:1,titulo:'Estágio em Desenvolvimento Web',descricao:'Vaga para estudantes de SI a partir do 3º período',empresa:'Accenture',link:'#'},
    {id:2,titulo:'Bolsa de Iniciação Científica',descricao:'Projeto de pesquisa em IA aplicada à agricultura',empresa:'UFRPE',link:'#'},
    {id:3,titulo:'Trainee em Dados',descricao:'Programa de formação em engenharia de dados',empresa:'Embrapa',link:'#'},
  ];
}

/* TRILHA ACADÊMICA */

const trilhaState = {
  nos: [],
  arestas: [],
  periodoFiltro: null,
};

const STATUS_META = {
  APROVADO:  { cor: 'var(--green)',   borda: '#16a34a', icone: '✓', label: 'Concluída'    },
  CURSANDO:  { cor: 'var(--blue-m)',  borda: '#2563eb', icone: '▶', label: 'Em andamento' },
  REPROVADO: { cor: 'var(--red)',     borda: '#dc2626', icone: '✕', label: 'Reprovada'    },
  TRANCADO:  { cor: 'var(--yellow)',  borda: '#eab308', icone: '⏸', label: 'Trancada'     },
};

async function loadTrilha() {
  const loading = document.getElementById('trilha-loading');
  const wrap    = document.getElementById('trilha-canvas-wrap');
  loading.style.display = 'flex';
  wrap.style.visibility = 'hidden';
  try {
    const data = await api('GET', '/api/trilha/');
    trilhaState.nos    = data.nos;
    trilhaState.arestas = data.arestas;
  } catch(e) {
    // fallback offline
    const statusMap = {};
    (state.progresso || []).forEach(p => { statusMap[p.disciplina_id] = p.status; });
    const disc = state.disciplinas.length ? state.disciplinas : getMockDisciplinas();
    trilhaState.nos    = disc.map(d => ({
      disciplina: d, status: statusMap[d.id] || null, pre_requisitos: [], desbloqueada: true,
    }));
    trilhaState.arestas = [];
  } finally {
    loading.style.display = 'none';
    wrap.style.visibility = '';
    renderTrilha();
  }
}

function trilhaFilterPeriodo(periodo, btn) {
  trilhaState.periodoFiltro = periodo;
  document.querySelectorAll('#trilha-period-filter .periodo-pill').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  renderTrilha();
}

function renderTrilha() {
  const container = document.getElementById('trilha-graph');
  const svgEl     = document.getElementById('trilha-edges');
  const wrap      = document.getElementById('trilha-canvas-wrap');
  container.innerHTML = '';

  let nos = trilhaState.nos;
  const f = trilhaState.periodoFiltro;
  if (f !== null) {
    if (f === 'opt') nos = nos.filter(n => !n.disciplina.periodo);
    else             nos = nos.filter(n => n.disciplina.periodo === f);
  }

  if (!nos.length) {
    container.innerHTML = '<div style="padding:60px;text-align:center;color:var(--gray-400)">Nenhuma disciplina neste período.</div>';
    svgEl.setAttribute('width','0'); svgEl.setAttribute('height','0');
    return;
  }

  // Agrupar por período
  const grupos = {};
  nos.forEach(n => {
    const p = n.disciplina.periodo ?? 'opt';
    if (!grupos[p]) grupos[p] = [];
    grupos[p].push(n);
  });
  const periodos = Object.keys(grupos).sort((a,b) => {
    if (a==='opt') return 1; if (b==='opt') return -1; return Number(a)-Number(b);
  });

  // Layout
  const COL_W  = 190;
  const COL_GAP = 32;
  const NODE_W = 176;
  const NODE_H = 76;
  const GAP_Y  = 16;
  const PAD_X  = 16;
  const PAD_Y  = 44;

  const posMap = {};
  let totalH = 0;

  periodos.forEach((p, col) => {
    const colX = PAD_X + col * (COL_W + COL_GAP);
    grupos[p].forEach((n, row) => {
      const y = PAD_Y + row * (NODE_H + GAP_Y);
      posMap[n.disciplina.id] = { x: colX, y, cx: colX + NODE_W/2, cy: y + NODE_H/2 };
      totalH = Math.max(totalH, y + NODE_H + PAD_Y);
    });
  });

  const totalW = PAD_X + periodos.length * (COL_W + COL_GAP);

  wrap.style.width  = totalW + 'px';
  wrap.style.height = totalH + 'px';
  container.style.width  = totalW + 'px';
  container.style.height = totalH + 'px';
  svgEl.setAttribute('width',  totalW);
  svgEl.setAttribute('height', totalH);

  // Cabeçalhos de período
  periodos.forEach((p, col) => {
    const colX = PAD_X + col * (COL_W + COL_GAP);
    const lbl = document.createElement('div');
    lbl.style.cssText = `position:absolute;top:10px;left:${colX}px;width:${NODE_W}px;
      text-align:center;font-size:10px;font-weight:700;letter-spacing:.08em;
      text-transform:uppercase;color:var(--gray-400)`;
    lbl.textContent = p === 'opt' ? 'Optativas' : `${p}º Período`;
    container.appendChild(lbl);
  });

  // Nós
  const visibleIds = new Set(nos.map(n => n.disciplina.id));

  nos.forEach(n => {
    const pos    = posMap[n.disciplina.id];
    const meta   = STATUS_META[n.status];
    const locked = !n.desbloqueada && !n.status;
    const cor    = meta ? meta.borda : (locked ? 'var(--gray-100)' : 'var(--gray-200)');
    const bg     = meta ? meta.borda + '12' : 'var(--white)';

    const card = document.createElement('div');
    card.className = 'trilha-node';
    card.dataset.discId = n.disciplina.id;
    card.style.cssText = `
      position:absolute;left:${pos.x}px;top:${pos.y}px;
      width:${NODE_W}px;height:${NODE_H}px;
      border-radius:10px;border:2px solid ${cor};background:${bg};
      padding:8px 10px;cursor:${locked?'default':'pointer'};
      opacity:${locked?'.38':'1'};transition:transform .15s,box-shadow .15s;
      box-sizing:border-box;overflow:hidden;`;

    const iconHTML = meta
      ? `<span style="font-size:13px;color:${meta.cor};line-height:1">${meta.icone}</span>`
      : locked
        ? `<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="var(--gray-300)" stroke-width="2.5"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>`
        : `<svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="var(--gray-300)" stroke-width="2.5"><circle cx="12" cy="12" r="10"/></svg>`;

    card.innerHTML = `
      <div style="display:flex;align-items:center;gap:5px;margin-bottom:5px">
        ${iconHTML}
        <span style="font-size:10px;color:var(--gray-400);font-weight:600;letter-spacing:.03em">${n.disciplina.codigo}</span>
      </div>
      <div style="font-size:12px;font-weight:600;color:var(--blue);line-height:1.3;
                  display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden">
        ${n.disciplina.nome}
      </div>`;

    if (!locked) {
      card.addEventListener('mouseenter', () => {
        card.style.transform  = 'translateY(-2px)';
        card.style.boxShadow  = `0 8px 20px ${cor}44`;
        highlightTrilhaEdges(n.disciplina.id);
      });
      card.addEventListener('mouseleave', () => {
        card.style.transform = '';
        card.style.boxShadow = '';
        resetTrilhaEdges();
      });
      card.addEventListener('click', () => openTrilhaModal(n));
    }
    container.appendChild(card);
  });

  // Arestas SVG
  const defs = `<defs>
    <marker id="arrowhead" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
      <polygon points="0 0, 8 3, 0 6" fill="var(--gray-300)"/>
    </marker>
    <marker id="arrowhead-green" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
      <polygon points="0 0, 8 3, 0 6" fill="#16a34a"/>
    </marker>
  </defs>`;

  const linhas = trilhaState.arestas
    .filter(e => visibleIds.has(e.source) && visibleIds.has(e.target))
    .map(e => {
      const s = posMap[e.source]; const t = posMap[e.target];
      if (!s || !t) return '';
      const srcNodo = trilhaState.nos.find(n => n.disciplina.id === e.source);
      const aprov   = srcNodo?.status === 'APROVADO';
      const cor     = aprov ? '#16a34a' : '#c9c7be';
      const marker  = aprov ? 'url(#arrowhead-green)' : 'url(#arrowhead)';
      const x1 = s.x + NODE_W, y1 = s.cy, x2 = t.x, y2 = t.cy;
      const dx = Math.max((x2-x1)*0.5, 40);
      return `<path data-src="${e.source}" data-tgt="${e.target}"
        d="M${x1},${y1} C${x1+dx},${y1} ${x2-dx},${y2} ${x2},${y2}"
        fill="none" stroke="${cor}" stroke-width="1.5"
        marker-end="${marker}" opacity="0.55" class="trilha-edge"/>`;
    }).join('');

  svgEl.innerHTML = defs + linhas;
}

function highlightTrilhaEdges(discId) {
  document.querySelectorAll('#trilha-edges .trilha-edge').forEach(p => {
    const src = parseInt(p.dataset.src), tgt = parseInt(p.dataset.tgt);
    if (src === discId || tgt === discId) { p.setAttribute('stroke-width','2.5'); p.setAttribute('opacity','1'); }
    else p.setAttribute('opacity','0.1');
  });
}
function resetTrilhaEdges() {
  document.querySelectorAll('#trilha-edges .trilha-edge').forEach(p => {
    p.setAttribute('stroke-width','1.5'); p.setAttribute('opacity','0.55');
  });
}

function openTrilhaModal(nodo) {
  const d = nodo.disciplina;
  document.getElementById('modal-trilha-title').textContent = d.nome;

  const statusOpts = ['CURSANDO','APROVADO','REPROVADO','TRANCADO'];
  const opcoesHTML = statusOpts.map(s => {
    const m   = STATUS_META[s];
    const sel = nodo.status === s;
    return `<button onclick="setTrilhaStatus(${d.id},'${s}',this)" data-status="${s}"
      style="flex:1;min-width:110px;padding:12px 8px;border-radius:8px;cursor:pointer;font-family:inherit;
             border:2px solid ${sel ? m.borda : 'var(--gray-100)'};
             background:${sel ? m.borda+'18' : 'var(--white)'};
             font-size:12px;font-weight:600;color:var(--blue);transition:.15s">
        <div style="font-size:20px;margin-bottom:4px;color:${m.cor}">${m.icone}</div>
        ${m.label}
      </button>`;
  }).join('');

  const prereqsHTML = nodo.pre_requisitos.length
    ? `<div style="font-size:12px;color:var(--gray-400);margin-top:6px">
        Pré-requisitos: ${nodo.pre_requisitos.map(pid => {
          const nn = trilhaState.nos.find(x => x.disciplina.id === pid);
          const ok = nn?.status === 'APROVADO';
          return `<span style="color:${ok?'var(--green)':'var(--red)'}">${nn?nn.disciplina.nome:pid}</span>`;
        }).join(', ')}
       </div>` : '';

  document.getElementById('modal-trilha-body').innerHTML = `
    <div style="margin-bottom:16px">
      <div style="font-size:12px;color:var(--gray-400)">
        Código: <strong>${d.codigo}</strong> · ${d.carga_horaria}h
        ${d.periodo ? ` · <strong>${d.periodo}º período</strong>` : ' · <strong>Optativa</strong>'}
      </div>
      ${prereqsHTML}
    </div>
    <div style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:var(--gray-400);margin-bottom:10px">Atualizar status</div>
    <div style="display:flex;flex-wrap:wrap;gap:8px;margin-bottom:16px">${opcoesHTML}</div>
    ${nodo.status
      ? `<button onclick="removeTrilhaStatus(${d.id})"
           style="width:100%;padding:8px;border-radius:8px;border:1px solid var(--gray-100);
                  background:none;cursor:pointer;font-size:12px;color:var(--gray-400);font-family:inherit">
           Remover registro
         </button>`
      : ''}`;

  openModal('modal-trilha-disc');
}

async function setTrilhaStatus(disciplinaId, status, btn) {
  const meta = STATUS_META[status];
  btn.closest('[id="modal-trilha-body"]').querySelectorAll('[data-status]').forEach(b => {
    const m = STATUS_META[b.dataset.status];
    b.style.borderColor = 'var(--gray-100)';
    b.style.background  = 'var(--white)';
  });
  btn.style.borderColor = meta.borda;
  btn.style.background  = meta.borda + '22';

  try {
    await api('PUT', `/api/trilha/progresso/${disciplinaId}`, { status });
    const nodo = trilhaState.nos.find(n => n.disciplina.id === disciplinaId);
    if (nodo) nodo.status = status;
    _recalcDesbloqueios();
    renderTrilha();
    await loadProgresso().catch(() => {});
    updateDashboard();
    toast(`${meta.label}!`, 'success');
    closeModal('modal-trilha-disc');
  } catch(e) {
    toast(e.message, 'error');
  }
}

async function removeTrilhaStatus(disciplinaId) {
  try {
    await api('DELETE', `/api/trilha/progresso/${disciplinaId}`);
    const nodo = trilhaState.nos.find(n => n.disciplina.id === disciplinaId);
    if (nodo) nodo.status = null;
    _recalcDesbloqueios();
    renderTrilha();
    await loadProgresso().catch(() => {});
    updateDashboard();
    toast('Registro removido', 'info');
    closeModal('modal-trilha-disc');
  } catch(e) {
    toast(e.message, 'error');
  }
}

function _recalcDesbloqueios() {
  const statusMap = {};
  trilhaState.nos.forEach(n => { if (n.status) statusMap[n.disciplina.id] = n.status; });
  trilhaState.nos.forEach(n => {
    n.desbloqueada = n.pre_requisitos.every(pid => statusMap[pid] === 'APROVADO');
  });
}

/* KEYBOARD / FORM*/
document.addEventListener('keydown', e => {
  if (e.key === 'Enter') {
    if (document.getElementById('form-login').style.display !== 'none') doLogin();
    else if (document.getElementById('form-register').style.display !== 'none') doRegister();
  }
  if (e.key === 'Escape') {
    document.querySelectorAll('.modal-overlay.open').forEach(m => m.classList.remove('open'));
  }
});

/* BOOT */
if (state.token && state.user) {
  showApp();
} else {
  showAuth();
}
