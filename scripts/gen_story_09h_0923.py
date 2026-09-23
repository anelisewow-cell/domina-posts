#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Story 9h 2026-09-23: Recurso administrativo em licitacao (vertical version of feed post)."""
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920

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


def draw_center_text(draw, cy, text, fnt, fill, cx=W // 2):
    tw = draw.textlength(text, font=fnt)
    draw.text((cx - tw / 2, cy), text, font=fnt, fill=fill)
    return tw


img = Image.new("RGB", (W, H), NAVY_TOP)
draw = ImageDraw.Draw(img)
vertical_gradient(draw, W, H, NAVY_TOP, NAVY_BOTTOM)

draw.rectangle([0, 0, 14, H], fill=GOLD)
draw.rectangle([W - 14, 0, W, H], fill=GOLD)

CX = W // 2
content_w = 860
MARGIN_L = (W - content_w) // 2
RIGHT_X = MARGIN_L + content_w

# safe area: ~250px top, ~250px bottom
y = 300

# --- Logo centered ---
logo = Image.open("/tmp/logo_domina.png").convert("RGBA")
logo_size = 130
logo_resized = logo.resize((logo_size, logo_size), Image.LANCZOS)
img.paste(logo_resized, (CX - logo_size // 2, y), logo_resized)
y += logo_size + 30

f_label = font(F_BOLD, 30)
draw_center_text(draw, y, "FASE RECURSAL", f_label, GOLD)
y += 70

# --- Headline centered ---
f_head = font(F_BOLD, 58)
headline = "PERDEU A DISPUTA? AINDA DÁ PRA RECORRER"
h_lines = wrap_text(draw, headline, f_head, content_w)
for line in h_lines:
    draw_center_text(draw, y, line, f_head, WHITE)
    y += 68
y += 50

# --- Hero stat centered ---
f_stat = font(F_BOLD, 220)
stat_text = "3"
tw = draw.textlength(stat_text, font=f_stat)
draw.text((CX - tw / 2, y), stat_text, font=f_stat, fill=GOLD)
y += f_stat.size + 10

f_stat_cap = font(F_BOLD, 40)
draw_center_text(draw, y, "DIAS ÚTEIS PARA RECORRER", f_stat_cap, WHITE)
y += 60

f_stat_sub = font(F_REG, 32)
sub_text = "contados da intimação do ato ou da lavratura da ata"
sub_lines = wrap_text(draw, sub_text, f_stat_sub, content_w)
for line in sub_lines:
    draw_center_text(draw, y, line, f_stat_sub, LIGHT_GRAY)
    y += 42

y += 40
draw.line([(MARGIN_L, y), (RIGHT_X, y)], fill=(90, 100, 130), width=2)
y += 50

# --- Bullets centered ---
bullets = [
    "Cabe recurso contra habilitação, inabilitação e julgamento das propostas",
    "O recurso tem efeito suspensivo — a decisão fica parada até ser julgada",
]
f_bullet = font(F_REG, 34)
for b in bullets:
    lines = wrap_text(draw, b, f_bullet, content_w - 40)
    for line in lines:
        draw_center_text(draw, y, line, f_bullet, WHITE)
        y += 46
    y += 26

y += 30

# --- CTA button centered ---
f_cta = font(F_BOLD, 34)
cta_text = "Foi desclassificada? Fala com a Domina"
tw = draw.textlength(cta_text, font=f_cta)
btn_pad_x, btn_pad_y = 36, 22
btn_w = tw + btn_pad_x * 2
btn_h = f_cta.size + btn_pad_y * 2
bx0 = CX - btn_w / 2
draw.rounded_rectangle([bx0, y, bx0 + btn_w, y + btn_h], radius=btn_h // 2, fill=GOLD)
draw.text((bx0 + btn_pad_x, y + btn_pad_y - 4), cta_text, font=f_cta, fill=DARK_TEXT)

img.save("/tmp/story.png")
print("saved", img.size)
