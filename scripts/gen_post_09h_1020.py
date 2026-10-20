#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Post 9h 2026-10-20: limites do aditivo contratual (art. 125, Lei 14.133/2021)
- 25% de acrescimo ou supressao (regra geral, obras/servicos/compras) e 50%
de acrescimo para reforma de edificio ou equipamento. Angulo: empresa ja
contratada com o governo precisa saber ate onde e obrigada a aceitar que o
contrato cresca (ou diminua) sem nova licitacao - planejamento de capacidade
e fluxo de caixa. Tema novo: nenhum post dos ultimos 30 dias tratou de
alteracao/aditivo contratual (art. 125); o mais proximo foi reequilibrio
economico-financeiro (reajuste/repactuacao/revisao, 27/09), que e assunto
distinto (preco do contrato, nao quantidade/objeto).

Paleta: azul marinho (oposta ao ultimo post publicado, 19/10 18h, que foi
branco gelo - confirmado por amostragem de pixel do PNG local, fundo
(247,246,240)).

Layout variado: logo no canto SUPERIOR ESQUERDO (ultimo post navy, 19/10 9h,
tinha badge na esquerda e logo na direita - aqui invertido), badge de lei no
canto SUPERIOR DIREITO, titulo alinhado a ESQUERDA, elemento central em
DUAS COLUNAS DE ESTATISTICA GRANDE lado a lado (25% / 50% - formato inedito
nos posts recentes, que usaram card unico de citacao ou 3 passos em linha),
CTA alinhado a esquerda, brackets decorativos no canto SUPERIOR DIREITO e
INFERIOR ESQUERDO (invertido em relacao ao post de 18/10, que usava
inferior-direito).
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1080

NAVY = (16, 26, 48)
NAVY_LIGHT = (26, 38, 66)
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
MARGIN = 72
CX = W // 2

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

# ---- decorative corner brackets (top-right / bottom-left) ----
bl = 46
d.line([(W - MARGIN + 14, 40), (W - MARGIN + 14, 40 + bl)], fill=GOLD, width=3)
d.line([(W - MARGIN + 14, 40), (W - MARGIN + 14 - bl, 40)], fill=GOLD, width=3)
d.line([(MARGIN - 14, H - 40), (MARGIN - 14, H - 40 - bl)], fill=GOLD, width=3)
d.line([(MARGIN - 14, H - 40), (MARGIN - 14 + bl, H - 40)], fill=GOLD, width=3)

# ---- logo, top-left ----
logo = Image.open("/home/user/domina-posts/logo_domina.png").convert("RGBA")
logo_size = 100
logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
img.paste(logo, (MARGIN, 56), logo)

# ---- law badge, top-right ----
badge_font = F(20)
badge_text = "LEI 14.133/2021 · ART. 125"
tw = text_w(badge_text, badge_font)
pad_x, pad_y = 20, 12
bx1 = W - MARGIN
bx0 = bx1 - tw - pad_x * 2
by0 = 56 + (logo_size - (21 + pad_y * 2)) // 2
by1 = by0 + 21 + pad_y * 2
d.rounded_rectangle((bx0, by0, bx1, by1), radius=(by1 - by0) // 2, outline=GOLD, width=2)
d.text((bx0 + pad_x, by0 + pad_y - 1), badge_text, font=badge_font, fill=GOLD)

y = 56 + logo_size + 44

# ---- title, left-aligned ----
title_font = F(50)
title_lines = [
    ("SEU CONTRATO", WHITE),
    ("PODE CRESCER —", WHITE),
    ("MAS SÓ ATÉ AQUI", GOLD),
]
for line, color in title_lines:
    d.text((MARGIN, y), line, font=title_font, fill=color)
    y += 60

y += 18

# ---- subtitle, left-aligned ----
sub_font = FR(25)
subtitle = "A Lei 14.133/2021 limita o quanto a Administração pode acrescentar ou suprimir no seu contrato sem abrir uma nova licitação."
sub_lines = wrap(subtitle, sub_font, W - 2 * MARGIN - 20)
for line in sub_lines:
    d.text((MARGIN, y), line, font=sub_font, fill=SUBTITLE)
    y += 33

y += 30
d.line([(MARGIN, y), (W - MARGIN, y)], fill=LINE, width=2)
y += 54

# ---- two big stat columns ----
stat_top = y
col_w = (W - 2 * MARGIN) // 2
stats = [
    ("25%", "ACRÉSCIMO OU SUPRESSÃO", "regra geral — obras, serviços e compras"),
    ("50%", "ACRÉSCIMO", "reforma de edifício ou equipamento"),
]
num_font = F(92)
label_font = F(21)
desc_font = FR(19)

max_bottom = stat_top
for i, (num, label, desc) in enumerate(stats):
    col_cx = MARGIN + col_w * i + col_w // 2
    yy = stat_top
    center_text(col_cx, yy, num, num_font, GOLD)
    yy += 108
    center_text(col_cx, yy, label, label_font, WHITE)
    yy += 32
    for dline in wrap(desc, desc_font, col_w - 40):
        center_text(col_cx, yy, dline, desc_font, SUBTITLE)
        yy += 26
    max_bottom = max(max_bottom, yy)

# vertical divider between columns
d.line([(CX, stat_top + 6), (CX, max_bottom - 10)], fill=LINE, width=2)

y = max_bottom + 34
d.line([(MARGIN, y), (W - MARGIN, y)], fill=LINE, width=2)
y += 32

# ---- fine print ----
note_font = FR(20)
note = "O contratado é obrigado a aceitar, dentro desses limites, nas mesmas condições do contrato original."
for line in wrap(note, note_font, W - 2 * MARGIN):
    d.text((MARGIN, y), line, font=note_font, fill=SUBTITLE)
    y += 27

y += 30

# ---- CTA pill button, left-aligned ----
cta_font = F(26)
cta_text = "Fale com a Domina no direct  →"
tw = text_w(cta_text, cta_font)
pad_x, pad_y = 34, 18
cta_x0 = MARGIN
cta_x1 = cta_x0 + tw + pad_x * 2
cta_y0 = y
cta_y1 = cta_y0 + 26 + pad_y * 2
d.rounded_rectangle((cta_x0, cta_y0, cta_x1, cta_y1), radius=(cta_y1 - cta_y0) // 2, fill=GOLD)
d.text((cta_x0 + pad_x, cta_y0 + pad_y - 1), cta_text, font=cta_font, fill=GOLD_DARK_TEXT)

img.save("/tmp/post.png")
img.save("/home/user/domina-posts/images/post-2026-10-20-09h-limite-aditivo-contratual-art125.png")
print("saved", img.size)
