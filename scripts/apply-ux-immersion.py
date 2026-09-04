#!/usr/bin/env python3
"""Apply immersion mode + micro-feedback to index.html (run from repo root)."""
from pathlib import Path
p = Path("index.html")
c = p.read_text(encoding="utf-8")
if 'id="imm-btn"' in c:
    print("already applied")
    raise SystemExit(0)
c = c.replace(
  '.chip { font-family:"IBM Plex Mono",Consolas,monospace; font-size:11px; letter-spacing:1.2px; color:var(--gray); background:#fff; border:1px solid var(--line); border-radius:99px; padding:4px 12px; cursor:pointer; transition:color .2s, border-color .2s, box-shadow .2s, background .2s; }',
  '.chip { font-family:"IBM Plex Mono",Consolas,monospace; font-size:11px; letter-spacing:1.2px; color:var(--gray); background:#fff; border:1px solid var(--line); border-radius:99px; padding:4px 12px; cursor:pointer; transition:color .2s, border-color .2s, box-shadow .2s, background .2s, transform .15s; }'
)
c = c.replace(
  '.chip:hover { color:var(--ink); border-color:var(--cat,var(--red)); }',
  '.chip:hover { color:var(--ink); border-color:var(--cat,var(--red)); transform:translateY(-1px); }'
)
c = c.replace(
  '.vbtn { font-family:"IBM Plex Mono",Consolas,monospace; font-size:11.5px; letter-spacing:1.5px; color:var(--gray); background:#fff; border:1px solid var(--line); border-radius:99px; padding:4px 14px; cursor:pointer; transition:color .2s,border-color .2s,background .2s; }',
  '.vbtn { font-family:"IBM Plex Mono",Consolas,monospace; font-size:11.5px; letter-spacing:1.5px; color:var(--gray); background:#fff; border:1px solid var(--line); border-radius:99px; padding:4px 14px; cursor:pointer; transition:color .2s,border-color .2s,background .2s, transform .15s; }'
)
c = c.replace(
  '.vbtn:hover { color:var(--red); border-color:var(--red); }',
  '.vbtn:hover { color:var(--red); border-color:var(--red); transform:translateY(-1px); }'
)
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
idx = c.rfind("</style>", 0, c.find("</head>"))
c = c[:idx] + imm_css + "\n" + c[idx:]
old_vb = '<div class="viewbar" id="viewbar" role="group" aria-label="切换视图"><button type="button" class="vbtn on" data-view="list">列表</button><button type="button" class="vbtn" data-view="gallery">画廊</button><button type="button" class="vbtn" data-view="star">星图</button><span class="vhint" id="vhint">展示模式 · 列表</span><span class="vhint" id="vhint-r">已读 0 / 11</span></div>'
new_vb = '<div class="viewbar" id="viewbar" role="group" aria-label="切换视图"><button type="button" class="vbtn on" data-view="list">列表</button><button type="button" class="vbtn" data-view="gallery">画廊</button><button type="button" class="vbtn" data-view="star">星图</button><button type="button" id="imm-btn" title="隐藏浮动控件，专注阅读 (I)" aria-pressed="false">沉浸</button><span class="vhint" id="vhint">展示模式 · 列表</span><span class="vhint" id="vhint-r">已读 0 / 11</span></div>'
if old_vb not in c:
    raise SystemExit("viewbar pattern not found — index.html structure changed?")
c = c.replace(old_vb, new_vb)
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
    btn.textContent = on ? '退出沉浸' : '沉浸';
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
c = c.replace("</body>", imm_js + "\n</body>")
p.write_text(c, encoding="utf-8")
print("applied OK → index.html")
