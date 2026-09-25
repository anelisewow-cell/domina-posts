#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Post 18h 2026-09-25: Consorcio de empresas em licitacao (art. 15, Lei 14.133/2021)."""
from PIL import Image, ImageDraw, ImageFont

W = H = 1080

NAVY_TOP = (9, 20, 46)
NAVY_BOTTOM = (30, 58, 104)
GOLD = (212, 175, 55)
WHITE = (255, 255, 255)
LIGHT_GRAY = (198, 206, 224)
DARK_TEXT = (20, 24, 40)
LINE = (90, 104, 144)

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

# decorative thin gold ring, upper-right (varies vs. corner triangles / edge bars used before)
draw.ellipse([W - 260, -140, W + 160, 260], outline=GOLD, width=3)
draw.ellipse([W - 210, -90, W + 110, 210], outline=(GOLD[0], GOLD[1], GOLD[2]), width=1)

MARGIN_L = 92
MARGIN_R = 92
content_w = W - MARGIN_L - MARGIN_R

y = 96

# --- Kicker, left-aligned (no logo up top this time) ---
f_kicker = font(F_BOLD, 26)
kicker_text = "ESTRATÉGIA PARA DISPUTAR EDITAIS GRANDES"
draw.line([(MARGIN_L, y + 18), (MARGIN_L + 46, y + 18)], fill=GOLD, width=4)
draw.text((MARGIN_L + 62, y), kicker_text, font=f_kicker, fill=GOLD)
y += 78

# --- Headline, left-aligned ---
f_head = font(F_BOLD, 56)
headline = "SUA EMPRESA NÃO PRECISA COMPETIR SOZINHA"
for line in wrap_text(draw, headline, f_head, content_w):
    draw.text((MARGIN_L, y), line, font=f_head, fill=WHITE)
    y += 64
y += 10

f_big = font(F_BOLD, 78)
draw.text((MARGIN_L, y), "CONSÓRCIO", font=f_big, fill=GOLD)
y += 96

f_sub = font(F_BOLD, 32)
draw.text((MARGIN_L, y), "em licitações públicas", font=f_sub, fill=LIGHT_GRAY)
y += 60

draw.line([(MARGIN_L, y), (MARGIN_L + content_w, y)], fill=LINE, width=2)
y += 42

# --- Numbered checklist (variation vs. side-by-side boxes and stacked stat numbers) ---
f_num = font(F_BOLD, 34)
f_item = font(F_REG, 27)
items = [
    "Duas ou mais empresas se juntam para somar capacidade técnica e financeira.",
    "Edital pode exigir de 10% a 30% a mais na qualificação econômico-financeira do consórcio.",
    "Consorciados respondem de forma solidária pelos atos do consórcio.",
]

circle_d = 52
for i, text in enumerate(items, start=1):
    cy = y
    draw.ellipse([MARGIN_L, cy, MARGIN_L + circle_d, cy + circle_d], outline=GOLD, width=3)
    num_str = str(i)
    nw = draw.textlength(num_str, font=f_num)
    draw.text((MARGIN_L + circle_d / 2 - nw / 2, cy + circle_d / 2 - f_num.size / 2 - 4), num_str, font=f_num, fill=GOLD)

    text_x = MARGIN_L + circle_d + 28
    text_w = content_w - circle_d - 28
    lines = wrap_text(draw, text, f_item, text_w)
    ty = cy + 2
    for line in lines:
        draw.text((text_x, ty), line, font=f_item, fill=WHITE)
        ty += 34
    y = max(cy + circle_d, ty) + 30

y += 8

# --- Logo bottom-left + CTA button bottom-right, same row (new placement) ---
logo = Image.open("/tmp/logo_domina.png").convert("RGBA")
logo_size = 84
logo_resized = logo.resize((logo_size, logo_size), Image.LANCZOS)
logo_y = H - 130
img.paste(logo_resized, (MARGIN_L, logo_y), logo_resized)

f_cta = font(F_BOLD, 28)
cta_text = "Fale com a Domina sobre seu consórcio →"
tw = draw.textlength(cta_text, font=f_cta)
btn_pad_x, btn_pad_y = 30, 18
btn_w = tw + btn_pad_x * 2
btn_h = f_cta.size + btn_pad_y * 2
bx1 = MARGIN_L + content_w
bx0 = bx1 - btn_w
by0 = logo_y + logo_size / 2 - btn_h / 2
draw.rounded_rectangle([bx0, by0, bx1, by0 + btn_h], radius=btn_h // 2, fill=GOLD)
draw.text((bx0 + btn_pad_x, by0 + btn_pad_y - 4), cta_text, font=f_cta, fill=DARK_TEXT)

img.save("/tmp/post.png")
print("saved", img.size)
