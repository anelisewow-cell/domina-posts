"""Gera a arte do post das 18h (24/10/2026) - reequilibrio economico-financeiro."""
from PIL import Image, ImageDraw, ImageFont

W = H = 1080

# Paleta B: branco gelo (oposta ao ultimo post, que era azul marinho escuro)
BG = (247, 246, 240)          # off-white #F7F6F0
NAVY = (18, 32, 59)           # titulo
SLATE = (90, 101, 117)        # subtitulo / corpo
GOLD = (212, 175, 55)         # #D4AF37
GOLD_DARK = (168, 136, 40)
WHITE = (255, 255, 255)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"

def font(size, bold=True):
    path = FONT_DIR + ("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf")
    return ImageFont.truetype(path, size)

def text_w(draw, s, f):
    return draw.textbbox((0, 0), s, font=f)[2]

img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img)

# --- logo no topo, centralizado ---
logo = Image.open("/home/user/domina-posts/logo_domina.png").convert("RGBA")
logo_size = 105
logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
logo_x = (W - logo_size) // 2
logo_y = 72
img.paste(logo, (logo_x, logo_y), logo)

# --- linha fina dourada decorativa sob a logo ---
line_y = logo_y + logo_size + 34
line_w = 70
draw.line([(W // 2 - line_w // 2, line_y), (W // 2 + line_w // 2, line_y)], fill=GOLD, width=3)

# --- selo/tarja pequena "ATENCAO EMPRESARIO" ---
tag = "PARA EMPRESAS CONTRATADAS"
f_tag = font(26, bold=True)
tag_w = text_w(draw, tag, f_tag)
tag_y = line_y + 46
draw.text(((W - tag_w) // 2, tag_y), tag, font=f_tag, fill=GOLD_DARK)

# --- titulo central, 3 linhas ---
f_title = font(64, bold=True)

y = tag_y + 70
line_gap = 76

def draw_center_line(parts, yy, f):
    """parts: list of (text, color)"""
    total_w = sum(text_w(draw, t, f) for t, _ in parts)
    x = (W - total_w) // 2
    for t, c in parts:
        draw.text((x, yy), t, font=f, fill=c)
        x += text_w(draw, t, f)

draw_center_line([("SEU CONTRATO ", NAVY)], y, f_title)
y += line_gap
draw_center_line([("FICOU ", NAVY), ("DEFICITÁRIO?", GOLD_DARK)], y, f_title)
y += line_gap + 10
draw_center_line([("A LEI PODE", NAVY)], y, f_title)
y += line_gap
draw_center_line([("DEVOLVER ", NAVY), ("A MARGEM", GOLD_DARK)], y, f_title)

# --- subtitulo ---
y += line_gap + 30
f_sub = font(30, bold=False)
sub_lines = [
    "Aumento de insumo, combustível ou mão de obra",
    "pode justificar reequilíbrio econômico-financeiro",
    "do contrato público (art. 124, II, \"d\", Lei 14.133/2021).",
]
for sl in sub_lines:
    w = text_w(draw, sl, f_sub)
    draw.text(((W - w) // 2, y), sl, font=f_sub, fill=SLATE)
    y += 42

# --- botao CTA dourado ---
cta_text = "FALE COM A DOMINA LICITAÇÕES"
f_cta = font(28, bold=True)
cta_w = text_w(draw, cta_text, f_cta)
btn_pad_x = 44
btn_h = 74
btn_w = cta_w + btn_pad_x * 2
btn_y = y + 46
btn_x = (W - btn_w) // 2
draw.rounded_rectangle(
    [btn_x, btn_y, btn_x + btn_w, btn_y + btn_h],
    radius=btn_h // 2,
    fill=GOLD,
)
draw.text(
    (btn_x + btn_pad_x, btn_y + (btn_h - f_cta.size) // 2 - 6),
    cta_text,
    font=f_cta,
    fill=NAVY,
)

# --- rodape com handle ---
f_handle = font(22, bold=True)
handle = "@domina.licitacao"
hw = text_w(draw, handle, f_handle)
draw.text(((W - hw) // 2, H - 66), handle, font=f_handle, fill=SLATE)

img.save("/tmp/post.png")
print("saved /tmp/post.png", img.size)
