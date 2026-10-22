/* Rapture Ready Home Care — Built by Truly Digital Solutions, LLC (TruTech) · Build TT-RR-2026-04 */
(() => {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const OFFICE = {
    tz: 'America/New_York',
    // day index 0 = Sunday. [open, close] in 24h hours; null = closed
    hours: [null, [9, 17], [9, 17], [9, 17], [9, 17], [9, 17], null],
  };
  const KEY = 'rr-size';

  /* Text size */
  const root = document.documentElement;
  const setSize = (n) => {
    root.dataset.size = n;
    $$('[data-size-btn]').forEach((b) => b.setAttribute('aria-pressed', String(b.dataset.sizeBtn === String(n))));
    try { localStorage.setItem(KEY, n); } catch (e) { /* private mode */ }
    positionMenu();
  };
  $$('[data-size-btn]').forEach((b) => b.addEventListener('click', () => setSize(b.dataset.sizeBtn)));
  $$('[data-size-btn]').forEach((b) => b.setAttribute('aria-pressed', String(b.dataset.sizeBtn === (root.dataset.size || '1'))));

  /* Open / closed status, computed in Eastern time */
  const fmt = (h) => { const hr = Math.floor(h); const m = Math.round((h - hr) * 60); const ap = hr >= 12 ? 'pm' : 'am'; return `${((hr + 11) % 12) + 1}${m ? ':' + String(m).padStart(2, '0') : ''} ${ap}`; };
  const status = () => {
    const el = $('[data-status]'); if (!el) return;
    const parts = Object.fromEntries(new Intl.DateTimeFormat('en-US', { timeZone: OFFICE.tz, weekday: 'short', hour: 'numeric', minute: 'numeric', hour12: false })
      .formatToParts(new Date()).map((p) => [p.type, p.value]));
    const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    const names = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
    const d = days.indexOf(parts.weekday);
    const now = (Number(parts.hour) % 24) + Number(parts.minute) / 60;
    const today = OFFICE.hours[d];
    let text;
    if (today && now >= today[0] && now < today[1]) {
      el.classList.add('is-open');
      text = `Open now until ${fmt(today[1])}`;
    } else {
      el.classList.remove('is-open');
      let i = 0, nd = d, when, h;
      if (today && now < today[0]) { when = 'today'; h = today[0]; }
      else {
        do { nd = (nd + 1) % 7; i++; } while (!OFFICE.hours[nd] && i < 7);
        when = i === 1 ? 'tomorrow' : names[nd]; h = OFFICE.hours[nd][0];
      }
      text = `Closed now. Opens ${when} at ${fmt(h)}`;
    }
    $('[data-status-text]', el).textContent = text;
  };
  status(); setInterval(status, 60000);

  /* Header + mobile menu */
  const hdr = $('[data-hdr]'); const nav = $('[data-nav]'); const btn = $('[data-menu-btn]');
  function positionMenu() { if (hdr) root.style.setProperty('--hdr-bottom', `${Math.max(0, hdr.getBoundingClientRect().bottom)}px`); }
  const onScroll = () => hdr && hdr.classList.toggle('is-stuck', window.scrollY > 8);
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();
  const close = () => { nav.classList.remove('is-open'); btn.setAttribute('aria-expanded', 'false'); $('[data-menu-label]').textContent = 'Menu'; document.body.style.overflow = ''; };
  if (btn && nav) {
    nav.id = 'menu';
    btn.addEventListener('click', () => {
      if (nav.classList.contains('is-open')) return close();
      positionMenu(); nav.classList.add('is-open'); btn.setAttribute('aria-expanded', 'true');
      $('[data-menu-label]').textContent = 'Close'; document.body.style.overflow = 'hidden';
    });
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && nav.classList.contains('is-open')) { close(); btn.focus(); } });
    window.addEventListener('resize', () => { if (window.innerWidth > 1020) close(); else positionMenu(); });
  }

  /* Prefill from query string (e.g. ?ride=Dialysis) */
  const params = new URLSearchParams(location.search);
  $$('[data-form] select, [data-form] input[type=date]').forEach((el) => {
    const v = params.get(el.name); if (!v) return;
    if (el.tagName === 'SELECT') { const o = [...el.options].find((x) => x.value === v || x.text === v); if (o) el.value = o.value; }
    else el.value = v;
  });
  $$('[data-min-today]').forEach((el) => {
    const t = new Date(); el.min = `${t.getFullYear()}-${String(t.getMonth() + 1).padStart(2, '0')}-${String(t.getDate()).padStart(2, '0')}`;
  });

  /* Forms: validate, then compose an email (no data is stored on this website) */
  $$('[data-form]').forEach((form) => {
    const err = $('[data-form-err]', form);
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const f = Object.fromEntries(new FormData(form));
      const missing = ['name', 'phone'].filter((k) => !String(f[k] || '').trim());
      $$('input, select, textarea', form).forEach((el) => el.removeAttribute('aria-invalid'));
      missing.forEach((k) => form.elements[k].setAttribute('aria-invalid', 'true'));
      if (missing.length) {
        err.textContent = 'Please add your name and a phone number so we can call you back.';
        form.elements[missing[0]].focus();
        return;
      }
      err.textContent = '';
      const when = f.date ? new Date(f.date + 'T00:00:00').toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric', year: 'numeric' }) : '';
      const lines = [
        `Name: ${f.name}`, `Phone: ${f.phone}`, `Email: ${f.email || '—'}`,
        f.who && `Care is for: ${f.who}`, f.care && `Type of care: ${f.care}`, f.start && `Start: ${f.start}`, f.pay && `Payment: ${f.pay}`,
        f.ride && `Ride for: ${f.ride}`, when && `Date: ${when}`, f.time && `Appointment time: ${f.time}`,
        f.pickup && `Pick-up address: ${f.pickup}`, f.dest && `Destination: ${f.dest}`, f.mobility && `Mobility needs: ${f.mobility}`, f.repeat && `Recurring: ${f.repeat}`,
        '', f.message || '',
      ].filter((x) => typeof x === 'string');
      const subject = `${form.dataset.subject} from ${f.name}`;
      location.href = `mailto:${form.dataset.email}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(lines.join('\n'))}`;
    });
  });

  $$('[data-year]').forEach((el) => { el.textContent = new Date().getFullYear(); });
})();

/* Squarespace edition: move the page's Squarespace Form block into the form slot so
   submissions are stored in Squarespace. Does nothing on pages without a slot. */
(() => {
  if (window.top !== window.self) return; // inside the Squarespace editor
  const run = () => {
    const slots = [...document.querySelectorAll('[data-sq-form-slot]')];
    if (!slots.length) return;
    const blocks = [...document.querySelectorAll('form')]
      .filter((f) => !f.closest('.rr-site') && !f.closest('[data-sq-form-slot]'))
      .map((f) => f.closest('.sqs-block') || f.closest('.form-wrapper') || f);
    slots.filter((sl) => !sl.querySelector('form')).forEach((slot, i) => {
      const block = blocks[i];
      if (!block) return;
      const section = block.closest('.page-section, section');
      slot.innerHTML = '';
      slot.appendChild(block);
      if (section && !section.querySelector('.rr-site')) section.style.display = 'none';
    });
  };
  // Squarespace draws its form after the page loads, so keep checking briefly.
  let tries = 0;
  const tick = () => {
    const pending = [...document.querySelectorAll('[data-sq-form-slot]')].some((s) => !s.querySelector('form'));
    if (!pending) return;
    run();
    if (++tries < 40) setTimeout(tick, 250);
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', tick); else tick();
})();
