#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Apply visual contrast & polish to index.html (idempotent)."""
from pathlib import Path
import sys

def main():
    candidates = [Path('index.html'), Path(__file__).resolve().parent.parent / 'index.html']
    p = next((c for c in candidates if c.is_file()), None)
    if not p:
        print('ERROR: index.html not found', file=sys.stderr)
        return 1
    c = p.read_text(encoding='utf-8')
    if '#5f5f5b' in c and 'line-height:1.85' in c and 'box-shadow:0 2px 12px' in c:
        print('already applied')
        return 0
    reps = [
        (':root { --red:#A02C2C; --sage:#C9CBC0; --ink:#1a1a1a; --gray:#3d3d3d; --soft:#8a8a86; --line:#e6e4e0; }',
         ':root { --red:#A02C2C; --sage:#C9CBC0; --ink:#1a1a1a; --gray:#333333; --soft:#5f5f5b; --line:#e6e4e0; }'),
        ('.intro { color:var(--gray); margin:6px 0 0; }',
         '.intro { color:var(--gray); margin:6px 0 0; line-height:1.85; }'),
        ('.paper:hover { background:#faf8f6; border-left-color:var(--cat,var(--red)); }',
         '.paper:hover { background:#faf8f6; border-left-color:var(--cat,var(--red)); box-shadow:0 2px 12px rgba(0,0,0,.04); }'),
        ('box-shadow:0 1px 0 rgba(0,0,0,.02); }',
         'box-shadow:0 2px 8px rgba(0,0,0,.04); }'),
        ('color:var(--red); opacity:.06; user-select:none',
         'color:var(--red); opacity:.04; user-select:none'),
        ('#pbar, #toc-btn, #toc-panel, #totop, .wm, .hlink, #fltbar, .fltnone, .fltstat, #q { display:none !important; }',
         '#pbar, #toc-btn, #toc-panel, #totop, .wm, .hlink, #fltbar, .fltnone, .fltstat, #q, #imm-btn { display:none !important; }'),
    ]
    for old, new in reps:
        if old in c:
            c = c.replace(old, new, 1)
    rm = """
  @media (prefers-reduced-motion: reduce) {
    .chip:hover, .vbtn:hover, #imm-btn:hover { transform:none; }
  }
"""
    marker = '  #imm-btn:focus-visible { outline:2px solid var(--red); outline-offset:2px; }'
    if marker in c and '.chip:hover, .vbtn:hover, #imm-btn:hover { transform:none; }' not in c:
        c = c.replace(marker, marker + '\n' + rm)
    p.write_text(c, encoding='utf-8')
    print('applied OK ->', p.resolve())
    return 0

if __name__ == '__main__':
    sys.exit(main())
