#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Story 2026-09-28 (9h): Dialogo competitivo - nova modalidade para solucoes inovadoras (art. 32, Lei 14.133/2021)."""
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920

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

SAFE_TOP = 250
SAFE_BOTTOM = 250


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


def center_text(draw, cx, y, text, fnt, fill):
    tw = draw.textlength(text, font=fnt)
    draw.text((cx - tw / 2, y), text, font=fnt, fill=fill)
    return tw


img = Image.new("RGB", (W, H), NAVY_TOP)
draw = ImageDraw.Draw(img)
vertical_gradient(draw, W, H, NAVY_TOP, NAVY_BOTTOM)

CX = W / 2
MARGIN_L = 100
MARGIN_R = 100
content_w = W - MARGIN_L - MARGIN_R

y = SAFE_TOP

# --- Logo + kicker, centered as one unit ---
logo = Image.open("/tmp/logo_domina.png").convert("RGBA")
logo_size = 100
logo_resized = logo.resize((logo_size, logo_size), Image.LANCZOS)

f_kicker = font(F_BOLD, 26)
kicker_text = "MODALIDADE POUCO CONHECIDA"
kicker_w = draw.textlength(kicker_text, font=f_kicker)
gap = 22
unit_w = logo_size + gap + kicker_w
unit_x = CX - unit_w / 2

img.paste(logo_resized, (int(unit_x), int(y)), logo_resized)
draw.text((unit_x + logo_size + gap, y + logo_size / 2 - f_kicker.size / 2), kicker_text, font=f_kicker, fill=GOLD)

y += logo_size + 66

# --- Headline, centered ---
f_head = font(F_BOLD, 52)
for line in wrap_text(draw, "SUA EMPRESA TEM UMA SOLUÇÃO INOVADORA PARA O GOVERNO?", f_head, content_w):
    center_text(draw, CX, y, line, f_head, WHITE)
    y += 62

y += 30
draw.line([(MARGIN_L, y), (W - MARGIN_R, y)], fill=LINE, width=2)
y += 46

f_sub = font(F_REG, 31)
for line in wrap_text(draw, "A Lei 14.133/2021 criou o DIÁLOGO COMPETITIVO para contratações complexas e inovadoras. Ele se aplica quando:", f_sub, content_w):
    center_text(draw, CX, y, line, f_sub, LIGHT_GRAY)
    y += 40

y += 44

# --- 3 arrow-bullet items, left-aligned block centered on canvas ---
items = [
    ("INOVAÇÃO TÉCNICA", "a solução exige tecnologia ou técnica ainda pouco padronizada no mercado."),
    ("SOLUÇÃO SOB MEDIDA", "o que já existe pronto não atende à necessidade do órgão sem adaptação."),
    ("ESPECIFICAÇÃO EM ABERTO", "a Administração não consegue detalhar sozinha todos os requisitos técnicos."),
]

f_arrow = font(F_BOLD, 34)
f_title = font(F_BOLD, 35)
f_body = font(F_REG, 29)
text_x = MARGIN_L + 52

for title, body in items:
    draw.text((MARGIN_L, y - 2), "→", font=f_arrow, fill=GOLD)
    draw.text((text_x, y - 2), title, font=f_title, fill=GOLD)
    ty = y + 46
    for line in wrap_text(draw, body, f_body, content_w - 52):
        draw.text((text_x, ty), line, font=f_body, fill=WHITE)
        ty += 38
    y = ty + 30

y += 10

# --- CTA button, centered ---
f_cta = font(F_BOLD, 33)
cta_text = "Fala com a Domina →"
tw = draw.textlength(cta_text, font=f_cta)
btn_pad_x, btn_pad_y = 40, 22
btn_w = tw + btn_pad_x * 2
btn_h = f_cta.size + btn_pad_y * 2
bx0 = CX - btn_w / 2
draw.rounded_rectangle([bx0, y, bx0 + btn_w, y + btn_h], radius=btn_h // 2, fill=GOLD)
draw.text((bx0 + btn_pad_x, y + btn_pad_y - 4), cta_text, font=f_cta, fill=DARK_TEXT)

assert y + btn_h <= H - SAFE_BOTTOM, f"content extends into bottom safe area: {y + btn_h} > {H - SAFE_BOTTOM}"

img.save("/tmp/story.png")
print("saved", img.size, "content bottom:", y + btn_h, "limit:", H - SAFE_BOTTOM)
