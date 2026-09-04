# Visual Aesthetics Improvements

## 已落地（index.html）

1. **对比度**
   - `--soft`: `#8a8a86` → `#5f5f5b`
   - `--gray`: `#3d3d3d` → `#333333`

2. **节奏**
   - `.intro` 增加 `line-height: 1.85`

3. **卡片质感**
   - `.paper:hover` 轻阴影
   - `.gallery a` 默认阴影加强

4. **装饰克制**
   - 水印 `opacity: .06` → `.04`

5. **无障碍**
   - `prefers-reduced-motion` 下关闭 chip/vbtn/imm 的 translate 动效

6. **打印**
   - 隐藏 `#imm-btn`

## 已落地（交互，此前）

- 沉浸模式（按钮 + 快捷键 `I` + localStorage）
- chip / vbtn 微反馈

## 后续可选

- 同步对比度变量到论文页 / about / glossary
- 暗色模式
