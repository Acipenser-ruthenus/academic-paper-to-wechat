#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

from _poppler import find_pdftoppm


def main() -> None:
    parser = argparse.ArgumentParser(description="Render PDF pages to high-resolution PNG files.")
    parser.add_argument("pdf", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--dpi", type=int, default=180)
    parser.add_argument("--first-page", type=int)
    parser.add_argument("--last-page", type=int)
    args = parser.parse_args()

    if not args.pdf.is_file():
        parser.error(f"PDF not found: {args.pdf}")
    if args.dpi < 72 or args.dpi > 600:
        parser.error("--dpi must be between 72 and 600")
    if args.first_page is not None and args.first_page < 1:
        parser.error("--first-page must be at least 1")
    if args.last_page is not None and args.last_page < 1:
        parser.error("--last-page must be at least 1")
    if args.first_page and args.last_page and args.first_page > args.last_page:
        parser.error("--first-page cannot exceed --last-page")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    command = [find_pdftoppm(), "-png", "-r", str(args.dpi)]
    if args.first_page is not None:
        command += ["-f", str(args.first_page)]
    if args.last_page is not None:
        command += ["-l", str(args.last_page)]
    command += [str(args.pdf.resolve()), str((args.output_dir / "page").resolve())]
    subprocess.run(command, check=True)

    pages = sorted(args.output_dir.glob("page-*.png"))
    print(f"Rendered {len(pages)} page(s) to {args.output_dir.resolve()}")


if __name__ == "__main__":
    main()
