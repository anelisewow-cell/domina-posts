#!/usr/bin/env python3.12
# -*- coding: utf-8 -*-
"""
Post 18h - 2026-10-20
Tema: Preposto do contrato (art. 118, Lei 14.133/2021) - empresa que vence a
licitacao precisa manter um preposto aceito pela Administracao para
representa-la na execucao do contrato. Tema diferente do post das 9h de hoje
(limite do aditivo contratual, art. 125) e nao repetido nos ultimos 30 dias.

Paleta: BRANCO GELO (#F7F6F0) - oposta ao ultimo post publicado (hoje 9h,
navy solido, confirmado no script gen_post_09h_1020.py).

Layout variado em relacao aos posts recentes (18/10 18h = tudo centralizado;
19/10 9h e 20/10 9h = alinhado a esquerda): aqui TUDO ALINHADO A DIREITA,
logo no canto SUPERIOR DIREITO, badge de lei no canto SUPERIOR ESQUERDO,
titulo e subtitulo alinhados a direita, botao CTA alinhado a direita,
brackets decorativos no canto INFERIOR ESQUERDO e SUPERIOR DIREITO (abaixo da
logo), elemento central = linha dourada fina dividindo titulo do bloco de
explicacao (sem "estatistica grande" desta vez).
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1080
OFF_WHITE = (247, 246, 240)
NAVY = (16, 26, 48)
NAVY_SOFT = (62, 74, 98)      # subtitle gray-blue
GOLD = (212, 175, 55)
GOLD_DARK = (168, 136, 40)

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def F(path, size):
    return ImageFont.truetype(path, size)

img = Image.new("RGB", (W, H), OFF_WHITE)
draw = ImageDraw.Draw(img)

MARGIN = 80
RIGHT = W - MARGIN

def text_w(s, font):
    return draw.textlength(s, font=font)

def draw_right(y, s, font, fill):
    w = text_w(s, font)
    draw.text((RIGHT - w, y), s, font=font, fill=fill)
    return w

# ---- decorative brackets ----
BR_LEN = 46
BR_W = 4
# top-right bracket (below/around logo area, drawn first so logo sits in front)
draw.line([(W - 40, 40), (W - 40, 40 + BR_LEN)], fill=GOLD, width=BR_W)
draw.line([(W - 40, 40), (W - 40 - BR_LEN, 40)], fill=GOLD, width=BR_W)
# bottom-left bracket
draw.line([(40, H - 40), (40, H - 40 - BR_LEN)], fill=GOLD, width=BR_W)
draw.line([(40, H - 40), (40 + BR_LEN, H - 40)], fill=GOLD, width=BR_W)

# ---- logo, top-right ----
logo = Image.open("/home/user/domina-posts/logo_domina.png").convert("RGBA")
logo_size = 105
logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
img.paste(logo, (W - MARGIN - logo_size, 56), logo)

# ---- law badge, top-left ----
badge_font = F(FONT_BOLD, 21)
badge_text = "LEI 14.133/2021 · ART. 118"
pad_x, pad_y = 20, 11
bw = text_w(badge_text, badge_font)
bx0, by0 = MARGIN, 56 + (logo_size - (21 + pad_y * 2)) // 2
bx1, by1 = bx0 + bw + pad_x * 2, by0 + 21 + pad_y * 2
draw.rounded_rectangle([bx0, by0, bx1, by1], radius=(by1 - by0) // 2, outline=GOLD_DARK, width=2)
draw.text((bx0 + pad_x, by0 + pad_y - 2), badge_text, font=badge_font, fill=NAVY)

y = 56 + logo_size + 78

# ---- title, right-aligned ----
title_font = F(FONT_BOLD, 66)
lines = [
    ("SUA EMPRESA", NAVY),
    ("VENCEU O CONTRATO.", NAVY),
    ("QUEM VAI", GOLD),
    ("REPRESENTÁ-LA AGORA?", GOLD),
]
for text, color in lines:
    draw_right(y, text, title_font, color)
    y += 76

y += 28
# thin gold divider line, right-aligned, short
line_w = 150
draw.line([(RIGHT - line_w, y), (RIGHT, y)], fill=GOLD, width=3)
y += 42

# ---- subtitle, right-aligned ----
sub_font = F(FONT_REG, 30)
sub_lines = [
    "A Lei 14.133/2021 exige que sua empresa",
    "mantenha um preposto aceito pela Administração",
    "para representá-la na execução do contrato.",
]
for s in sub_lines:
    draw_right(y, s, sub_font, NAVY_SOFT)
    y += 42

y += 56

# ---- CTA button, right-aligned ----
cta_font = F(FONT_BOLD, 26)
cta_text = "FALE COM A DOMINA →"
cta_pad_x, cta_pad_y = 34, 20
cw = text_w(cta_text, cta_font)
cx1 = RIGHT
cx0 = cx1 - (cw + cta_pad_x * 2)
cy0 = y
cy1 = cy0 + 26 + cta_pad_y * 2
draw.rounded_rectangle([cx0, cy0, cx1, cy1], radius=(cy1 - cy0) // 2, fill=GOLD)
draw.text((cx0 + cta_pad_x, cy0 + cta_pad_y - 2), cta_text, font=cta_font, fill=NAVY)

img.save("/tmp/post.png")
print("saved /tmp/post.png", img.size)
