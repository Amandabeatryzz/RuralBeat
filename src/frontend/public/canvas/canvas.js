/**
 * RuralBeat — Infinite Canvas Workspace (Materiais)
 * Pan & Zoom + Drag & Drop de nós + integração FastAPI
 */

const canvasState = {
  disciplinaId: null,
  workspace: null,
  nodes: [],
  refs: [],
  camera: { x: 0, y: 0, zoom: 1 },
  isPanning: false,
  panStart: { x: 0, y: 0 },
  cameraStart: { x: 0, y: 0 },
  draggingNode: null,
  dragOffset: { x: 0, y: 0 },
  selectedNodeId: null,
  activeTool: null,
  viewportSaveTimer: null,
  nodeSaveTimers: {},
};

const ZOOM_MIN = 0.15;
const ZOOM_MAX = 3;
const ZOOM_STEP = 0.08;

const NODE_DEFAULTS = {
  TEXTO: { titulo: 'Anotação', conteudo: '# Título\n\nEscreva em **Markdown**...', largura: 300, altura: 200 },
  CODIGO: { titulo: 'Snippet', conteudo: '// seu código aqui\nfunction hello() {\n  console.log("RuralBeat");\n}', largura: 340, altura: 220 },
  ARQUIVO: { titulo: 'Documento PDF', conteudo: '', largura: 260, altura: 160 },
};

const NODE_ICONS = {
  TEXTO: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>',
  CODIGO: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="16,18 22,12 16,6"/><polyline points="8,6 2,12 8,18"/></svg>',
  ARQUIVO: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/><polyline points="13,2 13,9 20,9"/></svg>',
};

function canvasEl(id) {
  return document.getElementById(id);
}

function screenToWorld(sx, sy) {
  const vp = canvasEl('canvas-viewport');
  const rect = vp.getBoundingClientRect();
  return {
    x: (sx - rect.left - canvasState.camera.x) / canvasState.camera.zoom,
    y: (sy - rect.top - canvasState.camera.y) / canvasState.camera.zoom,
  };
}

function applyCameraTransform() {
  const world = canvasEl('canvas-world');
  const { x, y, zoom } = canvasState.camera;
  world.style.transform = `translate(${x}px, ${y}px) scale(${zoom})`;

  const vp = canvasEl('canvas-viewport');
  const gridSize = 24 * zoom;
  vp.style.backgroundSize = `${gridSize}px ${gridSize}px`;
  vp.style.backgroundPosition = `${x % gridSize}px ${y % gridSize}px`;

  const badge = canvasEl('canvas-zoom-badge');
  if (badge) badge.textContent = `${Math.round(zoom * 100)}%`;
}

function scheduleViewportSave() {
  clearTimeout(canvasState.viewportSaveTimer);
  canvasState.viewportSaveTimer = setTimeout(saveViewport, 600);
}

async function saveViewport() {
  if (!canvasState.disciplinaId) return;
  try {
    await api('PATCH', `/api/materiais/canvas/disciplina/${canvasState.disciplinaId}/viewport`, {
      viewport_x: canvasState.camera.x,
      viewport_y: canvasState.camera.y,
      zoom: canvasState.camera.zoom,
    });
  } catch (_) { /* offline — ignora */ }
}

function scheduleNodeSave(nodeId, payload) {
  clearTimeout(canvasState.nodeSaveTimers[nodeId]);
  canvasState.nodeSaveTimers[nodeId] = setTimeout(async () => {
    try {
      await api('PUT', `/api/materiais/canvas/nos/${nodeId}`, payload);
    } catch (e) {
      toast(e.message || 'Erro ao salvar nó', 'error');
    }
  }, 400);
}

/* ── Renderização ─────────────────────────────────────────────────────────── */

function renderCanvasNode(node) {
  const tipo = (node.tipo || 'TEXTO').toLowerCase();
  const el = document.createElement('div');
  el.className = `canvas-node canvas-node-${tipo}`;
  el.dataset.nodeId = node.id;
  el.style.left = `${node.pos_x}px`;
  el.style.top = `${node.pos_y}px`;
  el.style.width = `${node.largura}px`;
  el.style.height = `${node.altura}px`;
  el.style.zIndex = node.z_index || 1;

  let bodyHTML = '';
  if (node.tipo === 'TEXTO') {
    bodyHTML = `<textarea data-field="conteudo" placeholder="Markdown...">${escapeHtml(node.conteudo || '')}</textarea>`;
  } else if (node.tipo === 'CODIGO') {
    bodyHTML = `<textarea data-field="conteudo" spellcheck="false" placeholder="// código">${escapeHtml(node.conteudo || '')}</textarea>`;
  } else if (node.tipo === 'ARQUIVO') {
    const link = node.conteudo || node.meta_json || '#';
    bodyHTML = `
      <div class="canvas-node-arquivo-icon">${NODE_ICONS.ARQUIVO}</div>
      <div>${escapeHtml(node.titulo || 'PDF')}</div>
      ${link && link !== '#' ? `<a class="canvas-node-arquivo-link" href="${escapeAttr(link)}" target="_blank" rel="noopener">Abrir documento</a>` : ''}`;
  }

  el.innerHTML = `
    <div class="canvas-node-header" data-drag-handle>
      <div class="canvas-node-type canvas-node-type-${tipo}">${NODE_ICONS[node.tipo] || ''}</div>
      <span class="canvas-node-title">${escapeHtml(node.titulo || 'Nó')}</span>
      <button type="button" class="canvas-node-delete" data-action="delete" title="Excluir">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14"><path d="M18 6L6 18M6 6l12 12"/></svg>
      </button>
    </div>
    <div class="canvas-node-body">${bodyHTML}</div>`;

  bindNodeEvents(el, node);
  return el;
  
}

function renderAllNodes() {
    console.log('renderAllNodes');
  const world = canvasEl('canvas-world');
  world.querySelectorAll('.canvas-node').forEach(n => n.remove());
  canvasState.nodes.forEach(node => {
    world.appendChild(renderCanvasNode(node));
  });
}

function renderRefSidebar() {
  const list = canvasEl('canvas-ref-list');
  const count = canvasEl('canvas-ref-count');
  if (!list) return;

  const pdfs = canvasState.refs.filter(m => {
    const t = (m.tipo || '').toUpperCase();
    const link = (m.link || '').toLowerCase();
    return t === 'PDF' || t === 'LIVRO' || link.endsWith('.pdf');
  });

  if (count) count.textContent = pdfs.length;

  if (!pdfs.length) {
    list.innerHTML = '<div class="canvas-ref-empty">Nenhum PDF cadastrado para esta disciplina.<br>Arraste materiais quando disponíveis.</div>';
    return;
  }

  list.innerHTML = pdfs.map(m => `
    <div class="canvas-ref-item" draggable="true" data-material-id="${m.id}"
         data-title="${escapeAttr(m.titulo)}" data-link="${escapeAttr(m.link)}">
      <div class="canvas-ref-item-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/><polyline points="13,2 13,9 20,9"/></svg>
      </div>
      <div class="canvas-ref-item-info">
        <div class="canvas-ref-item-title">${escapeHtml(m.titulo)}</div>
        <div class="canvas-ref-item-meta">PDF · arraste para o canvas</div>
      </div>
    </div>`).join('');

  list.querySelectorAll('.canvas-ref-item').forEach(item => {
    item.addEventListener('dragstart', e => {
      e.dataTransfer.setData('application/ruralbeat-material', JSON.stringify({
        material_id: parseInt(item.dataset.materialId),
        titulo: item.dataset.title,
        link: item.dataset.link,
      }));
      e.dataTransfer.effectAllowed = 'copy';
    });
  });
}

function updateCopilot() {
  const msg = canvasEl('canvas-copilot-msg');
  const chips = canvasEl('canvas-copilot-suggestions');
  if (!msg || !chips) return;

  const textNodes = canvasState.nodes.filter(n => n.tipo === 'TEXTO' || n.tipo === 'CODIGO');
  const context = textNodes.map(n => (n.conteudo || '').slice(0, 80)).join(' ').toLowerCase();

  if (!context.trim()) {
    msg.textContent = 'Olá! Selecione uma disciplina e comece a anotar. Vou sugerir PDFs relacionados ao que você escrever.';
    chips.innerHTML = canvasState.refs.slice(0, 3).map(m => copilotChip(m)).join('') ||
      '<div class="canvas-ref-empty" style="padding:8px">Sem sugestões ainda</div>';
    return;
  }

  const keywords = ['python', 'java', 'sql', 'redes', 'dados', 'algoritmo', 'web', 'segurança', 'cripto'];
  const found = keywords.filter(k => context.includes(k));

  const related = canvasState.refs.filter(m => {
    const hay = `${m.titulo} ${m.descricao || ''} ${m.link || ''}`.toLowerCase();
    return found.some(k => hay.includes(k)) || hay.split(' ').some(w => context.includes(w) && w.length > 4);
  }).slice(0, 4);

  msg.textContent = found.length
    ? `Detectei temas sobre ${found.join(', ')}. Estes materiais podem ajudar:`
    : 'Com base nas suas anotações, estes arquivos podem ser úteis:';

  chips.innerHTML = related.length
    ? related.map(m => copilotChip(m)).join('')
    : canvasState.refs.slice(0, 2).map(m => copilotChip(m)).join('') || '<div class="canvas-ref-empty" style="padding:8px">Adicione materiais à disciplina</div>';
}

function copilotChip(m) {
  return `<div class="canvas-copilot-chip" data-material-id="${m.id}" data-title="${escapeAttr(m.titulo)}" data-link="${escapeAttr(m.link)}">
    ${NODE_ICONS.ARQUIVO}
    <span>${escapeHtml(m.titulo)}</span>
  </div>`;
}

/* ── Eventos de nó ──────────────────────────────────────────────────────── */

function bindNodeEvents(el, node) {
  const header = el.querySelector('[data-drag-handle]');
  header.addEventListener('mousedown', e => startNodeDrag(e, el, node));
  header.addEventListener('touchstart', e => startNodeDrag(e, el, node), { passive: false });

  el.querySelector('[data-action="delete"]')?.addEventListener('click', e => {
    e.stopPropagation();
    deleteCanvasNode(node.id);
  });

  el.addEventListener('mousedown', e => {
    if (e.target.closest('[data-drag-handle]')) return;
    selectNode(node.id);
  });

  el.querySelectorAll('textarea[data-field="conteudo"]').forEach(ta => {
    ta.addEventListener('input', () => {
      node.conteudo = ta.value;
      scheduleNodeSave(node.id, { conteudo: ta.value });
      updateCopilot();
    });
    ta.addEventListener('mousedown', e => e.stopPropagation());
  });
}

function selectNode(id) {
  canvasState.selectedNodeId = id;
  document.querySelectorAll('.canvas-node').forEach(n => {
    n.classList.toggle('is-selected', parseInt(n.dataset.nodeId) === id);
  });
}

function startNodeDrag(e, el, node) {
  if (e.target.closest('[data-action="delete"]')) return;
  e.preventDefault();
  e.stopPropagation();

  const point = e.touches ? e.touches[0] : e;
  const world = screenToWorld(point.clientX, point.clientY);

  canvasState.draggingNode = { el, node };
  canvasState.dragOffset = {
    x: world.x - node.pos_x,
    y: world.y - node.pos_y,
  };
  el.classList.add('is-dragging');
  canvasEl('canvas-viewport').classList.add('is-dragging-node');
  selectNode(node.id);
}

/* ── Pan & Zoom ─────────────────────────────────────────────────────────── */

function initCanvasEngine() {
  const vp = canvasEl('canvas-viewport');
  if (!vp || vp.dataset.bound) return;
  vp.dataset.bound = '1';

  vp.addEventListener('mousedown', e => {
    if (e.target.closest('.canvas-node')) return;
    if (e.button !== 0) return;
    canvasState.isPanning = true;
    canvasState.panStart = { x: e.clientX, y: e.clientY };
    canvasState.cameraStart = { ...canvasState.camera };
    vp.classList.add('is-panning');
    canvasState.selectedNodeId = null;
    document.querySelectorAll('.canvas-node.is-selected').forEach(n => n.classList.remove('is-selected'));
  });

  window.addEventListener('mousemove', onPointerMove);
  window.addEventListener('mouseup', onPointerUp);
  window.addEventListener('touchmove', onPointerMove, { passive: false });
  window.addEventListener('touchend', onPointerUp);

  vp.addEventListener('wheel', e => {
    e.preventDefault();
    const rect = vp.getBoundingClientRect();
    const mx = e.clientX - rect.left;
    const my = e.clientY - rect.top;
    const delta = e.deltaY > 0 ? -ZOOM_STEP : ZOOM_STEP;
    const newZoom = clamp(canvasState.camera.zoom + delta, ZOOM_MIN, ZOOM_MAX);
    const ratio = newZoom / canvasState.camera.zoom;
    canvasState.camera.x = mx - (mx - canvasState.camera.x) * ratio;
    canvasState.camera.y = my - (my - canvasState.camera.y) * ratio;
    canvasState.camera.zoom = newZoom;
    applyCameraTransform();
    scheduleViewportSave();
  }, { passive: false });

  vp.addEventListener('dragover', e => {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'copy';
  });

  vp.addEventListener('drop', e => {
    e.preventDefault();
    const raw = e.dataTransfer.getData('application/ruralbeat-material');
    if (!raw) return;
    const mat = JSON.parse(raw);
    const world = screenToWorld(e.clientX, e.clientY);
    createCanvasNode('ARQUIVO', world.x - 130, world.y - 80, {
      titulo: mat.titulo,
      conteudo: mat.link,
      material_id: mat.material_id,
    });
  });
}

function onPointerMove(e) {
  const point = e.touches ? e.touches[0] : e;

  if (canvasState.draggingNode) {
    e.preventDefault();
    const { el, node } = canvasState.draggingNode;
    const world = screenToWorld(point.clientX, point.clientY);
    node.pos_x = world.x - canvasState.dragOffset.x;
    node.pos_y = world.y - canvasState.dragOffset.y;
    el.style.left = `${node.pos_x}px`;
    el.style.top = `${node.pos_y}px`;
    return;
  }

  if (!canvasState.isPanning) return;
  
  // 👉 ADICIONE ESTA LINHA AQUI:
  e.preventDefault(); 

  const dx = point.clientX - canvasState.panStart.x;
  const dy = point.clientY - canvasState.panStart.y;
  canvasState.camera.x = canvasState.cameraStart.x + dx;
  canvasState.camera.y = canvasState.cameraStart.y + dy;
  applyCameraTransform();
}

function onPointerUp() {
  const vp = canvasEl('canvas-viewport');

  if (canvasState.draggingNode) {
    const { el, node } = canvasState.draggingNode;
    el.classList.remove('is-dragging');
    vp?.classList.remove('is-dragging-node');
    scheduleNodeSave(node.id, { pos_x: node.pos_x, pos_y: node.pos_y });
    canvasState.draggingNode = null;
  }

  if (canvasState.isPanning) {
    canvasState.isPanning = false;
    vp?.classList.remove('is-panning');
    scheduleViewportSave();
  }
}

/* ── API ──────────────────────────────────────────────────────────────────── */

async function loadCanvasWorkspace() {
    console.log('loadCanvasWorkspace');
  const discId = canvasEl('canvas-disc-select')?.value;
  const empty = canvasEl('canvas-empty-state');
  const workspace = canvasEl('canvas-workspace-inner');

  if (!discId) {
    canvasState.disciplinaId = null;
    empty.style.display = '';
    workspace.style.display = 'none';
    return;
  }

  canvasState.disciplinaId = parseInt(discId);
  empty.style.display = 'none';
  workspace.style.display = '';

  const disc = state.disciplinas.find(d => d.id === canvasState.disciplinaId);
  const titleEl = canvasEl('canvas-disc-title');
  if (titleEl && disc) titleEl.textContent = disc.nome;

  try {
    const [canvasData, refs] = await Promise.all([
      api('GET', `/api/materiais/canvas/disciplina/${discId}`),
      api('GET', `/api/materiais/disciplina/${discId}`),
    ]);
    canvasState.workspace = canvasData;
    canvasState.nodes = canvasData.nos || [];
    canvasState.refs = refs || [];
    canvasState.camera = {
      x: canvasData.viewport_x || 0,
      y: canvasData.viewport_y || 0,
      zoom: canvasData.zoom || 1,
    };
  } catch (e) {
    canvasState.nodes = [];
    canvasState.refs = [];
    canvasState.camera = { x: 0, y: 0, zoom: 1 };
    toast('Canvas offline — modo local', 'info');
  }

  applyCameraTransform();
  renderAllNodes();
  renderRefSidebar();
  updateCopilot();
  initCanvasEngine();
  initCanvasUI();
}

async function createCanvasNode(tipo, x, y, extra = {}) {
  if (!canvasState.disciplinaId) {
    toast('Selecione uma disciplina primeiro', 'error');
    return;
  }

  const defaults = NODE_DEFAULTS[tipo] || NODE_DEFAULTS.TEXTO;
  const payload = {
    tipo,
    titulo: extra.titulo || defaults.titulo,
    conteudo: extra.conteudo ?? defaults.conteudo,
    pos_x: x ?? 100 + Math.random() * 200,
    pos_y: y ?? 100 + Math.random() * 200,
    largura: defaults.largura,
    altura: defaults.altura,
    material_id: extra.material_id || null,
    z_index: canvasState.nodes.length + 1,
  };

  try {
    const created = await api('POST', `/api/materiais/canvas/disciplina/${canvasState.disciplinaId}/nos`, payload);
    canvasState.nodes.push(created);
    canvasEl('canvas-world').appendChild(renderCanvasNode(created));
    selectNode(created.id);
    updateCopilot();
    toast('Nó criado', 'success');
  } catch (e) {
    toast(e.message || 'Erro ao criar nó', 'error');
  }
} 

async function deleteCanvasNode(nodeId) {
  if (!confirm('Excluir este nó do canvas?')) return;
  try {
    await api('DELETE', `/api/materiais/canvas/nos/${nodeId}`);
    canvasState.nodes = canvasState.nodes.filter(n => n.id !== nodeId);
    document.querySelector(`.canvas-node[data-node-id="${nodeId}"]`)?.remove();
    updateCopilot();
    toast('Nó removido', 'info');
  } catch (e) {
    toast(e.message || 'Erro ao excluir', 'error');
  }
}

/* ── UI helpers ───────────────────────────────────────────────────────────── */

function initCanvasUI() {
  if (document.getElementById('canvas-ui-bound')) return;

  canvasEl('canvas-disc-select')?.addEventListener('change', loadCanvasWorkspace);

  canvasEl('canvas-toggle-sidebar')?.addEventListener('click', () => {
    canvasEl('canvas-ref-sidebar')?.classList.toggle('collapsed');
    canvasEl('canvas-toggle-sidebar')?.classList.toggle('active');
  });

  canvasEl('canvas-copilot')?.addEventListener('click', e => {
    if (canvasEl('canvas-copilot').classList.contains('collapsed') && !e.target.closest('.canvas-copilot-toggle')) {
      canvasEl('canvas-copilot').classList.remove('collapsed');
    }
  });

  canvasEl('canvas-copilot-toggle')?.addEventListener('click', e => {
    e.stopPropagation();
    canvasEl('canvas-copilot')?.classList.toggle('collapsed');
  });

  canvasEl('canvas-copilot-suggestions')?.addEventListener('click', e => {
    const chip = e.target.closest('.canvas-copilot-chip');
    if (!chip) return;
    const cx = (-canvasState.camera.x + 400) / canvasState.camera.zoom;
    const cy = (-canvasState.camera.y + 300) / canvasState.camera.zoom;
    createCanvasNode('ARQUIVO', cx, cy, {
      titulo: chip.dataset.title,
      conteudo: chip.dataset.link,
      material_id: parseInt(chip.dataset.materialId),
    });
  });

  document.querySelectorAll('.canvas-dock-btn[data-tool]').forEach(btn => {
    btn.addEventListener('click', () => {
      e.preventDefault();
      const tool = btn.dataset.tool;
      if (tool === 'desenhar' || tool === 'conectar') {
        toast(`${tool === 'desenhar' ? 'Desenho' : 'Conexões'} — em breve`, 'info');
        return;
      }
      const cx = (-canvasState.camera.x + window.innerWidth / 2 - 140) / canvasState.camera.zoom;
      const cy = (-canvasState.camera.y + window.innerHeight / 2 - 100) / canvasState.camera.zoom;
      const tipo = tool === 'codigo' ? 'CODIGO' : 'TEXTO';
      createCanvasNode(tipo, cx, cy);
    });
  });

  const marker = document.createElement('div');
  marker.id = 'canvas-ui-bound';
  marker.hidden = true;
  document.body.appendChild(marker);
}

function populateCanvasDiscSelect() {
  const sel = canvasEl('canvas-disc-select');
  if (!sel) return;
  sel.innerHTML = '<option value="">Selecione uma disciplina...</option>' +
    state.disciplinas.map(d => `<option value="${d.id}">${d.nome}</option>`).join('');
}

function initMateriaisCanvas() {
   console.log('initMateriaisCanvas');
  populateCanvasDiscSelect();
  initCanvasEngine();
  initCanvasUI();
}

function clamp(v, min, max) {
  return Math.min(max, Math.max(min, v));
}

function escapeHtml(str) {
  return String(str || '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function escapeAttr(str) {
  return String(str || '').replace(/"/g, '&quot;').replace(/'/g, '&#39;');
}


document.addEventListener('DOMContentLoaded', initMateriaisCanvas);
