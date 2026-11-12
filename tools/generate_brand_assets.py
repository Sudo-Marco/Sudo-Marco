from __future__ import annotations

import argparse
import base64
import io
from pathlib import Path
from xml.sax.saxutils import escape

from PIL import Image, ImageDraw, ImageFont


BASE = "#152126"
SUPPORT = "#FFD93B"
SPIKE = "#397581"
LIGHT = "#F1F2E8"
LIGHT_SURFACE = "#F8F8F0"
ASSET_ROOT = Path(__file__).resolve().parents[1] / "assets"
SOURCE = ASSET_ROOT / "source"


def read_base64(path: Path, mime: str) -> str:
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode("ascii")


def xml(text: str) -> str:
    return escape(text, {"'": "&apos;", '"': "&quot;"})


def svg(title: str, desc: str, view_box: str, body: str, styles: str = "") -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="{view_box}" role="img" aria-labelledby="title desc">
<title id="title">{xml(title)}</title><desc id="desc">{xml(desc)}</desc>
<defs><style>{styles}</style></defs>
{body}
</svg>
'''


def picture(path: str, alt: str, indent: str = "") -> str:
    return f'''{indent}<picture>
{indent}  <source media="(prefers-color-scheme: dark)" srcset="{path}-dark.svg" />
{indent}  <source media="(prefers-color-scheme: light)" srcset="{path}-light.svg" />
{indent}  <img src="{path}-light.svg" alt="{xml(alt)}" />
{indent}</picture>'''


def theme(is_dark: bool) -> tuple[str, str, str]:
    return (BASE, SUPPORT, SPIKE) if is_dark else (LIGHT, BASE, SPIKE)


def banner(is_dark: bool, idle_uri: str, happy_uri: str) -> str:
    bg, ink, accent = theme(is_dark)
    # The happy frame is exact pixel art from the approved Synapse atlas.
    # The corresponding idle frame appears before the spike in the animation.
    wave = "M 632 276 H 660 L 673 270 L 681 242 L 690 181 L 699 270 L 714 276 H 762 L 775 270 L 783 242 L 792 181 L 801 270 L 816 276 H 862 L 875 270 L 883 238 L 892 112 L 901 270 L 916 276 H 962 L 975 270 L 983 242 L 992 181 L 1001 270 L 1016 276 H 1144"
    accent_spike = "M 892 112 L 901 270"
    body = f'''
<rect width="1200" height="340" fill="{bg}" />
<path d="M 632 290 H 1144" fill="none" stroke="{ink}" stroke-opacity=".12" stroke-width="1" />
<path d="M 632 181 H 1144" fill="none" stroke="{ink}" stroke-opacity=".12" stroke-width="1" stroke-dasharray="4 9" />
<path class="trace" d="{wave}" pathLength="1000" fill="none" stroke="{ink}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" />
<path class="flow" d="{wave}" pathLength="1000" fill="none" stroke="{ink}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" />
<path class="spike" d="{accent_spike}" fill="none" stroke="{accent}" stroke-width="7" stroke-linecap="round" />
<text class="mono kicker" x="64" y="48">SUDO-MARCO  /  CIÊNCIA DA COMPUTAÇÃO</text>
<g class="copy">
  <text class="name" x="64" y="119">Marco Antônio</text>
  <text class="name" x="64" y="168">Veloso Sousa</text>
  <text class="role" x="66" y="218">Estudante · Engenharia de IA e Machine Learning</text>
  <text class="mono stack" x="66" y="257">Python  ·  NumPy  ·  Java  ·  PySide6</text>
</g>
<text class="mono axis" x="638" y="309">DISPAROS  /  LIF</text>
<text class="mono axis" x="1020" y="309">STDP</text>
<image class="bird idle" x="852" y="74" width="128" height="176" preserveAspectRatio="none" href="{idle_uri}" xlink:href="{idle_uri}" />
<image class="bird happy" x="852" y="74" width="128" height="176" preserveAspectRatio="none" href="{happy_uri}" xlink:href="{happy_uri}" />
<text class="mono threshold" x="1026" y="164">LIMIAR</text>
'''
    styles = f'''
text {{ fill: {ink}; font-family: 'Segoe UI', Arial, sans-serif; }}
.mono {{ font-family: Consolas, 'Courier New', monospace; letter-spacing: .4px; }}
.kicker,.stack,.axis,.threshold {{ font-size: 15px; }}
.name {{ font-size: 43px; font-weight: 700; }}
.role {{ font-size: 20px; }}
.axis,.threshold {{ opacity: .76; }}
.trace {{ stroke-dasharray: 1000; stroke-dashoffset: 0; }}
.flow {{ stroke-dasharray: 36 1000; animation: signal 5s linear infinite; }}
.spike {{ animation: spike 5s ease-in-out infinite; transform-box: fill-box; transform-origin: center; }}
.copy {{ animation: appear .8s ease-out both; }}
.bird {{ image-rendering: pixelated; }}
.idle {{ opacity: 1; }} .happy {{ opacity: 0; }}
.bird {{ animation: hop 5s ease-in-out infinite; transform-box: fill-box; transform-origin: center bottom; }}
.idle {{ animation-name: idle-face; animation-duration: 5s; animation-iteration-count: infinite; }}
.happy {{ animation-name: happy-face; animation-duration: 5s; animation-iteration-count: infinite; }}
@keyframes signal {{ to {{ stroke-dashoffset: -1036; }} }}
@keyframes spike {{ 0%,36%,54%,100% {{ opacity: .48; }} 42%,48% {{ opacity: 1; }} }}
@keyframes hop {{ 0%,38%,52%,100% {{ transform: translateY(0); }} 43% {{ transform: translateY(-7px); }} 48% {{ transform: translateY(-2px); }} }}
@keyframes idle-face {{ 0%,39%,52%,100% {{ opacity: 1; }} 42%,49% {{ opacity: 0; }} }}
@keyframes happy-face {{ 0%,39%,52%,100% {{ opacity: 0; }} 42%,49% {{ opacity: 1; }} }}
@keyframes appear {{ from {{ opacity: 0; transform: translateY(5px); }} to {{ opacity: 1; transform: translateY(0); }} }}
@media (prefers-reduced-motion: reduce) {{
  *,*::before,*::after {{ animation: none !important; transition: none !important; }}
  .flow {{ display: none; }} .spike {{ opacity: 1; }}
  .idle {{ opacity: 0 !important; }} .happy {{ opacity: 1 !important; }}
}}
'''
    return svg("Marco Antônio Veloso Sousa — Sudo-Marco", "Estudante de Ciência da Computação com foco em Engenharia de IA e Machine Learning. Um pintinho pixel art original reage ao trem de disparos de uma curva LIF.", "0 0 1200 340", body, styles)


def pulse_divider(is_dark: bool, with_bird: bool, happy_uri: str) -> str:
    bg, ink, accent = theme(is_dark)
    vb = "0 0 1200 92" if with_bird else "0 0 1200 44"
    y = 72 if with_bird else 22
    d = f"M 10 {y} H 80 L 95 {y-6} L 104 {y-26} L 113 {y} H 255 L 270 {y-6} L 279 {y-26} L 288 {y} H 510 L 525 {y-6} L 534 {y-26} L 543 {y} H 1120 L 1135 {y-6} L 1144 {y-26} L 1153 {y} H 1190"
    accent_d = f"M 525 {y-6} L 534 {y-26} L 543 {y}"
    bird = f'<image x="500" y="{y-87}" width="68" height="94" preserveAspectRatio="none" href="{happy_uri}" xlink:href="{happy_uri}" />' if with_bird else ""
    body = f'<rect width="1200" height="{92 if with_bird else 44}" fill="{bg}" fill-opacity="0"/><path d="{d}" fill="none" stroke="{ink}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/><path d="{accent_d}" fill="none" stroke="{accent}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>{bird}'
    return svg("Divisor em trem de pulsos", "Curva LIF estilizada em pequenos disparos; o pintinho original aparece apenas no divisor de destaque.", vb, body)


def brand_mark(is_dark: bool, size: int) -> str:
    bg, ink, accent = theme(is_dark)
    happy = read_base64(SOURCE / "piu-front-happy.png", "image/png")
    body = f'''
<rect width="100" height="100" rx="14" fill="{bg}" fill-opacity=".01"/>
<path d="M 5 84 H 24 L 32 78 L 38 59 L 44 83 H 56 L 62 30 L 69 83 H 96" fill="none" stroke="{ink}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M 62 30 L 69 83" fill="none" stroke="{accent}" stroke-width="5" stroke-linecap="round"/>
<image x="37" y="26" width="32" height="44" preserveAspectRatio="none" href="{happy}" xlink:href="{happy}"/>
'''
    return svg(f"Marca Sudo-Marco em {size}px", "Pintinho pixel art original sobreposto a uma curva LIF com um spike azul-petróleo.", "0 0 100 100", body)


def lockup(is_dark: bool, project: str | None = None) -> str:
    bg, ink, accent = theme(is_dark)
    happy = read_base64(SOURCE / "piu-front-happy.png", "image/png")
    project_line = f'<text class="project" x="190" y="110">{xml(project)}</text>' if project else '<text class="project" x="190" y="110">CIÊNCIA DA COMPUTAÇÃO  ·  ENGENHARIA DE IA E MACHINE LEARNING</text>'
    body = f'''
<rect width="1200" height="180" rx="16" fill="{bg}"/>
<path d="M 34 148 H 74 L 88 139 L 98 104 L 109 148 H 131 L 143 58 L 154 148 H 175" fill="none" stroke="{ink}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M 143 58 L 154 148" fill="none" stroke="{accent}" stroke-width="6" stroke-linecap="round"/>
<image x="105" y="26" width="48" height="66" preserveAspectRatio="none" href="{happy}" xlink:href="{happy}"/>
<text class="sudo" x="205" y="54">SUDO-MARCO</text>
<text class="name" x="202" y="102">Marco Antônio Veloso Sousa</text>
{project_line}
'''
    styles = f'''
text {{ fill:{ink}; font-family:'Segoe UI',Arial,sans-serif; }}
.sudo {{ font: 15px Consolas,'Courier New',monospace; letter-spacing:2px; }}
.name {{ font-size:32px; font-weight:700; }}
.project {{ font:15px Consolas,'Courier New',monospace; letter-spacing:.4px; }}
'''
    return svg(f"Sudo-Marco — {project or 'marca pessoal'}", "Marca pessoal com o pintinho original do Synapse Pet e a curva de potencial LIF.", "0 0 1200 180", body, styles)


def badge_row(is_dark: bool, project: str) -> str:
    bg, ink, accent = theme(is_dark)
    values = {
        "synapse": ["PYTHON 3.10+", "NUMPY", "PYSIDE6", "LIF + STDP"],
        "urna": ["JAVA 17", "SWING", "CLOUD FIRESTORE", "MODO LOCAL"],
    }[project]
    x = 16
    items = []
    for label in values:
        width = 18 + len(label) * 10
        items.append(f'<rect x="{x}" y="8" width="{width}" height="32" rx="8" fill="{ink}"/><text x="{x+width/2}" y="29" text-anchor="middle" class="badge">{xml(label)}</text>')
        x += width + 10
    body = "".join(items)
    styles = f'text {{ font: 13px Consolas,"Courier New",monospace; fill:{bg}; font-weight:700; letter-spacing:.2px; }}'
    return svg("Tecnologias do projeto", "Tecnologias descritas neste repositório, em badges locais sem widgets externos.", f"0 0 {x} 48", body, styles)


def demo_card(is_dark: bool, project: str, capture: Path, language: str = "pt") -> str:
    bg, ink, accent = theme(is_dark)
    if project == "synapse":
        # Keep the original capture untouched while embedding a compact copy.
        image = Image.open(capture).convert("RGB")
        buffer = io.BytesIO()
        image.save(buffer, format="JPEG", quality=68, optimize=True, progressive=True)
        image_uri = "data:image/jpeg;base64," + base64.b64encode(buffer.getvalue()).decode("ascii")
    else:
        image_uri = read_base64(capture, "image/png")
    if project == "synapse" and language == "en":
        title, subtitle = "SYNAPSE PET", "REAL CAPTURE  ·  PYSIDE6 PANEL  ·  SENSORS OFF"
    else:
        title, subtitle = {
            "synapse": ("SYNAPSE PET", "CAPTURA REAL  ·  PAINEL PYSIDE6  ·  SENSORES DESLIGADOS"),
            "urna": ("URNA CIDADÃ", "CAPTURA REAL  ·  MODO DEMONSTRAÇÃO  ·  VOTOS EM MEMÓRIA"),
        }[project]
    body = f'''
<rect width="1000" height="620" rx="22" fill="{bg}" stroke="{ink}" stroke-width="3"/>
<rect x="20" y="20" width="960" height="480" rx="12" fill="{ink}" fill-opacity=".08" stroke="{ink}" stroke-opacity=".35" stroke-width="2"/>
<image x="26" y="26" width="948" height="468" preserveAspectRatio="xMidYMid meet" href="{image_uri}"/>
<text class="title" x="28" y="548">{title}</text>
<text class="sub" x="28" y="582">{subtitle}</text>
<path d="M 838 570 H 900 L 912 562 L 921 538 L 930 570 H 962" fill="none" stroke="{ink}" stroke-width="4" stroke-linejoin="round" stroke-linecap="round"/>
<path d="M 921 538 L 930 570" fill="none" stroke="{accent}" stroke-width="6" stroke-linecap="round"/>
'''
    styles = f'text {{ fill:{ink}; }} .title {{ font:700 30px "Segoe UI",Arial,sans-serif; }} .sub {{ font:14px Consolas,"Courier New",monospace; letter-spacing:.3px; }}'
    return svg(f"Cartão de demonstração — {title}", f"Captura real da tela de {title}, em uma moldura da identidade Sudo-Marco.", "0 0 1000 620", body, styles)


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


def social_preview(project_repo: Path, project: str, capture: Path, is_dark: bool) -> None:
    bg = BASE if is_dark else LIGHT
    ink = SUPPORT if is_dark else BASE
    curve_color = SUPPORT if is_dark else BASE
    frame_color = SUPPORT if is_dark else BASE
    surface = "#1B2D33" if is_dark else LIGHT_SURFACE
    im = Image.new("RGB", (1280, 640), bg)
    d = ImageDraw.Draw(im)
    display = font(r"C:\Windows\Fonts\segoeuib.ttf", 42)
    regular = font(r"C:\Windows\Fonts\segoeui.ttf", 21)
    mono = font(r"C:\Windows\Fonts\consola.ttf", 15)
    small = font(r"C:\Windows\Fonts\consola.ttf", 13)
    screen = Image.open(capture).convert("RGB")
    d.text((64, 54), "SUDO-MARCO  /  CIÊNCIA DA COMPUTAÇÃO", font=small, fill=ink)
    if project == "synapse":
        name, lines, chips = "Synapse Pet", ["Companion desktop local", "SNN · LIF + STDP em NumPy"], ["PYTHON", "NUMPY", "PYSIDE6"]
    else:
        name, lines, chips = "Urna Cidadã", ["Simulador educativo", "Java 17 · Swing · Cloud Firestore"], ["JAVA 17", "SWING", "FIRESTORE"]
    d.text((64, 113), name, font=display, fill=ink)
    d.text((66, 184), lines[0], font=regular, fill=ink)
    d.text((66, 217), lines[1], font=regular, fill=ink)
    # Local color badges, sized to content.
    x = 64
    for chip in chips:
        width = int(d.textlength(chip, font=mono)) + 28
        d.rounded_rectangle((x, 276, x+width, 311), radius=8, fill=SUPPORT if is_dark else BASE)
        d.text((x+14, 285), chip, font=mono, fill=BASE if is_dark else LIGHT)
        x += width + 10
    # Trademark pulse; the spike hue is reserved for the firing point.
    pulse = [(70, 533),(142,533),(168,526),(185,468),(203,533),(276,533),(302,526),(318,468),(336,533),(412,533)]
    d.line(pulse, fill=curve_color, width=5, joint="curve")
    d.line([(318,468),(336,533)], fill=SPIKE, width=7)
    chick = Image.open(SOURCE / "piu-front-happy.png").convert("RGBA").resize((112,154), Image.Resampling.NEAREST)
    im.paste(chick, (289, 368), chick)

    # A real application screenshot sits inside the identity frame.
    frame = (552, 74, 1224, 562)
    d.rounded_rectangle(frame, radius=20, fill=surface, outline=frame_color, width=3)
    max_w, max_h = 628, 436
    scale = min(max_w/screen.width, max_h/screen.height)
    new_size = (round(screen.width*scale), round(screen.height*scale))
    screen = screen.resize(new_size, Image.Resampling.LANCZOS)
    x0 = frame[0] + (frame[2]-frame[0]-screen.width)//2
    y0 = frame[1] + (frame[3]-frame[1]-screen.height)//2
    im.paste(screen, (x0, y0))
    d.rounded_rectangle((x0, y0, x0+screen.width, y0+screen.height), radius=6, outline=BASE, width=2)
    dest = project_repo / "docs" / f"social-preview-{'dark' if is_dark else 'light'}.png"
    dest.parent.mkdir(parents=True, exist_ok=True)
    im.save(dest, format="PNG", optimize=True)
    if is_dark:
        im.save(project_repo / "docs" / "social-preview.png", format="PNG", optimize=True)


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def generate(profile: Path, synapse: Path | None, urna: Path | None) -> None:
    front_sheet = Image.open(SOURCE / "piu-front-sheet.png").convert("RGBA")
    idle_path, happy_path = SOURCE / "piu-front-idle.png", SOURCE / "piu-front-happy.png"
    front_sheet.crop((0, 0, 32, 44)).save(idle_path)
    front_sheet.crop((64, 0, 96, 44)).save(happy_path)
    idle = read_base64(idle_path, "image/png")
    happy = read_base64(happy_path, "image/png")
    profile_assets = profile / "assets"

    write(profile_assets / "profile-banner.svg", banner(True, idle, happy))
    write(profile_assets / "profile-banner-light.svg", banner(False, idle, happy))
    for is_dark, suffix in ((True, "dark"), (False, "light")):
        write(profile_assets / f"section-divider-{suffix}.svg", pulse_divider(is_dark, False, happy))
        write(profile_assets / f"section-divider-spike-{suffix}.svg", pulse_divider(is_dark, True, happy))
        write(profile_assets / f"stack-synapse-{suffix}.svg", badge_row(is_dark, "synapse"))
        write(profile_assets / f"stack-urna-{suffix}.svg", badge_row(is_dark, "urna"))
        write(profile_assets / f"brand-lockup-{suffix}.svg", lockup(is_dark))
        for size in (32, 64, 128):
            mark = brand_mark(is_dark, size).replace('viewBox="0 0 100 100"', f'width="{size}" height="{size}" viewBox="0 0 100 100"')
            write(profile_assets / f"brand-mark-{size}-{suffix}.svg", mark)

    synapse_capture = profile_assets / "source" / "synapse-capture.jpg"
    urna_capture = profile_assets / "source" / "urna-capture.png"
    for project in ("synapse", "urna"):
        capture = synapse_capture if project == "synapse" else urna_capture
        for is_dark, suffix in ((True, "dark"), (False, "light")):
            write(profile_assets / f"card-{project}-{suffix}.svg", demo_card(is_dark, project, capture))
    for project, repo, capture, subdir in (
        ("synapse", synapse, synapse_capture, "synapse-profile"),
        ("urna", urna, urna_capture, "urna-profile"),
    ):
        if repo is None:
            continue
        assets = repo / "assets" / "brand"
        capture = repo / "docs" / "screenshots" / ("synapse-demo-window.jpg" if project == "synapse" else "urna-demo-memoria.png")
        for is_dark, suffix in ((True, "dark"), (False, "light")):
            write(assets / f"readme-header-{suffix}.svg", lockup(is_dark, "SYNAPSE PET" if project == "synapse" else "URNA CIDADÃ"))
            write(assets / f"stack-badges-{suffix}.svg", badge_row(is_dark, project))
            write(assets / f"demo-card-{suffix}.svg", demo_card(is_dark, project, capture))
            if project == "synapse":
                write(assets / f"demo-card-en-{suffix}.svg", demo_card(is_dark, project, capture, "en"))
        social_preview(repo, project, capture, True)
        social_preview(repo, project, capture, False)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the local Sudo-Marco + Piu brand assets.")
    parser.add_argument("--profile", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--synapse", type=Path)
    parser.add_argument("--urna", type=Path)
    args = parser.parse_args()
    generate(args.profile.resolve(), args.synapse.resolve() if args.synapse else None,
             args.urna.resolve() if args.urna else None)


if __name__ == "__main__":
    main()
