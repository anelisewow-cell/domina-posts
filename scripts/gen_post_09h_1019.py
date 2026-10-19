#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Post 9h 2026-10-19: representacao direta ao TCU, sem esgotar recurso
administrativo (Acordao 1.063/2026-Plenario, rel. Min. Benjamin Zymler,
TC 004.829/2026-3; fundamento art. 170, par. 4o da Lei 14.133/2021).
Tema novo: nenhum post dos ultimos 30 dias tratou de representacao ao
TCU / controle externo durante a fase recursal.

Paleta: azul marinho solido (oposta ao ultimo post confirmado, 18/10 9h,
que foi branco gelo). Layout variado em relacao ao 18/10 (titulo+subtitulo
alinhados a direita, card horizontal, colunas) e ao 13/10 18h (tudo
centralizado): aqui o titulo e o bloco todo ficam alinhados a ESQUERDA,
logo no topo DIREITO (nos ultimos dois posts estava no topo esquerdo),
badge no topo ESQUERDO, bloco central e um CARD unico com numero do
acordao em destaque (nao e estatistica gigante nem duas colunas), CTA
alinhado a ESQUERDA, bracket decorativo no canto INFERIOR DIREITO.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1080

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

# ---- badge pill, top-left ----
badge_font = F(21)
badge_text = "LEI 14.133/2021 · ART. 170, § 4º"
tw = text_w(badge_text, badge_font)
pad_x, pad_y = 22, 12
bx0, by0 = MARGIN, 80
bx1 = bx0 + tw + pad_x * 2
by1 = by0 + 22 + pad_y * 2
d.rounded_rectangle((bx0, by0, bx1, by1), radius=(by1 - by0) // 2, outline=GOLD, width=2)
d.text((bx0 + pad_x, by0 + pad_y - 1), badge_text, font=badge_font, fill=GOLD)

# ---- logo, top-right ----
logo = Image.open("/home/user/domina-posts/logo_domina.png").convert("RGBA")
logo_size = 105
logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
img.paste(logo, (W - MARGIN - logo_size, 54), logo)

# ---- title, left-aligned ----
title_font = F(58)
title_lines = [
    ("SEU RECURSO", WHITE),
    ("TRAVOU NO", WHITE),
    ("ÓRGÃO?", GOLD),
]
y = 232
for line, color in title_lines:
    d.text((MARGIN, y), line, font=title_font, fill=color)
    y += 68

# ---- subtitle, left-aligned ----
y += 14
sub_font = FR(26)
subtitle = "Você não precisa esperar o julgamento interno para levar a irregularidade ao órgão de controle."
sub_lines = wrap(subtitle, sub_font, 820)
for line in sub_lines:
    d.text((MARGIN, y), line, font=sub_font, fill=SUBTITLE)
    y += 34

# ---- divider ----
y += 22
d.line([(MARGIN, y), (W - MARGIN, y)], fill=LINE, width=2)
y += 40

# ---- highlight card ----
card_y0 = y
card_pad = 34
d.rounded_rectangle((MARGIN, card_y0, W - MARGIN, card_y0 + 238), radius=20, outline=GOLD, width=2)

tag_font = F(23)
d.text((MARGIN + card_pad, card_y0 + 26), "TCU · ACÓRDÃO 1.063/2026-PLENÁRIO", font=tag_font, fill=GOLD)

body_font = FR(25)
body_lines = [
    "A empresa pode representar direto ao TCU contra",
    "uma irregularidade na licitação mesmo com recurso",
    "administrativo ainda pendente no próprio órgão —",
    "não é preciso esgotar essa via primeiro.",
]
yy = card_y0 + 76
for line in body_lines:
    d.text((MARGIN + card_pad, yy), line, font=body_font, fill=WHITE)
    yy += 36

y = card_y0 + 238 + 36

# ---- footer note ----
note_font = FR(20)
note = "Relator Min. Benjamin Zymler — base legal: direito de representação aos órgãos de controle (art. 170, § 4º)."
note_lines = wrap(note, note_font, W - 2 * MARGIN)
for line in note_lines:
    d.text((MARGIN, y), line, font=note_font, fill=SUBTITLE)
    y += 27

# ---- CTA pill, left-aligned, bottom ----
cta_font = F(28)
cta_text = "Fale com a Domina no direct  →"
tw3 = text_w(cta_text, cta_font)
pad_x3, pad_y3 = 36, 20
cy1 = H - 64
cy0 = cy1 - (23 + pad_y3 * 2)
cy0 = max(cy0, y + 26)
cy1 = cy0 + (23 + pad_y3 * 2)
cx0 = MARGIN
cx1 = cx0 + tw3 + pad_x3 * 2
d.rounded_rectangle((cx0, cy0, cx1, cy1), radius=(cy1 - cy0) // 2, fill=GOLD)
d.text((cx0 + pad_x3, cy0 + pad_y3 - 2), cta_text, font=cta_font, fill=GOLD_DARK_TEXT)

# ---- decorative corner bracket, bottom-right ----
bx0d, by0d = W - MARGIN, cy1
d.line([(bx0d - 50, by0d), (bx0d, by0d)], fill=GOLD, width=3)
d.line([(bx0d, by0d - 50), (bx0d, by0d)], fill=GOLD, width=3)

print("final y before CTA:", y, "cta top:", cy0, "cta bottom:", cy1, "H:", H)

out_path = "/home/user/domina-posts/images/post-2026-10-19-09h-representacao-tcu-art170.png"
img.save(out_path)
print("saved", out_path, img.size)
