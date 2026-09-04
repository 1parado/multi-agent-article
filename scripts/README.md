# Scripts

## `apply-ux-immersion.py`
Adds immersion mode + micro-feedback to `index.html` (already applied on main).

## `apply-ux-visual.py`
Applies visual polish to `index.html`:

- higher text contrast (`--soft` / `--gray`)
- intro line-height
- paper / gallery shadows
- softer watermark
- reduced-motion safety
- print: hide immersion button

```bash
python scripts/apply-ux-visual.py   # Windows
python3 scripts/apply-ux-visual.py # macOS/Linux
```

Idempotent: safe to re-run.
