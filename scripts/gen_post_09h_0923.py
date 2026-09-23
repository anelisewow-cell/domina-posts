#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Post 9h 2026-09-23: Recurso administrativo em licitacao (arts. 165, 166 e 168, Lei 14.133/2021)."""
from PIL import Image, ImageDraw, ImageFont

W = H = 1080

NAVY_TOP = (10, 14, 34)
NAVY_BOTTOM = (26, 34, 74)
GOLD = (212, 175, 55)
WHITE = (255, 255, 255)
LIGHT_GRAY = (198, 206, 224)
DARK_TEXT = (20, 24, 40)

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


def draw_right_text(draw, y, text, fnt, fill, right_x):
    tw = draw.textlength(text, font=fnt)
    draw.text((right_x - tw, y), text, font=fnt, fill=fill)
    return tw


img = Image.new("RGB", (W, H), NAVY_TOP)
draw = ImageDraw.Draw(img)
vertical_gradient(draw, W, H, NAVY_TOP, NAVY_BOTTOM)

# left-edge vertical gold bar (variation vs. frame / horizontal bars used previously)
draw.rectangle([0, 0, 14, H], fill=GOLD)

MARGIN_R = 92
MARGIN_L = 96
content_w = W - MARGIN_L - MARGIN_R
RIGHT_X = W - MARGIN_R

# --- Logo top-right (variation vs. bottom-right / top-center used previously) ---
logo = Image.open("/tmp/logo_domina.png").convert("RGBA")
logo_size = 100
logo_resized = logo.resize((logo_size, logo_size), Image.LANCZOS)
logo_x = RIGHT_X - logo_size
logo_y = 80
img.paste(logo_resized, (logo_x, logo_y), logo_resized)

y = 100

# --- Label, right aligned ---
f_label = font(F_BOLD, 25)
label_text = "FASE RECURSAL"
draw_right_text(draw, y, label_text, f_label, GOLD, logo_x - 30)
y = logo_y + logo_size + 44

# --- Headline, right aligned ---
f_head = font(F_BOLD, 50)
headline = "PERDEU A DISPUTA? AINDA DÁ PRA RECORRER"
h_lines = wrap_text(draw, headline, f_head, content_w)
for line in h_lines:
    draw_right_text(draw, y, line, f_head, WHITE, RIGHT_X)
    y += 58
y += 30

# --- Hero stat, right aligned ---
f_stat = font(F_BOLD, 150)
stat_text = "3"
tw = draw.textlength(stat_text, font=f_stat)
draw.text((RIGHT_X - tw, y), stat_text, font=f_stat, fill=GOLD)
stat_h = f_stat.size
f_stat_cap = font(F_BOLD, 32)
cap_text = "DIAS ÚTEIS PARA RECORRER"
draw_right_text(draw, y + stat_h - 18, cap_text, f_stat_cap, WHITE, RIGHT_X - tw - 24)
y += stat_h + 20

f_stat_sub = font(F_REG, 27)
sub_text = "contados da intimação do ato ou da lavratura da ata"
sub_lines = wrap_text(draw, sub_text, f_stat_sub, content_w)
for line in sub_lines:
    draw_right_text(draw, y, line, f_stat_sub, LIGHT_GRAY, RIGHT_X)
    y += 36

y += 30
draw.line([(MARGIN_L, y), (RIGHT_X, y)], fill=(90, 100, 130), width=2)
y += 34

# --- Bullet list, right aligned text with check marks on the right edge ---
bullets = [
    "Cabe recurso contra habilitação, inabilitação e julgamento das propostas",
    "O recurso tem efeito suspensivo — a decisão fica parada até ser julgada",
]
f_bullet = font(F_REG, 29)
for b in bullets:
    lines = wrap_text(draw, b, f_bullet, content_w - 50)
    for line in lines:
        draw_right_text(draw, y, line, f_bullet, WHITE, RIGHT_X)
        y += 38
    y += 18

y += 14

# --- CTA button, right aligned ---
f_cta = font(F_BOLD, 29)
cta_text = "Foi desclassificada? Fala com a Domina"
tw = draw.textlength(cta_text, font=f_cta)
btn_pad_x, btn_pad_y = 32, 18
btn_w = tw + btn_pad_x * 2
btn_h = f_cta.size + btn_pad_y * 2
bx1 = RIGHT_X
bx0 = bx1 - btn_w
draw.rounded_rectangle([bx0, y, bx1, y + btn_h], radius=btn_h // 2, fill=GOLD)
draw.text((bx0 + btn_pad_x, y + btn_pad_y - 4), cta_text, font=f_cta, fill=DARK_TEXT)

img.save("/tmp/post.png")
print("saved", img.size)
