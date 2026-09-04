# Interaction Polish Improvements

## 已实现方案（index.html）

1. **阅读沉浸模式**
   - 新增「沉浸」按钮（viewbar）
   - 隐藏进度条、TOC、返回顶部、水印
   - 快捷键 `I` 切换
   - localStorage 记住偏好

2. **微反馈强化**
   - chip / view 按钮 hover 上移与过渡

## 实现片段

### CSS（加入 v6 style 块）
```css
body.immersive #pbar,
body.immersive #toc-btn,
body.immersive #toc-panel,
body.immersive #totop,
body.immersive .wm {
  opacity: 0 !important;
  pointer-events: none !important;
  visibility: hidden !important;
}
body.immersive #imm-btn {
  background: var(--red);
  color: #fff;
  border-color: var(--red);
}
#imm-btn {
  font-family: "IBM Plex Mono", Consolas, monospace;
  font-size: 11.5px;
  letter-spacing: 1.5px;
  color: var(--gray);
  background: #fff;
  border: 1px solid var(--line);
  border-radius: 99px;
  padding: 4px 14px;
  cursor: pointer;
  transition: color .2s, border-color .2s, background .2s, transform .15s;
  margin-left: 6px;
}
#imm-btn:hover {
  color: var(--red);
  border-color: var(--red);
  transform: translateY(-1px);
}
```

### HTML（viewbar 内）
```html
<button type="button" id="imm-btn" title="隐藏浮动控件，专注阅读 (I)">沉浸</button>
```

### JS（</body> 前）
```js
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
    if (e.target && (/INPUT|TEXTAREA/.test(e.target.tagName) || e.target.isContentEditable)) return;
    if ((e.key === 'i' || e.key === 'I') && !e.metaKey && !e.ctrlKey && !e.altKey) {
      e.preventDefault();
      apply(!document.body.classList.contains('immersive'));
    }
  });
})();
```

## 后续

- 筛选 / 视图状态 URL 记忆
- 已读列表导出/导入
- 论文页同样支持沉浸模式

纯静态、无后端。
