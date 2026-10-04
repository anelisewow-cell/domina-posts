#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Post 18h 2026-10-04: orcamento sigiloso em licitacoes (art. 24, Lei 14.133/2021).
Paleta branco gelo (oposta ao post das 9h de hoje, que foi azul marinho).
Layout: headline alinhada a esquerda no topo, logo no canto inferior esquerdo,
CTA alinhado a direita no rodape - composicao diagonal nao usada nos posts recentes
(que usaram logo centralizada/topo ou cantos opostos com headline centralizada).
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1080

BG = (247, 246, 240)      # branco gelo
NAVY = (16, 28, 58)       # texto titulo
SUBTLE = (94, 104, 128)   # subtitulo / cinza-azulado
GOLD = (196, 154, 61)     # dourado (contraste em fundo claro)
LINE = (214, 208, 190)
LOGO_PATH = "/home/user/domina-posts/logo_domina.png"

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
F_BOLD = FONT_DIR + "DejaVuSans-Bold.ttf"
F_REG = FONT_DIR + "DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap_text(draw, text, fnt, max_width):
    words = text.split(" ")
    lines, cur = [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if draw.textlength(test, font=fnt) <= max_width:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img)

MARGIN_L = 96
MARGIN_R = 96
content_w = W - MARGIN_L - MARGIN_R

y = 92

# --- eyebrow, left aligned ---
f_kicker = font(F_BOLD, 22)
kicker = "VOCÊ SABIA?"
ktw = draw.textlength(kicker, font=f_kicker)
pill_pad_x, pill_pad_y = 24, 10
pill_h = f_kicker.size + pill_pad_y * 2
draw.rounded_rectangle(
    [MARGIN_L, y, MARGIN_L + ktw + pill_pad_x * 2, y + pill_h],
    radius=pill_h / 2, outline=GOLD, width=2,
)
draw.text((MARGIN_L + pill_pad_x, y + pill_pad_y - 2), kicker, font=f_kicker, fill=GOLD)

y += pill_h + 38

# --- headline, left aligned, 4 short lines ---
f_head = font(F_BOLD, 56)
head_lines = [
    ("O GOVERNO PODE", NAVY),
    ("LICITAR SEM", NAVY),
    ("REVELAR O VALOR", GOLD),
    ("QUE VAI PAGAR", NAVY),
]
for text, color in head_lines:
    draw.text((MARGIN_L, y), text, font=f_head, fill=color)
    y += 62

y += 16

f_sub = font(F_REG, 26)
sub_lines = wrap_text(
    draw,
    "A Lei 14.133/2021 permite orçamento sigiloso em licitações — e isso muda como sua empresa precisa precificar a proposta.",
    f_sub,
    content_w,
)
for line in sub_lines:
    draw.text((MARGIN_L, y), line, font=f_sub, fill=SUBTLE)
    y += 34

y += 28
draw.line([(MARGIN_L, y), (W - MARGIN_R, y)], fill=LINE, width=2)
y += 36

# --- 2 insight bullets, gold dash marker ---
bullets = [
    "O sigilo precisa ser justificado e não vale para licitação por melhor técnica, onde o prêmio é sempre público (art. 24).",
    "Sem o teto declarado, propor um preço \"no escuro\" pode custar a disputa — ou a margem de lucro do contrato.",
]
f_item = font(F_REG, 25)
dash_w = 34
for b in bullets:
    lines = wrap_text(draw, b, f_item, content_w - dash_w)
    draw.text((MARGIN_L, y + 2), "—", font=font(F_BOLD, 25), fill=GOLD)
    ty = y
    for line in lines:
        draw.text((MARGIN_L + dash_w, ty), line, font=f_item, fill=NAVY)
        ty += 33
    y = ty + 20

y += 10
draw.line([(MARGIN_L, y), (W - MARGIN_R, y)], fill=LINE, width=2)
y += 34

f_close = font(F_REG, 25)
close_lines = wrap_text(
    draw,
    "A Domina Licitações monta a pesquisa de mercado e a memória de cálculo pra sua empresa precificar com segurança — mesmo sem saber o orçamento do órgão.",
    f_close,
    content_w,
)
for line in close_lines:
    draw.text((MARGIN_L, y), line, font=f_close, fill=SUBTLE)
    y += 33

# --- logo bottom-left, CTA bottom-right (diagonal composition) ---
logo_size = 92
logo_y = H - 70 - logo_size
logo = Image.open(LOGO_PATH).convert("RGBA").resize((logo_size, logo_size), Image.LANCZOS)
img.paste(logo, (MARGIN_L, logo_y), logo)

f_cta = font(F_BOLD, 26)
cta_text = "Fale com a gente no direct →"
tw = draw.textlength(cta_text, font=f_cta)
btn_pad_x, btn_pad_y = 32, 18
btn_w = tw + btn_pad_x * 2
btn_h = f_cta.size + btn_pad_y * 2
bx1 = W - MARGIN_R
bx0 = bx1 - btn_w
by0 = H - 70 - btn_h
draw.rounded_rectangle([bx0, by0, bx1, by0 + btn_h], radius=btn_h // 2, fill=GOLD)
draw.text((bx0 + btn_pad_x, by0 + btn_pad_y - 4), cta_text, font=f_cta, fill=(255, 255, 255))

assert y <= logo_y - 20, f"content overflow into logo row: y={y}, logo_y={logo_y}"

img.save("/tmp/post.png")
print("saved", img.size, "content bottom:", y, "logo_y:", logo_y)
