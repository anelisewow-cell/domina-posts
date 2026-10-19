#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Post 18h 2026-10-19: Plano de Contratacoes Anual (PCA) - art. 12, VII,
Lei 14.133/2021, e Decreto 10.947/2022. Angulo: o governo publica, com
meses de antecedencia, o que cada orgao pretende comprar no ano seguinte
(PCA no PNCP) - quem acompanha chega preparado antes do edital sair.
Tema novo: nenhum post dos ultimos 30 dias mencionou o PCA (os posts de
mercado/oportunidade tratavam do tamanho do mercado e de editais ja
publicados, nunca do planejamento previo).

Paleta: branco gelo (oposta ao ultimo post publicado, 19/10 9h, que foi
azul marinho solido). Layout variado em relacao aos posts recentes:
TUDO CENTRALIZADO (o post de 18/10 era alinhado a direita com card
horizontal + duas colunas; o de 19/10 9h era alinhado a esquerda com
card unico) - logo centralizada no topo, badge de lei centralizado,
titulo e subtitulo centralizados, bloco de 3 PASSOS EM LINHA HORIZONTAL
com circulos numerados (nenhum post recente usou esse formato), CTA em
botao centralizado, brackets decorativos no canto SUPERIOR ESQUERDO e
INFERIOR DIREITO.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1080

BG = (247, 246, 240)
NAVY = (22, 34, 62)
SUBTITLE = (103, 115, 141)
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

def center_text(y, text, font, fill):
    tw = text_w(text, font)
    d.text((CX - tw / 2, y), text, font=font, fill=fill)

# ---- decorative corner brackets ----
bl = 46
d.line([(MARGIN - 14, 40), (MARGIN - 14, 40 + bl)], fill=GOLD, width=3)
d.line([(MARGIN - 14, 40), (MARGIN - 14 + bl, 40)], fill=GOLD, width=3)
d.line([(W - MARGIN + 14, H - 40), (W - MARGIN + 14, H - 40 - bl)], fill=GOLD, width=3)
d.line([(W - MARGIN + 14, H - 40), (W - MARGIN + 14 - bl, H - 40)], fill=GOLD, width=3)

# ---- logo, top-center ----
logo = Image.open("/home/user/domina-posts/logo_domina.png").convert("RGBA")
logo_size = 100
logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
img.paste(logo, (CX - logo_size // 2, 56), logo)

y = 56 + logo_size + 26

# ---- law badge, centered ----
badge_font = F(21)
badge_text = "LEI 14.133/2021 · ART. 12, VII"
tw = text_w(badge_text, badge_font)
pad_x, pad_y = 22, 12
bx0 = CX - tw / 2 - pad_x
bx1 = CX + tw / 2 + pad_x
by0 = y
by1 = by0 + 21 + pad_y * 2
d.rounded_rectangle((bx0, by0, bx1, by1), radius=(by1 - by0) // 2, outline=GOLD, width=2)
d.text((bx0 + pad_x, by0 + pad_y - 1), badge_text, font=badge_font, fill=GOLD)

y = by1 + 46

# ---- title, centered ----
title_font = F(52)
title_lines = [
    ("O EDITAL AINDA", NAVY),
    ("NEM SAIU.", NAVY),
    ("SEU CONCORRENTE", NAVY),
    ("JÁ SABE O QUE VEM.", GOLD),
]
for line, color in title_lines:
    center_text(y, line, title_font, color)
    y += 62

y += 20

# ---- subtitle, centered ----
sub_font = FR(26)
subtitle = "O Plano de Contratações Anual (PCA) revela, com meses de antecedência, o que cada órgão público pretende comprar."
sub_lines = wrap(subtitle, sub_font, 760)
for line in sub_lines:
    center_text(y, line, sub_font, SUBTITLE)
    y += 34

y += 28
d.line([(CX - 160, y), (CX + 160, y)], fill=LINE, width=2)
y += 48

# ---- 3 steps, horizontal row ----
steps = [
    ("1", "CONSULTE O PCA", "veja o que o órgão vai comprar"),
    ("2", "PREPARE-SE ANTES", "documentação e estratégia prontas"),
    ("3", "VENÇA COM VANTAGEM", "chegue pronto quando o edital sair"),
]
col_w = (W - 2 * MARGIN) // 3
num_font = F(30)
label_font = F(20)
desc_font = FR(19)

circle_r = 30
row_top = y
for i, (num, label, desc) in enumerate(steps):
    col_cx = MARGIN + col_w * i + col_w // 2
    cy = row_top + circle_r
    d.ellipse((col_cx - circle_r, cy - circle_r, col_cx + circle_r, cy + circle_r), outline=GOLD, width=3)
    nw = text_w(num, num_font)
    d.text((col_cx - nw / 2, cy - 19), num, font=num_font, fill=GOLD)

    ly = row_top + circle_r * 2 + 22
    lw_ = text_w(label, label_font)
    d.text((col_cx - lw_ / 2, ly), label, font=label_font, fill=NAVY)

    dyy = ly + 30
    max_col_text = col_w - 28
    for dline in wrap(desc, desc_font, max_col_text):
        dw = text_w(dline, desc_font)
        d.text((col_cx - dw / 2, dyy), dline, font=desc_font, fill=SUBTITLE)
        dyy += 25

y = dyy + 50

# ---- CTA pill button, centered ----
cta_font = F(26)
cta_text = "FALE COM A DOMINA LICITAÇÕES"
tw = text_w(cta_text, cta_font)
pad_x, pad_y = 38, 20
cta_x0 = CX - tw / 2 - pad_x
cta_x1 = CX + tw / 2 + pad_x
cta_y0 = y
cta_y1 = cta_y0 + 26 + pad_y * 2
d.rounded_rectangle((cta_x0, cta_y0, cta_x1, cta_y1), radius=(cta_y1 - cta_y0) // 2, fill=GOLD)
d.text((CX - tw / 2, cta_y0 + pad_y - 1), cta_text, font=cta_font, fill=GOLD_DARK_TEXT)

y = cta_y1 + 30

# ---- footer tag ----
tag_font = FR(20)
center_text(y, "@domina.licitacao", tag_font, SUBTITLE)

img.save("/tmp/post.png")
img.save("/home/user/domina-posts/images/post-2026-10-19-18h-pca-planejamento-anual.png")
print("saved", img.size)
