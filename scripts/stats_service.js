import { DatabaseSync } from 'node:sqlite';
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

export class StatsService {
  constructor(options = {}) {
    this.dbPath = options.dbPath || path.resolve('data', 'stats.db');
    this.adminPassword = process.env.IC_ADMIN_PASSWORD || options.adminPassword || 'innercurrent2026';
    this.salt = options.salt || 'ic_circuit_zen_2026';
    this.initDatabase();
  }

  initDatabase() {
    const dir = path.dirname(this.dbPath);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }

    this.db = new DatabaseSync(this.dbPath);
    this.db.exec(`PRAGMA journal_mode = WAL;`);
    this.db.exec(`PRAGMA synchronous = NORMAL;`);

    // Таблица просмотров страниц (визиты)
    this.db.exec(`
      CREATE TABLE IF NOT EXISTS page_views (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TEXT NOT NULL,
        date TEXT NOT NULL,
        path TEXT NOT NULL,
        title TEXT,
        referrer TEXT,
        ref_host TEXT,
        visitor_hash TEXT NOT NULL,
        ip TEXT,
        user_agent TEXT,
        device TEXT,
        screen TEXT,
        is_bot INTEGER DEFAULT 0
      );
    `);

    // Таблица скачиваний книг (PDF)
    this.db.exec(`
      CREATE TABLE IF NOT EXISTS downloads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TEXT NOT NULL,
        date TEXT NOT NULL,
        book_id TEXT NOT NULL,
        book_title TEXT NOT NULL,
        file_name TEXT NOT NULL,
        source_page TEXT,
        visitor_hash TEXT NOT NULL,
        ip TEXT,
        user_agent TEXT,
        device TEXT,
        referrer TEXT
      );
    `);

    // Таблица авторизационных токенов админки
    this.db.exec(`
      CREATE TABLE IF NOT EXISTS admin_auth (
        token TEXT PRIMARY KEY,
        created_at TEXT NOT NULL,
        expires_at TEXT NOT NULL
      );
    `);

    // Индексы для сверхбыстрой аналитики
    this.db.exec(`
      CREATE INDEX IF NOT EXISTS idx_pv_date ON page_views(date);
      CREATE INDEX IF NOT EXISTS idx_pv_path ON page_views(path);
      CREATE INDEX IF NOT EXISTS idx_pv_hash ON page_views(visitor_hash);
      CREATE INDEX IF NOT EXISTS idx_pv_bot ON page_views(is_bot);
      CREATE INDEX IF NOT EXISTS idx_dl_date ON downloads(date);
      CREATE INDEX IF NOT EXISTS idx_dl_book ON downloads(book_id);
      CREATE INDEX IF NOT EXISTS idx_dl_hash ON downloads(visitor_hash);
    `);

    // Подготовка стейтментов
    this.stmtInsertVisit = this.db.prepare(`
      INSERT INTO page_views (created_at, date, path, title, referrer, ref_host, visitor_hash, ip, user_agent, device, screen, is_bot)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    `);

    this.stmtInsertDownload = this.db.prepare(`
      INSERT INTO downloads (created_at, date, book_id, book_title, file_name, source_page, visitor_hash, ip, user_agent, device, referrer)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    `);

    this.stmtSaveToken = this.db.prepare(`
      INSERT OR REPLACE INTO admin_auth (token, created_at, expires_at)
      VALUES (?, ?, ?)
    `);

    this.stmtGetToken = this.db.prepare(`
      SELECT token, expires_at FROM admin_auth WHERE token = ?
    `);

    this.stmtDeleteToken = this.db.prepare(`
      DELETE FROM admin_auth WHERE token = ?
    `);
  }

  isBot(userAgent) {
    if (!userAgent) return 1;
    const ua = userAgent.toLowerCase();
    const botKeywords = [
      'bot', 'crawl', 'spider', 'slurp', 'mediapartners', 'lighthouse',
      'facebookexternalhit', 'whatsapp', 'telegrambot', 'twitterbot',
      'yandex', 'googlebot', 'bingbot', 'baiduspider', 'duckduckbot',
      'sogou', 'exabot', 'ahrefs', 'semrush', 'curl', 'wget', 'python',
      'go-http-client', 'postman', 'headlesschrome', 'pingdom', 'uptimerobot'
    ];
    return botKeywords.some(kw => ua.includes(kw)) ? 1 : 0;
  }

  computeHash(ip, userAgent) {
    const raw = `${ip || '127.0.0.1'}|${userAgent || ''}|${this.salt}`;
    return crypto.createHash('sha256').update(raw).digest('hex').slice(0, 16);
  }

  getRefHost(referrer) {
    if (!referrer || referrer === 'direct') return 'direct';
    try {
      const url = new URL(referrer);
      return url.hostname.replace(/^www\./, '');
    } catch {
      return referrer.slice(0, 50);
    }
  }

  detectDevice(ua, screen) {
    if (!ua) return 'desktop';
    const lower = ua.toLowerCase();
    if (lower.includes('ipad') || lower.includes('tablet')) return 'tablet';
    if (lower.includes('mobile') || lower.includes('iphone') || lower.includes('android')) return 'mobile';
    if (screen) {
      const [w] = screen.split('x').map(Number);
      if (w && w < 768) return 'mobile';
      if (w && w < 1024) return 'tablet';
    }
    return 'desktop';
  }

  canonicalizeBook(fileName, title) {
    const cleanFile = path.basename(fileName || '').trim();
    let bookId = cleanFile.toLowerCase().replace(/\.pdf$/, '');
    let bookTitle = title || cleanFile;

    const bookMap = {
      '01_inner_current': 'Внутренний ток (Архитектура человека)',
      '02_quaternary_fractal': 'Четверичный фрактал цепи',
      '03_universal_law': 'Универсальный закон потоковых систем',
      '04_flashlight_primer': 'Тайна карманного фонарика (Праймер)',
      'primer_flashlight': 'Тайна карманного фонарика (Праймер)',
      '05_field_manual': 'Полевой мануал оператора (30-сек протокол)',
      'field_manual': 'Полевой мануал оператора',
      '06_ukulele': 'Укулеле Бытия (Акустическая физика)',
      'ukulele': 'Укулеле Бытия (Акустическая физика)',
      '07_great_synthesis': 'Великий Синтез (Master Edition 2.0)',
      'great_synthesis': 'Великий Синтез (Master Edition 2.0)',
      'manifesto': 'Манифест Внутреннего тока (RU)',
      'manifesto_en': 'Manifesto of Inner Current (EN)',
      'manifesto_it': 'Manifesto del Flusso Interiore (IT)',
      'dual_circuit': 'Двухконтурная модель цепи',
      'copernicus': 'Коперниканский переворот сознания',
      'the_georgism_of_consciousness': 'Джорджизм сознания (Рента внимания)',
      'whitepaper': 'Master Whitepaper',
    };

    for (const [key, name] of Object.entries(bookMap)) {
      if (bookId.includes(key)) {
        return { bookId: key, bookTitle: name, fileName: cleanFile };
      }
    }

    if (cleanFile.includes('Итальянский триптих')) {
      return { bookId: 'italian_triptych', bookTitle: 'Итальянский триптих сверхпроводимости', fileName: cleanFile };
    }
    if (cleanFile.includes('Автомобил')) {
      return { bookId: 'benz_trilogy', bookTitle: 'Переход в эпоху Автомобиля (Карл Бенц)', fileName: cleanFile };
    }
    if (cleanFile.includes('Леванте')) {
      return { bookId: 'levante_triptych', bookTitle: 'Триптих Сверхпроводимости — Леванте', fileName: cleanFile };
    }

    return { bookId: bookId.slice(0, 40), bookTitle, fileName: cleanFile };
  }

  // --- Запись визита страницы ---
  recordVisit(data = {}) {
    try {
      const now = new Date();
      const createdAt = now.toISOString();
      const dateStr = createdAt.slice(0, 10);
      const cleanPath = (data.path || '/').split('?')[0];
      const title = (data.title || '').slice(0, 200);
      const referrer = (data.referrer || 'direct').slice(0, 500);
      const refHost = this.getRefHost(referrer);
      const ip = (data.ip || '127.0.0.1').replace(/^::ffff:/, '');
      const userAgent = (data.userAgent || '').slice(0, 500);
      const visitorHash = this.computeHash(ip, userAgent);
      const screen = (data.screen || '').slice(0, 20);
      const device = data.device || this.detectDevice(userAgent, screen);
      const isBot = this.isBot(userAgent);

      this.stmtInsertVisit.run(
        createdAt,
        dateStr,
        cleanPath,
        title,
        referrer,
        refHost,
        visitorHash,
        ip,
        userAgent,
        device,
        screen,
        isBot
      );

      return { ok: true, visitorHash };
    } catch (err) {
      console.error('StatsService recordVisit error:', err);
      return { ok: false, error: err.message };
    }
  }

  // --- Запись скачивания PDF книги ---
  recordDownload(data = {}) {
    try {
      const now = new Date();
      const createdAt = now.toISOString();
      const dateStr = createdAt.slice(0, 10);
      const { bookId, bookTitle, fileName } = this.canonicalizeBook(data.fileName, data.bookTitle);
      const sourcePage = (data.sourcePage || '/').slice(0, 200);
      const ip = (data.ip || '127.0.0.1').replace(/^::ffff:/, '');
      const userAgent = (data.userAgent || '').slice(0, 500);
      const visitorHash = this.computeHash(ip, userAgent);
      const device = data.device || this.detectDevice(userAgent);
      const referrer = (data.referrer || 'direct').slice(0, 500);

      this.stmtInsertDownload.run(
        createdAt,
        dateStr,
        bookId,
        bookTitle,
        fileName,
        sourcePage,
        visitorHash,
        ip,
        userAgent,
        device,
        referrer
      );

      return { ok: true, bookId, bookTitle };
    } catch (err) {
      console.error('StatsService recordDownload error:', err);
      return { ok: false, error: err.message };
    }
  }

  // --- Авторизация оператора ---
  login(password) {
    if (!password || password !== this.adminPassword) {
      return { success: false, error: 'Неверный мастер-пароль цепи' };
    }

    const token = crypto.randomBytes(32).toString('hex');
    const now = new Date();
    const createdAt = now.toISOString();
    // Срок действия сессии: 30 дней
    const expiresAt = new Date(now.getTime() + 30 * 24 * 60 * 60 * 1000).toISOString();

    this.stmtSaveToken.run(token, createdAt, expiresAt);
    return { success: true, token, expiresAt };
  }

  verifyToken(token) {
    if (!token) return false;
    const clean = token.replace(/^Bearer\s+/i, '').trim();
    if (!clean) return false;

    const row = this.stmtGetToken.get(clean);
    if (!row) return false;

    const now = new Date().toISOString();
    if (row.expires_at < now) {
      this.stmtDeleteToken.run(clean);
      return false;
    }

    return true;
  }

  logout(token) {
    if (!token) return;
    const clean = token.replace(/^Bearer\s+/i, '').trim();
    this.stmtDeleteToken.run(clean);
  }

  // --- Формирование сводной аналитики (Дашборд) ---
  getSummary(period = 'all') {
    const today = new Date().toISOString().slice(0, 10);
    let dateFilter = '';
    let params = [];

    if (period === 'today') {
      dateFilter = ' AND date = ?';
      params.push(today);
    } else if (period === '7d') {
      const d = new Date();
      d.setDate(d.getDate() - 7);
      dateFilter = ' AND date >= ?';
      params.push(d.toISOString().slice(0, 10));
    } else if (period === '30d') {
      const d = new Date();
      d.setDate(d.getDate() - 30);
      dateFilter = ' AND date >= ?';
      params.push(d.toISOString().slice(0, 10));
    }

    // 1. Общие счетчики (без ботов для чистоты метрик)
    const totalViewsQuery = `SELECT COUNT(*) AS total, COUNT(DISTINCT visitor_hash) AS unique_visitors FROM page_views WHERE is_bot = 0 ${dateFilter}`;
    const viewsRow = this.db.prepare(totalViewsQuery).get(...params) || { total: 0, unique_visitors: 0 };

    const todayViewsRow = this.db.prepare(`
      SELECT COUNT(*) AS total, COUNT(DISTINCT visitor_hash) AS unique_visitors 
      FROM page_views WHERE is_bot = 0 AND date = ?
    `).get(today) || { total: 0, unique_visitors: 0 };

    // 2. Скачивания книг в PDF
    const totalDownloadsQuery = `SELECT COUNT(*) AS total, COUNT(DISTINCT visitor_hash) AS unique_readers FROM downloads WHERE 1=1 ${dateFilter}`;
    const downloadsRow = this.db.prepare(totalDownloadsQuery).get(...params) || { total: 0, unique_readers: 0 };

    const todayDownloadsRow = this.db.prepare(`
      SELECT COUNT(*) AS total, COUNT(DISTINCT visitor_hash) AS unique_readers 
      FROM downloads WHERE date = ?
    `).get(today) || { total: 0, unique_readers: 0 };

    // Боты за период
    const botCountRow = this.db.prepare(`SELECT COUNT(*) AS total FROM page_views WHERE is_bot = 1 ${dateFilter}`).get(...params);

    // 3. Скачивания по каждой книге
    const booksQuery = `
      SELECT 
        book_id, 
        book_title, 
        file_name,
        COUNT(*) AS downloads_count, 
        COUNT(DISTINCT visitor_hash) AS unique_users,
        MAX(created_at) AS last_download
      FROM downloads 
      WHERE 1=1 ${dateFilter}
      GROUP BY book_id 
      ORDER BY downloads_count DESC
    `;
    const booksStats = this.db.prepare(booksQuery).all(...params);

    // Вычисляем процент от общего числа скачиваний
    const totalDl = downloadsRow.total || 0;
    const booksWithPercent = booksStats.map(b => ({
      ...b,
      percent: totalDl > 0 ? Math.round((b.downloads_count / totalDl) * 100) : 0
    }));

    // 4. Динамика по дням (за последние 30 дней)
    const daysBack = period === '7d' ? 7 : (period === 'today' ? 1 : 30);
    const startDate = new Date();
    startDate.setDate(startDate.getDate() - (daysBack - 1));
    const startStr = startDate.toISOString().slice(0, 10);

    const dailyViews = this.db.prepare(`
      SELECT date, COUNT(*) AS views, COUNT(DISTINCT visitor_hash) AS uniques
      FROM page_views
      WHERE is_bot = 0 AND date >= ?
      GROUP BY date
      ORDER BY date ASC
    `).all(startStr);

    const dailyDownloads = this.db.prepare(`
      SELECT date, COUNT(*) AS downloads
      FROM downloads
      WHERE date >= ?
      GROUP BY date
      ORDER BY date ASC
    `).all(startStr);

    // Сшиваем по датам
    const dailyMap = {};
    for (let i = 0; i < daysBack; i++) {
      const d = new Date(startDate);
      d.setDate(d.getDate() + i);
      const ds = d.toISOString().slice(0, 10);
      dailyMap[ds] = { date: ds, views: 0, uniques: 0, downloads: 0 };
    }

    dailyViews.forEach(r => {
      if (dailyMap[r.date]) {
        dailyMap[r.date].views = r.views;
        dailyMap[r.date].uniques = r.uniques;
      }
    });

    dailyDownloads.forEach(r => {
      if (dailyMap[r.date]) {
        dailyMap[r.date].downloads = r.downloads;
      }
    });

    const timeline = Object.values(dailyMap).sort((a, b) => a.date.localeCompare(b.date));

    // 5. Популярные страницы
    const topPages = this.db.prepare(`
      SELECT path, COUNT(*) AS views, COUNT(DISTINCT visitor_hash) AS uniques
      FROM page_views
      WHERE is_bot = 0 ${dateFilter}
      GROUP BY path
      ORDER BY views DESC
      LIMIT 12
    `).all(...params);

    // 6. Источники трафика (Referrers)
    const topReferrers = this.db.prepare(`
      SELECT ref_host, COUNT(*) AS visits
      FROM page_views
      WHERE is_bot = 0 ${dateFilter}
      GROUP BY ref_host
      ORDER BY visits DESC
      LIMIT 10
    `).all(...params);

    // 7. Устройства
    const devices = this.db.prepare(`
      SELECT device, COUNT(*) AS count
      FROM page_views
      WHERE is_bot = 0 ${dateFilter}
      GROUP BY device
      ORDER BY count DESC
    `).all(...params);

    return {
      period,
      generated_at: new Date().toISOString(),
      kpi: {
        total_views: viewsRow.total,
        unique_visitors: viewsRow.unique_visitors,
        today_views: todayViewsRow.total,
        today_uniques: todayViewsRow.unique_visitors,
        total_downloads: downloadsRow.total,
        unique_readers: downloadsRow.unique_readers,
        today_downloads: todayDownloadsRow.total,
        bot_hits: botCountRow ? botCountRow.total : 0,
        conversion_rate: viewsRow.unique_visitors > 0
          ? ((downloadsRow.unique_readers / viewsRow.unique_visitors) * 100).toFixed(1) + '%'
          : '0.0%'
      },
      books: booksWithPercent,
      timeline,
      top_pages: topPages,
      top_referrers: topReferrers,
      devices
    };
  }

  // --- Лента последних событий ---
  getRecentEvents(limit = 50) {
    const visits = this.db.prepare(`
      SELECT 'visit' AS event_type, created_at, path AS target, referrer, device, ip, visitor_hash
      FROM page_views
      WHERE is_bot = 0
      ORDER BY id DESC
      LIMIT ?
    `).all(limit);

    const downloads = this.db.prepare(`
      SELECT 'download' AS event_type, created_at, book_title AS target, file_name, source_page, device, ip, visitor_hash
      FROM downloads
      ORDER BY id DESC
      LIMIT ?
    `).all(limit);

    // Объединяем и сортируем по времени
    const merged = [...visits, ...downloads].sort((a, b) => b.created_at.localeCompare(a.created_at));
    return merged.slice(0, limit);
  }

  // --- Сброс статистики (с подтверждением) ---
  resetStats(confirmation) {
    if (confirmation !== 'RESET_INNER_CURRENT_STATS') {
      return { success: false, error: 'Требуется точная фраза подтверждения' };
    }

    this.db.exec(`DELETE FROM page_views;`);
    this.db.exec(`DELETE FROM downloads;`);
    this.db.exec(`VACUUM;`);

    return { success: true, message: 'Статистика успешно сброшена' };
  }

  // --- Экспорт данных ---
  exportData(format = 'json') {
    const views = this.db.prepare(`SELECT * FROM page_views WHERE is_bot = 0 ORDER BY id DESC LIMIT 5000`).all();
    const downloads = this.db.prepare(`SELECT * FROM downloads ORDER BY id DESC LIMIT 5000`).all();

    if (format === 'csv') {
      let csv = 'Type,Created_At,Target,File,Device,IP_Hash,Referrer\n';
      downloads.forEach(d => {
        csv += `Download,"${d.created_at}","${d.book_title}","${d.file_name}","${d.device}","${d.visitor_hash}","${d.referrer}"\n`;
      });
      views.forEach(v => {
        csv += `Visit,"${v.created_at}","${v.path}","-","${v.device}","${v.visitor_hash}","${v.referrer}"\n`;
      });
      return { format: 'csv', data: csv, mime: 'text/csv' };
    }

    return {
      format: 'json',
      data: JSON.stringify({ exported_at: new Date().toISOString(), downloads, views }, null, 2),
      mime: 'application/json'
    };
  }
}
