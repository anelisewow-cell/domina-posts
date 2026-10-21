#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Post 9h 2026-10-21: licitacao deserta x fracassada (art. 75, III, Lei
14.133/2021). Angulo: distincao entre as duas hipoteses e a consequencia
pratica pouco conhecida - dentro de 1 ano, a Administracao pode contratar
diretamente (dispensa), mantendo as condicoes do edital original, desde que
o fracasso/deserção nao tenha decorrido de exigencia indevida do proprio
edital e a empresa mantenha a habilitacao. Tema novo: nenhum post dos
ultimos 30 dias tratou dessa hipotese de dispensa (o mais proximo foi
"novos valores de dispensa 2026", que trata de limites de VALOR, nao desta
hipotese de insucesso do certame).

Fonte: Lei 14.133/2021, art. 75, III, "a" (planalto.gov.br); TCU, Licitacoes
e Contratos, item 5.10.2.2 (licitacoesecontratos.tcu.gov.br).

Paleta: azul marinho (oposta ao ultimo post publicado, 20/10 18h, que foi
branco gelo - confirmado pelo comentario do script gen_post_18h_1020.py).

Layout variado: logo CENTRALIZADA no topo (ultimos posts tinham logo no
canto esquerdo ou direito - aqui centralizada, inedito nos posts recentes),
badge de lei tambem centralizada abaixo da logo, titulo CENTRALIZADO (ultimo
post navy era alinhado a esquerda), elemento central em formato "VS" -
duas colunas comparativas lado a lado com circulo dourado "VS" no meio
(formato inedito - diferente do card unico e das duas colunas numericas
dos posts anteriores), estatistica de destaque unica abaixo (nao duas),
CTA centralizado, brackets decorativos no canto SUPERIOR-ESQUERDO e
INFERIOR-DIREITO (invertido em relacao ao ultimo post navy, que usava
superior-direito/inferior-esquerdo).
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1080

NAVY = (16, 26, 48)
WHITE = (247, 247, 244)
SUBTITLE = (167, 177, 201)
GOLD = (212, 175, 55)
GOLD_DARK_TEXT = (24, 20, 4)
LINE = (56, 68, 96)
CARD_BG = (23, 34, 58)

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
    return tw

# ---- decorative corner brackets (top-left / bottom-right) ----
bl = 46
d.line([(MARGIN - 14, 40), (MARGIN - 14, 40 + bl)], fill=GOLD, width=3)
d.line([(MARGIN - 14, 40), (MARGIN - 14 + bl, 40)], fill=GOLD, width=3)
d.line([(W - MARGIN + 14, H - 40), (W - MARGIN + 14, H - 40 - bl)], fill=GOLD, width=3)
d.line([(W - MARGIN + 14, H - 40), (W - MARGIN + 14 - bl, H - 40)], fill=GOLD, width=3)

y = 50

# ---- logo, centered top ----
logo = Image.open("/home/user/domina-posts/logo_domina.png").convert("RGBA")
logo_size = 92
logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
img.paste(logo, (CX - logo_size // 2, y), logo)
y += logo_size + 30

# ---- law badge, centered ----
badge_font = F(19)
badge_text = "LEI 14.133/2021 · ART. 75, III"
tw = text_w(badge_text, badge_font)
pad_x, pad_y = 20, 11
bx0 = CX - tw / 2 - pad_x
bx1 = CX + tw / 2 + pad_x
by0 = y
by1 = by0 + 20 + pad_y * 2
d.rounded_rectangle((bx0, by0, bx1, by1), radius=(by1 - by0) // 2, outline=GOLD, width=2)
center_text(CX, by0 + pad_y - 1, badge_text, badge_font, GOLD)
y = by1 + 38

# ---- title, centered ----
title_font = F(50)
title_lines = [
    ("SUA LICITAÇÃO", WHITE),
    ("FRACASSOU OU FICOU", WHITE),
    ("DESERTA?", GOLD),
]
for line, color in title_lines:
    center_text(CX, y, line, title_font, color)
    y += 60

y += 16

# ---- subtitle, centered ----
sub_font = FR(24)
subtitle = "Mesmo assim, a Lei 14.133/2021 pode permitir que o governo contrate sua empresa direto — sem abrir nova disputa."
sub_lines = wrap(subtitle, sub_font, W - 2 * MARGIN - 30)
for line in sub_lines:
    center_text(CX, y, line, sub_font, SUBTITLE)
    y += 32

y += 20
d.line([(MARGIN, y), (W - MARGIN, y)], fill=LINE, width=2)
y += 36

# ---- VS comparison cards ----
gap = 36
col_w = (W - 2 * MARGIN - gap) // 2
card_top = y
num_font = F(26)
label_font = F(28)
desc_font = FR(19)

cards = [
    ("01", "DESERTA", "Nenhuma empresa apresentou proposta."),
    ("02", "FRACASSADA", "Houve propostas, mas nenhuma foi válida ou habilitada."),
]

card_bottoms = []
for i, (num, label, desc) in enumerate(cards):
    cx0 = MARGIN + i * (col_w + gap)
    cx1 = cx0 + col_w
    col_cx = cx0 + col_w // 2
    yy = card_top + 26
    center_text(col_cx, yy, num, num_font, GOLD)
    yy += 42
    center_text(col_cx, yy, label, label_font, WHITE)
    yy += 42
    for dline in wrap(desc, desc_font, col_w - 48):
        center_text(col_cx, yy, dline, desc_font, SUBTITLE)
        yy += 26
    yy += 24
    d.rounded_rectangle((cx0, card_top, cx1, yy), radius=18, outline=LINE, width=2)
    card_bottoms.append(yy)

card_bottom = max(card_bottoms)

# gold "VS" circle at the midpoint between cards
vs_r = 28
vs_cy = card_top + (card_bottom - card_top) // 2
d.ellipse((CX - vs_r, vs_cy - vs_r, CX + vs_r, vs_cy + vs_r), fill=NAVY, outline=GOLD, width=2)
vs_font = F(20)
tw = text_w("VS", vs_font)
d.text((CX - tw / 2, vs_cy - 13), "VS", font=vs_font, fill=GOLD)

y = card_bottom + 30
d.line([(MARGIN, y), (W - MARGIN, y)], fill=LINE, width=2)
y += 34

# ---- highlight stat ----
stat_font = F(72)
center_text(CX, y, "ATÉ 1 ANO", stat_font, GOLD)
y += 82

note_font = FR(21)
note = "para contratação direta, nas mesmas condições do edital original — se a sua empresa mantiver a habilitação (art. 75, III)."
for line in wrap(note, note_font, W - 2 * MARGIN - 40):
    center_text(CX, y, line, note_font, SUBTITLE)
    y += 28

y += 24

# ---- CTA pill button, centered ----
cta_font = F(26)
cta_text = "Fale com a Domina no direct  →"
tw = text_w(cta_text, cta_font)
pad_x, pad_y = 34, 18
cta_x0 = CX - tw / 2 - pad_x
cta_x1 = CX + tw / 2 + pad_x
cta_y0 = y
cta_y1 = cta_y0 + 26 + pad_y * 2
d.rounded_rectangle((cta_x0, cta_y0, cta_x1, cta_y1), radius=(cta_y1 - cta_y0) // 2, fill=GOLD)
center_text(CX, cta_y0 + pad_y - 1, cta_text, cta_font, GOLD_DARK_TEXT)

print("final y bottom:", cta_y1, "canvas:", H)

img.save("/tmp/post.png")
img.save("/home/user/domina-posts/images/post-2026-10-21-09h-deserta-fracassada-art75.png")
print("saved", img.size)
