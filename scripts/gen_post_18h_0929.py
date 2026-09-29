#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Post 18h 2026-09-29: garantia contratual (art. 96/98, Lei 14.133/2021) - tom comercial.
Paleta branco gelo (oposta ao post das 9h de hoje, que foi azul marinho).
Layout: composicao centralizada (titulo/kicker/logo) + lista de itens alinhada a esquerda,
variando do layout right-aligned com badges circulares usado no post de ontem 18h.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1080

BG = (247, 246, 240)          # branco gelo
NAVY = (16, 28, 58)           # texto titulo
SUBTLE = (94, 104, 128)       # subtitulo / cinza-azulado
GOLD = (196, 154, 61)         # dourado (ligeiramente mais escuro p/ contraste no fundo claro)
GOLD_BTN = (196, 154, 61)
DARK_TEXT = (26, 22, 12)
LINE = (214, 208, 190)

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


def draw_center(draw, y, text, fnt, fill, cx):
    tw = draw.textlength(text, font=fnt)
    draw.text((cx - tw / 2, y), text, font=fnt, fill=fill)
    return tw


img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img)

MARGIN_L = 96
MARGIN_R = 96
content_w = W - MARGIN_L - MARGIN_R
cx = W / 2

# --- logo top-center (variation: centered, not corner like the two previous posts) ---
logo = Image.open("/tmp/logo_domina.png").convert("RGBA")
logo_size = 84
logo_resized = logo.resize((logo_size, logo_size), Image.LANCZOS)
logo_y = 48
img.paste(logo_resized, (int(cx - logo_size / 2), logo_y), logo_resized)

y = logo_y + logo_size + 26

# --- eyebrow pill, centered ---
f_kicker = font(F_BOLD, 22)
kicker = "GARANTIA CONTRATUAL"
ktw = draw.textlength(kicker, font=f_kicker)
pill_pad_x, pill_pad_y = 26, 11
pill_w = ktw + pill_pad_x * 2
pill_h = f_kicker.size + pill_pad_y * 2
px0 = cx - pill_w / 2
draw.rounded_rectangle([px0, y, px0 + pill_w, y + pill_h], radius=pill_h / 2, outline=GOLD, width=2)
draw_center(draw, y + pill_pad_y - 2, kicker, f_kicker, GOLD, cx)

y += pill_h + 30

# --- headline, centered, 3 lines ---
f_head = font(F_BOLD, 48)
head_lines = [
    ("A GARANTIA DO CONTRATO", NAVY),
    ("PODE SER MAIS BARATA", NAVY),
    ("DO QUE VOCÊ PENSA", GOLD),
]
for text, color in head_lines:
    draw_center(draw, y, text, f_head, color, cx)
    y += 55

y += 12

f_sub = font(F_REG, 25)
sub_lines = wrap_text(
    draw,
    "3 coisas que poucas empresas sabem antes de assinar um contrato com o poder público:",
    f_sub,
    content_w - 60,
)
for line in sub_lines:
    draw_center(draw, y, line, f_sub, SUBTLE, cx)
    y += 33

y += 26
draw.line([(MARGIN_L, y), (W - MARGIN_R, y)], fill=LINE, width=2)
y += 34

# --- 3 items, left aligned block, large gold numerals (no circle, contrast vs. yesterday) ---
items = [
    "Nem toda licitação exige garantia — o edital é que decide, conforme o art. 96 da Lei 14.133/2021.",
    "A empresa escolhe a modalidade: caução em dinheiro, seguro-garantia ou fiança bancária — a que pesar menos no caixa.",
    "O percentual padrão é de até 5% do valor do contrato, podendo subir para até 10% só em casos justificados.",
]

f_num = font(F_BOLD, 40)
f_item = font(F_REG, 24)
text_x = MARGIN_L + 70

for idx, text in enumerate(items, start=1):
    lines = wrap_text(draw, text, f_item, content_w - 70)
    num_text = f"0{idx}"
    draw.text((MARGIN_L, y), num_text, font=f_num, fill=GOLD)
    ty = y
    for line in lines:
        draw.text((text_x, ty), line, font=f_item, fill=NAVY)
        ty += 31
    block_h = max(f_num.size + 4, len(lines) * 31)
    y += block_h + 22

y += 4
draw.line([(MARGIN_L, y), (W - MARGIN_R, y)], fill=LINE, width=2)
y += 28

f_close = font(F_REG, 24)
close_lines = wrap_text(
    draw,
    "A Domina Licitações ajuda sua empresa a escolher a modalidade certa e negociar os termos sem travar o fluxo de caixa.",
    f_close,
    content_w - 40,
)
for line in close_lines:
    draw_center(draw, y, line, f_close, SUBTLE, cx)
    y += 31

y += 22

# --- CTA button, centered ---
f_cta = font(F_BOLD, 27)
cta_text = "Fale com a gente no direct →"
tw = draw.textlength(cta_text, font=f_cta)
btn_pad_x, btn_pad_y = 34, 19
btn_w = tw + btn_pad_x * 2
btn_h = f_cta.size + btn_pad_y * 2
bx0 = cx - btn_w / 2
draw.rounded_rectangle([bx0, y, bx0 + btn_w, y + btn_h], radius=btn_h // 2, fill=GOLD_BTN)
draw.text((bx0 + btn_pad_x, y + btn_pad_y - 4), cta_text, font=f_cta, fill=(255, 255, 255))

assert y + btn_h <= H - 40, f"content overflow: {y + btn_h}"

img.save("/tmp/post.png")
print("saved", img.size, "bottom:", y + btn_h)
