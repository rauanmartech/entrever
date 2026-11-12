"""Prepare the approved Entrever images for the static site."""

from pathlib import Path
from PIL import Image, ImageOps


BRAND_ROOT = Path(__file__).resolve().parents[1]
SITE_ROOT = BRAND_ROOT / "site"
OUTPUT = SITE_ROOT / "assets" / "images"
OUTPUT.mkdir(parents=True, exist_ok=True)


def webp(source: Path, destination: str, *, width: int | None = None, quality: int = 82, lossless: bool = False) -> None:
    with Image.open(source) as image:
        image.load()
        if width and image.width > width:
            height = round(image.height * width / image.width)
            image = image.resize((width, height), Image.Resampling.LANCZOS)
        image.save(OUTPUT / destination, "WEBP", quality=quality, method=6, lossless=lossless)


logo_source = BRAND_ROOT / "identidade" / "gerada-v2" / "entrever-colorida.png"
with Image.open(logo_source) as logo:
    logo.load()
    logo = logo.convert("RGBA")
    mark = logo.crop((160, 215, 470, 550))
    square = Image.new("RGBA", (360, 360), (0, 0, 0, 0))
    square.alpha_composite(mark, ((360 - mark.width) // 2, (360 - mark.height) // 2))
    square = square.resize((128, 128), Image.Resampling.LANCZOS)
    square.save(OUTPUT / "favicon.webp", "WEBP", lossless=True, method=6)
    bounds = logo.getchannel("A").getbbox()
    if bounds is None:
        raise ValueError("A logo está vazia")
    logo = ImageOps.expand(logo.crop(bounds), border=24, fill=(0, 0, 0, 0))
    logo.thumbnail((1100, 1100), Image.Resampling.LANCZOS)
    logo.save(OUTPUT / "entrever-logo.webp", "WEBP", lossless=True, method=6)
    light_logo = Image.new("RGBA", logo.size, (242, 232, 223, 0))
    light_logo.putalpha(logo.getchannel("A"))
    light_logo.save(OUTPUT / "entrever-logo-clara.webp", "WEBP", lossless=True, method=6)

webp(BRAND_ROOT / "identidade" / "origemdev-logo-fonte.webp", "origemdev-logo.webp", width=480, quality=84)

webp(BRAND_ROOT / "imagens" / "hero" / "hero-fotografo-v1.png", "hero-fotografo.webp", quality=84)
webp(BRAND_ROOT / "imagens" / "sobre" / "fotografo-sobre-v1.png", "sobre-fotografo.webp", quality=83)

for category in ("formatura", "casamento", "newborn"):
    webp(BRAND_ROOT / "imagens" / "cards" / f"{category}.png", f"card-{category}.webp", width=640, quality=82)

for category in ("casamento", "formatura", "newborn", "filmes"):
    webp(BRAND_ROOT / "imagens" / "trabalhos" / f"{category}.png", f"trabalho-{category}.webp", width=960, quality=84)

for subject in ("conversa", "naturalidade", "atencao", "narrativa", "edicao", "entrega"):
    webp(BRAND_ROOT / "imagens" / "diferenciais" / f"{subject}.png", f"vantagem-{subject}.webp", width=600, quality=82)

webp(BRAND_ROOT / "imagens" / "diferenciais" / "proposta.png", "vantagem-proposta.webp", width=1000, quality=84)

for output in sorted(OUTPUT.glob("*.webp")):
    print(f"{output.name}: {output.stat().st_size / 1024:.0f} KB")
