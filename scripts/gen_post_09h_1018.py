#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Post 9h 2026-10-18: impugnacao de edital (art. 164, Lei 14.133/2021).
Angulo: qualquer pessoa (nao so quem vai disputar) pode impugnar um edital
por irregularidade, ou pedir esclarecimento - prazo de 3 dias uteis antes
da abertura do certame. Tema novo, nao coberto nos ultimos 30 dias.

Paleta: branco gelo (oposta ao ultimo post publicado, que foi azul marinho
solido). Layout variado em relacao aos posts recentes: logo no topo
ESQUERDO, badge no topo DIREITO, titulo e subtitulo alinhados a DIREITA,
bloco central em CARD com borda dourada, comparacao em DUAS COLUNAS
abaixo, CTA alinhado a direita, bracket decorativo no canto INFERIOR
ESQUERDO. Posicionamento vertical por cursor (evita sobreposicao).
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1080

BG = (247, 246, 240)
NAVY = (18, 30, 58)
NAVY_SOFT = (33, 48, 82)
SUBTITLE = (104, 116, 142)
GOLD = (196, 155, 58)
GOLD_DARK_TEXT = (24, 20, 4)
LINE = (214, 210, 198)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
def F(size):
    return ImageFont.truetype(FONT_DIR + "DejaVuSans-Bold.ttf", size)
def FR(size):
    return ImageFont.truetype(FONT_DIR + "DejaVuSans.ttf", size)

img = Image.new("RGB", (W, H), BG)
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

def right_text(y, text, font, fill, right_x):
    tw = text_w(text, font)
    d.text((right_x - tw, y), text, font=font, fill=fill)

# ---- logo, top-left ----
logo = Image.open("/home/user/domina-posts/logo_domina.png").convert("RGBA")
logo_size = 105
logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
img.paste(logo, (MARGIN, 58), logo)

# ---- badge pill, top-right ----
badge_font = F(22)
badge_text = "LEI 14.133/2021 · ART. 164"
tw = text_w(badge_text, badge_font)
pad_x, pad_y = 24, 13
bx1 = W - MARGIN
bx0 = bx1 - (tw + pad_x * 2)
by0 = 80
by1 = by0 + 23 + pad_y * 2
d.rounded_rectangle((bx0, by0, bx1, by1), radius=(by1 - by0) // 2, outline=GOLD, width=2)
d.text((bx0 + pad_x, by0 + pad_y - 1), badge_text, font=badge_font, fill=GOLD)

right_x = W - MARGIN

# ---- title, right-aligned ----
title_font = F(54)
title_lines = [
    ("QUALQUER PESSOA", NAVY),
    ("PODE IMPUGNAR", NAVY),
    ("O EDITAL.", GOLD),
]
y = 222
for line, color in title_lines:
    right_text(y, line, title_font, color, right_x)
    y += 64

# ---- subtitle, right-aligned ----
y += 16
sub_font = FR(26)
subtitle = "Não precisa ser licitante: a lei garante a qualquer pessoa, física ou jurídica, o direito de contestar irregularidades no edital."
sub_lines = wrap(subtitle, sub_font, 820)
for line in sub_lines:
    right_text(y, line, sub_font, SUBTITLE, right_x)
    y += 34

# ---- divider ----
y += 22
d.line([(MARGIN, y), (W - MARGIN, y)], fill=LINE, width=2)
y += 36

# ---- stat card ----
card_y0 = y
card_h = 128
card_y1 = card_y0 + card_h
d.rounded_rectangle((MARGIN, card_y0, W - MARGIN, card_y1), radius=18, outline=GOLD, width=2)

num_font = F(70)
num_text = "3"
num_x = MARGIN + 42
num_y = card_y0 + (card_h - 70) // 2 - 6
d.text((num_x, num_y), num_text, font=num_font, fill=GOLD)

label_font = F(25)
label_x = num_x + text_w(num_text, num_font) + 24
d.text((label_x, card_y0 + 28), "DIAS ÚTEIS", font=label_font, fill=NAVY)
desc_font = FR(22)
desc_lines = [
    "antes da abertura do certame — prazo para",
    "impugnar o edital ou pedir esclarecimento.",
]
dyy = card_y0 + 66
for line in desc_lines:
    d.text((label_x, dyy), line, font=desc_font, fill=SUBTITLE)
    dyy += 28

y = card_y1 + 44

# ---- two-column comparison ----
col_label_font = F(23)
col_body_font = FR(22)
mid_x = W // 2
col_w = (W - 2 * MARGIN - 60) // 2
right_col_x = mid_x + 60

col_y0 = y
d.text((MARGIN, col_y0), "IMPUGNAÇÃO", font=col_label_font, fill=GOLD)
d.text((right_col_x, col_y0), "ESCLARECIMENTO", font=col_label_font, fill=GOLD)

left_body = wrap("Contesta uma irregularidade e exige correção antes da disputa abrir.", col_body_font, col_w)
right_body = wrap("Tira uma dúvida sobre o texto do edital, sem apontar ilegalidade.", col_body_font, col_w)

yy = col_y0 + 34
for line in left_body:
    d.text((MARGIN, yy), line, font=col_body_font, fill=NAVY_SOFT)
    yy += 29
left_end = yy

yy = col_y0 + 34
for line in right_body:
    d.text((right_col_x, yy), line, font=col_body_font, fill=NAVY_SOFT)
    yy += 29
right_end = yy

col_bottom = max(left_end, right_end)
d.line([(mid_x, col_y0), (mid_x, col_bottom - 4)], fill=LINE, width=2)

y = col_bottom + 20

# ---- footer note ----
note_font = FR(20)
note = "A administração responde em até 3 dias úteis, antes da abertura (art. 164, § único)."
note_lines = wrap(note, note_font, W - 2 * MARGIN - 40)
for line in note_lines:
    d.text((MARGIN, y), line, font=note_font, fill=SUBTITLE)
    y += 27

# ---- CTA pill, right-aligned, bottom ----
cta_font = F(28)
cta_text = "Fale com a Domina no direct  →"
tw3 = text_w(cta_text, cta_font)
pad_x3, pad_y3 = 36, 20
cy1 = H - 60
cy0 = cy1 - (23 + pad_y3 * 2)
cy0 = max(cy0, y + 24)
cy1 = cy0 + (23 + pad_y3 * 2)
cx1 = W - MARGIN
cx0 = cx1 - (tw3 + pad_x3 * 2)
d.rounded_rectangle((cx0, cy0, cx1, cy1), radius=(cy1 - cy0) // 2, fill=GOLD)
d.text((cx0 + pad_x3, cy0 + pad_y3 - 2), cta_text, font=cta_font, fill=GOLD_DARK_TEXT)

# ---- decorative corner bracket, bottom-left ----
bx0d, by0d = MARGIN, cy1
d.line([(bx0d, by0d), (bx0d + 50, by0d)], fill=GOLD, width=3)
d.line([(bx0d, by0d - 50), (bx0d, by0d)], fill=GOLD, width=3)

print("final y before CTA:", y, "cta top:", cy0, "cta bottom:", cy1, "H:", H)

out_path = "/home/user/domina-posts/images/post-2026-10-18-09h-impugnacao-edital-art164.png"
img.save(out_path)
print("saved", out_path, img.size)
