#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Story 9h 2026-10-18: mesma capa do feed (impugnacao de edital, art. 164),
versao vertical 1080x1920, centralizada, com areas seguras de 250px no
topo e embaixo."""
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920

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
MARGIN = 90
SAFE_TOP = 250
SAFE_BOTTOM = 250
content_w = W - 2 * MARGIN

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

def ctext(y, text, font, fill):
    tw = text_w(text, font)
    d.text(((W - tw) // 2, y), text, font=font, fill=fill)

y = SAFE_TOP

# ---- logo, centered ----
logo = Image.open("/home/user/domina-posts/logo_domina.png").convert("RGBA")
logo_size = 110
logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
img.paste(logo, ((W - logo_size) // 2, y), logo)
y += logo_size + 44

# ---- badge pill, centered ----
badge_font = F(28)
badge_text = "LEI 14.133/2021 · ART. 164"
tw = text_w(badge_text, badge_font)
pad_x, pad_y = 30, 16
pill_w = tw + pad_x * 2
pill_h = 28 + pad_y * 2
d.rounded_rectangle(((W - pill_w) // 2, y, (W + pill_w) // 2, y + pill_h), radius=pill_h // 2, outline=GOLD, width=2)
d.text(((W - pill_w) // 2 + pad_x, y + pad_y - 2), badge_text, font=badge_font, fill=GOLD)
y += pill_h + 64

# ---- title, centered ----
title_font = F(70)
title_lines = [
    ("QUALQUER PESSOA", NAVY),
    ("PODE IMPUGNAR", NAVY),
    ("O EDITAL.", GOLD),
]
for line, color in title_lines:
    ctext(y, line, title_font, color)
    y += 80

y += 34

# ---- subtitle, centered ----
sub_font = FR(34)
subtitle = "Não precisa ser licitante: a lei garante a qualquer pessoa, física ou jurídica, o direito de contestar irregularidades no edital."
sub_lines = wrap(subtitle, sub_font, content_w - 60)
for line in sub_lines:
    ctext(y, line, sub_font, SUBTITLE)
    y += 46

y += 30
d.line([(MARGIN + 60, y), (W - MARGIN - 60, y)], fill=LINE, width=2)
y += 60

# ---- stat card, centered block ----
card_w = content_w - 40
card_h = 220
card_x0 = (W - card_w) // 2
card_y0 = y
card_y1 = card_y0 + card_h
d.rounded_rectangle((card_x0, card_y0, card_x0 + card_w, card_y1), radius=24, outline=GOLD, width=3)

num_font = F(110)
num_text = "3"
tw_num = text_w(num_text, num_font)
label_font = F(36)
label_text = "DIAS ÚTEIS"
tw_label = text_w(label_text, label_font)
desc_font = FR(28)
desc_lines = [
    "antes da abertura do certame — prazo para",
    "impugnar o edital ou pedir esclarecimento.",
]

inner_y = card_y0 + 36
block_x = card_x0 + 60
d.text((block_x, inner_y), num_text, font=num_font, fill=GOLD)
d.text((block_x + tw_num + 32, inner_y + 26), label_text, font=label_font, fill=NAVY)
dyy = inner_y + 26 + 50
for line in desc_lines:
    d.text((block_x + tw_num + 32, dyy), line, font=desc_font, fill=SUBTITLE)
    dyy += 36

y = card_y1 + 64

# ---- two-column comparison, centered pair ----
col_label_font = F(30)
col_body_font = FR(27)
gap = 70
col_w = (content_w - gap) // 2
left_x = (W - (col_w * 2 + gap)) // 2
right_x = left_x + col_w + gap

d.text((left_x, y), "IMPUGNAÇÃO", font=col_label_font, fill=GOLD)
d.text((right_x, y), "ESCLARECIMENTO", font=col_label_font, fill=GOLD)

left_body = wrap("Contesta uma irregularidade e exige correção antes da disputa abrir.", col_body_font, col_w)
right_body = wrap("Tira uma dúvida sobre o texto do edital, sem apontar ilegalidade.", col_body_font, col_w)

yy = y + 46
for line in left_body:
    d.text((left_x, yy), line, font=col_body_font, fill=NAVY_SOFT)
    yy += 38
left_end = yy

yy = y + 46
for line in right_body:
    d.text((right_x, yy), line, font=col_body_font, fill=NAVY_SOFT)
    yy += 38
right_end = yy

col_bottom = max(left_end, right_end)
mid_x = W // 2
d.line([(mid_x, y), (mid_x, col_bottom - 6)], fill=LINE, width=2)

y = col_bottom + 30

# ---- footer note, centered ----
note_font = FR(26)
note = "A administração responde em até 3 dias úteis, antes da abertura (art. 164, § único)."
note_lines = wrap(note, note_font, content_w - 80)
for line in note_lines:
    ctext(y, line, note_font, SUBTITLE)
    y += 34

# ---- CTA pill, centered, above bottom safe zone ----
cta_font = F(36)
cta_text = "Fale com a Domina no direct  →"
tw3 = text_w(cta_text, cta_font)
btn_pad_x, btn_pad_y = 46, 26
btn_w = tw3 + btn_pad_x * 2
btn_h = 32 + btn_pad_y * 2
btn_y0 = min(max(y + 24, H - SAFE_BOTTOM - btn_h - 40), H - SAFE_BOTTOM - btn_h)
btn_x0 = (W - btn_w) // 2
d.rounded_rectangle((btn_x0, btn_y0, btn_x0 + btn_w, btn_y0 + btn_h), radius=btn_h // 2, fill=GOLD)
d.text((btn_x0 + btn_pad_x, btn_y0 + btn_pad_y - 2), cta_text, font=cta_font, fill=GOLD_DARK_TEXT)

print("content bottom:", y, "cta top:", btn_y0, "cta bottom:", btn_y0 + btn_h, "safe bottom line:", H - SAFE_BOTTOM)

out_path = "/home/user/domina-posts/images/story-2026-10-18-1792325607-impugnacao-edital.png"
img.save(out_path)
print("saved", out_path, img.size)
