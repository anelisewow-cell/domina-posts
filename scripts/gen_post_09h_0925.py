#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Post 9h 2026-09-25: Dispensa x Inexigibilidade de licitacao (arts. 74 e 75, Lei 14.133/2021)."""
from PIL import Image, ImageDraw, ImageFont

W = H = 1080

NAVY_TOP = (13, 27, 56)
NAVY_BOTTOM = (35, 66, 118)
GOLD = (212, 175, 55)
WHITE = (255, 255, 255)
LIGHT_GRAY = (198, 206, 224)
DARK_TEXT = (20, 24, 40)
LINE = (98, 118, 160)

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


def center_text(draw, cx, y, text, fnt, fill):
    tw = draw.textlength(text, font=fnt)
    draw.text((cx - tw / 2, y), text, font=fnt, fill=fill)
    return tw


img = Image.new("RGB", (W, H), NAVY_TOP)
draw = ImageDraw.Draw(img)
vertical_gradient(draw, W, H, NAVY_TOP, NAVY_BOTTOM)

CX = W / 2
MARGIN_L = 90
MARGIN_R = 90
content_w = W - MARGIN_L - MARGIN_R

# --- Logo + kicker, centered as one unit near top (new composition) ---
logo = Image.open("/tmp/logo_domina.png").convert("RGBA")
logo_size = 78
logo_resized = logo.resize((logo_size, logo_size), Image.LANCZOS)

f_kicker = font(F_BOLD, 25)
kicker_text = "CONTRATAÇÃO PÚBLICA"
kicker_w = draw.textlength(kicker_text, font=f_kicker)
gap = 20
unit_w = logo_size + gap + kicker_w
unit_x = CX - unit_w / 2
top_y = 66

img.paste(logo_resized, (int(unit_x), top_y), logo_resized)
draw.text((unit_x + logo_size + gap, top_y + logo_size / 2 - f_kicker.size / 2), kicker_text, font=f_kicker, fill=GOLD)

y = top_y + logo_size + 46

# --- Headline, centered ---
f_head = font(F_BOLD, 46)
for line in ["SUA EMPRESA SABE A DIFERENÇA ENTRE"]:
    center_text(draw, CX, y, line, f_head, WHITE)
    y += 54

y += 6
f_big = font(F_BOLD, 70)
center_text(draw, CX, y, "DISPENSA", f_big, GOLD)
y += 82
f_e = font(F_BOLD, 30)
center_text(draw, CX, y, "E", f_e, LIGHT_GRAY)
y += 46
center_text(draw, CX, y, "INEXIGIBILIDADE", f_big, GOLD)
y += 82
f_sub = font(F_BOLD, 34)
center_text(draw, CX, y, "DE LICITAÇÃO?", f_sub, WHITE)
y += 66

draw.line([(MARGIN_L, y), (W - MARGIN_R, y)], fill=LINE, width=2)
y += 40

# --- Two comparison boxes side by side ---
box_gap = 24
box_w = (content_w - box_gap) / 2
box_h = 300
box_y = y
box1_x = MARGIN_L
box2_x = MARGIN_L + box_w + box_gap

draw.rounded_rectangle([box1_x, box_y, box1_x + box_w, box_y + box_h], radius=18, outline=GOLD, width=2)
draw.rounded_rectangle([box2_x, box_y, box2_x + box_w, box_y + box_h], radius=18, outline=GOLD, width=2)

f_box_title = font(F_BOLD, 30)
f_box_art = font(F_BOLD, 22)
f_box_body = font(F_REG, 24)

pad = 26

# Box 1: DISPENSA
bx = box1_x + pad
by = box_y + pad
draw.text((bx, by), "DISPENSA", font=f_box_title, fill=WHITE)
by += 42
draw.text((bx, by), "art. 75", font=f_box_art, fill=GOLD)
by += 40
body1 = "Competir é possível, mas a lei permite não licitar (valor baixo, urgência, entre outros casos)."
for line in wrap_text(draw, body1, f_box_body, box_w - pad * 2):
    draw.text((bx, by), line, font=f_box_body, fill=LIGHT_GRAY)
    by += 32

# Box 2: INEXIGIBILIDADE
bx = box2_x + pad
by = box_y + pad
draw.text((bx, by), "INEXIGIBI-", font=f_box_title, fill=WHITE)
by += 38
draw.text((bx, by), "LIDADE", font=f_box_title, fill=WHITE)
by += 44
draw.text((bx, by), "art. 74", font=f_box_art, fill=GOLD)
by += 40
body2 = "Competir é inviável: fornecedor exclusivo, notória especialização ou credenciamento."
for line in wrap_text(draw, body2, f_box_body, box_w - pad * 2):
    draw.text((bx, by), line, font=f_box_body, fill=LIGHT_GRAY)
    by += 32

y = box_y + box_h + 44

# --- CTA button, centered ---
f_cta = font(F_BOLD, 28)
cta_text = "Fala com a Domina e não erre a modalidade →"
tw = draw.textlength(cta_text, font=f_cta)
btn_pad_x, btn_pad_y = 32, 18
btn_w = tw + btn_pad_x * 2
btn_h = f_cta.size + btn_pad_y * 2
bx0 = CX - btn_w / 2
draw.rounded_rectangle([bx0, y, bx0 + btn_w, y + btn_h], radius=btn_h // 2, fill=GOLD)
draw.text((bx0 + btn_pad_x, y + btn_pad_y - 4), cta_text, font=f_cta, fill=DARK_TEXT)

img.save("/tmp/post.png")
print("saved", img.size)
