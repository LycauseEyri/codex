# Codex Blog

基于 GitHub Pages 的自动化博客系统。写 Markdown → 推送 → 自动部署。

## 目录结构

```
codex/
├── blog/
│   ├── posts/          ← 你的文章（Markdown 格式）
│   ├── templates/      ← HTML 模板
│   ├── static/         ← CSS 样式和静态资源
│   └── build.py        ← 构建脚本
├── .github/workflows/  ← GitHub Actions 自动部署
└── README.md
```

## 写文章

在 `blog/posts/` 下新建 `.md` 文件，用以下格式：

```markdown
---
title: "文章标题"
date: 2026-06-13
tags: 标签1, 标签2
---

这里是文章正文，支持完整 Markdown 语法。
```

文件名建议用 `YYYY-MM-DD-标题.md` 的格式。

## 自动部署

1. 写好文章后，`git add`、`git commit`、`git push` 到 `main` 分支
2. GitHub Actions 会自动运行 `blog/build.py`，生成静态网页
3. 部署到 GitHub Pages

## 启用 GitHub Pages

1. 在仓库页面点击 **Settings → Pages**
2. **Source** 选 **GitHub Actions**
3. 推送一次代码触发部署，几分钟后博客就上线了

## 本地预览（可选）

需要 Python 3.8+：

```bash
pip install markdown jinja2 pygments
python blog/build.py
# 用浏览器打开 _site/index.html
```

## License

MIT
