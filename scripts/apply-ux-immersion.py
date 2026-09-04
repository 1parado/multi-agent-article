#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Apply immersion mode + micro-feedback to index.html.

Usage (from repo root):
  python3 scripts/apply-ux-immersion.py
"""
from __future__ import print_function
import sys
from pathlib import Path

def main():
    # Allow running from repo root or scripts/
    candidates = [
        Path('index.html'),
        Path(__file__).resolve().parent.parent / 'index.html',
    ]
    p = None
    for cand in candidates:
        if cand.is_file():
            p = cand
            break
    if p is None:
        print('ERROR: index.html not found.', file=sys.stderr)
        print('Please run from the repo root:', file=sys.stderr)
        print('  cd /path/to/multi-agent-article', file=sys.stderr)
        print('  python3 scripts/apply-ux-immersion.py', file=sys.stderr)
        return 1

    try:
        c = p.read_text(encoding='utf-8')
    except Exception as e:
        print('ERROR: cannot read %s: %s' % (p, e), file=sys.stderr)
        return 1

    if 'id="imm-btn"' in c:
        print('already applied (imm-btn present in %s)' % p)
        return 0

    replacements = [
        (
            '.chip { font-family:"IBM Plex Mono",Consolas,monospace; font-size:11px; letter-spacing:1.2px; color:var(--gray); background:#fff; border:1px solid var(--line); border-radius:99px; padding:4px 12px; cursor:pointer; transition:color .2s, border-color .2s, box-shadow .2s, background .2s; }',
            '.chip { font-family:"IBM Plex Mono",Consolas,monospace; font-size:11px; letter-spacing:1.2px; color:var(--gray); background:#fff; border:1px solid var(--line); border-radius:99px; padding:4px 12px; cursor:pointer; transition:color .2s, border-color .2s, box-shadow .2s, background .2s, transform .15s; }',
            'chip transition',
        ),
        (
            '.chip:hover { color:var(--ink); border-color:var(--cat,var(--red)); }',
            '.chip:hover { color:var(--ink); border-color:var(--cat,var(--red)); transform:translateY(-1px); }',
            'chip hover',
        ),
        (
            '.vbtn { font-family:"IBM Plex Mono",Consolas,monospace; font-size:11.5px; letter-spacing:1.5px; color:var(--gray); background:#fff; border:1px solid var(--line); border-radius:99px; padding:4px 14px; cursor:pointer; transition:color .2s,border-color .2s,background .2s; }',
            '.vbtn { font-family:"IBM Plex Mono",Consolas,monospace; font-size:11.5px; letter-spacing:1.5px; color:var(--gray); background:#fff; border:1px solid var(--line); border-radius:99px; padding:4px 14px; cursor:pointer; transition:color .2s,border-color .2s,background .2s, transform .15s; }',
            'vbtn transition',
        ),
        (
            '.vbtn:hover { color:var(--red); border-color:var(--red); }',
            '.vbtn:hover { color:var(--red); border-color:var(--red); transform:translateY(-1px); }',
            'vbtn hover',
        ),
    ]

    missing = []
    for old, new, label in replacements:
        if old not in c:
            missing.append(label)
        else:
            c = c.replace(old, new, 1)

    imm_css = """
  /* ---- immersion mode (ux) ---- */
  body.immersive #pbar,
  body.immersive #toc-btn,
  body.immersive #toc-panel,
  body.immersive #totop,
  body.immersive .wm { opacity:0 !important; pointer-events:none !important; visibility:hidden !important; }
  body.immersive #imm-btn { background:var(--red); color:#fff; border-color:var(--red); }
  #imm-btn { font-family:"IBM Plex Mono",Consolas,monospace; font-size:11.5px; letter-spacing:1.5px; color:var(--gray); background:#fff; border:1px solid var(--line); border-radius:99px; padding:4px 14px; cursor:pointer; transition:color .2s,border-color .2s,background .2s, transform .15s; margin-left:6px; }
  #imm-btn:hover { color:var(--red); border-color:var(--red); transform:translateY(-1px); }
  #imm-btn:focus-visible { outline:2px solid var(--red); outline-offset:2px; }
"""
    head_end = c.find('</head>')
    if head_end == -1:
        print('ERROR: </head> not found in index.html', file=sys.stderr)
        return 1
    style_end = c.rfind('</style>', 0, head_end)
    if style_end == -1:
        print('ERROR: no </style> found before </head>', file=sys.stderr)
        return 1
    c = c[:style_end] + imm_css + '\n' + c[style_end:]

    old_vb = (
        '<div class="viewbar" id="viewbar" role="group" aria-label="切换视图">'
        '<button type="button" class="vbtn on" data-view="list">列表</button>'
        '<button type="button" class="vbtn" data-view="gallery">画廊</button>'
        '<button type="button" class="vbtn" data-view="star">星图</button>'
        '<span class="vhint" id="vhint">展示模式 · 列表</span>'
        '<span class="vhint" id="vhint-r">已读 0 / 11</span></div>'
    )
    new_vb = (
        '<div class="viewbar" id="viewbar" role="group" aria-label="切换视图">'
        '<button type="button" class="vbtn on" data-view="list">列表</button>'
        '<button type="button" class="vbtn" data-view="gallery">画廊</button>'
        '<button type="button" class="vbtn" data-view="star">星图</button>'
        '<button type="button" id="imm-btn" title="隐藏浮动控件，专注阅读 (I)" aria-pressed="false">沉浸</button>'
        '<span class="vhint" id="vhint">展示模式 · 列表</span>'
        '<span class="vhint" id="vhint-r">已读 0 / 11</span></div>'
    )
    if old_vb not in c:
        print('ERROR: viewbar block not found — index.html structure may differ.', file=sys.stderr)
        print('Tip: git checkout main -- index.html && git pull', file=sys.stderr)
        return 1
    c = c.replace(old_vb, new_vb, 1)

    imm_js = """
<script>
/* ---- immersion mode (ux) ---- */
(function () {
  var KEY = 'ma-immersive';
  var btn = document.getElementById('imm-btn');
  if (!btn) return;
  function apply(on) {
    document.body.classList.toggle('immersive', !!on);
    btn.setAttribute('aria-pressed', on ? 'true' : 'false');
    btn.textContent = on ? '\u9000\u51fa\u6c89\u6d8e' : '\u6c89\u6d8e';
    try { localStorage.setItem(KEY, on ? '1' : '0'); } catch (e) {}
  }
  var saved = false;
  try { saved = localStorage.getItem(KEY) === '1'; } catch (e) {}
  apply(saved);
  btn.addEventListener('click', function () {
    apply(!document.body.classList.contains('immersive'));
  });
  document.addEventListener('keydown', function (e) {
    if (e.target && (/INPUT|TEXTAREA|SELECT/.test(e.target.tagName) || e.target.isContentEditable)) return;
    if ((e.key === 'i' || e.key === 'I') && !e.metaKey && !e.ctrlKey && !e.altKey) {
      e.preventDefault();
      apply(!document.body.classList.contains('immersive'));
    }
  });
})();
</script>
"""
    if '</body>' not in c:
        print('ERROR: </body> not found', file=sys.stderr)
        return 1
    c = c.replace('</body>', imm_js + '\n</body>', 1)

    try:
        p.write_text(c, encoding='utf-8')
    except Exception as e:
        print('ERROR: cannot write %s: %s' % (p, e), file=sys.stderr)
        return 1

    if missing:
        print('WARN: some CSS patterns were already different: %s' % ', '.join(missing))
    print('applied OK -> %s' % p.resolve())
    print('Next:')
    print('  git add index.html')
    print('  git commit -m "feat(ux): immersion mode + micro-feedback on index"')
    print('  git push origin main')
    return 0

if __name__ == '__main__':
    sys.exit(main())
