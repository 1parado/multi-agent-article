#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Apply full UX reading/design polish to index.html (idempotent)."""
from pathlib import Path
import re
import sys

def main():
    candidates = [Path('index.html'), Path(__file__).resolve().parent.parent / 'index.html']
    p = next((x for x in candidates if x.is_file()), None)
    if not p:
        print('ERROR: index.html not found', file=sys.stderr)
        return 1
    c = p.read_text(encoding='utf-8')
    if 'ux-all: URL state' in c and '#5f5f5b' in c and 'id="skip"' in c:
        print('already applied')
        return 0

    c = c.replace(
      ':root { --red:#A02C2C; --sage:#C9CBC0; --ink:#1a1a1a; --gray:#3d3d3d; --soft:#8a8a86; --line:#e6e4e0; }',
      ':root { --red:#A02C2C; --sage:#C9CBC0; --ink:#1a1a1a; --gray:#333333; --soft:#5f5f5b; --line:#e6e4e0; --link:#8B3A3A; color-scheme:light; }')
    c = c.replace(
      '.wrap { max-width:780px; margin:0 auto; padding:72px 24px 90px; }',
      '.wrap { max-width:720px; margin:0 auto; padding:72px 24px 90px; }')
    c = c.replace(
      'body { font-family:-apple-system,"Segoe UI","Microsoft YaHei",system-ui,sans-serif; color:var(--ink); background:#fff; margin:0; line-height:2.0; font-size:15.5px; }',
      'body { font-family:-apple-system,"Segoe UI","Microsoft YaHei",system-ui,sans-serif; color:var(--ink); background:#fff; margin:0; line-height:1.85; font-size:15.5px; }')
    c = c.replace(
      '.intro { color:var(--gray); margin:6px 0 0; }',
      '.intro { color:var(--gray); margin:6px 0 0; line-height:1.85; }')
    c = c.replace(
      '.paper a { color:var(--red); text-decoration:none; font-size:13.5px; font-weight:600; margin-right:16px; }',
      '.paper a { color:var(--link,var(--red)); text-decoration:none; font-size:13.5px; font-weight:600; margin-right:16px; }')
    c = c.replace(
      '.paper:hover { background:#faf8f6; border-left-color:var(--cat,var(--red)); }',
      '.paper:hover { background:#faf8f6; border-left-color:var(--cat,var(--red)); box-shadow:0 2px 12px rgba(0,0,0,.04); }\n  .paper.is-read { opacity:.72; }\n  .paper.is-read .idx::after { content:" \u00b7 \u5df2\u8bfb"; font-size:10px; letter-spacing:1px; opacity:.7; }')
    if 'box-shadow:0 1px 0 rgba(0,0,0,.02); }' in c:
        c = c.replace('box-shadow:0 1px 0 rgba(0,0,0,.02); }', 'box-shadow:0 2px 8px rgba(0,0,0,.04); }', 1)
    c = c.replace('color:var(--red); opacity:.06; user-select:none', 'color:var(--red); opacity:.04; user-select:none')
    c = c.replace(
      '.reveal { opacity:0; transform:translateY(16px); transition:opacity .6s ease, transform .6s ease; }\n  .reveal.in { opacity:1; transform:none; }',
      '.reveal { opacity:1; transform:none; transition:opacity .45s ease, transform .45s ease; }\n  .reveal.js-animate { opacity:0; transform:translateY(12px); }\n  .reveal.in { opacity:1; transform:none; }')
    c = c.replace(
      '#pbar, #toc-btn, #toc-panel, #totop, .wm, .hlink, #fltbar, .fltnone, .fltstat, #q { display:none !important; }',
      '#pbar, #toc-btn, #toc-panel, #totop, .wm, .hlink, #fltbar, .fltnone, .fltstat, #q, #imm-btn, #skip, #imm-chip { display:none !important; }')
    c = c.replace(
      '#pbar, #toc-btn, #toc-panel, #totop, .wm, .hlink, #fltbar, .fltnone, .fltstat, #q, #imm-btn { display:none !important; }',
      '#pbar, #toc-btn, #toc-panel, #totop, .wm, .hlink, #fltbar, .fltnone, .fltstat, #q, #imm-btn, #skip, #imm-chip { display:none !important; }')

    extra_css = """
  /* ---- ux-all: skip / layout / immersive chip / view groups ---- */
  #skip { position:absolute; left:-999px; top:8px; z-index:2000; background:var(--red); color:#fff; padding:8px 14px; border-radius:8px; font-size:13px; text-decoration:none; font-weight:600; }
  #skip:focus { left:12px; outline:2px solid var(--red); outline-offset:2px; }
  .fltbar { margin-bottom:12px; }
  .viewbar { margin-top:4px; padding-top:12px; border-top:1px solid var(--line); }
  .viewbar .vsep { width:1px; height:16px; background:var(--line); margin:0 6px; }
  #imm-chip { position:fixed; top:10px; left:50%; transform:translateX(-50%); z-index:1300; font-family:"IBM Plex Mono",Consolas,monospace; font-size:11px; letter-spacing:1.5px; color:var(--red); background:rgba(255,255,255,.92); border:1px solid var(--line); border-radius:99px; padding:4px 12px; box-shadow:0 2px 10px rgba(0,0,0,.08); display:none; max-width:80vw; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
  body.immersive #imm-chip { display:block; }
  body.immersive #imm-chip:hover { background:#fff; }
  @media (prefers-reduced-motion: reduce) {
    .chip:hover, .vbtn:hover, #imm-btn:hover { transform:none; }
    .reveal.js-animate { opacity:1; transform:none; transition:none; }
  }
"""
    if '#skip {' not in c:
        marker = '  #imm-btn:focus-visible { outline:2px solid var(--red); outline-offset:2px; }'
        if marker in c:
            c = c.replace(marker, marker + '\n' + extra_css)
        else:
            head_end = c.find('</head>')
            style_end = c.rfind('</style>', 0, head_end)
            c = c[:style_end] + extra_css + '\n' + c[style_end:]

    if 'id="skip"' not in c:
        if '<body>\n<div class="wrap">' in c:
            c = c.replace('<body>\n<div class="wrap">', '<body>\n<a id="skip" href="#sec-papers">\u8df3\u5230\u8bba\u6587\u5217\u8868</a>\n<div class="wrap" id="top">')
        else:
            c = c.replace('<body>', '<body>\n<a id="skip" href="#sec-papers">\u8df3\u5230\u8bba\u6587\u5217\u8868</a>', 1)

    if 'id="sec-papers"' not in c:
        c2 = re.sub(r'(<h2[^>]*>)(\s*<span class="secno">[^<]*</span>\s*\u8bba\u6587\u5217\u8868)', r'<h2 id="sec-papers">\2', c, count=1)
        if c2 != c:
            c = c2
        elif '>\u8bba\u6587\u5217\u8868</h2>' in c:
            c = c.replace('>\u8bba\u6587\u5217\u8868</h2>', ' id="sec-papers">\u8bba\u6587\u5217\u8868</h2>', 1)

    if 'id="imm-chip"' not in c:
        c = c.replace('<body>', '<body>\n<div id="imm-chip" aria-live="polite">\u6c89\u6d8e\u9605\u8bfb \u00b7 \u6309 I \u9000\u51fa</div>', 1)

    old_vb = '<div class="viewbar" id="viewbar" role="group" aria-label="\u5207\u6362\u89c6\u56fe"><button type="button" class="vbtn on" data-view="list">\u5217\u8868</button><button type="button" class="vbtn" data-view="gallery">\u753b\u5eca</button><button type="button" class="vbtn" data-view="star">\u661f\u56fe</button><button type="button" id="imm-btn" title="\u9690\u85cf\u6d6e\u52a8\u63a7\u4ef6\uff0c\u4e13\u6ce8\u9605\u8bfb (I)" aria-pressed="false">\u6c89\u6d8e</button><span class="vhint" id="vhint">\u5c55\u793a\u6a21\u5f0f \u00b7 \u5217\u8868</span><span class="vhint" id="vhint-r">\u5df2\u8bfb 0 / 11</span></div>'
    new_vb = '<div class="viewbar" id="viewbar" role="group" aria-label="\u5207\u6362\u89c6\u56fe"><button type="button" class="vbtn on" data-view="list">\u5217\u8868</button><button type="button" class="vbtn" data-view="gallery">\u753b\u5eca</button><button type="button" class="vbtn" data-view="star">\u661f\u56fe</button><span class="vsep" aria-hidden="true"></span><button type="button" id="imm-btn" title="\u9690\u85cf\u6d6e\u52a8\u63a7\u4ef6\uff0c\u4e13\u6ce8\u9605\u8bfb (I)" aria-pressed="false">\u6c89\u6d8e</button><span class="vhint" id="vhint">\u5217\u8868\uff1a\u5feb\u901f\u626b\u8bfb\u6458\u8981</span><span class="vhint" id="vhint-r">\u5df2\u8bfb 0 / 11</span></div>'
    if old_vb in c:
        c = c.replace(old_vb, new_vb)

    extra_js = r"""
<script>
/* ---- ux-all: URL state / reveal / read marks / view hints / imm chip ---- */
(function () {
  var VIEW_HINTS = {
    list: '\u5217\u8868\uff1a\u5feb\u901f\u626b\u8bfb\u6458\u8981',
    gallery: '\u753b\u5eca\uff1a\u5c01\u9762\u6d4f\u89c8\u4e0e\u5bf9\u6bd4',
    star: '\u661f\u56fe\uff1a\u4e3b\u9898\u5173\u7cfb\u4e00\u89c8'
  };
  function setParam(key, val) {
    try {
      var u = new URL(location.href);
      if (val == null || val === '' || val === 'list' || val === 'all') u.searchParams.delete(key);
      else u.searchParams.set(key, val);
      history.replaceState(null, '', u.pathname + u.search + u.hash);
    } catch (e) {}
  }
  var vhint = document.getElementById('vhint');
  document.querySelectorAll('.vbtn[data-view]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var v = btn.getAttribute('data-view') || 'list';
      if (vhint && VIEW_HINTS[v]) vhint.textContent = VIEW_HINTS[v];
      setParam('view', v === 'list' ? null : v);
    });
  });
  try {
    var sp = new URLSearchParams(location.search);
    var urlView = sp.get('view');
    if (urlView && document.querySelector('.vbtn[data-view="' + urlView + '"]')) {
      var vb = document.querySelector('.vbtn[data-view="' + urlView + '"]');
      if (vb) vb.click();
    }
    if (sp.get('immersive') === '1') {
      try { localStorage.setItem('ma-immersive', '1'); } catch (e) {}
    }
  } catch (e) {}
  var immBtn = document.getElementById('imm-btn');
  var immChip = document.getElementById('imm-chip');
  if (immBtn) {
    var obs = new MutationObserver(function () {
      var on = document.body.classList.contains('immersive');
      setParam('immersive', on ? '1' : null);
      if (immChip) {
        var active = document.querySelector('#toc-panel a.active');
        immChip.textContent = on
          ? ('\u6c89\u6d8e\u9605\u8bfb' + (active ? ' \u00b7 ' + active.textContent.trim() : '') + ' \u00b7 \u6309 I \u9000\u51fa')
          : '\u6c89\u6d8e\u9605\u8bfb \u00b7 \u6309 I \u9000\u51fa';
      }
    });
    obs.observe(document.body, { attributes: true, attributeFilter: ['class'] });
    if (immChip) {
      immChip.style.cursor = 'pointer';
      immChip.addEventListener('click', function () { immBtn.click(); });
    }
  }
  function markRead() {
    try {
      var raw = localStorage.getItem('ma-read') || localStorage.getItem('readPapers') || '[]';
      var arr = JSON.parse(raw);
      if (!Array.isArray(arr)) return;
      document.querySelectorAll('.paper').forEach(function (el) {
        var id = el.getAttribute('data-id') || el.getAttribute('data-slug') || '';
        var link = el.querySelector('h3 a');
        var href = link ? (link.getAttribute('href') || '') : '';
        var hit = arr.some(function (x) {
          return x === id || (href && (x === href || href.indexOf(String(x)) !== -1));
        });
        if (hit) el.classList.add('is-read');
      });
    } catch (e) {}
  }
  markRead();
  window.addEventListener('storage', markRead);
  function setupReveal() {
    var nodes = document.querySelectorAll('.reveal');
    if (!nodes.length) return;
    var vh = window.innerHeight || 800;
    nodes.forEach(function (el) {
      var rect = el.getBoundingClientRect();
      if (rect.top < vh * 0.92) el.classList.add('in');
      else el.classList.add('js-animate');
    });
    if (!('IntersectionObserver' in window)) {
      nodes.forEach(function (el) { el.classList.add('in'); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          en.target.classList.add('in');
          en.target.classList.remove('js-animate');
          io.unobserve(en.target);
        }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    nodes.forEach(function (el) {
      if (!el.classList.contains('in')) io.observe(el);
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', setupReveal);
  else setupReveal();
})();
</script>
"""
    if 'ux-all: URL state' not in c:
        c = c.replace('</body>', extra_js + '\n</body>', 1)

    p.write_text(c, encoding='utf-8')
    print('applied OK ->', p.resolve())
    return 0

if __name__ == '__main__':
    sys.exit(main())
