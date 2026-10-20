#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Story 9h 2026-10-20: versao vertical (1080x1920) do post do feed sobre
limites do aditivo contratual (art. 125, Lei 14.133/2021) - 25% / 50%.
Mesma paleta azul marinho, mesmo conteudo, mesmas caracteristicas premium.
Area segura: ~250px livres no topo e embaixo.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920

NAVY = (16, 26, 48)
WHITE = (247, 247, 244)
SUBTITLE = (167, 177, 201)
GOLD = (212, 175, 55)
GOLD_DARK_TEXT = (24, 20, 4)
LINE = (56, 68, 96)

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

# ---- decorative corner brackets within safe area ----
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

y = SAFE_TOP + logo_size + 36

# ---- law badge, centered ----
badge_font = F(23)
badge_text = "LEI 14.133/2021 · ART. 125"
tw = text_w(badge_text, badge_font)
pad_x, pad_y = 24, 14
bx0 = CX - tw / 2 - pad_x
bx1 = CX + tw / 2 + pad_x
by0 = y
by1 = by0 + 23 + pad_y * 2
d.rounded_rectangle((bx0, by0, bx1, by1), radius=(by1 - by0) // 2, outline=GOLD, width=2)
d.text((bx0 + pad_x, by0 + pad_y - 1), badge_text, font=badge_font, fill=GOLD)

y = by1 + 64

# ---- title, centered ----
title_font = F(60)
title_lines = [
    ("SEU CONTRATO", WHITE),
    ("PODE CRESCER —", WHITE),
    ("MAS SÓ ATÉ AQUI", GOLD),
]
for line, color in title_lines:
    center_text(CX, y, line, title_font, color)
    y += 72

y += 26

# ---- subtitle, centered ----
sub_font = FR(29)
subtitle = "A Lei 14.133/2021 limita o quanto a Administração pode acrescentar ou suprimir no seu contrato sem abrir nova licitação."
sub_lines = wrap(subtitle, sub_font, W - 2 * MARGIN - 40)
for line in sub_lines:
    center_text(CX, y, line, sub_font, SUBTITLE)
    y += 38

y += 40
d.line([(MARGIN + 40, y), (W - MARGIN - 40, y)], fill=LINE, width=2)
y += 70

# ---- two big stat columns ----
stat_top = y
col_w = (W - 2 * MARGIN) // 2
stats = [
    ("25%", "ACRÉSCIMO OU SUPRESSÃO", "regra geral — obras, serviços e compras"),
    ("50%", "ACRÉSCIMO", "reforma de edifício ou equipamento"),
]
num_font = F(104)
label_font = F(24)
desc_font = FR(22)

max_bottom = stat_top
for i, (num, label, desc) in enumerate(stats):
    col_cx = MARGIN + col_w * i + col_w // 2
    yy = stat_top
    center_text(col_cx, yy, num, num_font, GOLD)
    yy += 124
    for lline in wrap(label, label_font, col_w - 30):
        center_text(col_cx, yy, lline, label_font, WHITE)
        yy += 32
    yy += 6
    for dline in wrap(desc, desc_font, col_w - 50):
        center_text(col_cx, yy, dline, desc_font, SUBTITLE)
        yy += 30
    max_bottom = max(max_bottom, yy)

d.line([(CX, stat_top + 10), (CX, max_bottom - 14)], fill=LINE, width=2)

y = max_bottom + 50
d.line([(MARGIN + 40, y), (W - MARGIN - 40, y)], fill=LINE, width=2)
y += 46

# ---- fine print ----
note_font = FR(24)
note = "O contratado é obrigado a aceitar, dentro desses limites, nas mesmas condições do contrato original."
for line in wrap(note, note_font, W - 2 * MARGIN - 20):
    center_text(CX, y, line, note_font, SUBTITLE)
    y += 32

y += 50

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

assert y + 30 <= SAFE_BOTTOM, f"content overflow into unsafe bottom area: {y+30} > {SAFE_BOTTOM}"

img.save("/tmp/story.png")
img.save("/home/user/domina-posts/images/story-2026-10-20-09h-limite-aditivo-contratual-art125.png")
print("saved", img.size, "content bottom:", y + 30, "safe bottom:", SAFE_BOTTOM)
