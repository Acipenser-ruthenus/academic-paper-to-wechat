# Article source format

The builder accepts UTF-8 Markdown with optional YAML-like front matter.

```markdown
---
browser-title: 示例论文公众号图文复制版
accent-color: "#00b0f0"
---

# English Paper Title

**作者：** A. Author, B. Author

**单位：** University A；University B

**邮箱：** author@example.com

**发表期刊：** Journal Name

**引用：** A. Author et al., “Paper title,” Journal, 2026.

{{note:卷期及页码请以论文正式出版信息为准。}}

## 1. 论文简介

正文段落。

{{image:figures/framework.png|图 1 方法总体框架（论文图 2）}}
```

Supported constructs are headings `#` to `###`, paragraphs, unordered lists, `**bold**`, `*italic*`, Markdown links, notes, and local images. Image paths are resolved relative to the Markdown file.

Use one image directive per paragraph: `{{image:relative/or/absolute/path.png|caption text}}`.

Use notes for publication caveats: `{{note:note text}}`.

The first `#` heading is styled as the centered English paper title. `##` headings are centered blue numbered sections. `###` headings are left-aligned blue subheadings. Paragraphs beginning with bold metadata labels such as `作者：` are left aligned without first-line indentation.

For complex source tables and equations, use image directives rather than Markdown tables. This protects alignment during WeChat rich-text paste.

Run `python scripts/build_wechat_html.py article.md output.html`. Optional flags include `--article-width 731`, `--image-dir output_images`, and `--no-embed`. Embedding is the default. `--image-dir` copies source images into a separate folder for manual WeChat uploads.
