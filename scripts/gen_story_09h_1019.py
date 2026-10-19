#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Story version (1080x1920) of the 2026-10-19 09h feed post: representacao
direta ao TCU sem esgotar recurso administrativo (Acordao 1.063/2026-
Plenario). Mesma paleta azul marinho, mesmo conteudo, composicao vertical
centralizada com ~250px livres no topo e embaixo."""
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920

NAVY = (14, 25, 50)
WHITE = (247, 246, 240)
SUBTITLE = (164, 177, 203)
GOLD = (212, 175, 55)
GOLD_DARK_TEXT = (24, 20, 4)
LINE = (54, 68, 100)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
def F(size):
    return ImageFont.truetype(FONT_DIR + "DejaVuSans-Bold.ttf", size)
def FR(size):
    return ImageFont.truetype(FONT_DIR + "DejaVuSans.ttf", size)

img = Image.new("RGB", (W, H), NAVY)
d = ImageDraw.Draw(img)
MARGIN = 96

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

SAFE_TOP = 250
SAFE_BOTTOM = H - 250

y = SAFE_TOP

# ---- logo, centered ----
logo = Image.open("/home/user/domina-posts/logo_domina.png").convert("RGBA")
logo_size = 120
logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
img.paste(logo, ((W - logo_size) // 2, y), logo)
y += logo_size + 54

# ---- badge pill, centered ----
badge_font = F(24)
badge_text = "LEI 14.133/2021 · ART. 170, § 4º"
tw = text_w(badge_text, badge_font)
pad_x, pad_y = 24, 13
bx0 = (W - (tw + pad_x * 2)) / 2
bx1 = bx0 + tw + pad_x * 2
by0 = y
by1 = by0 + 24 + pad_y * 2
d.rounded_rectangle((bx0, by0, bx1, by1), radius=(by1 - by0) // 2, outline=GOLD, width=2)
d.text((bx0 + pad_x, by0 + pad_y - 1), badge_text, font=badge_font, fill=GOLD)
y = by1 + 64

# ---- title, centered ----
title_font = F(66)
title_lines = [
    ("SEU RECURSO", WHITE),
    ("TRAVOU NO", WHITE),
    ("ÓRGÃO?", GOLD),
]
for line, color in title_lines:
    center_text(y, line, title_font, color)
    y += 80

y += 20

# ---- subtitle, centered ----
sub_font = FR(30)
subtitle = "Você não precisa esperar o julgamento interno para levar a irregularidade ao órgão de controle."
sub_lines = wrap(subtitle, sub_font, 860)
for line in sub_lines:
    center_text(y, line, sub_font, SUBTITLE)
    y += 40

# ---- divider ----
y += 30
d.line([(MARGIN, y), (W - MARGIN, y)], fill=LINE, width=2)
y += 54

# ---- highlight card ----
card_y0 = y
card_pad = 44
card_h = 360
d.rounded_rectangle((MARGIN, card_y0, W - MARGIN, card_y0 + card_h), radius=24, outline=GOLD, width=2)

tag_font = F(27)
tag_text = "TCU · ACÓRDÃO 1.063/2026-PLENÁRIO"
tw2 = text_w(tag_text, tag_font)
d.text(((W - tw2) / 2, card_y0 + 40), tag_text, font=tag_font, fill=GOLD)

body_font = FR(29)
body_text = "A empresa pode representar direto ao TCU contra uma irregularidade na licitação mesmo com recurso administrativo ainda pendente no próprio órgão — não é preciso esgotar essa via primeiro."
body_lines = wrap(body_text, body_font, W - 2 * MARGIN - card_pad * 2)
yy = card_y0 + 110
for line in body_lines:
    center_text(yy, line, body_font, WHITE)
    yy += 40

y = card_y0 + card_h + 48

# ---- footer note, centered ----
note_font = FR(23)
note = "Relator Min. Benjamin Zymler — base legal: direito de representação aos órgãos de controle (art. 170, § 4º)."
note_lines = wrap(note, note_font, W - 2 * MARGIN)
for line in note_lines:
    center_text(y, line, note_font, SUBTITLE)
    y += 32

# ---- CTA pill, centered ----
cta_y = SAFE_BOTTOM - 110
cta_font = F(32)
cta_text = "Fale com a Domina no direct  →"
tw3 = text_w(cta_text, cta_font)
pad_x3, pad_y3 = 40, 22
cy0 = cta_y
cy0 = max(cy0, y + 36)
cy1 = cy0 + (26 + pad_y3 * 2)
cx0 = (W - (tw3 + pad_x3 * 2)) / 2
cx1 = cx0 + tw3 + pad_x3 * 2
d.rounded_rectangle((cx0, cy0, cx1, cy1), radius=(cy1 - cy0) // 2, fill=GOLD)
d.text((cx0 + pad_x3, cy0 + pad_y3 - 2), cta_text, font=cta_font, fill=GOLD_DARK_TEXT)

out_path = "/home/user/domina-posts/images/story-2026-10-19-1019-representacao-tcu.png"
img.save(out_path)
print("saved", out_path, img.size)
