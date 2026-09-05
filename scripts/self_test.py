#!/usr/bin/env python3
from __future__ import annotations

import base64
import subprocess
import sys
import tempfile
from pathlib import Path


def main() -> None:
    script_dir = Path(__file__).resolve().parent
    with tempfile.TemporaryDirectory(prefix="wechat-skill-test-") as temporary:
        root = Path(temporary)
        image = root / "figure.png"
        image.write_bytes(base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="))
        source = root / "article.md"
        source.write_text(
            "---\nbrowser-title: 测试复制版\naccent-color: \"#00b0f0\"\n---\n\n"
            "# Example Paper\n\n**作者：** A. Author\n\n## 1. 简介\n\n正文包含 **重点**。\n\n"
            "{{image:figure.png|图 1 测试图}}\n\n{{note:发布前核对。}}\n",
            encoding="utf-8",
        )
        output = root / "article.html"
        images = root / "images"
        subprocess.run(
            [sys.executable, str(script_dir / "build_wechat_html.py"), str(source), str(output), "--image-dir", str(images)],
            check=True,
        )
        built = output.read_text(encoding="utf-8")
        assert '<article id="article">' in built
        assert built.count("data:image/png;base64,") == 2  # article image and its download link
        assert "Example Paper" in built and "发布前核对" in built
        assert len(list(images.iterdir())) == 1
    print("Self-test passed")


if __name__ == "__main__":
    main()
