#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Story 9h 2026-09-24: Plano de Contratacoes Anual (PCA) - vertical version of feed post."""
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920

NAVY_TOP = (8, 20, 46)
NAVY_BOTTOM = (21, 50, 98)
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


def center_text(draw, cy, text, fnt, fill, cx=W // 2):
    tw = draw.textlength(text, font=fnt)
    draw.text((cx - tw / 2, cy), text, font=fnt, fill=fill)


img = Image.new("RGB", (W, H), NAVY_TOP)
draw = ImageDraw.Draw(img)
vertical_gradient(draw, W, H, NAVY_TOP, NAVY_BOTTOM)

MARGIN_L = 100
MARGIN_R = 100
content_w = W - MARGIN_L - MARGIN_R

# safe area: ~250px free top and bottom
y = 300

# --- Logo centered ---
logo = Image.open("/tmp/logo_domina.png").convert("RGBA")
logo_size = 130
logo_resized = logo.resize((logo_size, logo_size), Image.LANCZOS)
img.paste(logo_resized, (W // 2 - logo_size // 2, y), logo_resized)
y += logo_size + 50

f_kicker = font(F_BOLD, 30)
center_text(draw, y, "PLANEJAMENTO PÚBLICO", f_kicker, GOLD)
y += 70

# --- Headline centered ---
f_head = font(F_BOLD, 58)
headline = "SAIBA O QUE O GOVERNO VAI COMPRAR ANTES DO EDITAL SAIR"
h_lines = wrap_text(draw, headline, f_head, content_w)
for line in h_lines:
    center_text(draw, y, line, f_head, WHITE)
    y += 68
y += 40

# --- Highlight PCA ---
f_pca = font(F_BOLD, 140)
center_text(draw, y, "PCA", f_pca, GOLD)
y += 170

f_pca_cap = font(F_REG, 32)
cap_lines = wrap_text(draw, "Plano de Contratações Anual dos órgãos públicos", f_pca_cap, content_w - 80)
for line in cap_lines:
    center_text(draw, y, line, f_pca_cap, LIGHT_GRAY)
    y += 42
y += 40

draw.line([(MARGIN_L + 60, y), (W - MARGIN_R - 60, y)], fill=(90, 108, 150), width=2)
y += 50

# --- Bullet list, centered block, left-aligned lines ---
bullets = [
    "Todo órgão público é obrigado a publicar seu PCA no PNCP, com antecedência",
    "O documento lista os itens e serviços que pretende contratar no ano seguinte",
    "Quem consulta o PCA se prepara e chega na disputa antes da concorrência",
]
f_bullet = font(F_REG, 34)
bullet_w = content_w - 120
bx = W // 2 - bullet_w // 2
for b in bullets:
    lines = wrap_text(draw, "•  " + b, f_bullet, bullet_w)
    for line in lines:
        draw.text((bx, y), line, font=f_bullet, fill=WHITE)
        y += 46
    y += 22

y += 30

# --- CTA button centered ---
f_cta = font(F_BOLD, 33)
cta_text = "Fala com a Domina e se antecipe →"
tw = draw.textlength(cta_text, font=f_cta)
btn_pad_x, btn_pad_y = 36, 22
btn_w = tw + btn_pad_x * 2
btn_h = f_cta.size + btn_pad_y * 2
bx0 = W / 2 - btn_w / 2
draw.rounded_rectangle([bx0, y, bx0 + btn_w, y + btn_h], radius=btn_h // 2, fill=GOLD)
draw.text((bx0 + btn_pad_x, y + btn_pad_y - 4), cta_text, font=f_cta, fill=DARK_TEXT)

img.save("/tmp/story.png")
print("saved", img.size)
