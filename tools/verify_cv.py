from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CV_FILES = {
    "en": ROOT / "CV_EN.md",
    "es": ROOT / "CV_ES.md",
    "he": ROOT / "CV_HE.md",
}
REQUIRED_COMMON = (
    "Kevin Cusnir",
    "Lirioth Teltanion",
    "kevincusnir@gmail.com",
    "https://github.com/LiriothTeltanion",
    "https://www.linkedin.com/in/kevin-cusnir-883173b4/",
    "Nova Music Lab",
    "Ivrit Sheli 2.2.0",
    "NovaFit 4.2.0",
    "Christopher Rodríguez Portfolio",
    "139",
    "48",
    "187",
    "OAuth",
    "2025–2026",
)
STALE_IVRIT_MARKERS = ("Ivrit Sheli 2.1.0", "127 automated tests", "127 pruebas", "127 בדיקות")


def fail(message: str) -> None:
    print(f"[FAIL] {message}")
    raise SystemExit(1)


def load(path: Path) -> str:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        fail(f"Cannot read {path.relative_to(ROOT)} as UTF-8: {error}")
    if not text.strip():
        fail(f"{path.relative_to(ROOT)} is empty")
    return text


def main() -> int:
    version = load(ROOT / "VERSION").strip()
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        fail("VERSION must use semantic x.y.z format")

    readme = load(ROOT / "README.md")
    changelog = load(ROOT / "CHANGELOG.md")
    if f"`{version}`" not in readme or f"## {version} —" not in changelog:
        fail("README or CHANGELOG does not match VERSION")
    if readme.count("# 📄 Kevin Cusnir — Multilingual Professional CV") != 1:
        fail("README must contain exactly one canonical title")

    texts = {language: load(path) for language, path in CV_FILES.items()}
    for language, text in texts.items():
        for marker in REQUIRED_COMMON:
            if marker not in text:
                fail(f"{CV_FILES[language].name} is missing {marker!r}")
        for stale in STALE_IVRIT_MARKERS:
            if stale in text:
                fail(f"{CV_FILES[language].name} contains stale Ivrit evidence {stale!r}")
        if text.count("\n# "):
            fail(f"{CV_FILES[language].name} contains more than one top-level title")

    language_markers = {
        "en": ("Junior Frontend & Full-Stack Developer", "In progress", "not claimed", "under end-to-end verification"),
        "es": ("Frontend y Full-Stack Junior", "En progreso", "No se afirma", "pendiente de verificación integral"),
        "he": ("Full-Stack ג׳וניור", "בתהליך", "אין כאן טענה", "ממתינה לאימות מקצה לקצה"),
    }
    for language, markers in language_markers.items():
        for marker in markers:
            if marker not in texts[language]:
                fail(f"{CV_FILES[language].name} is missing semantic boundary {marker!r}")

    if not re.search(r"[\u0590-\u05FF]", texts["he"]):
        fail("Hebrew CV contains no Hebrew text")

    print(f"[OK] CV system {version}: EN/ES/HE identity, projects, evidence and boundaries verified")
    return 0


if __name__ == "__main__":
    sys.exit(main())
