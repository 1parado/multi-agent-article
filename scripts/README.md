# Scripts

## `apply-ux-all.py` (recommended)

One-shot reading & design polish for `index.html`:

- contrast (`--soft` / `--gray`)
- measure & line-height
- first-screen reveal fix
- skip link
- immersion chip + URL state (`?view=` / `?immersive=1`)
- view hints, read marks, shadows, watermark, print, reduced-motion

```bash
python scripts/apply-ux-all.py    # Windows
python3 scripts/apply-ux-all.py  # macOS/Linux
git add index.html && git commit -m "feat(ux): full reading/design polish" && git push
```

Idempotent.

## Older scripts

- `apply-ux-immersion.py` — immersion + micro-feedback (already on main)
- `apply-ux-visual.py` — contrast/shadow subset (superseded by `apply-ux-all.py`)
