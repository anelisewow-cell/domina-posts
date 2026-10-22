#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Story 9h 2026-10-22: versao vertical (1080x1920) do post do feed sobre
modo de disputa aberto x fechado no pregao eletronico (art. 56, Lei
14.133/2021). Mesma paleta azul marinho, mesmo conteudo, mesmas
caracteristicas premium. Area segura: ~250px livres no topo e embaixo.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920

NAVY = (14, 23, 45)
WHITE = (247, 247, 244)
SUBTITLE = (167, 177, 201)
GOLD = (212, 175, 55)
GOLD_DARK_TEXT = (24, 20, 4)
LINE = (58, 70, 98)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
def F(size):
    return ImageFont.truetype(FONT_DIR + "DejaVuSans-Bold.ttf", size)
def FR(size):
    return ImageFont.truetype(FONT_DIR + "DejaVuSans.ttf", size)

img = Image.new("RGB", (W, H), NAVY)
d = ImageDraw.Draw(img)
MARGIN = 90
CX = W // 2
SAFE_TOP = 250
SAFE_BOTTOM = H - 250

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

def center_text(cx, y, text, font, fill):
    tw = text_w(text, font)
    d.text((cx - tw / 2, y), text, font=font, fill=fill)

# ---- decorative corner brackets within safe area (top-right / bottom-left) ----
bl = 50
d.line([(W - MARGIN + 10, SAFE_TOP - 6), (W - MARGIN + 10, SAFE_TOP - 6 + bl)], fill=GOLD, width=3)
d.line([(W - MARGIN + 10, SAFE_TOP - 6), (W - MARGIN + 10 - bl, SAFE_TOP - 6)], fill=GOLD, width=3)
d.line([(MARGIN - 10, SAFE_BOTTOM + 6), (MARGIN - 10, SAFE_BOTTOM + 6 - bl)], fill=GOLD, width=3)
d.line([(MARGIN - 10, SAFE_BOTTOM + 6), (MARGIN - 10 + bl, SAFE_BOTTOM + 6)], fill=GOLD, width=3)

# ---- logo, centered, top of safe area ----
logo = Image.open("/home/user/domina-posts/logo_domina.png").convert("RGBA")
logo_size = 110
logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
img.paste(logo, (CX - logo_size // 2, SAFE_TOP), logo)

y = SAFE_TOP + logo_size + 40

# ---- law badge, centered ----
badge_font = F(23)
badge_text = "LEI 14.133/2021 · ART. 56"
tw = text_w(badge_text, badge_font)
pad_x, pad_y = 24, 14
bx0 = CX - tw / 2 - pad_x
bx1 = CX + tw / 2 + pad_x
by0 = y
by1 = by0 + 23 + pad_y * 2
d.rounded_rectangle((bx0, by0, bx1, by1), radius=(by1 - by0) // 2, outline=GOLD, width=2)
center_text(CX, by0 + pad_y - 1, badge_text, badge_font, GOLD)

y = by1 + 56

# ---- title, centered ----
title_font = F(58)
title_lines = [
    ("SEU PREGÃO É", WHITE),
    ("ABERTO OU", WHITE),
    ("FECHADO?", GOLD),
]
for line, color in title_lines:
    center_text(CX, y, line, title_font, color)
    y += 70

y += 28

# ---- subtitle, centered ----
sub_font = FR(29)
subtitle = "A Lei 14.133/2021 prevê dois modos de disputa no pregão — e cada um exige uma estratégia de preço diferente."
sub_lines = wrap(subtitle, sub_font, W - 2 * MARGIN - 40)
for line in sub_lines:
    center_text(CX, y, line, sub_font, SUBTITLE)
    y += 38

y += 44
d.line([(MARGIN + 40, y), (W - MARGIN - 40, y)], fill=LINE, width=2)
y += 64

# ---- OU comparison cards ----
gap = 40
col_w = (W - 2 * MARGIN - gap) // 2
card_top = y
num_font = F(30)
label_font = F(32)
desc_font = FR(23)

cards = [
    ("01", "ABERTO", "Lances públicos e sucessivos. Você acompanha e melhora a oferta."),
    ("02", "FECHADO", "Proposta sigilosa até a abertura. Não há lances — só uma chance."),
]

card_bottoms = []
for i, (num, label, desc) in enumerate(cards):
    cx0 = MARGIN + i * (col_w + gap)
    cx1 = cx0 + col_w
    col_cx = cx0 + col_w // 2
    yy = card_top + 32
    center_text(col_cx, yy, num, num_font, GOLD)
    yy += 48
    center_text(col_cx, yy, label, label_font, WHITE)
    yy += 48
    for dline in wrap(desc, desc_font, col_w - 50):
        center_text(col_cx, yy, dline, desc_font, SUBTITLE)
        yy += 31
    yy += 30
    d.rounded_rectangle((cx0, card_top, cx1, yy), radius=20, outline=LINE, width=2)
    card_bottoms.append(yy)

card_bottom = max(card_bottoms)
vs_r = 32
vs_cy = card_top + (card_bottom - card_top) // 2
d.ellipse((CX - vs_r, vs_cy - vs_r, CX + vs_r, vs_cy + vs_r), fill=NAVY, outline=GOLD, width=2)
vs_font = F(23)
tw = text_w("OU", vs_font)
d.text((CX - tw / 2, vs_cy - 15), "OU", font=vs_font, fill=GOLD)

y = card_bottom + 56
d.line([(MARGIN + 40, y), (W - MARGIN - 40, y)], fill=LINE, width=2)
y += 60

# ---- highlight callout ----
stat_font = F(60)
for line in ["CONFIRA NO EDITAL", "ANTES DE PRECIFICAR"]:
    center_text(CX, y, line, stat_font, GOLD)
    y += 70

y += 20

note_font = FR(26)
note = "No modo fechado não existe segunda chance de lance — a primeira proposta já precisa ser a melhor."
for line in wrap(note, note_font, W - 2 * MARGIN - 30):
    center_text(CX, y, line, note_font, SUBTITLE)
    y += 34

y += 46

# ---- CTA pill button, centered ----
cta_font = F(30)
cta_text = "Fale com a Domina no direct  →"
tw = text_w(cta_text, cta_font)
pad_x, pad_y = 40, 22
cta_x0 = CX - tw / 2 - pad_x
cta_x1 = CX + tw / 2 + pad_x
cta_y0 = y
cta_y1 = cta_y0 + 30 + pad_y * 2
d.rounded_rectangle((cta_x0, cta_y0, cta_x1, cta_y1), radius=(cta_y1 - cta_y0) // 2, fill=GOLD)
d.text((CX - tw / 2, cta_y0 + pad_y - 1), cta_text, font=cta_font, fill=GOLD_DARK_TEXT)

y = cta_y1 + 34
tag_font = FR(23)
center_text(CX, y, "@domina.licitacao", tag_font, SUBTITLE)

print("content bottom:", y + 30, "safe bottom:", SAFE_BOTTOM)

img.save("/tmp/story.png")
print("saved", img.size)
