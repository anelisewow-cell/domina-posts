#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Post 9h 2026-09-24: Plano de Contratacoes Anual (PCA) - art. 12, VII, Lei 14.133/2021."""
from PIL import Image, ImageDraw, ImageFont

W = H = 1080

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


img = Image.new("RGB", (W, H), NAVY_TOP)
draw = ImageDraw.Draw(img)
vertical_gradient(draw, W, H, NAVY_TOP, NAVY_BOTTOM)

# thin gold top bar (variation vs. side bar used previously)
draw.rectangle([0, 0, W, 10], fill=GOLD)

MARGIN_L = 96
MARGIN_R = 96
content_w = W - MARGIN_L - MARGIN_R

# --- Logo top-left (variation vs. top-right / top-center used previously) ---
logo = Image.open("/tmp/logo_domina.png").convert("RGBA")
logo_size = 100
logo_resized = logo.resize((logo_size, logo_size), Image.LANCZOS)
logo_x = MARGIN_L
logo_y = 80
img.paste(logo_resized, (logo_x, logo_y), logo_resized)

f_kicker = font(F_BOLD, 26)
kicker_text = "PLANEJAMENTO PÚBLICO"
kicker_y = logo_y + logo_size / 2 - f_kicker.size / 2
draw.text((logo_x + logo_size + 26, kicker_y), kicker_text, font=f_kicker, fill=GOLD)

y = logo_y + logo_size + 56

# --- Headline, left aligned ---
f_head = font(F_BOLD, 54)
headline = "SAIBA O QUE O GOVERNO VAI COMPRAR ANTES DO EDITAL SAIR"
h_lines = wrap_text(draw, headline, f_head, content_w)
for line in h_lines:
    draw.text((MARGIN_L, y), line, font=f_head, fill=WHITE)
    y += 62
y += 30

# --- Highlight: PCA in gold + caption ---
f_pca = font(F_BOLD, 118)
pca_text = "PCA"
draw.text((MARGIN_L, y), pca_text, font=f_pca, fill=GOLD)
pca_w = draw.textlength(pca_text, font=f_pca)
f_pca_cap = font(F_BOLD, 28)
cap_lines = wrap_text(draw, "Plano de Contratações Anual dos órgãos públicos", f_pca_cap, content_w - pca_w - 30)
cy = y + 24
for line in cap_lines:
    draw.text((MARGIN_L + pca_w + 26, cy), line, font=f_pca_cap, fill=WHITE)
    cy += 36
y += 150

draw.line([(MARGIN_L, y), (W - MARGIN_R, y)], fill=(90, 108, 150), width=2)
y += 36

# --- Bullet list, left aligned ---
bullets = [
    "Todo órgão público é obrigado a publicar seu PCA no PNCP, com antecedência",
    "O documento lista os itens e serviços que pretende contratar no ano seguinte",
    "Quem consulta o PCA se prepara e chega na disputa antes da concorrência",
]
f_bullet = font(F_REG, 29)
for b in bullets:
    lines = wrap_text(draw, "•  " + b, f_bullet, content_w)
    for line in lines:
        draw.text((MARGIN_L, y), line, font=f_bullet, fill=WHITE)
        y += 38
    y += 16

y += 16

# --- CTA button, left aligned ---
f_cta = font(F_BOLD, 29)
cta_text = "Fala com a Domina e se antecipe →"
tw = draw.textlength(cta_text, font=f_cta)
btn_pad_x, btn_pad_y = 32, 18
btn_w = tw + btn_pad_x * 2
btn_h = f_cta.size + btn_pad_y * 2
bx0 = MARGIN_L
draw.rounded_rectangle([bx0, y, bx0 + btn_w, y + btn_h], radius=btn_h // 2, fill=GOLD)
draw.text((bx0 + btn_pad_x, y + btn_pad_y - 4), cta_text, font=f_cta, fill=DARK_TEXT)

img.save("/tmp/post.png")
print("saved", img.size)
