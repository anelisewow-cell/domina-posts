#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Post 18h 2026-09-21: Registro de precos e "carona" - vender para varios orgaos sem nova disputa."""
from PIL import Image, ImageDraw, ImageFont

W = H = 1080

NAVY_TOP = (10, 22, 50)
NAVY_BOTTOM = (26, 54, 98)
GOLD = (212, 175, 55)
WHITE = (255, 255, 255)
LIGHT_GRAY = (198, 206, 224)
DARK_TEXT = (20, 24, 40)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
F_BOLD = FONT_DIR + "DejaVuSans-Bold.ttf"
F_REG = FONT_DIR + "DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def vertical_gradient(draw, w, h, top, bottom):
    for y in range(h):
        t = y / h
        r = int(top[0] + (bottom[0] - top[0]) * t)
        g = int(top[1] + (bottom[1] - top[1]) * t)
        b = int(top[2] + (bottom[2] - top[2]) * t)
        draw.line([(0, y), (w, y)], fill=(r, g, b))


def wrap_text(draw, text, fnt, max_width):
    words = text.split(" ")
    lines, cur = [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if draw.textlength(test, font=fnt) <= max_width:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


img = Image.new("RGB", (W, H), NAVY_TOP)
draw = ImageDraw.Draw(img)
vertical_gradient(draw, W, H, NAVY_TOP, NAVY_BOTTOM)

# decorative diagonal gold corner accents (top-left + bottom-right) - varies vs. previous edge-bar/top-bottom-bar posts
draw.polygon([(0, 0), (170, 0), (0, 170)], fill=GOLD)
draw.polygon([(0, 0), (140, 0), (0, 140)], fill=NAVY_TOP)
draw.polygon([(W, H), (W - 170, H), (W, H - 170)], fill=GOLD)
draw.polygon([(W, H), (W - 140, H), (W, H - 140)], fill=NAVY_BOTTOM)

MARGIN_L = 96
MARGIN_R = 96
content_w = W - MARGIN_L - MARGIN_R
CX = W // 2

# --- Logo top-right (variation vs. top-center/top-left placements used previously) ---
logo = Image.open("/tmp/logo_domina.png").convert("RGBA")
logo_size = 84
logo_resized = logo.resize((logo_size, logo_size), Image.LANCZOS)
logo_x = W - MARGIN_R - logo_size
logo_y = 66
img.paste(logo_resized, (logo_x, logo_y), logo_resized)

y = 182

# --- Ribbon-style label banner (varies vs. pill badge used in previous posts) ---
f_label = font(F_BOLD, 26)
label_text = "OPORTUNIDADE POUCO CONHECIDA"
tw = draw.textlength(label_text, font=f_label)
draw.line([(MARGIN_L, y + 18), (MARGIN_L + 46, y + 18)], fill=GOLD, width=4)
draw.text((MARGIN_L + 62, y), label_text, font=f_label, fill=GOLD)
y += 70

# --- Headline, left-aligned, upper area ---
f_head = font(F_BOLD, 54)
headline = "VENCEU UMA LICITAÇÃO? DÁ PRA VENDER PARA OUTROS ÓRGÃOS SEM DISPUTAR DE NOVO"
h_lines = wrap_text(draw, headline, f_head, content_w)
for line in h_lines:
    draw.text((MARGIN_L, y), line, font=f_head, fill=WHITE)
    y += 62
y += 30

# --- Big stat block: two numbers side by side, left aligned pair (variation: numbers stacked with left labels instead of centered columns) ---
f_stat = font(F_BOLD, 92)
f_stat_cap = font(F_REG, 25)

stats = [
    ("1 ANO", "vigência da ata de registro de preços, prorrogável por + 1 ano"),
    ("2x", "quantidade extra que outros órgãos podem comprar via adesão (\"carona\")"),
]

row_y = y
for num, cap in stats:
    draw.text((MARGIN_L, row_y), num, font=f_stat, fill=GOLD)
    num_w = draw.textlength(num, font=f_stat)
    cap_x = MARGIN_L + num_w + 34
    cap_max_w = content_w - num_w - 34
    lines = wrap_text(draw, cap, f_stat_cap, cap_max_w)
    cap_y = row_y + 18
    for line in lines:
        draw.text((cap_x, cap_y), line, font=f_stat_cap, fill=LIGHT_GRAY)
        cap_y += 33
    row_bottom = max(row_y + f_stat.size + 10, cap_y)
    row_y = row_bottom + 26

y = row_y + 6
draw.line([(MARGIN_L, y), (MARGIN_L + content_w, y)], fill=(90, 100, 130), width=2)
y += 34

# --- Support paragraph ---
f_support = font(F_REG, 30)
support_text = "Pelo sistema de registro de preços, outros órgãos públicos podem aderir à sua ata vencedora e comprar direto de você — sem nova licitação."
s_lines = wrap_text(draw, support_text, f_support, content_w)
for line in s_lines:
    draw.text((MARGIN_L, y), line, font=f_support, fill=WHITE)
    y += 42

y += 36

# --- CTA button, right-aligned (variation vs. left/center CTA of previous posts) ---
f_cta = font(F_BOLD, 30)
cta_text = "Fale com a Domina e amplie suas vendas →"
tw = draw.textlength(cta_text, font=f_cta)
btn_pad_x, btn_pad_y = 34, 20
btn_w = tw + btn_pad_x * 2
btn_h = f_cta.size + btn_pad_y * 2
bx1 = MARGIN_L + content_w
bx0 = bx1 - btn_w
draw.rounded_rectangle([bx0, y, bx1, y + btn_h], radius=btn_h // 2, fill=GOLD)
draw.text((bx0 + btn_pad_x, y + btn_pad_y - 4), cta_text, font=f_cta, fill=DARK_TEXT)

img.save("/tmp/post.png")
print("saved", img.size)
