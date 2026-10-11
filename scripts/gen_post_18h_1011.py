#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Post 18h 2026-10-11: prazo de pagamento do governo (art. 95 e art. 141,
Lei 14.133/2021) - mito de que existe um prazo unico de 30 dias x verdade de
que o prazo esta definido no edital/contrato de cada orgao. Angulo comercial:
empresa precisa checar isso antes de aceitar o contrato.

Paleta: azul marinho solido (oposta ao post das 9h de hoje, que foi branco
gelo). Layout variado: tudo alinhado a esquerda, logo no topo direito,
bloco comparativo MITO / VERDADE (nao repete o bloco de estatistica grande
centralizado do post das 9h de ontem nem a lista em duas colunas do post
das 18h de anteontem).
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1080

NAVY = (12, 22, 46)
WHITE = (247, 246, 240)
SUBTITLE = (164, 177, 203)
GOLD = (212, 175, 55)
GOLD_DARK_TEXT = (24, 20, 4)
LINE = (54, 68, 100)
MITO_RED = (168, 100, 94)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
def F(size):
    return ImageFont.truetype(FONT_DIR + "DejaVuSans-Bold.ttf", size)
def FR(size):
    return ImageFont.truetype(FONT_DIR + "DejaVuSans.ttf", size)

img = Image.new("RGB", (W, H), NAVY)
d = ImageDraw.Draw(img)
MARGIN = 72

def text_w(s, font):
    bbox = d.textbbox((0, 0), s, font=font)
    return bbox[2] - bbox[0]

def wrap(text, font, max_w):
    words = text.split(" ")
    lines, cur = [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if text_w(trial, font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines

def rounded_pill(xy, radius, fill=None, outline=None, width=2):
    d.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)

# --- decorative corner bracket, top-left ---
bl = 40
d.line([(MARGIN - 16, 56), (MARGIN - 16, 56 + bl)], fill=GOLD, width=3)
d.line([(MARGIN - 16, 56), (MARGIN - 16 + bl, 56)], fill=GOLD, width=3)

# --- logo top-right ---
logo = Image.open("/home/user/domina-posts/logo_domina.png").convert("RGBA")
logo_size = 100
logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
img.paste(logo, (W - MARGIN - logo_size, 58), logo)

# --- badge pill top-left ---
badge_font = F(23)
badge_text = "LEI 14.133/2021 · ART. 95 E ART. 141"
tw = text_w(badge_text, badge_font)
pad_x, pad_y = 24, 13
bx0, by0 = MARGIN, 168
bx1, by1 = bx0 + tw + pad_x * 2, by0 + 23 + pad_y * 2
rounded_pill((bx0, by0, bx1, by1), radius=(by1 - by0) // 2, outline=GOLD, width=2)
d.text((bx0 + pad_x, by0 + pad_y - 1), badge_text, font=badge_font, fill=GOLD)

# --- title, left aligned ---
title_font = F(60)
title_lines = [
    ("O GOVERNO TEM", WHITE),
    ("30 DIAS PARA", GOLD),
    ("TE PAGAR?", WHITE),
]
ty = 240
line_gap = 70
for line, color in title_lines:
    d.text((MARGIN, ty), line, font=title_font, fill=color)
    ty += line_gap

# --- subtitle ---
sub_font = FR(27)
subtitle = "Esse número não está na lei. É a confusão mais comum de quem está começando a vender para o governo."
sub_lines = wrap(subtitle, sub_font, W - 2 * MARGIN)
sy = ty + 22
for line in sub_lines:
    d.text((MARGIN, sy), line, font=sub_font, fill=SUBTITLE)
    sy += 36

# --- divider ---
dy = sy + 24
d.line([(MARGIN, dy), (W - MARGIN, dy)], fill=LINE, width=2)

# --- MITO / VERDADE comparative block ---
label_font = F(24)
body_font = FR(27)
y = dy + 34

d.text((MARGIN, y), "MITO", font=label_font, fill=MITO_RED)
y += 36
mito_lines = wrap("A lei garante 30 dias fixos para a Administração pagar qualquer fornecedor.", body_font, W - 2 * MARGIN)
for line in mito_lines:
    d.text((MARGIN, y), line, font=body_font, fill=SUBTITLE)
    y += 36

y += 22
d.text((MARGIN, y), "VERDADE", font=label_font, fill=GOLD)
y += 36
verdade_lines = wrap("A Lei 14.133/2021 não fixa prazo único (art. 95) — ele está no edital e no contrato de cada órgão. Na esfera federal, a norma interna dá 10 dias úteis para liquidar + 10 para pagar.", body_font, W - 2 * MARGIN)
for line in verdade_lines:
    d.text((MARGIN, y), line, font=body_font, fill=WHITE)
    y += 36

# --- CTA pill, bottom-left ---
cta_font = F(29)
cta_text = "Fale com a Domina no direct  →"
tw2 = text_w(cta_text, cta_font)
pad_x2, pad_y2 = 38, 21
cy1 = H - 86
cy0 = cy1 - (24 + pad_y2 * 2)
cx0 = MARGIN
cx1 = cx0 + tw2 + pad_x2 * 2
rounded_pill((cx0, cy0, cx1, cy1), radius=(cy1 - cy0) // 2, fill=GOLD)
d.text((cx0 + pad_x2, cy0 + pad_y2 - 2), cta_text, font=cta_font, fill=GOLD_DARK_TEXT)

out_path = "/home/user/domina-posts/images/post-2026-10-11-18h-prazo-pagamento-governo-art95.png"
img.save(out_path)
print("saved", out_path, img.size)
