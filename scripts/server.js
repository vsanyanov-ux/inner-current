import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';

const PORT = Number(process.env.PORT) || 3333;
const PUBLIC_DIR = path.resolve('public');

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
  '.mp3': 'audio/mpeg',
  '.m4a': 'audio/mp4',
  '.m4b': 'audio/mp4',
};

const server = http.createServer((req, res) => {
  try {
    let reqPath = decodeURI((req.url || '/').split('?')[0]);
    if (reqPath === '/' || reqPath === '') {
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

    // Если запрошена директория, проверяем trailing slash и отдаем index.html
    if (fs.existsSync(filePath) && fs.statSync(filePath).isDirectory()) {
      const pathname = (req.url || '/').split('?')[0];
      if (!pathname.endsWith('/')) {
        const qIndex = (req.url || '').indexOf('?');
        const query = qIndex !== -1 ? req.url.slice(qIndex) : '';
        res.writeHead(301, { Location: pathname + '/' + query });
        return res.end();
      }
      filePath = path.join(filePath, 'index.html');
    }

    if (!fs.existsSync(filePath)) {
      res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
      return res.end('404 Not Found');
    }

    const stat = fs.statSync(filePath);
    const ext = path.extname(filePath).toLowerCase();
    const contentType = MIME_TYPES[ext] || 'application/octet-stream';

    // Поддержка HTTP Range запросов для перемотки аудио (EBU / Safari / Chrome)
    const range = req.headers.range;
    if (range) {
      const parts = range.replace(/bytes=/, "").split("-");
      const start = parseInt(parts[0], 10);
      const end = parts[1] ? parseInt(parts[1], 10) : stat.size - 1;
      const chunksize = (end - start) + 1;

      res.writeHead(206, {
        'Content-Range': `bytes ${start}-${end}/${stat.size}`,
        'Accept-Ranges': 'bytes',
        'Content-Length': chunksize,
        'Content-Type': contentType,
      });

      const stream = fs.createReadStream(filePath, { start, end });
      stream.on('error', (err) => {
        console.error('File stream error:', err.message);
      });
      stream.pipe(res);
      return;
    }

    res.writeHead(200, {
      'Content-Length': stat.size,
      'Accept-Ranges': 'bytes',
      'Content-Type': contentType
    });
    const stream = fs.createReadStream(filePath);
    stream.on('error', (err) => {
      console.error('File stream error:', err.message);
      if (!res.headersSent) {
        res.writeHead(500, { 'Content-Type': 'text/plain; charset=utf-8' });
        res.end('500 Internal Server Error');
      }
    });
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
  console.log(`   - 🎛️  Интерактивный тренажер: http://localhost:${PORT}`);
  console.log(`   - 📖 Веб-ридер книги:        http://localhost:${PORT}/book/`);
  console.log(`   - 🎧 Веб-аудиоплеер книги:    http://localhost:${PORT}/audiobook/`);
});

// Корректное завершение процесса (Graceful Shutdown)
process.on('SIGINT', () => {
  server.close(() => process.exit(0));
});
process.on('SIGTERM', () => {
  server.close(() => process.exit(0));
});
