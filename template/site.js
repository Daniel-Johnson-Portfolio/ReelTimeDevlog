/* Devlog interactions. Everything works without this file; it adds the lightbox, the
   before/after slider, gallery filters and search. */
(() => {
  const $ = (sel, el = document) => el.querySelector(sel);
  const $$ = (sel, el = document) => [...el.querySelectorAll(sel)];
  const isVideo = (url) => /\.(mp4|webm)(\?|#|$)/i.test(url);

  /* ---------- lightbox ---------- */
  const links = () => $$('a[data-lightbox]').filter((a) => !a.closest('[hidden]'));
  if ($$('a[data-lightbox]').length && 'HTMLDialogElement' in window) {
    const dlg = document.createElement('dialog');
    dlg.className = 'lightbox';
    dlg.setAttribute('aria-label', 'Media viewer');
    dlg.innerHTML =
      '<div class="lb-stage"></div>' +
      '<p class="lb-text"><span class="lb-caption"></span> <a class="lb-post" hidden>Read the post</a></p>' +
      '<button type="button" class="lb-btn lb-close">Close</button>' +
      '<button type="button" class="lb-btn lb-prev" aria-label="Previous">&#8249;</button>' +
      '<button type="button" class="lb-btn lb-next" aria-label="Next">&#8250;</button>';
    document.body.appendChild(dlg);
    let current = null;
    const show = (a) => {
      current = a;
      const url = a.getAttribute('href');
      const stage = $('.lb-stage', dlg);
      stage.textContent = '';
      const el = document.createElement(isVideo(url) ? 'video' : 'img');
      el.src = url;
      if (isVideo(url)) { Object.assign(el, { controls: true, autoplay: true, loop: true, muted: true, playsInline: true }); }
      else { el.alt = a.dataset.caption || ''; }
      stage.appendChild(el);
      $('.lb-caption', dlg).textContent = a.dataset.caption || '';
      const post = $('.lb-post', dlg);
      post.hidden = !a.dataset.post;
      if (a.dataset.post) post.href = a.dataset.post;
      const many = links().length > 1;
      $('.lb-prev', dlg).hidden = !many;
      $('.lb-next', dlg).hidden = !many;
    };
    const step = (d) => {
      const all = links();
      if (!current || all.length < 2) return;
      show(all[(all.indexOf(current) + d + all.length) % all.length]);
    };
    document.addEventListener('click', (e) => {
      const a = e.target.closest('a[data-lightbox]');
      if (!a || e.metaKey || e.ctrlKey || e.shiftKey) return;
      e.preventDefault();
      show(a);
      dlg.showModal();
    });
    $('.lb-close', dlg).addEventListener('click', () => dlg.close());
    $('.lb-prev', dlg).addEventListener('click', () => step(-1));
    $('.lb-next', dlg).addEventListener('click', () => step(1));
    dlg.addEventListener('click', (e) => { if (e.target === dlg) dlg.close(); });
    dlg.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowLeft') step(-1);
      if (e.key === 'ArrowRight') step(1);
    });
    dlg.addEventListener('close', () => { $('.lb-stage', dlg).textContent = ''; if (current) current.focus(); });
  }

  /* ---------- play in the browser: load the game only when asked ---------- */
  $$('.play-embed').forEach((box) => {
    const btn = $('.play-load', box);
    if (!btn) return;
    btn.addEventListener('click', () => {
      const frame = document.createElement('iframe');
      frame.src = box.dataset.src;
      frame.title = 'The game';
      frame.allow = 'autoplay; fullscreen; cross-origin-isolated; gamepad';
      frame.allowFullscreen = true;
      box.textContent = '';
      box.appendChild(frame);
    });
  });

  /* ---------- before / after ---------- */
  $$('.compare').forEach((fig) => {
    const range = $('input[type=range]', fig);
    if (!range) return;
    const set = () => fig.style.setProperty('--pos', `${range.value}%`);
    range.addEventListener('input', set);
    set();
  });

  /* ---------- gallery filter ---------- */
  const filter = $('.filter');
  if (filter) {
    filter.hidden = false;
    filter.addEventListener('click', (e) => {
      const btn = e.target.closest('button[data-filter]');
      if (!btn) return;
      const want = btn.dataset.filter;
      $$('button[data-filter]', filter).forEach((b) => b.setAttribute('aria-pressed', String(b === btn)));
      $$('[data-cats]').forEach((item) => {
        item.hidden = want !== 'all' && !item.dataset.cats.split(' ').includes(want);
      });
    });
  }

  /* ---------- search ---------- */
  const results = $('.search-results');
  if (results && window.DEVLOG_INDEX) {
    const input = $('#q');
    const count = $('.search-count');
    const params = new URLSearchParams(location.search);
    input.value = params.get('q') || '';
    const card = (r) => {
      const art = document.createElement('article');
      art.className = 'card';
      const media = document.createElement('a');
      media.className = 'card-media';
      media.href = r.u;
      media.tabIndex = -1;
      media.setAttribute('aria-hidden', 'true');
      if (r.i) { const img = document.createElement('img'); img.src = r.i; img.alt = ''; img.loading = 'lazy'; media.appendChild(img); }
      const body = document.createElement('div');
      body.className = 'card-body';
      const meta = document.createElement('div');
      meta.className = 'card-meta';
      if (r.c.length) { const c = document.createElement('span'); c.className = 'chip'; c.textContent = r.c.join(', '); meta.appendChild(c); }
      const when = document.createElement('span'); when.className = 'card-when'; when.textContent = r.d; meta.appendChild(when);
      const h = document.createElement('h3');
      const a = document.createElement('a');
      a.href = r.u;
      a.textContent = r.t;
      h.appendChild(a);
      const p = document.createElement('p');
      p.className = 'summary';
      p.textContent = r.s;
      body.append(meta, h, p);
      art.append(media, body);
      return art;
    };
    const run = () => {
      const q = input.value.trim().toLowerCase();
      results.textContent = '';
      if (!q) { count.textContent = `${window.DEVLOG_INDEX.length} posts. Type to search titles, topics, sessions and text.`; return; }
      const terms = q.split(/\s+/);
      const scored = window.DEVLOG_INDEX.map((r) => {
        const fields = { t: r.t.toLowerCase(), m: (r.c.join(' ') + ' ' + r.w.join(' ')).toLowerCase(), s: r.s.toLowerCase(), x: r.x.toLowerCase() };
        let score = 0;
        for (const term of terms) {
          const hit = (fields.t.includes(term) ? 6 : 0) + (fields.m.includes(term) ? 4 : 0) + (fields.s.includes(term) ? 2 : 0) + (fields.x.includes(term) ? 1 : 0);
          if (!hit) return null;
          score += hit;
        }
        return { r, score };
      }).filter(Boolean).sort((a, b) => b.score - a.score || b.r.o - a.r.o);
      count.textContent = scored.length ? `${scored.length} ${scored.length === 1 ? 'post' : 'posts'} found for "${input.value.trim()}".` : `Nothing found for "${input.value.trim()}". Try a topic name, a session (like "world") or a single word.`;
      scored.forEach(({ r }) => results.appendChild(card(r)));
    };
    input.addEventListener('input', () => {
      run();
      try { history.replaceState(null, '', `?q=${encodeURIComponent(input.value.trim())}`); } catch (e) { /* file:// */ }
    });
    run();
  }
})();
