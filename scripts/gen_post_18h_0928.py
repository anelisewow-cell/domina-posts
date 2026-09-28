#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Post 18h 2026-09-28: 3 sinais de que a empresa precisa terceirizar o setor de licitacoes (tom comercial)."""
from PIL import Image, ImageDraw, ImageFont

W = H = 1080

NAVY_TOP = (7, 16, 38)
NAVY_BOTTOM = (18, 40, 84)
GOLD = (212, 175, 55)
WHITE = (255, 255, 255)
LIGHT_GRAY = (198, 206, 224)
DARK_TEXT = (20, 24, 40)
LINE = (90, 104, 144)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
F_BOLD = FONT_DIR + "DejaVuSans-Bold.ttf"
F_REG = FONT_DIR + "DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def vertical_gradient(draw, w, h, top, bottom):
    for y in range(h):
        t = y / h
        r = int(top[0] + (bottom[0] - top[0]) * t)
        g = int(top[1] + (bottom[1] - top[1]) * t)
        b = int(top[2] + (bottom[2] - top[2]) * t)
        draw.line([(0, y), (w, y)], fill=(r, g, b))


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


def draw_right(draw, y, text, fnt, fill, right_edge):
    tw = draw.textlength(text, font=fnt)
    draw.text((right_edge - tw, y), text, font=fnt, fill=fill)


img = Image.new("RGB", (W, H), NAVY_TOP)
draw = ImageDraw.Draw(img)
vertical_gradient(draw, W, H, NAVY_TOP, NAVY_BOTTOM)

MARGIN_L = 90
MARGIN_R = 90
content_w = W - MARGIN_L - MARGIN_R
right_edge = W - MARGIN_R

# --- logo top-right (variation vs. top-left / bottom-center used previously) ---
logo = Image.open("/tmp/logo_domina.png").convert("RGBA")
logo_size = 78
logo_x = right_edge - logo_size
logo_y = 66
logo_resized = logo.resize((logo_size, logo_size), Image.LANCZOS)
img.paste(logo_resized, (logo_x, logo_y), logo_resized)

# --- kicker, right aligned, left of logo baseline ---
f_kicker = font(F_BOLD, 24)
kicker = "SINAL DE ALERTA"
draw_right(draw, logo_y + logo_size / 2 - f_kicker.size / 2, kicker, f_kicker, GOLD, logo_x - 22)

y = logo_y + logo_size + 44

# --- headline, right aligned ---
f_head = font(F_BOLD, 49)
head_lines = [
    ("SUA EMPRESA PRECISA", WHITE),
    ("TERCEIRIZAR AS", WHITE),
    ("LICITAÇÕES?", GOLD),
]
for text, color in head_lines:
    draw_right(draw, y, text, f_head, color, right_edge)
    y += 58

y += 20
draw.line([(MARGIN_L, y), (right_edge, y)], fill=LINE, width=2)
y += 36

f_sub = font(F_REG, 26)
sub_lines = wrap_text(
    draw,
    "Se sua empresa se encaixa em pelo menos um desses 3 sinais, provavelmente está deixando contratos públicos na mesa:",
    f_sub,
    content_w,
)
for line in sub_lines:
    draw_right(draw, y, line, f_sub, LIGHT_GRAY, right_edge)
    y += 34

y += 30

# --- 3 numbered items, circular gold badge + text (new bullet style) ---
items = [
    "A equipe descobre o edital quando já falta pouco tempo para o prazo de envio.",
    "Certidão vencida ou documento desatualizado trava a proposta na habilitação.",
    "Ninguém acompanha o PNCP e outras plataformas de compras de forma constante.",
]

badge_r = 28
badge_cx = MARGIN_L + badge_r
text_x = MARGIN_L + badge_r * 2 + 26
f_num = font(F_BOLD, 28)
f_item = font(F_REG, 25)

for idx, text in enumerate(items, start=1):
    lines = wrap_text(draw, text, f_item, content_w - (badge_r * 2 + 26))
    block_h = max(badge_r * 2, len(lines) * 32)
    badge_cy = y + block_h / 2

    draw.ellipse(
        [badge_cx - badge_r, badge_cy - badge_r, badge_cx + badge_r, badge_cy + badge_r],
        outline=GOLD,
        width=3,
    )
    num_text = f"{idx:02d}"
    ntw = draw.textlength(num_text, font=f_num)
    draw.text((badge_cx - ntw / 2, badge_cy - f_num.size / 2 - 2), num_text, font=f_num, fill=GOLD)

    ty = y + (block_h - len(lines) * 32) / 2
    for line in lines:
        draw.text((text_x, ty), line, font=f_item, fill=WHITE)
        ty += 32

    y += block_h + 30

y += 4
draw.line([(MARGIN_L, y), (right_edge, y)], fill=LINE, width=2)
y += 30

f_close = font(F_REG, 25)
close_lines = wrap_text(
    draw,
    "Terceirizar com a Domina Licitações custa menos do que montar uma equipe interna — e já vem com estratégia pronta.",
    f_close,
    content_w,
)
for line in close_lines:
    draw_right(draw, y, line, f_close, LIGHT_GRAY, right_edge)
    y += 33

y += 26

# --- CTA button, right aligned ---
f_cta = font(F_BOLD, 28)
cta_text = "Comente QUERO e vamos analisar →"
tw = draw.textlength(cta_text, font=f_cta)
btn_pad_x, btn_pad_y = 32, 18
btn_w = tw + btn_pad_x * 2
btn_h = f_cta.size + btn_pad_y * 2
bx0 = right_edge - btn_w
draw.rounded_rectangle([bx0, y, bx0 + btn_w, y + btn_h], radius=btn_h // 2, fill=GOLD)
draw.text((bx0 + btn_pad_x, y + btn_pad_y - 4), cta_text, font=f_cta, fill=DARK_TEXT)

assert y + btn_h <= H - 40, f"content overflow: {y + btn_h}"

img.save("/tmp/post.png")
print("saved", img.size, "bottom:", y + btn_h)
