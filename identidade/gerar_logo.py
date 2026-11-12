from pathlib import Path
from xml.sax.saxutils import escape

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont


HERE = Path(__file__).resolve().parent
FONT_PATH = Path(r"C:\Windows\Fonts\GOTHIC.TTF")
FONT = TTFont(FONT_PATH)
GLYPHS = FONT.getGlyphSet()
CMAP = FONT.getBestCmap()
ADVANCES = FONT["hmtx"].metrics
UNITS = FONT["head"].unitsPerEm

COLORS = {
    "dark": "#261D1D",
    "light": "#F2E8DF",
    "copper": "#A66B4F",
}


def outlined_text(label: str, x: float, baseline: float, size: float, tracking: float, color: str) -> str:
    scale = size / UNITS
    position = x
    parts = []
    for character in label:
        if character == " ":
            position += size * 0.36 + tracking
            continue
        glyph_name = CMAP[ord(character)]
        pen = SVGPathPen(GLYPHS)
        GLYPHS[glyph_name].draw(pen)
        path = pen.getCommands()
        if path:
            parts.append(
                f'<path d="{escape(path)}" transform="translate({position:.3f} {baseline:.3f}) '
                f'scale({scale:.6f} {-scale:.6f})" fill="{color}"/>'
            )
        position += ADVANCES[glyph_name][0] * scale + tracking
    return "\n    ".join(parts)


def svg_version(name: str) -> str:
    base = COLORS["light"] if name == "clara" else COLORS["dark"]
    right_arc = COLORS["copper"] if name == "colorida" else base
    descriptor = COLORS["copper"] if name == "colorida" else base
    title = outlined_text("entrever", 254, 119, 87, 1.2, base)
    subtitle = outlined_text("FOTOGRAFIA  E  FILMES", 259, 168, 18.5, 3.4, descriptor)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="700" height="240" viewBox="0 0 700 240" role="img" aria-labelledby="title desc">
  <title id="title">Entrever — fotografia e filmes, versão {name}</title>
  <desc id="desc">Símbolo de dois arcos que criam uma abertura central, seguido pelo nome Entrever.</desc>
  <g fill="none" stroke-linecap="round" stroke-width="6.5">
    <path d="M105 66 C82 66 70 90 70 120 C70 150 82 174 105 174" stroke="{base}"/>
    <path d="M131 66 C154 66 166 90 166 120 C166 150 154 174 131 174" stroke="{right_arc}"/>
  </g>
  <g>
    {title}
  </g>
  <g>
    {subtitle}
  </g>
</svg>
'''


for version in ("escura", "clara", "colorida"):
    (HERE / f"entrever-{version}.svg").write_text(svg_version(version), encoding="utf-8")

print("SVGs da Entrever gerados.")
