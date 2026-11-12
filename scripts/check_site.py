"""Check the files that will be published from site/ before deploying."""

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import json
import re


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
errors: list[str] = []


def local_file(page: Path, reference: str) -> Path | None:
    parsed = urlsplit(reference)
    if parsed.scheme or parsed.netloc or reference.startswith(("#", "//")):
        return None
    path = unquote(parsed.path)
    target = SITE / path.lstrip("/") if path.startswith("/") else page.parent / path
    return target / "index.html" if path.endswith("/") else target


class PageParser(HTMLParser):
    def __init__(self, page: Path) -> None:
        super().__init__()
        self.page = page
        self.ids: set[str] = set()
        self.anchors: list[str] = []

    def handle_starttag(self, tag: str, attributes: list[tuple[str, str | None]]) -> None:
        attrs = dict(attributes)
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        if tag == "a" and (attrs.get("href") or "").startswith("#"):
            self.anchors.append(attrs["href"][1:])
        if tag == "img":
            if not all(key in attrs for key in ("alt", "width", "height")):
                errors.append(f"{self.page}: imagem sem alt ou dimensões: {attrs.get('src')}")
            if not (attrs.get("src") or "").endswith(".webp"):
                errors.append(f"{self.page}: imagem fora de WebP: {attrs.get('src')}")
        for key in ("src", "href"):
            reference = attrs.get(key)
            if not reference:
                continue
            target = local_file(self.page, reference)
            if target is not None and not target.is_file():
                errors.append(f"{self.page}: arquivo ausente: {reference}")


for page in SITE.glob("*.html"):
    parser = PageParser(page)
    parser.feed(page.read_text(encoding="utf-8"))
    for anchor in parser.anchors:
        if anchor and anchor not in parser.ids:
            errors.append(f"{page}: âncora ausente: #{anchor}")

for stylesheet in (SITE / "assets" / "css").glob("*.css"):
    css = stylesheet.read_text(encoding="utf-8")
    for reference in re.findall(r"url\(\s*['\"]?([^)'\"]+)", css):
        target = local_file(stylesheet, reference.strip())
        if target is not None and not target.is_file():
            errors.append(f"{stylesheet}: arquivo ausente: {reference}")

config = json.loads((ROOT / "vercel.json").read_text(encoding="utf-8"))
if config.get("outputDirectory") != "site":
    errors.append("vercel.json: outputDirectory deve apontar para site")
if not (SITE / "index.html").is_file():
    errors.append("site/index.html ausente")

if errors:
    print("\n".join(errors))
    raise SystemExit(1)

print("Site pronto: páginas, âncoras, imagens, fontes e configuração encontrados.")
