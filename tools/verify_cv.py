from __future__ import annotations

import re
import struct
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
    "NovaFit 4.2.0",
    "Christopher Rodríguez Portfolio",
    "Google",
    "2025–2026",
)
# La version de Ivrit Sheli y sus cifras de pruebas ya no se fijan aqui. Clavar
# "Ivrit Sheli 2.2.0" dejo esta comprobacion en rojo dos dias mientras los tres
# CV decian 2.12.3, que era lo correcto: fallaba el vigilante, no el contenido.
# En su lugar se exige que los tres coincidan y que la version no este superada.
STALE_IVRIT_MARKERS = ("127 automated tests", "127 pruebas", "127 בדיקות")
IVRIT_HEADING = re.compile(r"Ivrit Sheli (\d+\.\d+\.\d+)")
SUPERSEDED_IVRIT_VERSIONS = ("2.1.0", "2.2.0", "2.4.0")
IVRIT_TEST_FIGURES = ("859", "387")
# Un despliegue retirado en un CV es un 404 delante de un reclutador. El servicio
# de Singapur se borro el 13 sep 2026 y los tres CV siguieron apuntando a el.
RETIRED_DEPLOYMENTS = ("ivrit-sheli-staging.onrender.com", "railway.app")
CV_BANNER = ROOT / "assets" / "cv-banner.svg"
SOCIAL_SVG = ROOT / "assets" / "social" / "cv-social-preview.svg"
SOCIAL_PNG = ROOT / "assets" / "social" / "cv-social-preview.png"
SOCIAL_SIZE = (1280, 640)
MAX_SOCIAL_BYTES = 1_000_000


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


def png_dimensions(path: Path) -> tuple[int, int]:
    try:
        data = path.read_bytes()
    except OSError as error:
        fail(f"Cannot read {path.relative_to(ROOT)}: {error}")
    if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        fail(f"{path.relative_to(ROOT)} is not a valid PNG with an IHDR header")
    return struct.unpack(">II", data[16:24])


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
    banner_reference = "./assets/cv-banner.svg"
    if banner_reference not in readme:
        fail("README does not reference the shared CV banner")
    for language, text in texts.items():
        if banner_reference not in text:
            fail(f"{CV_FILES[language].name} does not reference the shared CV banner")
        for marker in REQUIRED_COMMON:
            if marker not in text:
                fail(f"{CV_FILES[language].name} is missing {marker!r}")
        for stale in STALE_IVRIT_MARKERS:
            if stale in text:
                fail(f"{CV_FILES[language].name} contains stale Ivrit evidence {stale!r}")
        if len(re.findall(r"(?m)^# [^#]", text)) != 1:
            fail(f"{CV_FILES[language].name} must contain exactly one top-level title")

    versions: dict[str, str] = {}
    for language, text in texts.items():
        named = set(IVRIT_HEADING.findall(text))
        if len(named) != 1:
            fail(
                f"{CV_FILES[language].name} must name exactly one Ivrit Sheli "
                f"version, found {sorted(named)}"
            )
        versions[language] = named.pop()
    if len(set(versions.values())) != 1:
        fail(f"The three CVs disagree on the Ivrit Sheli version: {versions}")
    ivrit_version = next(iter(versions.values()))
    if ivrit_version in SUPERSEDED_IVRIT_VERSIONS:
        fail(
            f"Ivrit Sheli {ivrit_version} is superseded; the CV must state the "
            "version the project actually publishes"
        )
    for language, text in texts.items():
        for figure in IVRIT_TEST_FIGURES:
            if figure not in text:
                fail(f"{CV_FILES[language].name} is missing the {figure}-test figure")

    for label, text in (
        ("README.md", readme),
        *((CV_FILES[language].name, text) for language, text in texts.items()),
    ):
        for host in RETIRED_DEPLOYMENTS:
            if host in text:
                fail(f"{label} still points at the retired deployment {host!r}")

    language_markers = {
        # La ultima marca de cada idioma es el limite de honestidad: lo que el CV
        # reconoce que NO esta verificado. La redaccion cambio cuando Google
        # sign-in paso a operativo y solo quedo el aislamiento entre dos cuentas.
        "en": ("Junior Frontend & Full-Stack Developer", "In progress", "not claimed", "still listed as unverified"),
        "es": ("Frontend y Full-Stack Junior", "En progreso", "No se afirma", "sigue figurando como no verificado"),
        "he": ("Full-Stack ג׳וניור", "בתהליך", "אין כאן טענה", "עדיין מסומן כלא מאומת"),
    }
    for language, markers in language_markers.items():
        for marker in markers:
            if marker not in texts[language]:
                fail(f"{CV_FILES[language].name} is missing semantic boundary {marker!r}")

    if not re.search(r"[\u0590-\u05FF]", texts["he"]):
        fail("Hebrew CV contains no Hebrew text")

    banner = load(CV_BANNER)
    social_svg = load(SOCIAL_SVG)
    for path, svg in ((CV_BANNER, banner), (SOCIAL_SVG, social_svg)):
        for marker in ("Kevin Cusnir", "Lirioth Teltanion", "KC", "LT"):
            if marker not in svg:
                fail(f"{path.relative_to(ROOT)} is missing visual identity marker {marker!r}")
        if "<animate" in svg or "@keyframes" in svg:
            fail(f"{path.relative_to(ROOT)} must remain static")
        if not re.search(r"[\u0590-\u05FF]", svg):
            fail(f"{path.relative_to(ROOT)} contains no Hebrew text")

    if not SOCIAL_PNG.is_file():
        fail(f"Missing {SOCIAL_PNG.relative_to(ROOT)}")
    dimensions = png_dimensions(SOCIAL_PNG)
    if dimensions != SOCIAL_SIZE:
        fail(f"Social preview must be {SOCIAL_SIZE[0]} x {SOCIAL_SIZE[1]}, found {dimensions[0]} x {dimensions[1]}")
    if SOCIAL_PNG.stat().st_size >= MAX_SOCIAL_BYTES:
        fail(f"Social preview must stay below {MAX_SOCIAL_BYTES} bytes")

    print(
        f"[OK] CV system {version}: EN/ES/HE identity, projects, Ivrit Sheli "
        f"{ivrit_version} agreed across all three, no retired deployment, "
        f"boundaries and {dimensions[0]}x{dimensions[1]} visual assets verified"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
