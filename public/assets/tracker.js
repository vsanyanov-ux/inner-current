/**
 * ⚡ Inner Current — High-Precision Analytics & Download Tracker
 * Autonomous, zero-cookie, zero-external-dependency telemetry
 */
(function() {
  if (typeof window === 'undefined' || window.__IC_TRACKER_LOADED__) return;
  window.__IC_TRACKER_LOADED__ = true;

  const STATS_API_VISIT = '/api/stats/visit';
  const STATS_API_DOWNLOAD = '/api/stats/download';

  // Вспомогательная функция отправки данных через sendBeacon / fetch keepalive
  function sendPayload(url, data) {
    try {
      const json = JSON.stringify(data);
      if (navigator.sendBeacon) {
        const blob = new Blob([json], { type: 'application/json' });
        navigator.sendBeacon(url, blob);
      } else {
        fetch(url, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: json,
          keepalive: true
        }).catch(() => {});
      }
    } catch (e) {
      // Graceful degradation (Мусин)
    }
  }

  // 1. Отправка события просмотра страницы (Page View)
  function trackPageView() {
    // Не трекаем служебные страницы предпросмотра
    const path = window.location.pathname || '/';
    if (path.startsWith('/admin')) return;

    const searchParams = new URLSearchParams(window.location.search);
    let referrer = document.referrer || 'direct';

    const utmSource = searchParams.get('utm_source');
    const utmMedium = searchParams.get('utm_medium');
    const utmCampaign = searchParams.get('utm_campaign');
    if (utmSource) {
      referrer = `utm:${utmSource}` + (utmMedium ? `/${utmMedium}` : '') + (utmCampaign ? ` (${utmCampaign})` : '');
    }

    sendPayload(STATS_API_VISIT, {
      path: path,
      title: document.title || 'Inner Current',
      referrer: referrer,
      screen: `${window.screen?.width || 0}x${window.screen?.height || 0}`,
      device: window.innerWidth < 768 ? 'mobile' : (window.innerWidth < 1024 ? 'tablet' : 'desktop')
    });
  }

  // 2. Определение информации о книге из ссылки
  function extractBookInfo(linkEl) {
    const href = linkEl.getAttribute('href') || '';
    const cleanHref = href.split('?')[0].split('#')[0];
    
    // Проверяем, PDF ли это или ссылка на книгу
    if (!cleanHref.toLowerCase().endsWith('.pdf') && !cleanHref.includes('/books/')) {
      return null;
    }

    const fileName = cleanHref.split('/').pop();
    if (!fileName) return null;

    // Пытаемся достать понятное название книги
    let bookTitle = linkEl.getAttribute('data-book-title') 
      || linkEl.getAttribute('title') 
      || linkEl.innerText.replace(/[\n\r]+/g, ' ').trim();

    // Очищаем от служебных значков скачивания
    bookTitle = bookTitle.replace(/^[📥📖📄⚡\s]+/, '').replace(/Скачать PDF/gi, '').replace(/\(.*?стр.*?\)/gi, '').trim();

    // Если в карточке родителя есть заголовок h2/h3
    if (!bookTitle || bookTitle.length < 3) {
      const card = linkEl.closest('.book-card, article, section, div[class*="rounded"]');
      if (card) {
        const heading = card.querySelector('h2, h3, h4, .font-bold, .font-serif');
        if (heading) {
          bookTitle = heading.innerText.replace(/[\n\r]+/g, ' ').trim();
        }
      }
    }

    return {
      fileName: decodeURIComponent(fileName),
      bookTitle: bookTitle || fileName
    };
  }

  // 3. Отслеживание кликов по ссылкам скачивания
  function initDownloadTracker() {
    document.addEventListener('click', function(e) {
      const link = e.target.closest('a');
      if (!link) return;

      const bookInfo = extractBookInfo(link);
      if (bookInfo) {
        sendPayload(STATS_API_DOWNLOAD, {
          fileName: bookInfo.fileName,
          bookTitle: bookInfo.bookTitle,
          sourcePage: window.location.pathname || '/'
        });
      }
    }, { capture: true, passive: true });
  }

  // 4. Секретный вход в админку для оператора (Видна только автору)
  function initSecretAdminAccess() {
    // А) Хоткей Ctrl + Shift + A (или Cmd + Shift + A на Mac)
    window.addEventListener('keydown', function(e) {
      if ((e.ctrlKey || e.metaKey) && e.shiftKey && (e.key === 'A' || e.key === 'a' || e.key === 'Ф' || e.key === 'ф')) {
        e.preventDefault();
        window.location.href = '/admin';
      }
    });

    // Б) Тройной клик / тап по логотипу или значку молнии ⚡
    let tapCount = 0;
    let tapTimer = null;

    document.addEventListener('click', function(e) {
      const logoEl = e.target.closest('a[href="/"], .brand-logo, #logo, header a, nav a:first-child');
      if (!logoEl) return;

      // Проверяем, что кликнули именно по главному логотипу
      const text = logoEl.innerText || '';
      if (text.includes('Inner Current') || text.includes('Внутренний ток') || text.includes('⚡')) {
        tapCount++;
        clearTimeout(tapTimer);
        tapTimer = setTimeout(function() {
          tapCount = 0;
        }, 1500);

        if (tapCount >= 3) {
          tapCount = 0;
          window.location.href = '/admin';
        }
      }
    });
  }

  // Запуск при готовности DOM
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
      trackPageView();
      initDownloadTracker();
      initSecretAdminAccess();
    });
  } else {
    trackPageView();
    initDownloadTracker();
    initSecretAdminAccess();
  }
})();
