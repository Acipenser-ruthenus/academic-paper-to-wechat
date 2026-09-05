#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import subprocess
from pathlib import Path

from _poppler import find_pdftoppm


def point_to_pixel(value: float, dpi: int) -> int:
    return max(0, round(value * dpi / 72))


def main() -> None:
    parser = argparse.ArgumentParser(description="Crop named PDF regions to PNG using a JSON manifest.")
    parser.add_argument("pdf", type=Path)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()

    if not args.pdf.is_file():
        parser.error(f"PDF not found: {args.pdf}")
    if not args.manifest.is_file():
        parser.error(f"Manifest not found: {args.manifest}")

    config = json.loads(args.manifest.read_text(encoding="utf-8"))
    default_dpi = int(config.get("dpi", 240))
    regions = config.get("regions")
    if not isinstance(regions, list) or not regions:
        parser.error("manifest must contain a non-empty 'regions' list")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    executable = find_pdftoppm()
    outputs: list[Path] = []

    for index, region in enumerate(regions, start=1):
        try:
            page = int(region["page"])
            dpi = int(region.get("dpi", default_dpi))
            left, top, right, bottom = (float(value) for value in region["bbox"])
            raw_name = str(region["name"])
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError(f"Invalid region #{index}: {region}") from exc
        if page < 1 or not (72 <= dpi <= 600):
            raise ValueError(f"Invalid page or dpi in region #{index}")
        if not all(math.isfinite(value) for value in (left, top, right, bottom)):
            raise ValueError(f"Non-finite bbox in region #{index}")
        if left < 0 or top < 0 or right <= left or bottom <= top:
            raise ValueError(f"Invalid bbox in region #{index}: {region['bbox']}")

        name = Path(raw_name).name
        if name.lower().endswith(".png"):
            name = name[:-4]
        if not name or name in {".", ".."}:
            raise ValueError(f"Invalid output name in region #{index}")

        x = point_to_pixel(left, dpi)
        y = point_to_pixel(top, dpi)
        width = max(1, point_to_pixel(right - left, dpi))
        height = max(1, point_to_pixel(bottom - top, dpi))
        prefix = (args.output_dir / name).resolve()
        command = [
            executable, "-f", str(page), "-l", str(page), "-singlefile",
            "-png", "-r", str(dpi), "-x", str(x), "-y", str(y),
            "-W", str(width), "-H", str(height), str(args.pdf.resolve()), str(prefix),
        ]
        subprocess.run(command, check=True)
        outputs.append(prefix.with_suffix(".png"))

    print(f"Created {len(outputs)} crop(s) in {args.output_dir.resolve()}")


if __name__ == "__main__":
    main()
