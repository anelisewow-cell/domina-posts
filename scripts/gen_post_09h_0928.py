#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Post 9h 2026-09-28: Dialogo Competitivo - nova modalidade para solucoes inovadoras (art. 32, Lei 14.133/2021)."""
from PIL import Image, ImageDraw, ImageFont

W = H = 1080

NAVY_TOP = (9, 20, 46)
NAVY_BOTTOM = (24, 50, 96)
GOLD = (212, 175, 55)
WHITE = (255, 255, 255)
LIGHT_GRAY = (198, 206, 224)
DARK_TEXT = (20, 24, 40)
LINE = (90, 108, 150)

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

MARGIN_L = 92
MARGIN_R = 92
content_w = W - MARGIN_L - MARGIN_R

# --- Logo top-left, kicker to its right (variation vs. top-right used last post) ---
logo = Image.open("/tmp/logo_domina.png").convert("RGBA")
logo_size = 88
logo_x = MARGIN_L
logo_y = 72
logo_resized = logo.resize((logo_size, logo_size), Image.LANCZOS)
img.paste(logo_resized, (logo_x, logo_y), logo_resized)

f_kicker = font(F_BOLD, 23)
kicker_text = "MODALIDADE POUCO CONHECIDA"
draw.text((logo_x + logo_size + 20, logo_y + logo_size / 2 - f_kicker.size / 2), kicker_text, font=f_kicker, fill=GOLD)

y = logo_y + logo_size + 46

# --- Headline, left aligned ---
f_head = font(F_BOLD, 47)
headline_lines = wrap_text(draw, "SUA EMPRESA TEM UMA SOLUÇÃO INOVADORA PARA O GOVERNO?", f_head, content_w)
for line in headline_lines:
    draw.text((MARGIN_L, y), line, font=f_head, fill=WHITE)
    y += 56

y += 30
draw.line([(MARGIN_L, y), (W - MARGIN_R, y)], fill=LINE, width=2)
y += 36

f_sub = font(F_REG, 27)
sub_lines = wrap_text(draw, "A Lei 14.133/2021 criou o DIÁLOGO COMPETITIVO para contratações complexas e inovadoras. Ele se aplica quando:", f_sub, content_w)
for line in sub_lines:
    draw.text((MARGIN_L, y), line, font=f_sub, fill=LIGHT_GRAY)
    y += 35

y += 28

# --- 3 arrow-bullet items (variation vs. circle badges used last post) ---
items = [
    ("INOVAÇÃO TÉCNICA", "a solução exige tecnologia ou técnica ainda pouco padronizada no mercado."),
    ("SOLUÇÃO SOB MEDIDA", "o que já existe pronto não atende à necessidade do órgão sem adaptação."),
    ("ESPECIFICAÇÃO EM ABERTO", "a Administração não consegue detalhar sozinha todos os requisitos técnicos."),
]

f_arrow = font(F_BOLD, 30)
f_title = font(F_BOLD, 31)
f_body = font(F_REG, 25)
text_x = MARGIN_L + 46

for title, body in items:
    draw.text((MARGIN_L, y - 2), "→", font=f_arrow, fill=GOLD)
    draw.text((text_x, y - 2), title, font=f_title, fill=GOLD)
    ty = y + 38
    for line in wrap_text(draw, body, f_body, content_w - 46):
        draw.text((text_x, ty), line, font=f_body, fill=WHITE)
        ty += 32
    y = ty + 24

y += 6

# --- CTA button, left aligned ---
f_cta = font(F_BOLD, 28)
cta_text = "Descubra se sua empresa se encaixa →"
tw = draw.textlength(cta_text, font=f_cta)
btn_pad_x, btn_pad_y = 32, 18
btn_w = tw + btn_pad_x * 2
btn_h = f_cta.size + btn_pad_y * 2
bx0 = MARGIN_L
draw.rounded_rectangle([bx0, y, bx0 + btn_w, y + btn_h], radius=btn_h // 2, fill=GOLD)
draw.text((bx0 + btn_pad_x, y + btn_pad_y - 4), cta_text, font=f_cta, fill=DARK_TEXT)

assert y + btn_h <= H - 40, f"content overflow: {y + btn_h}"

img.save("/tmp/post.png")
print("saved", img.size, "bottom:", y + btn_h)
