# academic-paper-to-wechat

把学术论文 PDF 整理为中文微信公众号解读稿，并生成一个可从浏览器复制到公众号编辑器的单文件富文本 HTML。图片、公式和复杂表格可作为图片嵌入，同时导出备用素材。

## 能做什么

- 从论文建立题录与事实核对表，减少作者、单位、指标和结果误写；
- 参考既有公众号文章的内容顺序与视觉样式；
- 从 PDF 高分辨率渲染、按坐标裁剪图片、公式和表格；
- 把 Markdown 稿件生成为内联样式、图片内嵌的公众号复制页；
- 按桌面端、手机端和微信粘贴行为进行发布前检查。

## 安装为 Codex Skill

仓库地址：[Acipenser-ruthenus/academic-paper-to-wechat](https://github.com/Acipenser-ruthenus/academic-paper-to-wechat)

可以直接让 Codex 执行：

```text
请用 skill-installer 安装这个 GitHub Skill：https://github.com/Acipenser-ruthenus/academic-paper-to-wechat
```

也可以克隆仓库后，把整个 `academic-paper-to-wechat` 目录放到 Codex 的 skills 目录中。Windows 默认通常是：

```text
%USERPROFILE%\.codex\skills\academic-paper-to-wechat
```

重新打开 Codex 任务后，用下面的提示词调用：

```text
使用 $academic-paper-to-wechat，参考这篇公众号文章的格式，把这个论文 PDF 整理成可复制到微信公众号的图文稿。
```

## 脚本依赖

- `build_wechat_html.py`：仅需 Python 3.9+。
- `render_pdf.py`、`crop_pdf_regions.py`：另需 Poppler 的 `pdftoppm`。可将它加入 `PATH`，或通过 `PDFTOPPM` 环境变量指定完整路径。

脚本参数可用 `python scripts/<脚本名> --help` 查看。详细流程由 [SKILL.md](SKILL.md) 及 `references/` 中的按需说明定义。

## 隐私与版权

不要把未公开论文、作者私人邮箱、浏览器数据、访问令牌或具体项目生成稿提交到公共仓库。公开使用论文图片前，请确认论文与期刊许可。

## License

MIT
