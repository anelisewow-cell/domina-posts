#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Post 9h 2026-10-22: modo de disputa aberto x fechado no pregao eletronico
(art. 56, Lei 14.133/2021). Angulo: dica pratica de alto impacto - a lei
preve dois modos de disputa (aberto, com lances publicos e sucessivos; e
fechado, com propostas sigilosas ate a abertura) e isso muda a estrategia
de precificacao da empresa antes mesmo da sessao comecar. Tema novo:
nenhum post dos ultimos 30 dias tratou do modo de disputa do pregao (o
mais proximo foi "empate ficto no pregao" em 17/10, que trata de
desempate ME/EPP, assunto diferente).

Fonte: Lei 14.133/2021, art. 56, I, II, §§ 1 e 2 (planalto.gov.br); TCU,
Licitacoes e Contratos, item 3.5 - Modos de disputa (licitacoesecontratos.tcu.gov.br).

Paleta: azul marinho solido (oposta ao ultimo post publicado, 21/10 18h,
que foi branco gelo - confirmado por amostragem de pixels da imagem
images/post-2026-10-21-18h-registro-precos-art82-86.png).

Layout variado em relacao ao ultimo post navy (21/10 9h, que tinha logo
CENTRALIZADA, titulo centralizado e comparacao em "VS" com circulo
dourado no meio): aqui a logo fica no canto SUPERIOR ESQUERDO, badge no
canto SUPERIOR DIREITO, titulo e subtitulo alinhados a ESQUERDA, a
comparacao e feita em DOIS CARDS lado a lado (nao um "VS"), CTA em
pill dourado alinhado a DIREITA no rodape, e os brackets decorativos
ficam no canto SUPERIOR-DIREITO e INFERIOR-ESQUERDO (invertido em
relacao ao post anterior, que usava superior-esquerdo/inferior-direito).
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1080

NAVY = (14, 23, 45)
NAVY_SOFT = (22, 34, 60)
CARD_BG = (24, 36, 63)
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
MARGIN = 80

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

def draw_rich_line(x, y, segments, default_color):
    cx = x
    for seg_text, seg_font, seg_color in segments:
        color = seg_color if seg_color else default_color
        d.text((cx, y), seg_text, font=seg_font, fill=color)
        cx += text_w(seg_text, seg_font)
    return cx

# --- subtle vertical gradient for depth ---
for yy in range(H):
    t = yy / H
    r = int(NAVY[0] + (NAVY_SOFT[0] - NAVY[0]) * t)
    g = int(NAVY[1] + (NAVY_SOFT[1] - NAVY[1]) * t)
    b = int(NAVY[2] + (NAVY_SOFT[2] - NAVY[2]) * t)
    d.line([(0, yy), (W, yy)], fill=(r, g, b))

# --- decorative corner brackets: top-right / bottom-left ---
BL = 46
lw = 3
# top-right
d.line([(W - MARGIN - BL, MARGIN - 18), (W - MARGIN, MARGIN - 18)], fill=GOLD, width=lw)
d.line([(W - MARGIN, MARGIN - 18), (W - MARGIN, MARGIN - 18 + BL)], fill=GOLD, width=lw)
# bottom-left
d.line([(MARGIN, H - MARGIN + 18), (MARGIN + BL, H - MARGIN + 18)], fill=GOLD, width=lw)
d.line([(MARGIN, H - MARGIN + 18 - BL), (MARGIN, H - MARGIN + 18)], fill=GOLD, width=lw)

# --- logo top-left ---
logo = Image.open("/home/user/domina-posts/logo_domina.png").convert("RGBA")
LOGO_SIZE = 100
logo = logo.resize((LOGO_SIZE, LOGO_SIZE), Image.LANCZOS)
img.paste(logo, (MARGIN, 64), logo)

# --- badge top-right: "LEI 14.133/2021 . ART. 56" ---
badge_font = F(21)
badge_text = "LEI 14.133/2021  ·  ART. 56"
bw = text_w(badge_text, badge_font)
bpad_x, bpad_y = 20, 12
bx1 = W - MARGIN - bw - bpad_x * 2
by1 = 74
bx2 = W - MARGIN
by2 = by1 + 21 + bpad_y * 2
d.rounded_rectangle([bx1, by1, bx2, by2], radius=20, outline=GOLD, width=2)
d.text((bx1 + bpad_x, by1 + bpad_y - 1), badge_text, font=badge_font, fill=GOLD)

# --- title, left aligned ---
title_font = F(58)
title_y = 200
line_gap = 68
lines = [
    [("No pregão ", title_font, WHITE), ("FECHADO", title_font, GOLD), (",", title_font, WHITE)],
    [("sua empresa tem", title_font, WHITE)],
    [("só ", title_font, WHITE), ("UMA CHANCE", title_font, GOLD), (".", title_font, WHITE)],
]
ty = title_y
for segs in lines:
    draw_rich_line(MARGIN, ty, segs, WHITE)
    ty += line_gap

# --- subtitle ---
sub_font = FR(27)
sub_text = "A Lei 14.133/2021 prevê dois modos de disputa no pregão — e cada um exige uma estratégia de preço diferente."
sub_lines = wrap(sub_text, sub_font, W - 2 * MARGIN)
sy = ty + 22
for ln in sub_lines:
    d.text((MARGIN, sy), ln, font=sub_font, fill=SUBTITLE)
    sy += 37

# --- two comparison cards ---
cards_y = sy + 40
card_gap = 24
card_w = (W - 2 * MARGIN - card_gap) // 2
card_h = 258
card1_x = MARGIN
card2_x = MARGIN + card_w + card_gap

def draw_card(x, label, body_lines, highlight):
    d.rounded_rectangle([x, cards_y, x + card_w, cards_y + card_h], radius=22, fill=CARD_BG, outline=LINE, width=1)
    pad = 28
    # label pill
    lab_font = F(23)
    lw_ = text_w(label, lab_font)
    d.rounded_rectangle([x + pad, cards_y + pad, x + pad + lw_ + 28, cards_y + pad + 42],
                         radius=18, fill=GOLD if highlight else None,
                         outline=None if highlight else GOLD, width=2)
    txt_color = GOLD_DARK_TEXT if highlight else GOLD
    d.text((x + pad + 14, cards_y + pad + 8), label, font=lab_font, fill=txt_color)
    # body
    body_font = FR(22)
    by = cards_y + pad + 42 + 22
    for ln in body_lines:
        wrapped = wrap(ln, body_font, card_w - 2 * pad)
        for wl in wrapped:
            d.text((x + pad, by), wl, font=body_font, fill=WHITE)
            by += 31

draw_card(
    card1_x, "ABERTO",
    ["Lances públicos e", "sucessivos.", "Você acompanha e", "melhora sua oferta."],
    highlight=False,
)
draw_card(
    card2_x, "FECHADO",
    ["Proposta sigilosa", "até a abertura.", "Não há lances —", "só uma chance."],
    highlight=True,
)

# --- CTA pill, right aligned ---
cta_text = "FALE COM A DOMINA →"
cta_font = F(25)
cw = text_w(cta_text, cta_font)
pad_x, pad_y = 28, 16
cta_y1 = cards_y + card_h + 44
cta_x2 = W - MARGIN
cta_x1 = cta_x2 - cw - pad_x * 2
cta_y2 = cta_y1 + 25 + pad_y * 2
d.rounded_rectangle([cta_x1, cta_y1, cta_x2, cta_y2], radius=(cta_y2 - cta_y1) // 2, fill=GOLD)
d.text((cta_x1 + pad_x, cta_y1 + pad_y - 2), cta_text, font=cta_font, fill=GOLD_DARK_TEXT)

img.save("/tmp/post.png")
print("saved /tmp/post.png", img.size)
