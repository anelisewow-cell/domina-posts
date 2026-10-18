#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Post 9h 2026-10-13: adjudicacao e homologacao (art. 71, Lei 14.133/2021).
Angulo: vencer a disputa nao e o mesmo que ter o contrato - a lei exige
adjudicacao e homologacao (hoje reunidas num so ato da autoridade superior)
antes da assinatura.

Paleta: branco gelo (oposta ao post das 18h de ontem, que foi azul marinho
solido). Layout variado: titulo CENTRALIZADO (o post das 9h de ontem era
alinhado a esquerda), logo no topo DIREITO e badge no topo ESQUERDO
(invertido em relacao a ontem), bloco central em timeline VERTICAL com
marcadores (nao repete a fileira horizontal de steps nem o bloco
COMO ERA/COMO E AGORA do post de ontem).
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1080

OFFWHITE = (247, 246, 240)
NAVY = (18, 30, 58)
SUBTITLE = (104, 116, 142)
GOLD = (212, 175, 55)
GOLD_DARK_TEXT = (24, 20, 4)
LINE = (214, 210, 198)
DOT_INACTIVE = (190, 186, 172)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
def F(size):
    return ImageFont.truetype(FONT_DIR + "DejaVuSans-Bold.ttf", size)
def FR(size):
    return ImageFont.truetype(FONT_DIR + "DejaVuSans.ttf", size)

img = Image.new("RGB", (W, H), OFFWHITE)
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

def center_text(y, text, font, fill):
    tw = text_w(text, font)
    d.text(((W - tw) / 2, y), text, font=font, fill=fill)

def rounded_pill(xy, radius, fill=None, outline=None, width=2):
    d.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)

# --- badge pill, top-left ---
badge_font = F(23)
badge_text = "LEI 14.133/2021 · ART. 71"
tw = text_w(badge_text, badge_font)
pad_x, pad_y = 24, 13
bx0, by0 = MARGIN, 64
bx1, by1 = bx0 + tw + pad_x * 2, by0 + 23 + pad_y * 2
rounded_pill((bx0, by0, bx1, by1), radius=(by1 - by0) // 2, outline=GOLD, width=2)
d.text((bx0 + pad_x, by0 + pad_y - 1), badge_text, font=badge_font, fill=GOLD)

# --- logo, top-right ---
logo = Image.open("/home/user/domina-posts/logo_domina.png").convert("RGBA")
logo_size = 105
logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
img.paste(logo, (W - MARGIN - logo_size, 54), logo)

# --- title, centered ---
title_font = F(58)
title_lines = [
    ("GANHAR A DISPUTA", NAVY),
    ("NÃO É O FIM.", GOLD),
    ("É SÓ O COMEÇO.", NAVY),
]
ty = 210
line_gap = 68
for line, color in title_lines:
    tw2 = text_w(line, title_font)
    d.text(((W - tw2) / 2, ty), line, font=title_font, fill=color)
    ty += line_gap

# --- subtitle, centered ---
sub_font = FR(26)
subtitle = "Depois do julgamento, a lei ainda exige adjudicação e homologação — e sua empresa segue sendo avaliada nesse intervalo."
sub_lines = wrap(subtitle, sub_font, 760)
sy = ty + 16
for line in sub_lines:
    center_text(sy, line, sub_font, SUBTITLE)
    sy += 34

# --- divider ---
dy = sy + 20
d.line([(MARGIN, dy), (W - MARGIN, dy)], fill=LINE, width=2)

# --- vertical timeline, centered ---
steps = [
    ("JULGAMENTO", "disputa encerrada, vencedor classificado", False),
    ("ADJUDICAÇÃO", "objeto é atribuído oficialmente ao vencedor", False),
    ("HOMOLOGAÇÃO", "autoridade superior confirma todo o processo", True),
    ("CONTRATO", "só agora vem a convocação para assinar", False),
]

tl_x = MARGIN + 14
label_font = F(25)
desc_font = FR(22)
y = dy + 34
row_h = 70
dot_r = 9

for i, (label, desc, hi) in enumerate(steps):
    cy = y + i * row_h
    if i < len(steps) - 1:
        d.line([(tl_x, cy + dot_r), (tl_x, cy + row_h + dot_r)], fill=LINE, width=3)
    dot_fill = GOLD if hi else OFFWHITE
    d.ellipse((tl_x - dot_r, cy, tl_x + dot_r, cy + dot_r * 2), fill=dot_fill, outline=(GOLD if hi else DOT_INACTIVE), width=3)
    tx = tl_x + 34
    label_color = GOLD if hi else NAVY
    d.text((tx, cy - 6), label, font=label_font, fill=label_color)
    d.text((tx, cy + 28), desc, font=desc_font, fill=SUBTITLE)

# --- footer note ---
fy = y + (len(steps) - 1) * row_h + 76
note_font = FR(20)
note = "Antes, atos separados. Hoje, a autoridade superior adjudica e homologa juntos."
note_lines = wrap(note, note_font, W - 2 * MARGIN)
ny = fy
for line in note_lines:
    center_text(ny, line, note_font, SUBTITLE)
    ny += 27

# --- CTA pill, centered, bottom ---
cta_font = F(28)
cta_text = "Fale com a Domina no direct  →"
tw3 = text_w(cta_text, cta_font)
pad_x3, pad_y3 = 36, 20
cy1 = H - 78
cy0 = cy1 - (23 + pad_y3 * 2)
cx0 = (W - (tw3 + pad_x3 * 2)) / 2
cx1 = cx0 + tw3 + pad_x3 * 2
rounded_pill((cx0, cy0, cx1, cy1), radius=(cy1 - cy0) // 2, fill=GOLD)
d.text((cx0 + pad_x3, cy0 + pad_y3 - 2), cta_text, font=cta_font, fill=GOLD_DARK_TEXT)

out_path = "/home/user/domina-posts/images/post-2026-10-13-09h-adjudicacao-homologacao-art71.png"
img.save(out_path)
print("saved", out_path, img.size)
