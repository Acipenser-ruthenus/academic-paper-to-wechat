#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import html
import mimetypes
import re
import shutil
from pathlib import Path


IMAGE_RE = re.compile(r"^\{\{image:(.+?)\|(.+?)\}\}$", re.DOTALL)
NOTE_RE = re.compile(r"^\{\{note:(.+?)\}\}$", re.DOTALL)
META_RE = re.compile(r"^\*\*(作者|单位|邮箱|发表期刊|发表会议|引用|DOI|论文链接|项目主页)[：:]\*\*")


def parse_source(source: str) -> tuple[dict[str, str], str]:
    metadata: dict[str, str] = {}
    if not source.startswith("---\n"):
        return metadata, source
    end = source.find("\n---\n", 4)
    if end == -1:
        raise ValueError("Front matter starts with --- but has no closing ---")
    for line in source[4:end].splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            raise ValueError(f"Invalid front matter line: {line}")
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip('"').strip("'")
    return metadata, source[end + 5 :]


def inline_markdown(value: str) -> str:
    escaped = html.escape(value, quote=True)
    escaped = re.sub(r"\[([^\]]+)\]\((https?://[^\s)]+|mailto:[^\s)]+)\)", r'<a href="\2" style="color:#176b91;text-decoration:none">\1</a>', escaped)
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"(?<!\*)\*([^*]+?)\*(?!\*)", r"<em>\1</em>", escaped)
    return escaped


def image_source(path: Path, embed: bool) -> str:
    if not embed:
        return path.resolve().as_uri()
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    payload = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{payload}"


def unique_export_path(directory: Path, source: Path, used: set[str]) -> Path:
    stem = re.sub(r"[^\w.-]+", "-", source.stem, flags=re.UNICODE).strip("-.") or "image"
    suffix = source.suffix.lower() or ".bin"
    candidate = f"{stem}{suffix}"
    number = 2
    while candidate.casefold() in used:
        candidate = f"{stem}-{number}{suffix}"
        number += 1
    used.add(candidate.casefold())
    return directory / candidate


def render_blocks(markdown_text: str, base_dir: Path, embed: bool, image_dir: Path | None) -> tuple[str, list[tuple[str, str]]]:
    blocks: list[str] = []
    gallery: list[tuple[str, str]] = []
    exported_names: set[str] = set()

    for raw_block in re.split(r"\n\s*\n", markdown_text.strip()):
        block = raw_block.strip()
        if not block:
            continue

        image_match = IMAGE_RE.fullmatch(block)
        if image_match:
            raw_path, caption = image_match.groups()
            source = Path(raw_path.strip())
            if not source.is_absolute():
                source = base_dir / source
            source = source.resolve()
            if not source.is_file():
                raise FileNotFoundError(f"Image not found: {source}")
            src = image_source(source, embed)
            caption_html = inline_markdown(caption.strip())
            blocks.append(
                '<section style="margin:24px 0;text-align:center">'
                f'<img alt="{html.escape(caption.strip(), quote=True)}" src="{src}" '
                'style="display:block;max-width:100%;height:auto;margin:0 auto"/>'
                f'<p style="font-size:13px;color:#777;line-height:1.6;margin:9px 0 0;text-align:center;text-indent:0">{caption_html}</p>'
                '</section>'
            )
            gallery.append((src, caption.strip()))
            if image_dir is not None:
                destination = unique_export_path(image_dir, source, exported_names)
                shutil.copy2(source, destination)
            continue

        note_match = NOTE_RE.fullmatch(block)
        if note_match:
            blocks.append(
                '<section style="border-left:3px solid #ddd;padding:9px 10px;margin:16px 0 14px;'
                'font-size:14px;line-height:1.6;font-style:italic;text-align:left">'
                f'{inline_markdown(note_match.group(1).strip())}</section>'
            )
            continue

        heading = re.match(r"^(#{1,3})\s+(.+)$", block, re.DOTALL)
        if heading:
            level = len(heading.group(1))
            styles = {
                1: "font-size:20px;font-weight:700;line-height:1.5;color:var(--accent);text-align:center;letter-spacing:.5px;margin:18px 0 30px;overflow-wrap:anywhere",
                2: "font-size:18px;font-weight:400;line-height:1.6;color:var(--accent);text-align:center;border-top:1px solid #f2f2f2;padding-top:13px;margin:16px 0 12px",
                3: "font-size:16px;font-weight:700;line-height:1.7;color:var(--accent);text-align:left;margin:22px 0 12px",
            }
            blocks.append(f'<h{level} style="{styles[level]}">{inline_markdown(heading.group(2).strip())}</h{level}>')
            continue

        lines = block.splitlines()
        if all(line.lstrip().startswith("- ") for line in lines):
            items = "".join(f'<li style="margin:8px 0">{inline_markdown(line.lstrip()[2:].strip())}</li>' for line in lines)
            blocks.append(f'<ul style="padding-left:28px;font-size:14px;line-height:1.8;margin:14px 0">{items}</ul>')
            continue

        content = "<br/>".join(inline_markdown(line.strip()) for line in lines)
        metadata_style = bool(META_RE.match(block))
        style = "font-size:14px;letter-spacing:.5px;line-height:1.8;text-align:left;overflow-wrap:anywhere"
        if metadata_style:
            style += ";text-indent:0;margin:8px 0"
        else:
            style += ";text-indent:2em;text-align:justify;margin:0 0 14px"
        blocks.append(f'<p style="{style}">{content}</p>')

    return "\n".join(blocks), gallery


def build_html(article: str, gallery: list[tuple[str, str]], title: str, accent: str, width: int) -> str:
    gallery_html = "".join(
        f'<a download="image-{index:02d}" href="{src}" style="display:block;margin:9px 0;color:#176b91">保存：{html.escape(caption)}</a>'
        for index, (src, caption) in enumerate(gallery, start=1)
    )
    return f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)}</title>
<style>:root{{--accent:{html.escape(accent)}}}body{{margin:0;background:#edf1f4;font-family:"Microsoft YaHei","PingFang SC",sans-serif;color:#333}}.toolbar{{max-width:820px;margin:24px auto 14px;padding:20px;box-sizing:border-box;background:#fff;border-radius:10px;font-size:14px;line-height:1.8}}button{{background:#176b91;color:#fff;border:0;border-radius:5px;padding:11px 18px;margin:4px 8px 4px 0;cursor:pointer;font-size:15px}}#article{{box-sizing:border-box;max-width:{width}px;margin:0 auto;padding:18px 27px 36px;background:#fff;color:#000;font-size:14px;line-height:1.8}}#status{{color:#176b91}}details{{max-width:780px;margin:20px auto 40px;padding:20px;background:#fff}}@media(max-width:600px){{#article{{padding:26px 20px}}.toolbar{{margin:0 0 12px;border-radius:0}}}}@media print{{.toolbar,details{{display:none}}body{{background:#fff}}#article{{max-width:none;padding:0}}}}</style></head>
<body><div class="toolbar"><strong>公众号图文复制版 · 本地文件，不会自动上传或发布</strong><br/>点击“复制图文正文”后粘贴到公众号编辑器。粘贴后请等待图片上传，并逐张检查；若缺图，可从页面底部保存后补传。<br/><button id="copy">复制图文正文</button><button id="select">只选中正文</button><span id="status" role="status"></span></div>
<article id="article">{article}</article>
<details><summary>图片、公式及表格单独保存（粘贴缺图时使用）</summary>{gallery_html or '本文没有引用本地图片。'}</details>
<script>const article=document.getElementById('article'),status=document.getElementById('status');function selectArticle(){{const range=document.createRange();range.selectNodeContents(article);const selection=window.getSelection();selection.removeAllRanges();selection.addRange(range)}}document.getElementById('select').onclick=()=>{{selectArticle();status.textContent='正文已选中，请按 Ctrl+C。'}};document.getElementById('copy').onclick=async()=>{{selectArticle();try{{if(!document.execCommand('copy'))throw new Error('copy failed');status.textContent='已复制。粘贴后请检查图片上传状态。'}}catch(error){{status.textContent='已选中正文，请按 Ctrl+C 手动复制。'}}}};</script></body></html>'''


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a self-contained WeChat rich-text copy page from Markdown.")
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--article-width", type=int, default=731)
    parser.add_argument("--image-dir", type=Path)
    parser.add_argument("--no-embed", action="store_true")
    args = parser.parse_args()

    if not args.source.is_file():
        parser.error(f"Source not found: {args.source}")
    if args.article_width < 320 or args.article_width > 1200:
        parser.error("--article-width must be between 320 and 1200")
    if args.image_dir:
        args.image_dir.mkdir(parents=True, exist_ok=True)

    metadata, markdown_text = parse_source(args.source.read_text(encoding="utf-8-sig"))
    accent = metadata.get("accent-color", "#00b0f0")
    if not re.fullmatch(r"#[0-9a-fA-F]{6}", accent):
        parser.error("accent-color must be a six-digit hex color")
    title = metadata.get("browser-title", args.source.stem)
    article, gallery = render_blocks(markdown_text, args.source.parent, not args.no_embed, args.image_dir)
    if not article:
        parser.error("Source produced an empty article")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(build_html(article, gallery, title, accent, args.article_width), encoding="utf-8")
    print(f"Created {args.output.resolve()} with {len(gallery)} image(s); embedded={not args.no_embed}")


if __name__ == "__main__":
    main()
