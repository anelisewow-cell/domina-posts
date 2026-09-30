#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Post 18h 2026-09-27: empresa em recuperacao judicial pode licitar (art. 69, II, Lei 14.133/2021)."""
from PIL import Image, ImageDraw, ImageFont

W = H = 1080

NAVY_TOP = (6, 14, 34)
NAVY_BOTTOM = (24, 48, 98)
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


def draw_center(draw, y, text, fnt, fill):
    tw = draw.textlength(text, font=fnt)
    draw.text(((W - tw) / 2, y), text, font=fnt, fill=fill)


img = Image.new("RGB", (W, H), NAVY_TOP)
draw = ImageDraw.Draw(img)
vertical_gradient(draw, W, H, NAVY_TOP, NAVY_BOTTOM)

# thin inset gold frame (new decorative element vs. previous posts)
FRAME = 34
draw.rectangle([FRAME, FRAME, W - FRAME, H - FRAME], outline=GOLD, width=2)

MARGIN = 96
content_w = W - MARGIN * 2

y = 66

# --- kicker, top-left ---
f_kicker = font(F_BOLD, 25)
kicker = "DÚVIDA FREQUENTE"
draw.text((MARGIN, y), kicker, font=f_kicker, fill=GOLD)
draw.line([(MARGIN, y + 38), (MARGIN + 60, y + 38)], fill=GOLD, width=3)
y += 70

# --- headline, centered, mixed white/gold ---
f_head = font(F_BOLD, 50)
head_lines = [
    ("SUA EMPRESA ESTÁ EM", WHITE),
    ("RECUPERAÇÃO JUDICIAL", GOLD),
    ("E QUER LICITAR?", WHITE),
]
for text, color in head_lines:
    draw_center(draw, y, text, f_head, color)
    y += 57
y += 18

# --- big stat-style centerpiece answer ---
f_small_lead = font(F_REG, 26)
draw_center(draw, y, "a resposta é:", f_small_lead, LIGHT_GRAY)
y += 42

f_big = font(F_BOLD, 72)
draw_center(draw, y, "AINDA PODE", f_big, GOLD)
y += 84

f_sub = font(F_REG, 26)
sub_lines = wrap_text(
    draw,
    "A Lei 14.133/2021 não exige certidão negativa de recuperação judicial para habilitar sua empresa.",
    f_sub,
    content_w - 40,
)
for line in sub_lines:
    draw_center(draw, y, line, f_sub, LIGHT_GRAY)
    y += 34

y += 18
draw.line([(MARGIN + 30, y), (W - MARGIN - 30, y)], fill=LINE, width=2)
y += 34

# --- checkmark bullets ---
f_item = font(F_REG, 25)
f_check = font(F_BOLD, 25)
items = [
    "A lei só exige certidão negativa de FALÊNCIA (art. 69, II) — recuperação judicial é situação diferente.",
    "Cabe à Administração avaliar se sua empresa comprova capacidade econômico-financeira para executar o contrato.",
    "A jurisprudência já admite a participação de recuperandas, desde que demonstrada viabilidade de execução.",
]
check_x = MARGIN
text_x = MARGIN + 42
for text in items:
    draw.text((check_x, y), "✓", font=f_check, fill=GOLD)
    lines = wrap_text(draw, text, f_item, content_w - 42)
    for line in lines:
        draw.text((text_x, y), line, font=f_item, fill=WHITE)
        y += 32
    y += 12

# --- CTA button, centered ---
f_cta = font(F_BOLD, 29)
cta_text = "Fale com a Domina e prove sua viabilidade →"
tw = draw.textlength(cta_text, font=f_cta)
btn_pad_x, btn_pad_y = 32, 19
btn_w = tw + btn_pad_x * 2
btn_h = f_cta.size + btn_pad_y * 2
bx0 = (W - btn_w) / 2
draw.rounded_rectangle([bx0, y, bx0 + btn_w, y + btn_h], radius=btn_h // 2, fill=GOLD)
draw.text((bx0 + btn_pad_x, y + btn_pad_y - 4), cta_text, font=f_cta, fill=DARK_TEXT)
y += btn_h + 24

# --- logo bottom-center, small, standalone (new placement) ---
logo = Image.open("/tmp/logo_domina.png").convert("RGBA")
logo_size = 66
logo_resized = logo.resize((logo_size, logo_size), Image.LANCZOS)
logo_x = (W - logo_size) / 2
img.paste(logo_resized, (int(logo_x), int(y)), logo_resized)
y += logo_size

assert y <= H - FRAME - 10, f"content overflow: {y}"

img.save("/tmp/post.png")
print("saved", img.size, "bottom:", y)
