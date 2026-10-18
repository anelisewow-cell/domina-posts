#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Story 9h 2026-10-13: versao vertical do post sobre adjudicacao e
homologacao (art. 71, Lei 14.133/2021). Mesmo tema e paleta (branco gelo)
do post de feed do dia, conteudo centralizado na area segura de stories."""
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920

OFFWHITE = (247, 246, 240)
NAVY = (18, 30, 58)
SUBTITLE = (104, 116, 142)
GOLD = (212, 175, 55)
GOLD_DARK_TEXT = (24, 20, 4)
LINE = (214, 210, 198)
DOT_INACTIVE = (190, 186, 172)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
def font(size, bold=True):
    path = FONT_DIR + ("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf")
    return ImageFont.truetype(path, size)

img = Image.new("RGB", (W, H), OFFWHITE)
d = ImageDraw.Draw(img)

MARGIN = 90
SAFE_TOP = 250
SAFE_BOTTOM = 250
content_w = W - 2 * MARGIN

def text_w(s, f):
    bbox = d.textbbox((0, 0), s, font=f)
    return bbox[2] - bbox[0]

def wrap(text, f, max_w):
    words = text.split(" ")
    lines, cur = [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if text_w(trial, f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines

def center_text(y, text, f, fill):
    tw = text_w(text, f)
    d.text(((W - tw) / 2, y), text, font=f, fill=fill)

# ---- logo, centered, top safe area ----
logo = Image.open("/home/user/domina-posts/logo_domina.png").convert("RGBA")
logo_size = 115
logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
logo_x = (W - logo_size) // 2
logo_y = SAFE_TOP - logo_size - 30
img.paste(logo, (logo_x, logo_y), logo)

y = SAFE_TOP

# ---- badge pill, centered ----
f_tag = font(28)
tag_text = "LEI 14.133/2021 · ART. 71"
tw = text_w(tag_text, f_tag)
pad_x, pad_y = 30, 16
pill_w = tw + pad_x * 2
pill_h = 28 + pad_y * 2
pill_x0 = (W - pill_w) // 2
d.rounded_rectangle([pill_x0, y, pill_x0 + pill_w, y + pill_h], radius=pill_h // 2, outline=GOLD, width=2)
d.text((pill_x0 + pad_x, y + pad_y - 2), tag_text, font=f_tag, fill=GOLD)
y += pill_h + 64

# ---- title, centered ----
f_title = font(70)
title_lines = [
    ("GANHAR A DISPUTA", NAVY),
    ("NÃO É O FIM.", GOLD),
    ("É SÓ O COMEÇO.", NAVY),
]
for line, color in title_lines:
    tw = text_w(line, f_title)
    d.text(((W - tw) / 2, y), line, font=f_title, fill=color)
    y += 80

y += 30

# ---- subtitle, centered ----
f_sub = font(34, bold=False)
subtitle = "Depois do julgamento, a lei ainda exige adjudicação e homologação — e sua empresa segue sendo avaliada nesse intervalo."
sub_lines = wrap(subtitle, f_sub, content_w - 40)
for line in sub_lines:
    center_text(y, line, f_sub, SUBTITLE)
    y += 46

y += 28
d.line([(MARGIN + 60, y), (W - MARGIN - 60, y)], fill=LINE, width=2)
y += 56

# ---- vertical timeline, centered block ----
steps = [
    ("JULGAMENTO", "disputa encerrada, vencedor classificado", False),
    ("ADJUDICAÇÃO", "objeto é atribuído oficialmente ao vencedor", False),
    ("HOMOLOGAÇÃO", "autoridade superior confirma todo o processo", True),
    ("CONTRATO", "só agora vem a convocação para assinar", False),
]

label_font = font(32)
desc_font = font(27, bold=False)
row_h = 96
dot_r = 10

label_w = max(text_w(s[0], label_font) for s in steps)
desc_w = max(text_w(s[1], desc_font) for s in steps)
block_w = 34 + max(label_w, desc_w)
block_x0 = (W - block_w) // 2
tl_x = block_x0 + dot_r

for i, (label, desc, hi) in enumerate(steps):
    cy = y + i * row_h
    if i < len(steps) - 1:
        d.line([(tl_x, cy + dot_r), (tl_x, cy + row_h + dot_r)], fill=LINE, width=3)
    dot_fill = GOLD if hi else OFFWHITE
    d.ellipse((tl_x - dot_r, cy, tl_x + dot_r, cy + dot_r * 2), fill=dot_fill, outline=(GOLD if hi else DOT_INACTIVE), width=3)
    tx = tl_x + 34
    label_color = GOLD if hi else NAVY
    d.text((tx, cy - 8), label, font=label_font, fill=label_color)
    d.text((tx, cy + 32), desc, font=desc_font, fill=SUBTITLE)

y = y + (len(steps) - 1) * row_h + 92

# ---- footer note, centered ----
f_note = font(26, bold=False)
note = "Antes, atos separados. Hoje, a autoridade superior adjudica e homologa juntos."
note_lines = wrap(note, f_note, content_w - 40)
for line in note_lines:
    center_text(y, line, f_note, SUBTITLE)
    y += 36

# ---- CTA button, centered, above bottom safe zone ----
cta_text = "Fale com a Domina no direct  →"
f_cta = font(34)
tw = text_w(cta_text, f_cta)
btn_pad_x, btn_pad_y = 44, 26
btn_w = tw + btn_pad_x * 2
btn_h = 30 + btn_pad_y * 2
btn_y0 = min(max(y + 30, H - SAFE_BOTTOM - btn_h - 40), H - SAFE_BOTTOM - btn_h)
btn_x0 = (W - btn_w) // 2
d.rounded_rectangle([btn_x0, btn_y0, btn_x0 + btn_w, btn_y0 + btn_h], radius=btn_h // 2, fill=GOLD)
d.text((btn_x0 + btn_pad_x, btn_y0 + btn_pad_y - 2), cta_text, font=f_cta, fill=GOLD_DARK_TEXT)

out_path = "/home/user/domina-posts/images/story-2026-10-13-1791894188-adjudicacao-homologacao.png"
img.save(out_path)
print("saved", out_path, img.size, "cta bottom:", btn_y0 + btn_h, "safe bottom line:", H - SAFE_BOTTOM)
