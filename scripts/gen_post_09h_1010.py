from PIL import Image, ImageDraw, ImageFont

W = H = 1080

# paleta azul marinho (gradiente sutil topo->base), oposta ao ultimo post (branco gelo)
NAVY_TOP = (10, 20, 44)
NAVY_BOTTOM = (22, 40, 78)
WHITE = (247, 246, 240)
SUBTITLE = (168, 181, 206)
GOLD = (212, 175, 55)
GOLD_DARK_TEXT = (24, 20, 4)
LINE = (58, 72, 104)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
def F(size):
    return ImageFont.truetype(FONT_DIR + "DejaVuSans-Bold.ttf", size)
def FR(size):
    return ImageFont.truetype(FONT_DIR + "DejaVuSans.ttf", size)

img = Image.new("RGB", (W, H), NAVY_TOP)
d = ImageDraw.Draw(img)

for y in range(H):
    t = y / H
    r = int(NAVY_TOP[0] + (NAVY_BOTTOM[0] - NAVY_TOP[0]) * t)
    g = int(NAVY_TOP[1] + (NAVY_BOTTOM[1] - NAVY_TOP[1]) * t)
    b = int(NAVY_TOP[2] + (NAVY_BOTTOM[2] - NAVY_TOP[2]) * t)
    d.line([(0, y), (W, y)], fill=(r, g, b))

def text_w(draw, s, font):
    bbox = draw.textbbox((0, 0), s, font=font)
    return bbox[2] - bbox[0]

def center_text(draw, cx, y, s, font, fill):
    tw = text_w(draw, s, font)
    draw.text((cx - tw / 2, y), s, font=font, fill=fill)

def rounded_pill(draw, xy, radius, fill=None, outline=None, width=2):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)

CX = W // 2

# --- decorative corner brackets (gold), top-left and bottom-right ---
bl = 42
d.line([(56, 56), (56, 56 + bl)], fill=GOLD, width=3)
d.line([(56, 56), (56 + bl, 56)], fill=GOLD, width=3)
d.line([(W - 56, H - 56), (W - 56, H - 56 - bl)], fill=GOLD, width=3)
d.line([(W - 56, H - 56), (W - 56 - bl, H - 56)], fill=GOLD, width=3)

# --- logo top-center ---
logo = Image.open("/home/user/domina-posts/logo_domina.png").convert("RGBA")
logo_size = 92
logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
img.paste(logo, (CX - logo_size // 2, 64), logo)

# --- badge pill, centered ---
badge_font = F(23)
badge_text = "LEI 14.133/2021 · ART. 25, §4º"
tw = text_w(d, badge_text, badge_font)
pad_x, pad_y = 24, 13
by0 = 176
bx0 = CX - (tw + pad_x * 2) / 2
bx1 = CX + (tw + pad_x * 2) / 2
by1 = by0 + 23 + pad_y * 2
rounded_pill(d, (bx0, by0, bx1, by1), radius=(by1 - by0) // 2, outline=GOLD, width=2)
d.text((bx0 + pad_x, by0 + pad_y - 1), badge_text, font=badge_font, fill=GOLD)

# --- title, centered, 3 lines ---
title_font = F(64)
lines = [
    ("COMPLIANCE", WHITE),
    ("PODE DESEMPATAR", GOLD),
    ("UMA LICITAÇÃO", WHITE),
]
ty = 268
line_gap = 76
for line, color in lines:
    center_text(d, CX, ty, line, title_font, color)
    ty += line_gap

# --- subtitle, centered ---
sub_font = FR(27)
sub_lines = [
    "Decreto 12.304/2024: o programa de integridade virou",
    "critério de desempate em contratos de grande vulto.",
]
sy = ty + 36
for line in sub_lines:
    center_text(d, CX, sy, line, sub_font, SUBTITLE)
    sy += 38

# --- divider, centered, curto ---
dy = sy + 30
d.line([(CX - 90, dy), (CX + 90, dy)], fill=LINE, width=2)

# --- big stat block, centered ---
stat_font = F(92)
stat_text = "R$ 200 MI"
sty = dy + 40
center_text(d, CX, sty, stat_text, stat_font, GOLD)

stat_label_font = FR(24)
stat_label_lines = [
    "valor a partir do qual a exigência entra em jogo",
    "(art. 6º, XXII — obras, serviços e fornecimentos de grande vulto)",
]
sly = sty + 116
for line in stat_label_lines:
    center_text(d, CX, sly, line, stat_label_font, SUBTITLE)
    sly += 32

# --- CTA pill, centered, bottom ---
cta_font = F(29)
cta_text = "Fale com a Domina no direct  →"
tw2 = text_w(d, cta_text, cta_font)
pad_x2, pad_y2 = 38, 21
cy1 = H - 96
cy0 = cy1 - (24 + pad_y2 * 2)
cx0 = CX - (tw2 + pad_x2 * 2) / 2
cx1 = CX + (tw2 + pad_x2 * 2) / 2
rounded_pill(d, (cx0, cy0, cx1, cy1), radius=(cy1 - cy0) // 2, fill=GOLD)
d.text((cx0 + pad_x2, cy0 + pad_y2 - 2), cta_text, font=cta_font, fill=GOLD_DARK_TEXT)

out_path = "/home/user/domina-posts/images/post-2026-10-10-09h-programa-integridade-desempate-art25.png"
img.save(out_path)
print("saved", out_path, img.size)
