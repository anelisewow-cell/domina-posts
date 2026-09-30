#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Post 18h 2026-09-26: preco inexequivel - erro comum ao precificar proposta (art. 59, Lei 14.133/2021)."""
from PIL import Image, ImageDraw, ImageFont

W = H = 1080

NAVY_TOP = (7, 15, 38)
NAVY_BOTTOM = (22, 40, 84)
GOLD = (212, 175, 55)
WHITE = (255, 255, 255)
LIGHT_GRAY = (196, 205, 224)
DARK_TEXT = (26, 20, 6)
LINE = (86, 100, 140)

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


def draw_center(draw, y, text, fnt, fill):
    tw = draw.textlength(text, font=fnt)
    draw.text(((W - tw) / 2, y), text, font=fnt, fill=fill)


img = Image.new("RGB", (W, H), NAVY_TOP)
draw = ImageDraw.Draw(img)
vertical_gradient(draw, W, H, NAVY_TOP, NAVY_BOTTOM)

# decorative diagonal accent lines, both bottom corners (variation vs. rings/circles used before)
for dx in (0, 46):
    draw.line([(0, H - 150 + dx), (150 - dx, H)], fill=GOLD, width=4)
    draw.line([(W, H - 150 + dx), (W - 150 + dx, H)], fill=GOLD, width=4)

MARGIN = 90
content_w = W - MARGIN * 2

y = 90

# --- logo top-center, small ---
logo = Image.open("/home/user/domina-posts/logo_domina.png").convert("RGBA")
logo_size = 88
logo_resized = logo.resize((logo_size, logo_size), Image.LANCZOS)
img.paste(logo_resized, (int((W - logo_size) / 2), y), logo_resized)
y += logo_size + 40

# --- kicker, centered ---
f_kicker = font(F_BOLD, 27)
kicker = "ERRO COMUM NA HORA DE PRECIFICAR"
draw_center(draw, y, kicker, f_kicker, GOLD)
y += 56

draw.line([(W / 2 - 60, y), (W / 2 + 60, y)], fill=GOLD, width=3)
y += 40

# --- headline, centered, mixed white/gold ---
f_head = font(F_BOLD, 60)
head_lines = [
    ("SEU PREÇO PODE SER", WHITE),
    ("BAIXO DEMAIS", GOLD),
    ("PARA GANHAR A DISPUTA", WHITE),
]
for text, color in head_lines:
    draw_center(draw, y, text, f_head, color)
    y += 68
y += 6

f_sub = font(F_REG, 30)
draw_center(draw, y, "Lei nº 14.133/2021, art. 59", f_sub, LIGHT_GRAY)
y += 50

draw.line([(MARGIN + 40, y), (W - MARGIN - 40, y)], fill=LINE, width=2)
y += 44

# --- body: 3 short blocks, centered paragraphs ---
f_item = font(F_REG, 28)
items = [
    "Proposta é desclassificada quando não demonstra capacidade de cumprir o contrato pelo valor ofertado.",
    "Em obras e serviços de engenharia, preço abaixo de 75% do valor orçado já é presumido inexequível (art. 59, §4º).",
    "Antes de desclassificar, a Administração deve dar chance de a empresa comprovar que o preço é exequível (art. 59, §2º).",
]
for text in items:
    for line in wrap_text(draw, text, f_item, content_w - 60):
        draw_center(draw, y, line, f_item, WHITE)
        y += 38
    y += 18

y += 10

# --- CTA button, centered ---
f_cta = font(F_BOLD, 30)
cta_text = "Fale com a Domina sobre sua precificação →"
tw = draw.textlength(cta_text, font=f_cta)
btn_pad_x, btn_pad_y = 36, 20
btn_w = tw + btn_pad_x * 2
btn_h = f_cta.size + btn_pad_y * 2
bx0 = (W - btn_w) / 2
by0 = H - 150
draw.rounded_rectangle([bx0, by0, bx0 + btn_w, by0 + btn_h], radius=btn_h // 2, fill=GOLD)
draw.text((bx0 + btn_pad_x, by0 + btn_pad_y - 4), cta_text, font=f_cta, fill=DARK_TEXT)

img.save("/tmp/post.png")
print("saved", img.size)
