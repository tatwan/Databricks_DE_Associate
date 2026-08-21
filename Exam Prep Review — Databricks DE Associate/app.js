/* =========================================================================
   Exam Prep Review — interaction layer.
   State is in-memory only (sandboxed iframes block storage).
   ========================================================================= */

const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
const el = (tag, cls, html) => {
  const n = document.createElement(tag);
  if (cls) n.className = cls;
  if (html != null) n.innerHTML = html;
  return n;
};
const mm = (s) => `${String(Math.floor(s / 60)).padStart(2, '0')}:${String(s % 60).padStart(2, '0')}`;

const state = {
  ratings: {},           // cardKey -> 'ok' | 'weak'
  filters: { fix: false, weak: false, core: false },
  query: '',
  quiz: {},              // index -> chosen option
};

/* --------------------------------------------------------------- theme */

(function theme() {
  const t = $('[data-theme-toggle]');
  const root = document.documentElement;
  let mode = matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  const sun = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="4.5"/><path d="M12 2v2M12 20v2M4.2 4.2l1.4 1.4M18.4 18.4l1.4 1.4M2 12h2M20 12h2M4.2 19.8l1.4-1.4M18.4 5.6l1.4-1.4"/></svg>';
  const moon = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.8A9 9 0 1 1 11.2 3 7 7 0 0 0 21 12.8Z"/></svg>';
  const paint = () => {
    root.setAttribute('data-theme', mode);
    t.innerHTML = mode === 'dark' ? sun : moon;
    t.setAttribute('aria-label', `Switch to ${mode === 'dark' ? 'light' : 'dark'} mode`);
  };
  paint();
  t.addEventListener('click', () => {
    mode = mode === 'dark' ? 'light' : 'dark';
    paint();
  });
})();

/* ----------------------------------------------------------- blueprint */

(function blueprint() {
  const host = $('[data-blueprint]');
  const max = Math.max(...DOMAINS.map((d) => d.weight));
  DOMAINS.forEach((d) => {
    const row = el('button', 'bp__row');
    row.type = 'button';
    row.innerHTML = `
      <span class="bp__n">0${d.num}</span>
      <span class="bp__name">${d.title}</span>
      <span class="bp__bar"><i style="width:${(d.weight / max) * 100}%"></i></span>
      <span class="bp__w">${d.weight}%</span>`;
    row.addEventListener('click', () => {
      document.getElementById(d.id)?.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
    host.append(row);
  });
})();

/* ------------------------------------------------------- block renderer */

function renderBlock(b) {
  switch (b.type) {
    case 'points': {
      const w = el('div', 'pts');
      b.items.forEach(([t, d]) => w.append(el('div', 'pt', `<b>${t}</b><span>${d}</span>`)));
      return w;
    }
    case 'cols': {
      const w = el('div', 'cols');
      b.cols.forEach((c) => {
        w.append(
          el('div', 'col', `<h4>${c.head}</h4><ul role="list">${c.items.map((i) => `<li>${i}</li>`).join('')}</ul>`)
        );
      });
      return w;
    }
    case 'table': {
      const w = el('div', 'tablewrap');
      w.innerHTML = `<table><thead><tr>${b.head.map((h) => `<th scope="col">${h}</th>`).join('')}</tr></thead>
        <tbody>${b.rows.map((r) => `<tr>${r.map((c) => `<td>${c}</td>`).join('')}</tr>`).join('')}</tbody></table>`;
      return w;
    }
    case 'code': {
      const w = el('div', 'code');
      w.innerHTML = `<span class="code__lang">${b.lang}</span><pre><code>${b.body
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')}</code></pre>`;
      return w;
    }
    case 'flow': {
      const w = el('div', 'flow');
      b.steps.forEach(([t, d], i) => {
        w.append(el('div', 'flow__step', `<b>${t}</b><span>${d}</span>`));
        if (i < b.steps.length - 1) {
          w.append(
            el('span', 'flow__arrow',
              '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M13 6l6 6-6 6"/></svg>')
          );
        }
      });
      return w;
    }
    case 'callout':
      return el('div', `note${b.tone === 'warn' ? ' note--warn' : ''}`, `<b>${b.label}</b><span>${b.body}</span>`);
    case 'correction':
      return el('div', 'note note--fix', `<b>Correction applied</b><span>${b.body}</span>`);
    default:
      return el('div');
  }
}

/* ---------------------------------------------------------- domain cards */

const cardIndex = []; // { key, node, text, hasFix, optional, domain }

(function domains() {
  const host = $('[data-domains]');
  const rail = $('[data-rail]');

  DOMAINS.forEach((d) => {
    const link = el('a', 'rail__link');
    link.href = `#${d.id}`;
    link.innerHTML = `<i>0${d.num}</i><b>${d.title}</b><span>${d.weight}%</span>`;
    link.dataset.railFor = d.id;
    rail.append(link);

    const sec = el('section', 'domain');
    sec.id = d.id;
    sec.setAttribute('aria-labelledby', `${d.id}-h`);
    const head = el('header', 'domain__head');
    head.innerHTML = `
      <div class="domain__meta">
        <span class="domain__num">Domain ${d.num}</span>
        <span class="badge badge--accent">${d.weight}% · ≈${d.approxQ} questions</span>
        <span class="badge">${d.week}</span>
      </div>
      <h2 id="${d.id}-h">${d.title}</h2>
      <p>${d.summary}</p>`;
    sec.append(head);

    const cards = el('div', 'cards');
    d.cards.forEach((c) => {
      const key = `${d.id}-${c.slide}`;
      const card = el('article', 'card');
      card.dataset.key = key;

      const top = el('div', 'card__top');
      top.innerHTML = `
        <span class="card__id">S${c.slide}</span>
        <div class="card__ttl">
          <span class="eyebrow">${c.kicker}${c.optional ? ' · optional' : ''}</span>
          <h3>${c.title}</h3>
        </div>`;
      const conf = el('div', 'conf');
      conf.innerHTML = `
        <button type="button" data-v="ok" aria-pressed="false">Solid</button>
        <button type="button" data-v="weak" aria-pressed="false">Shaky</button>`;
      conf.addEventListener('click', (e) => {
        const btn = e.target.closest('button');
        if (!btn) return;
        const v = btn.dataset.v;
        state.ratings[key] = state.ratings[key] === v ? undefined : v;
        $$('button', conf).forEach((b) =>
          b.setAttribute('aria-pressed', String(state.ratings[key] === b.dataset.v))
        );
        updateReadiness();
        applyFilters();
      });
      top.append(conf);
      card.append(top);

      const body = el('div', 'card__body');
      c.blocks.forEach((b) => body.append(renderBlock(b)));
      if (c.src?.length) {
        const s = el('div', 'srcs');
        s.innerHTML = c.src
          .map(([label, url]) => `<a href="${url}" target="_blank" rel="noopener noreferrer">${label}</a>`)
          .join('');
        body.append(s);
      }
      card.append(body);
      cards.append(card);

      cardIndex.push({
        key,
        node: card,
        text: (c.title + ' ' + c.kicker + ' ' + card.textContent).toLowerCase(),
        hasFix: c.blocks.some((b) => b.type === 'correction'),
        optional: !!c.optional,
        domain: d.id,
      });
    });

    sec.append(cards);
    host.append(sec);
  });

  $('[data-count-fix]').textContent = cardIndex.filter((c) => c.hasFix).length;
  updateReadiness();
})();

/* ---------------------------------------------------------- filter logic */

function applyFilters() {
  const q = state.query.trim().toLowerCase();
  let shown = 0;
  cardIndex.forEach((c) => {
    let ok = true;
    if (q && !c.text.includes(q)) ok = false;
    if (state.filters.fix && !c.hasFix) ok = false;
    if (state.filters.weak && state.ratings[c.key] !== 'weak') ok = false;
    if (state.filters.core && c.optional) ok = false;
    c.node.classList.toggle('is-hidden', !ok);
    if (ok) shown++;
  });

  // Hide a domain section whose cards are all filtered out.
  DOMAINS.forEach((d) => {
    const visible = cardIndex.filter((c) => c.domain === d.id && !c.node.classList.contains('is-hidden'));
    const sec = document.getElementById(d.id);
    sec.hidden = visible.length === 0;
    $(`[data-rail-for="${d.id}"]`).style.opacity = visible.length === 0 ? '.35' : '';
  });

  let empty = $('[data-empty]');
  if (!shown) {
    if (!empty) {
      empty = el('div', 'empty', '<b>No cards match</b><p>Clear the filters or try a different keyword.</p>');
      empty.dataset.empty = '';
      $('[data-domains]').append(empty);
    }
    empty.hidden = false;
  } else if (empty) empty.hidden = true;
}

$('[data-search]').addEventListener('input', (e) => {
  state.query = e.target.value;
  applyFilters();
});

$$('[data-filter]').forEach((btn) => {
  btn.addEventListener('click', () => {
    const k = btn.dataset.filter;
    state.filters[k] = !state.filters[k];
    btn.setAttribute('aria-pressed', String(state.filters[k]));
    applyFilters();
  });
});

/* ------------------------------------------------------------ readiness */

function updateReadiness() {
  const total = cardIndex.length;
  const rated = cardIndex.filter((c) => state.ratings[c.key]);
  const ok = rated.filter((c) => state.ratings[c.key] === 'ok').length;
  const weak = rated.length - ok;

  $('[data-r-pct]').textContent = rated.length ? `${Math.round((ok / rated.length) * 100)}%` : '0%';
  $('[data-r-count]').textContent = `${rated.length} of ${total} cards rated`;
  $('[data-r-ok]').style.width = `${(ok / total) * 100}%`;
  $('[data-r-weak]').style.width = `${(weak / total) * 100}%`;
  $('[data-count-weak]').textContent = weak;

  const out = $('[data-r-out]');
  if (!weak) {
    out.innerHTML = rated.length
      ? 'Nothing flagged shaky yet. Keep rating as you teach — flags drive the final-week plan.'
      : 'Rate each card <strong>Solid</strong> or <strong>Shaky</strong> as you teach it. The weakest domain leads the final-week plan.';
    return;
  }
  const byDomain = DOMAINS.map((d) => ({
    d,
    n: cardIndex.filter((c) => c.domain === d.id && state.ratings[c.key] === 'weak').length,
  })).filter((x) => x.n);
  byDomain.sort((a, b) => b.n * b.d.weight - a.n * a.d.weight);
  const lead = byDomain[0];
  out.innerHTML = `Final-week plan starts with <strong>Domain ${lead.d.num} — ${lead.d.title}</strong>
    (${lead.n} flagged, ${lead.d.weight}% of the exam)${
    byDomain[1] ? `, then Domain ${byDomain[1].d.num}` : ''
  }.`;
}

$('[data-r-reset]').addEventListener('click', () => {
  state.ratings = {};
  $$('.conf button').forEach((b) => b.setAttribute('aria-pressed', 'false'));
  updateReadiness();
  applyFilters();
});

/* ---------------------------------------------------------- rail scroll */

(function railHighlight() {
  const links = $$('[data-rail-for]');
  const io = new IntersectionObserver(
    (entries) => {
      entries.forEach((e) => {
        if (!e.isIntersecting) return;
        links.forEach((l) => l.classList.toggle('is-active', l.dataset.railFor === e.target.id));
      });
    },
    { rootMargin: '-25% 0px -65% 0px' }
  );
  DOMAINS.forEach((d) => io.observe(document.getElementById(d.id)));
})();

/* ----------------------------------------------------------- plan + timer */

const timer = { i: 0, left: PLAN[0].min * 60, elapsed: 0, running: false, tick: null };

(function plan() {
  const host = $('[data-plan]');
  PLAN.forEach((p, i) => {
    const row = el('button', 'plan__row');
    row.type = 'button';
    row.dataset.seg = String(i);
    row.innerHTML = `<span class="plan__min">${p.min} min</span>
      <span class="plan__lab">${p.label}</span>
      <span class="plan__note">${p.note}</span>`;
    row.addEventListener('click', () => {
      goTo(i);
      if (p.target !== 'top') document.getElementById(p.target)?.scrollIntoView({ behavior: 'smooth' });
    });
    host.append(row);
  });
})();

function paintTimer() {
  const p = PLAN[timer.i];
  $('[data-t-seg]').textContent = mm(Math.max(0, timer.left));
  $('[data-t-name]').textContent = p.label;
  $('[data-t-total]').textContent = mm(timer.elapsed);
  $('[data-t-bar]').style.width = `${Math.min(100, (timer.elapsed / (EXAM.minutes * 60)) * 100)}%`;

  $$('[data-seg]').forEach((r) => {
    const i = Number(r.dataset.seg);
    r.setAttribute('aria-current', String(i === timer.i));
    r.classList.toggle('is-done', i < timer.i);
  });

  const clock = $('[data-clock]');
  clock.hidden = !timer.running && timer.elapsed === 0;
  $('[data-clock-time]').textContent = mm(Math.max(0, EXAM.minutes * 60 - timer.elapsed));
  $('[data-clock-seg]').textContent = p.label;
  $('[data-t-start]').textContent = timer.running ? 'Pause' : timer.elapsed ? 'Resume' : 'Start';
}

function goTo(i) {
  timer.i = Math.max(0, Math.min(PLAN.length - 1, i));
  timer.left = PLAN[timer.i].min * 60;
  timer.elapsed = PLAN.slice(0, timer.i).reduce((a, p) => a + p.min * 60, 0);
  paintTimer();
}

function run(on) {
  timer.running = on;
  clearInterval(timer.tick);
  if (on) {
    timer.tick = setInterval(() => {
      timer.left--;
      timer.elapsed++;
      if (timer.left <= 0) {
        if (timer.i < PLAN.length - 1) {
          timer.i++;
          timer.left = PLAN[timer.i].min * 60;
        } else {
          timer.left = 0;
          run(false);
        }
      }
      paintTimer();
    }, 1000);
  }
  paintTimer();
}

$('[data-t-start]').addEventListener('click', () => run(!timer.running));
$('[data-t-next]').addEventListener('click', () => {
  goTo(timer.i + 1);
  const t = PLAN[timer.i].target;
  if (t !== 'top') document.getElementById(t)?.scrollIntoView({ behavior: 'smooth' });
});
$('[data-t-reset]').addEventListener('click', () => {
  run(false);
  goTo(0);
  timer.elapsed = 0;
  paintTimer();
});
$('[data-clock-toggle]').addEventListener('click', () => run(!timer.running));
paintTimer();

/* ---------------------------------------------------------------- drills */

(function drills() {
  const host = $('[data-drills]');
  DRILLS.forEach((d) => {
    const dom = DOMAINS.find((x) => x.id === d.d);
    const card = el('button', 'drill');
    card.type = 'button';
    card.setAttribute('aria-expanded', 'false');
    card.innerHTML = `
      <span class="eyebrow">Domain ${dom.num}</span>
      <span class="drill__q">${d.q}</span>
      <span class="drill__hint">Select to reveal</span>
      <span class="drill__a"><b>${d.a}</b><span>${d.why}</span></span>`;
    card.addEventListener('click', () => {
      const open = card.classList.toggle('is-open');
      card.setAttribute('aria-expanded', String(open));
    });
    host.append(card);
  });
})();

/* ------------------------------------------------------------------ quiz */

(function quiz() {
  const host = $('[data-quiz]');
  QUIZ.forEach((q, i) => {
    const dom = DOMAINS.find((x) => x.id === q.d);
    const card = el('article', 'q');
    card.innerHTML = `
      <div class="q__head">
        <span class="q__n">${String(i + 1).padStart(2, '0')}</span>
        <div>
          <p class="q__q">${q.q}</p>
          <p class="eyebrow" style="margin-top:var(--space-2)">Domain ${dom.num} · ${dom.title}</p>
        </div>
      </div>`;
    const opts = el('div', 'q__opts');
    q.opts.forEach((o, oi) => {
      const b = el('button', 'opt', `<i>${'ABCD'[oi]}</i><span>${o}</span>`);
      b.type = 'button';
      b.addEventListener('click', () => {
        if (state.quiz[i] != null) return;
        state.quiz[i] = oi;
        $$('button', opts).forEach((x, xi) => {
          x.disabled = true;
          if (xi === q.a) x.classList.add('is-right');
          else if (xi === oi) x.classList.add('is-wrong');
        });
        card.classList.add('is-done');
        score();
      });
      opts.append(b);
    });
    card.append(opts);
    card.append(el('p', 'q__why', q.why));
    host.append(card);
  });
})();

function score() {
  const answered = Object.keys(state.quiz).length;
  const right = Object.entries(state.quiz).filter(([i, v]) => QUIZ[i].a === v).length;
  const box = $('[data-score]');
  box.hidden = false;
  $('[data-score-n]').textContent = `${right} / ${answered} correct`;

  if (answered < QUIZ.length) {
    $('[data-score-msg]').textContent = `${QUIZ.length - answered} question${
      QUIZ.length - answered === 1 ? '' : 's'
    } remaining.`;
    return;
  }
  const missed = DOMAINS.map((d) => ({
    d,
    n: Object.entries(state.quiz).filter(([i, v]) => QUIZ[i].d === d.id && QUIZ[i].a !== v).length,
  })).filter((x) => x.n);
  missed.sort((a, b) => b.n * b.d.weight - a.n * a.d.weight);
  $('[data-score-msg]').innerHTML = missed.length
    ? `Re-read <strong>Domain ${missed[0].d.num} — ${missed[0].d.title}</strong> first (${missed[0].n} missed, ${missed[0].d.weight}% of the exam).${
        missed[1] ? ` Then Domain ${missed[1].d.num}.` : ''
      }`
    : 'Clean sweep. Move on to timed mock questions.';
}
