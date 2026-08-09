#!/usr/bin/env python3
"""Genera un EPUB Kindle-ready dai capitoli markdown del progetto 2076."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CAPITOLI_DIR = ROOT / "capitoli"
COVER = CAPITOLI_DIR / "copertina-2076.png"
OUTPUT = CAPITOLI_DIR / "2076-kindle.epub"
COMBINED = CAPITOLI_DIR / ".2076-kindle-source.md"


def strip_first_h1(text: str) -> str:
    """Rimuove il primo # Capitolo N se presente (lo mettiamo come title)."""
    return re.sub(r"^#\s+Capitolo\s+\d+\s*\n+", "", text.lstrip(), count=1)


def build_markdown() -> str:
    parts: list[str] = [
        "---",
        'title: "2076"',
        'author: ""',
        'lang: it-IT',
        "---",
        "",
    ]
    for i in range(1, 17):
        path = CAPITOLI_DIR / f"{i:02d}.md"
        if not path.exists():
            raise FileNotFoundError(path)
        body = strip_first_h1(path.read_text(encoding="utf-8"))
        parts.append(f"# Capitolo {i}")
        parts.append("")
        parts.append(body.rstrip())
        parts.append("")
        parts.append("")
    return "\n".join(parts)


def main() -> None:
    if not COVER.exists():
        raise FileNotFoundError(COVER)

    COMBINED.write_text(build_markdown(), encoding="utf-8")

    cmd = [
        "pandoc",
        str(COMBINED),
        "-o",
        str(OUTPUT),
        "--from=markdown",
        "--to=epub",
        f"--epub-cover-image={COVER}",
        "--toc",
        "--toc-depth=1",
        "--split-level=1",
        "--metadata",
        "title=2076",
        "--metadata",
        "lang=it-IT",
        "--css",
        str(ROOT / "scripts" / "kindle.css"),
    ]
    subprocess.run(cmd, check=True)
    COMBINED.unlink(missing_ok=True)
    print(f"Kindle EPUB creato: {OUTPUT}")

    azw3 = OUTPUT.with_suffix(".azw3")
    try:
        subprocess.run(
            ["ebook-convert", str(OUTPUT), str(azw3)],
            check=True,
            capture_output=True,
            text=True,
        )
        print(f"Kindle AZW3 creato: {azw3}")
    except (FileNotFoundError, subprocess.CalledProcessError) as exc:
        print(f"AZW3 non generato ({exc}); EPUB resta il formato Kindle principale.")


if __name__ == "__main__":
    main()
