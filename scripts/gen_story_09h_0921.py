#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Story 9h 2026-09-21 (vertical): limite legal do atestado de capacidade tecnica."""
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920

NAVY_TOP = (9, 16, 38)
NAVY_BOTTOM = (22, 48, 92)
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


def draw_center_text(draw, cy, text, fnt, fill, cx=W // 2):
    tw = draw.textlength(text, font=fnt)
    draw.text((cx - tw / 2, cy), text, font=fnt, fill=fill)
    return tw


img = Image.new("RGB", (W, H), NAVY_TOP)
draw = ImageDraw.Draw(img)
vertical_gradient(draw, W, H, NAVY_TOP, NAVY_BOTTOM)

draw.rectangle([0, 0, W, 10], fill=GOLD)
draw.rectangle([0, H - 10, W, H], fill=GOLD)

CX = W // 2
content_w = 880

# Safe area: ~250px top, ~250px bottom reserved
y = 300

logo = Image.open("/tmp/logo_domina.png").convert("RGBA")
logo_size = 120
logo_resized = logo.resize((logo_size, logo_size), Image.LANCZOS)
img.paste(logo_resized, (CX - logo_size // 2, y), logo_resized)
y += logo_size + 26

f_brand = font(F_BOLD, 30)
draw_center_text(draw, y, "DOMINA LICITAÇÕES", f_brand, WHITE)
y += 60

f_pill = font(F_BOLD, 28)
pill_text = "VOCÊ SABIA?"
tw = draw.textlength(pill_text, font=f_pill)
pad_x, pad_y = 26, 14
bx0 = CX - tw / 2 - pad_x
bx1 = CX + tw / 2 + pad_x
by0 = y
by1 = y + f_pill.size + pad_y * 2
draw.rounded_rectangle([bx0, by0, bx1, by1], radius=(by1 - by0) // 2, outline=GOLD, width=2)
draw.text((CX - tw / 2, by0 + pad_y - 2), pill_text, font=f_pill, fill=GOLD)
y = by1 + 56

f_head = font(F_BOLD, 62)
headline = "EXIGÊNCIA DE ATESTADO TÉCNICO TEM LIMITE NA LEI"
h_lines = wrap_text(draw, headline, f_head, content_w)
for line in h_lines:
    draw_center_text(draw, y, line, f_head, WHITE)
    y += 74
y += 60

f_stat = font(F_BOLD, 128)
f_stat_cap = font(F_REG, 32)

col_w = content_w // 2
stat_y = y
stats = [
    ("4%", "valor mínimo do item pra virar \"parcela de maior relevância\""),
    ("50%", "máximo de quantidade que o edital pode exigir em atestados"),
]
col_centers = [CX - col_w // 2, CX + col_w // 2]

max_stat_h = 0
for (num, cap), ccx in zip(stats, col_centers):
    tw = draw.textlength(num, font=f_stat)
    draw.text((ccx - tw / 2, stat_y), num, font=f_stat, fill=GOLD)
    max_stat_h = max(max_stat_h, f_stat.size)

cap_y = stat_y + max_stat_h + 14
cap_bottoms = []
for (num, cap), ccx in zip(stats, col_centers):
    lines = wrap_text(draw, cap, f_stat_cap, col_w - 50)
    cy = cap_y
    for line in lines:
        tw = draw.textlength(line, font=f_stat_cap)
        draw.text((ccx - tw / 2, cy), line, font=f_stat_cap, fill=LIGHT_GRAY)
        cy += 42
    cap_bottoms.append(cy)

divider_top = stat_y + 14
divider_bottom = max(cap_bottoms) - 14
draw.line([(CX, divider_top), (CX, divider_bottom)], fill=(90, 100, 130), width=2)

y = max(cap_bottoms) + 60

f_support = font(F_REG, 36)
support_text = "Exigência acima disso é restritiva e pode ser impugnada."
s_lines = wrap_text(draw, support_text, f_support, content_w)
for line in s_lines:
    draw_center_text(draw, y, line, f_support, WHITE)
    y += 50

y += 70

f_cta = font(F_BOLD, 36)
cta_text = "Fale com a Domina antes de desistir do edital"
tw = draw.textlength(cta_text, font=f_cta)
btn_pad_x, btn_pad_y = 40, 24
btn_w = tw + btn_pad_x * 2
btn_h = f_cta.size + btn_pad_y * 2
bx0 = CX - btn_w / 2
draw.rounded_rectangle([bx0, y, bx0 + btn_w, y + btn_h], radius=btn_h // 2, fill=GOLD)
draw.text((bx0 + btn_pad_x, y + btn_pad_y - 4), cta_text, font=f_cta, fill=DARK_TEXT)

img.save("/tmp/story.png")
print("saved", img.size, "content bottom:", y + btn_h, "safe bottom limit:", H - 250)
