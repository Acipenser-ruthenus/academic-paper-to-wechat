from __future__ import annotations

import os
import shutil
from pathlib import Path


def find_pdftoppm() -> str:
    configured = os.environ.get("PDFTOPPM")
    if configured and Path(configured).is_file():
        return configured

    discovered = shutil.which("pdftoppm")
    if discovered:
        return discovered

    home = Path.home()
    candidates = [
        home / ".cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/Library/bin/pdftoppm.exe",
        Path("C:/Program Files/poppler/Library/bin/pdftoppm.exe"),
        Path("C:/Program Files/poppler/bin/pdftoppm.exe"),
    ]
    for candidate in candidates:
        if candidate.is_file():
            return str(candidate)

    raise FileNotFoundError(
        "pdftoppm was not found. Install Poppler and add it to PATH, or set "
        "the PDFTOPPM environment variable to the executable path."
    )
