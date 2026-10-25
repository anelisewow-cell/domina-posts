#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Post 18h 2026-10-25: Mito x Verdade - parcelamento do objeto em lotes (art. 40, V, "b", Lei 14.133/2021).
Paleta: branco gelo (oposta ao post das 9h de hoje, que foi azul marinho).
Layout: alinhamento à direita, logo no topo-esquerdo, barra dourada à direita do bloco de texto
(variação em relação ao post das 9h - barra à esquerda/logo direita - e ao post mito x verdade anterior,
que era centralizado com logo no topo-centro)."""
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1080

OFFWHITE_TOP = (248, 247, 241)
OFFWHITE_BOTTOM = (241, 239, 230)
NAVY = (18, 35, 64)
NAVY_SOFT = (46, 64, 94)
GOLD = (196, 155, 61)
GOLD_LINE = (196, 155, 61)
SUBTITLE = (99, 112, 134)
SOURCE_GRAY = (140, 148, 163)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


f_tag = font("DejaVuSans-Bold.ttf", 25)
f_label = font("DejaVuSans-Bold.ttf", 26)
f_title = font("DejaVuSans-Bold.ttf", 52)
f_body = font("DejaVuSans.ttf", 29)
f_source = font("DejaVuSans.ttf", 21)
f_cta = font("DejaVuSans-Bold.ttf", 27)
f_handle = font("DejaVuSans-Bold.ttf", 21)


def vertical_gradient(w, h, top, bottom):
    base = Image.new("RGB", (w, h), top)
    draw = ImageDraw.Draw(base)
    for y in range(h):
        t = y / h
        r = int(top[0] + (bottom[0] - top[0]) * t)
        g = int(top[1] + (bottom[1] - top[1]) * t)
        b = int(top[2] + (bottom[2] - top[2]) * t)
        draw.line([(0, y), (w, y)], fill=(r, g, b))
    return base


img = vertical_gradient(W, H, OFFWHITE_TOP, OFFWHITE_BOTTOM)
draw = ImageDraw.Draw(img)

MARGIN = 84
RIGHT_EDGE = W - MARGIN


def text_w(txt, fnt):
    bbox = draw.textbbox((0, 0), txt, font=fnt)
    return bbox[2] - bbox[0]


def draw_right(y, txt, fnt, fill, spacing=None, letter_spacing=0):
    if letter_spacing:
        txt_draw = " ".join(list(txt)) if False else txt
    w = text_w(txt, fnt)
    draw.text((RIGHT_EDGE - w, y), txt, font=fnt, fill=fill)
    return w


# --- logo pequena no topo-esquerdo ---
logo_size = 100
logo = Image.open("/home/user/domina-posts/logo_domina.png").convert("RGBA")
logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
img.paste(logo, (MARGIN, 78), logo)

# --- bloco de texto alinhado a direita ---
y = 268

tag = "LEI 14.133/2021 · ART. 40"
draw_right(y, tag, f_tag, GOLD)
y += 54

mito_label = "MITO"
draw_right(y, mito_label, f_label, SUBTITLE)
y += 42

mito_lines = ["SÓ EMPRESA GRANDE", "GANHA CONTRATO GRANDE."]
for line in mito_lines:
    draw_right(y, line, f_title, NAVY_SOFT)
    y += 62

y += 22

verdade_label = "VERDADE"
draw_right(y, verdade_label, f_label, GOLD)
y += 42

# título com destaque dourado na palavra PARCELAR
line1 = "A LEI MANDA "
word_gold = "PARCELAR"
line2 = "EM LOTES."
w1 = text_w(line1 + word_gold, f_title)
x1 = RIGHT_EDGE - w1
draw.text((x1, y), line1, font=f_title, fill=NAVY)
x_gold = x1 + text_w(line1, f_title)
draw.text((x_gold, y), word_gold, font=f_title, fill=GOLD)
y += 62
draw_right(y, line2, f_title, NAVY)
y += 78

# --- linha dourada fina a direita do bloco ---
bar_x = RIGHT_EDGE + 0
# desenha barra vertical fininha alinhada a borda direita do texto, um pouco acima/abaixo
draw.rectangle([RIGHT_EDGE + 26, 268, RIGHT_EDGE + 30, y - 20], fill=GOLD)

# --- corpo de apoio ---
body_lines = [
    "Sua empresa pode disputar só o lote",
    "que consegue entregar — sem competir",
    "pelo pacote inteiro contra gigantes.",
]
for line in body_lines:
    draw_right(y, line, f_body, SUBTITLE)
    y += 40

y += 28

source_line = 'Lei 14.133/2021, art. 40, V, "b" — parcelamento técnica e'
source_line2 = "economicamente viável (planalto.gov.br); Súmula 247 do TCU"
draw_right(y, source_line, f_source, SOURCE_GRAY)
y += 28
draw_right(y, source_line2, f_source, SOURCE_GRAY)
y += 50

# --- CTA botao dourado arredondado, alinhado a direita ---
cta_text = "FALE COM A DOMINA LICITAÇÕES"
cta_w = text_w(cta_text, f_cta)
pad_x = 42
pad_y = 20
btn_w = cta_w + pad_x * 2
btn_h = f_cta.size + pad_y * 2
btn_x1 = RIGHT_EDGE
btn_x0 = btn_x1 - btn_w
btn_y0 = y
btn_y1 = y + btn_h
draw.rounded_rectangle([btn_x0, btn_y0, btn_x1, btn_y1], radius=btn_h // 2, fill=GOLD)
draw.text((btn_x0 + pad_x, btn_y0 + pad_y - 2), cta_text, font=f_cta, fill=NAVY)

# --- handle no rodape ---
handle = "@domina.licitacao"
hw = text_w(handle, f_handle)
handle_y = max(btn_y1 + 26, H - 58)
draw.text(((W - hw) / 2, handle_y), handle, font=f_handle, fill=SUBTITLE)

img.save("/tmp/claude-0/-home-user-domina-posts/0d86308d-13d6-5bc4-b6ea-4d79eb07def6/scratchpad/post_18h_1025.png")
print("saved")
