import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';

const PORT = Number(process.env.PORT) || 3333;
const PUBLIC_DIR = path.resolve('public');
const DATA_FILE = path.resolve('data', 'cockpit_ideas.json');
const LOCAL_WIKI_DIR = path.resolve('wiki');
const OBSIDIAN_VAULT_WIKI = 'C:\\Users\\vanya\\Antigravity Projects\\Misc\\LLM Wiki\\02_Wiki';
const OBSIDIAN_MOC_FILE = 'C:\\Users\\vanya\\Antigravity Projects\\Misc\\LLM Wiki\\04_Maps\\Inner Current MOC.md';

const MIME_TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.png': 'image/png',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon',
  '.pdf': 'application/pdf',
  '.mp3': 'audio/mpeg',
  '.m4a': 'audio/mp4',
  '.m4b': 'audio/mp4',
};

// =============================================================
// Хелперы для работы с хранилищем идей (Cockpit Kanban)
// =============================================================
function loadIdeas() {
  try {
    if (!fs.existsSync(DATA_FILE)) {
      return [];
    }
    const raw = fs.readFileSync(DATA_FILE, 'utf-8');
    return JSON.parse(raw);
  } catch (err) {
    console.error('Ошибка загрузки идей:', err.message);
    return [];
  }
}

function saveIdeas(ideas) {
  const dir = path.dirname(DATA_FILE);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  fs.writeFileSync(DATA_FILE, JSON.stringify(ideas, null, 2), 'utf-8');
}

function parseJsonBody(req) {
  return new Promise((resolve, reject) => {
    let body = '';
    req.on('data', chunk => {
      body += chunk;
      if (body.length > 2 * 1024 * 1024) {
        reject(new Error('Payload too large'));
      }
    });
    req.on('end', () => {
      try {
        resolve(body ? JSON.parse(body) : {});
      } catch (err) {
        reject(err);
      }
    });
    req.on('error', reject);
  });
}

// =============================================================
// Хелперы для Онлайн-Ридера Вики (динамическое сканирование Vault и repo)
// =============================================================
function getWikiCatalog() {
  const mocFile = fs.existsSync(OBSIDIAN_MOC_FILE) 
    ? OBSIDIAN_MOC_FILE 
    : path.join(LOCAL_WIKI_DIR, 'Inner Current MOC.md');
  
  const layers = [];
  const layerMap = {};
  const indexedFiles = new Set();

  if (fs.existsSync(mocFile)) {
    const mocContent = fs.readFileSync(mocFile, 'utf-8');
    const lines = mocContent.split('\n');
    let currentLayer = null;

    for (const line of lines) {
      const layerMatch = line.match(/^####\s+(.+)$/);
      if (layerMatch) {
        currentLayer = layerMatch[1].trim();
        const layerId = 'layer-' + (layers.length + 1);
        if (!layerMap[currentLayer]) {
          const lObj = {
            id: layerId,
            title: currentLayer,
            articles: []
          };
          layerMap[currentLayer] = lObj;
          layers.push(lObj);
        }
        continue;
      }

      const articleMatch = line.match(/^\s*(\d+)\.\s+\*\*\[\[([^\]|]+)(?:\|([^\]]+))?\]\]\*\*(?:\s*[—–-]\s*(.*))?$/);
      if (articleMatch && currentLayer) {
        const rawTarget = articleMatch[2].trim();
        const displayName = articleMatch[3] ? articleMatch[3].trim() : rawTarget;
        const summary = articleMatch[4] ? articleMatch[4].trim() : '';
        const cleanBase = rawTarget.replace(/^02_Wiki\//, '').replace(/\.md$/, '');
        const filename = cleanBase + '.md';

        // Проверяем наличие файла на диске
        let fullPath = path.join(OBSIDIAN_VAULT_WIKI, filename);
        if (!fs.existsSync(fullPath)) {
          fullPath = path.join(LOCAL_WIKI_DIR, filename);
        }
        const exists = fs.existsSync(fullPath);
        let mtime = null;
        let size = 0;
        if (exists) {
          const st = fs.statSync(fullPath);
          mtime = st.mtime.toISOString();
          size = st.size;
        }

        indexedFiles.add(cleanBase.toLowerCase());

        layerMap[currentLayer].articles.push({
          mocIndex: Number(articleMatch[1]),
          filename,
          slug: cleanBase,
          title: displayName,
          summary,
          layer: currentLayer,
          layerId: layerMap[currentLayer].id,
          mtime,
          size,
          exists
        });
      }
    }
  }

  // Автообнаружение новых/неиндексированных статей прямо на диске
  const unindexedArticles = [];
  const scanDirs = [OBSIDIAN_VAULT_WIKI, LOCAL_WIKI_DIR];
  const seenFilenames = new Set();

  for (const dir of scanDirs) {
    if (!fs.existsSync(dir)) continue;
    try {
      const files = fs.readdirSync(dir).filter(f => f.endsWith('.md') && !f.includes('MOC') && !f.includes('index.md'));
      for (const f of files) {
        if (seenFilenames.has(f.toLowerCase())) continue;
        seenFilenames.add(f.toLowerCase());

        const base = f.replace(/\.md$/, '');
        if (!indexedFiles.has(base.toLowerCase())) {
          const fullPath = path.join(dir, f);
          const st = fs.statSync(fullPath);
          let title = base;
          let summary = '';
          try {
            const head = fs.readFileSync(fullPath, 'utf-8').slice(0, 1000);
            const titleMatch = head.match(/^#\s+(.+)$/m);
            if (titleMatch) title = titleMatch[1].trim();
            const quoteMatch = head.match(/>\s*\[!quote\]\s*(.+)/);
            if (quoteMatch) summary = quoteMatch[1].trim();
          } catch (_) {}

          unindexedArticles.push({
            mocIndex: unindexedArticles.length + 1,
            filename: f,
            slug: base,
            title,
            summary: summary || 'Новый материал / протокол контура',
            layer: 'V. Новые входящие статьи и черновики',
            layerId: 'layer-new',
            mtime: st.mtime.toISOString(),
            size: st.size,
            exists: true,
            isNew: true
          });
        }
      }
    } catch (e) {
      console.error('Scan error:', e.message);
    }
  }

  if (unindexedArticles.length > 0) {
    layers.push({
      id: 'layer-new',
      title: 'V. Новые входящие статьи и черновики',
      articles: unindexedArticles
    });
  }

  const total = layers.reduce((acc, l) => acc + l.articles.length, 0);
  return {
    layers,
    total,
    vaultPath: OBSIDIAN_VAULT_WIKI,
    lastScanned: new Date().toISOString()
  };
}

function readWikiArticle(requestedFile) {
  if (!requestedFile) return null;
  let filename = decodeURIComponent(requestedFile).trim();
  if (filename.startsWith('02_Wiki/')) {
    filename = filename.replace(/^02_Wiki\//, '');
  }
  if (!filename.endsWith('.md')) {
    filename += '.md';
  }

  const safeFilename = path.basename(filename);

  let fullPath = path.join(OBSIDIAN_VAULT_WIKI, safeFilename);
  if (!fs.existsSync(fullPath)) {
    fullPath = path.join(LOCAL_WIKI_DIR, safeFilename);
  }
  if (!fs.existsSync(fullPath)) {
    return null;
  }

  const raw = fs.readFileSync(fullPath, 'utf-8');
  const stat = fs.statSync(fullPath);

  let frontmatter = {};
  let content = raw;
  const fmMatch = raw.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n([\s\S]*)$/);
  if (fmMatch) {
    content = fmMatch[2];
    const lines = fmMatch[1].split('\n');
    for (const l of lines) {
      const kv = l.match(/^([a-zA-Z0-9_-]+):\s*(.*)$/);
      if (kv) {
        let val = kv[2].trim();
        if (val.startsWith('[') && val.endsWith(']')) {
          val = val.slice(1, -1).split(',').map(s => s.trim().replace(/^['"]|['"]$/g, ''));
        }
        frontmatter[kv[1]] = val;
      }
    }
  }

  let title = safeFilename.replace(/\.md$/, '');
  const titleMatch = content.match(/^#\s+(.+)$/m);
  if (titleMatch) {
    title = titleMatch[1].trim();
  }

  return {
    filename: safeFilename,
    slug: safeFilename.replace(/\.md$/, ''),
    title,
    frontmatter,
    content,
    raw,
    mtime: stat.mtime.toISOString(),
    size: stat.size,
    fullPath
  };
}

// =============================================================
// HTTP СЕРВЕР И РОУТЕР
// =============================================================
const server = http.createServer(async (req, res) => {
  // CORS заголовки
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.writeHead(204);
    return res.end();
  }

  const parsedUrl = new URL(req.url || '/', `http://${req.headers.host || 'localhost'}`);
  const pathname = parsedUrl.pathname;

  // -------------------------------------------------------------
  // REST API: Inner Current Cockpit
  // -------------------------------------------------------------
  if (pathname.startsWith('/api/cockpit/')) {
    res.setHeader('Content-Type', 'application/json; charset=utf-8');

    // GET /api/cockpit/ideas
    if (pathname === '/api/cockpit/ideas' && req.method === 'GET') {
      const ideas = loadIdeas();
      res.writeHead(200);
      return res.end(JSON.stringify(ideas));
    }

    // POST /api/cockpit/ideas
    if (pathname === '/api/cockpit/ideas' && req.method === 'POST') {
      try {
        const payload = await parseJsonBody(req);
        const ideas = loadIdeas();
        const newIdea = {
          id: 'quantum-' + Date.now().toString(36),
          title: payload.title || 'Новый квант тока',
          category: payload.category || 'Общее',
          stage: Number(payload.stage) || 0,
          r_ego: Number(payload.r_ego) || 5,
          somatic_symptom: payload.somatic_symptom || '',
          circuit_law: payload.circuit_law || '',
          manual_title: payload.manual_title || '',
          wiki_file: payload.wiki_file || '',
          switch_formula: payload.switch_formula || '',
          field_test_notes: payload.field_test_notes || '',
          media_format: payload.media_format || 'YouTube Shorts',
          media_hook: payload.media_hook || '',
          energy_return: payload.energy_return || '',
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString(),
          days_in_stage: 0
        };
        ideas.unshift(newIdea);
        saveIdeas(ideas);
        res.writeHead(201);
        return res.end(JSON.stringify(newIdea));
      } catch (err) {
        res.writeHead(400);
        return res.end(JSON.stringify({ error: err.message }));
      }
    }

    // PUT /api/cockpit/ideas/:id
    const putMatch = pathname.match(/^\/api\/cockpit\/ideas\/([^/]+)$/);
    if (putMatch && req.method === 'PUT') {
      const ideaId = putMatch[1];
      try {
        const payload = await parseJsonBody(req);
        const ideas = loadIdeas();
        const index = ideas.findIndex(i => i.id === ideaId);
        if (index === -1) {
          res.writeHead(404);
          return res.end(JSON.stringify({ error: 'Идея не найдена' }));
        }

        const oldStage = ideas[index].stage;
        const newStage = payload.stage !== undefined ? Number(payload.stage) : oldStage;
        const daysInStage = newStage !== oldStage ? 0 : (payload.days_in_stage !== undefined ? payload.days_in_stage : ideas[index].days_in_stage);

        ideas[index] = {
          ...ideas[index],
          ...payload,
          stage: newStage,
          days_in_stage: daysInStage,
          updated_at: new Date().toISOString()
        };
        saveIdeas(ideas);
        res.writeHead(200);
        return res.end(JSON.stringify(ideas[index]));
      } catch (err) {
        res.writeHead(400);
        return res.end(JSON.stringify({ error: err.message }));
      }
    }

    // DELETE /api/cockpit/ideas/:id
    const delMatch = pathname.match(/^\/api\/cockpit\/ideas\/([^/]+)$/);
    if (delMatch && req.method === 'DELETE') {
      const ideaId = delMatch[1];
      let ideas = loadIdeas();
      const initialLen = ideas.length;
      ideas = ideas.filter(i => i.id !== ideaId);
      if (ideas.length === initialLen) {
        res.writeHead(404);
        return res.end(JSON.stringify({ error: 'Идея не найдена' }));
      }
      saveIdeas(ideas);
      res.writeHead(200);
      return res.end(JSON.stringify({ success: true, id: ideaId }));
    }

    // POST /api/cockpit/generate-wiki
    // Создает файл мануала в папке wiki/ и Obsidian Vault 02_Wiki
    if (pathname === '/api/cockpit/generate-wiki' && req.method === 'POST') {
      try {
        const payload = await parseJsonBody(req);
        const title = payload.title || 'Новый протокол цепи';
        const sanitized = title.replace(/[\\/:*?"<>|]/g, '').trim();
        const fileName = `Inner Current (${sanitized}).md`;

        const markdownContent = `---
created: ${new Date().toISOString().slice(0, 10)}
source: [[index|Wiki Index]]
tags: [inner-current, protocol, zen-engineering, deai, tanden]
type: protocol
status: evergreen
---

# ${title}

> [!quote] Главная формула протокола
> **${payload.switch_formula || 'R_{\\text{ego}} \\to 0 \\implies I > 0'}**

## 1. Соматический симптом и затык в цепи
- **Исходное сопротивление $R_{\\text{ego}}$:** ${payload.r_ego || 5} $\\Omega$
- **Физиологический датчик:** ${payload.somatic_symptom || 'Омический зажим мышц, потеря Мусин.'}
- **Схема сбоя:** ${payload.circuit_law || 'Паразитное сопротивление в цепи внимания.'}

---

## 2. Схемотехника рубильника (30 секунд на сброс)
1. **Тандэн:** Внимание мгновенно переносится в соматический центр тяжести (3 пальца ниже пупка).
2. **Снятие паразитной емкости ($C_{\\text{future}} = 0$):** Ликвидация симуляций будущего. Будущего не существует.
3. **Закон Вольтметра / Мультиметра:** Действие из режима беспристрастного измерительного прибора.

---

## 3. Результаты полевого стенда (Дэай)
${payload.field_test_notes || '- Проведено полевое тестирование.\n- Проводимость среды восстановлена.'}

---

## 4. Индукция в мир (YouTube / Медиа)
- **Формат:** ${payload.media_format || 'YouTube Shorts'}
- **Вирусный хук:** ${payload.media_hook || title}
- **Возврат чистой энергии:** ${payload.energy_return || 'Сверхпроводимость контура восстановлена.'}
`;

        // 1. Сохраняем в локальную wiki/
        const localPath = path.join(LOCAL_WIKI_DIR, fileName);
        fs.writeFileSync(localPath, markdownContent, 'utf-8');

        // 2. Синхронизируем в основной Obsidian Vault 02_Wiki (если доступен)
        let obsidianPath = null;
        if (fs.existsSync(OBSIDIAN_VAULT_WIKI)) {
          obsidianPath = path.join(OBSIDIAN_VAULT_WIKI, fileName);
          fs.writeFileSync(obsidianPath, markdownContent, 'utf-8');
        }

        res.writeHead(200);
        return res.end(JSON.stringify({
          success: true,
          fileName,
          localPath,
          obsidianPath
        }));
      } catch (err) {
        res.writeHead(500);
        return res.end(JSON.stringify({ error: err.message }));
      }
    }

    res.writeHead(404);
    return res.end(JSON.stringify({ error: 'Cockpit API route not found' }));
  }

  // -------------------------------------------------------------
  // REST API: Inner Current Wiki Reader (Динамический поиск и загрузка статей)
  // -------------------------------------------------------------
  if (pathname.startsWith('/api/wiki/')) {
    res.setHeader('Content-Type', 'application/json; charset=utf-8');

    // GET /api/wiki/articles
    if (pathname === '/api/wiki/articles' && req.method === 'GET') {
      try {
        const catalog = getWikiCatalog();
        res.writeHead(200);
        return res.end(JSON.stringify(catalog));
      } catch (err) {
        res.writeHead(500);
        return res.end(JSON.stringify({ error: err.message }));
      }
    }

    // GET /api/wiki/article?file=...
    if (pathname === '/api/wiki/article' && req.method === 'GET') {
      try {
        const fileParam = parsedUrl.searchParams.get('file');
        if (!fileParam) {
          res.writeHead(400);
          return res.end(JSON.stringify({ error: 'Параметр file обязателен' }));
        }
        const article = readWikiArticle(fileParam);
        if (!article) {
          res.writeHead(404);
          return res.end(JSON.stringify({ error: 'Статья не найдена' }));
        }
        res.writeHead(200);
        return res.end(JSON.stringify(article));
      } catch (err) {
        res.writeHead(500);
        return res.end(JSON.stringify({ error: err.message }));
      }
    }

    res.writeHead(404);
    return res.end(JSON.stringify({ error: 'Wiki API route not found' }));
  }

  // -------------------------------------------------------------
  // Статические файлы и роутинг страниц
  // -------------------------------------------------------------
  try {
    let reqPath = decodeURI(pathname);

    // Алиасы для страниц
    if (reqPath === '/cockpit' || reqPath === '/cockpit/' || reqPath === '/dashboard') {
      reqPath = '/cockpit.html';
    } else if (reqPath === '/wiki' || reqPath === '/wiki/' || reqPath === '/reader') {
      reqPath = '/wiki.html';
    } else if (reqPath === '/' || reqPath === '') {
      reqPath = '/index.html';
    } else if (reqPath.endsWith('/')) {
      reqPath += 'index.html';
    }

    // Безопасное кроссплатформенное разрешение пути
    const safeSuffix = path.normalize(reqPath).replace(/^(\.\.[\/\\])+/, '');
    let filePath = path.resolve(PUBLIC_DIR, '.' + safeSuffix);

    // Защита от Directory Traversal атаки (канон Дзансин)
    if (!filePath.startsWith(PUBLIC_DIR)) {
      res.writeHead(403, { 'Content-Type': 'text/plain; charset=utf-8' });
      return res.end('403 Forbidden');
    }

    if (fs.existsSync(filePath) && fs.statSync(filePath).isDirectory()) {
      filePath = path.join(filePath, 'index.html');
    }

    if (!fs.existsSync(filePath)) {
      res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
      return res.end('404 Not Found');
    }

    const stat = fs.statSync(filePath);
    const ext = path.extname(filePath).toLowerCase();
    const contentType = MIME_TYPES[ext] || 'application/octet-stream';

    // HTTP Range для аудио
    const range = req.headers.range;
    if (range) {
      const parts = range.replace(/bytes=/, '').split('-');
      const start = parseInt(parts[0], 10);
      const end = parts[1] ? parseInt(parts[1], 10) : stat.size - 1;
      const chunksize = end - start + 1;

      res.writeHead(206, {
        'Content-Range': `bytes ${start}-${end}/${stat.size}`,
        'Accept-Ranges': 'bytes',
        'Content-Length': chunksize,
        'Content-Type': contentType,
      });

      const stream = fs.createReadStream(filePath, { start, end });
      stream.on('error', err => console.error('Stream error:', err.message));
      stream.pipe(res);
      return;
    }

    res.writeHead(200, {
      'Content-Length': stat.size,
      'Accept-Ranges': 'bytes',
      'Content-Type': contentType,
    });
    const stream = fs.createReadStream(filePath);
    stream.on('error', err => console.error('Stream error:', err.message));
    stream.pipe(res);
  } catch (err) {
    console.error('Request handling error:', err);
    if (!res.headersSent) {
      res.writeHead(500, { 'Content-Type': 'text/plain; charset=utf-8' });
      res.end('500 Internal Server Error');
    }
  }
});

server.listen(PORT, () => {
  console.log(`⚡ Inner Current server running:`);
  console.log(`   - 🎛️  Пульт Сверхпроводимости: http://localhost:${PORT}/cockpit`);
  console.log(`   - 📚 Онлайн-Ридер Вики:       http://localhost:${PORT}/wiki`);
  console.log(`   - ⚡ Интерактивный тренажер:  http://localhost:${PORT}`);
  console.log(`   - 📖 Веб-ридер книги:         http://localhost:${PORT}/book/`);
  console.log(`   - 🎧 Веб-аудиоплеер книги:     http://localhost:${PORT}/audiobook/`);
});

process.on('SIGINT', () => {
  server.close(() => process.exit(0));
});
process.on('SIGTERM', () => {
  server.close(() => process.exit(0));
});
