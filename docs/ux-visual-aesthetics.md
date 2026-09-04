# Visual Aesthetics Improvements

## 已实现（index.html）

1. **对比度提升**
   - `--soft`: `#8a8a86` → `#5f5f5b`
   - `--gray`: `#3d3d3d` → `#333333`

2. **微反馈**
   - chip / view 按钮 hover 轻微上移

3. **卡片质感**
   - 画廊与列表 hover 阴影加强

## 参考 CSS 片段

```css
/* UX Visual Improvements (index) */
:root {
  --red: #A02C2C;
  --sage: #C9CBC0;
  --ink: #1a1a1a;
  --gray: #333333;   /* was #3d3d3d */
  --soft: #5f5f5b;   /* was #8a8a86 — higher contrast */
  --line: #e6e4e0;
}
.intro { line-height: 1.85; }
.chip, .vbtn { transition: color .2s, border-color .2s, box-shadow .2s, background .2s, transform .15s; }
.chip:hover, .vbtn:hover { transform: translateY(-1px); }
.paper:hover { box-shadow: 0 2px 12px rgba(0,0,0,.04); }
.gallery a { box-shadow: 0 2px 8px rgba(0,0,0,.04); }
```

## 后续

- 同步到全部论文页、about、glossary
- 暗色模式
- 打印样式

纯静态、无后端。
