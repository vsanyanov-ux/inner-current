import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { StatsService } from './stats_service.js';

const PORT = Number(process.env.STATS_PORT || process.env.PORT) || 8033;
const DB_PATH = process.env.STATS_DB_PATH || path.resolve('data', 'stats.db');
const stats = new StatsService({ dbPath: DB_PATH });

function getClientIp(req) {
  const forwarded = req.headers['x-forwarded-for'];
  if (forwarded) {
    return forwarded.split(',')[0].trim();
  }
  return req.socket.remoteAddress || '127.0.0.1';
}

function parseJsonBody(req) {
  return new Promise((resolve, reject) => {
    let body = '';
    req.on('data', chunk => {
      body += chunk;
      if (body.length > 1024 * 1024) {
        reject(new Error('Payload too large'));
      }
    });
    req.on('end', () => {
      try {
        resolve(body ? JSON.parse(body) : {});
      } catch (err) {
        resolve({});
      }
    });
    req.on('error', reject);
  });
}

function sendCors(res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
}

export function handleStatsRequest(req, res, parsedUrl) {
  sendCors(res);

  if (req.method === 'OPTIONS') {
    res.writeHead(204);
    return res.end();
  }

  const pathname = parsedUrl.pathname;
  const ip = getClientIp(req);
  const userAgent = req.headers['user-agent'] || '';

  // 1. Трекинг прямого скачивания файла: GET /dl/:filename
  if (pathname.startsWith('/dl/') && req.method === 'GET') {
    const fileName = pathname.slice(4);
    stats.recordDownload({
      fileName,
      ip,
      userAgent,
      sourcePage: 'direct_dl_link',
      referrer: req.headers['referer'] || 'direct'
    });
    res.writeHead(302, { Location: `/books/${encodeURIComponent(fileName)}` });
    return res.end();
  }

  // 2. Трекинг визита страницы: POST /api/stats/visit
  if (pathname === '/api/stats/visit' && req.method === 'POST') {
    parseJsonBody(req).then(body => {
      const result = stats.recordVisit({
        path: body.path || '/',
        title: body.title || '',
        referrer: body.referrer || req.headers['referer'] || 'direct',
        screen: body.screen || '',
        device: body.device || '',
        ip,
        userAgent
      });
      res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
      res.end(JSON.stringify(result));
    }).catch(err => {
      res.writeHead(400, { 'Content-Type': 'application/json; charset=utf-8' });
      res.end(JSON.stringify({ ok: false, error: err.message }));
    });
    return true;
  }

  // 3. Трекинг клика на скачивание PDF книги: POST /api/stats/download
  if (pathname === '/api/stats/download' && req.method === 'POST') {
    parseJsonBody(req).then(body => {
      const result = stats.recordDownload({
        fileName: body.fileName || body.file_name || 'book.pdf',
        bookTitle: body.bookTitle || body.book_title || '',
        sourcePage: body.sourcePage || body.source_page || '/',
        referrer: body.referrer || req.headers['referer'] || 'direct',
        device: body.device || '',
        ip,
        userAgent
      });
      res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
      res.end(JSON.stringify(result));
    }).catch(err => {
      res.writeHead(400, { 'Content-Type': 'application/json; charset=utf-8' });
      res.end(JSON.stringify({ ok: false, error: err.message }));
    });
    return true;
  }

  // 4. Авторизация: POST /api/stats/login
  if (pathname === '/api/stats/login' && req.method === 'POST') {
    parseJsonBody(req).then(body => {
      const auth = stats.login(body.password);
      if (!auth.success) {
        res.writeHead(401, { 'Content-Type': 'application/json; charset=utf-8' });
        return res.end(JSON.stringify(auth));
      }
      res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
      res.end(JSON.stringify(auth));
    });
    return true;
  }

  // 5. Выход: POST /api/stats/logout
  if (pathname === '/api/stats/logout' && req.method === 'POST') {
    const token = req.headers['authorization'];
    stats.logout(token);
    res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
    return res.end(JSON.stringify({ success: true }));
  }

  // -------------------------------------------------------------
  // Защищенные эндпоинты статистики (требуют валидный токен)
  // -------------------------------------------------------------
  if (pathname.startsWith('/api/stats/')) {
    const authHeader = req.headers['authorization'];
    if (!stats.verifyToken(authHeader)) {
      res.writeHead(401, { 'Content-Type': 'application/json; charset=utf-8' });
      return res.end(JSON.stringify({ error: 'Unauthorized: Требуется авторизация в админке' }));
    }

    // GET /api/stats/summary
    if (pathname === '/api/stats/summary' && req.method === 'GET') {
      const period = parsedUrl.searchParams.get('period') || 'all';
      const summary = stats.getSummary(period);
      res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
      return res.end(JSON.stringify(summary));
    }

    // GET /api/stats/recent
    if (pathname === '/api/stats/recent' && req.method === 'GET') {
      const limit = Number(parsedUrl.searchParams.get('limit')) || 50;
      const recent = stats.getRecentEvents(limit);
      res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
      return res.end(JSON.stringify(recent));
    }

    // POST /api/stats/reset
    if (pathname === '/api/stats/reset' && req.method === 'POST') {
      parseJsonBody(req).then(body => {
        const result = stats.resetStats(body.confirm);
        res.writeHead(result.success ? 200 : 400, { 'Content-Type': 'application/json; charset=utf-8' });
        res.end(JSON.stringify(result));
      });
      return true;
    }

    // GET /api/stats/export
    if (pathname === '/api/stats/export' && req.method === 'GET') {
      const format = parsedUrl.searchParams.get('format') || 'json';
      const exp = stats.exportData(format);
      res.writeHead(200, {
        'Content-Type': exp.mime + '; charset=utf-8',
        'Content-Disposition': `attachment; filename="innercurrent_stats_${new Date().toISOString().slice(0, 10)}.${exp.format}"`
      });
      return res.end(exp.data);
    }
  }

  return false;
}

// Запуск в качестве автономного микросервиса (если запущен напрямую)
if (process.argv[1] && path.resolve(process.argv[1]) === path.resolve(new URL(import.meta.url).pathname.replace(/^\/([A-Z]:)/, '$1'))) {
  const standaloneServer = http.createServer((req, res) => {
    const parsedUrl = new URL(req.url, `http://${req.headers.host || 'localhost'}`);
    const handled = handleStatsRequest(req, res, parsedUrl);
    if (!handled) {
      res.writeHead(404, { 'Content-Type': 'application/json; charset=utf-8' });
      res.end(JSON.stringify({ error: 'Endpoint not found' }));
    }
  });

  standaloneServer.listen(PORT, '0.0.0.0', () => {
    console.log(`⚡ Inner Current Stats Engine running on http://127.0.0.1:${PORT}`);
    console.log(`   Database: ${DB_PATH}`);
  });
}
