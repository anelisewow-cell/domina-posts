#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Story 2026-09-25 (9h): Dispensa x Inexigibilidade de licitacao (arts. 74 e 75, Lei 14.133/2021)."""
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920

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

SAFE_TOP = 250
SAFE_BOTTOM = 250


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
MARGIN_L = 96
MARGIN_R = 96
content_w = W - MARGIN_L - MARGIN_R

y = SAFE_TOP

# --- Logo + kicker, centered as one unit ---
logo = Image.open("/tmp/logo_domina.png").convert("RGBA")
logo_size = 96
logo_resized = logo.resize((logo_size, logo_size), Image.LANCZOS)

f_kicker = font(F_BOLD, 28)
kicker_text = "CONTRATAÇÃO PÚBLICA"
kicker_w = draw.textlength(kicker_text, font=f_kicker)
gap = 22
unit_w = logo_size + gap + kicker_w
unit_x = CX - unit_w / 2

img.paste(logo_resized, (int(unit_x), int(y)), logo_resized)
draw.text((unit_x + logo_size + gap, y + logo_size / 2 - f_kicker.size / 2), kicker_text, font=f_kicker, fill=GOLD)

y += logo_size + 70

# --- Headline, centered ---
f_head = font(F_BOLD, 52)
for line in wrap_text(draw, "SUA EMPRESA SABE A DIFERENÇA ENTRE", f_head, content_w):
    center_text(draw, CX, y, line, f_head, WHITE)
    y += 62

y += 20
f_big = font(F_BOLD, 84)
center_text(draw, CX, y, "DISPENSA", f_big, GOLD)
y += 100
f_e = font(F_BOLD, 34)
center_text(draw, CX, y, "E", f_e, LIGHT_GRAY)
y += 56
center_text(draw, CX, y, "INEXIGIBILIDADE", f_big, GOLD)
y += 100
f_sub = font(F_BOLD, 40)
center_text(draw, CX, y, "DE LICITAÇÃO?", f_sub, WHITE)
y += 80

draw.line([(MARGIN_L, y), (W - MARGIN_R, y)], fill=LINE, width=2)
y += 56

# --- Two comparison boxes stacked (vertical layout) ---
box_w = content_w
box_h = 260
box_gap = 24

f_box_title = font(F_BOLD, 36)
f_box_art = font(F_BOLD, 26)
f_box_body = font(F_REG, 30)
pad = 34

for title, art, body in [
    ("DISPENSA", "art. 75", "Competir é possível, mas a lei permite não licitar (valor baixo, urgência, entre outros casos)."),
    ("INEXIGIBILIDADE", "art. 74", "Competir é inviável: fornecedor exclusivo, notória especialização ou credenciamento."),
]:
    draw.rounded_rectangle([MARGIN_L, y, MARGIN_L + box_w, y + box_h], radius=22, outline=GOLD, width=3)
    bx = MARGIN_L + pad
    by = y + pad
    draw.text((bx, by), title, font=f_box_title, fill=WHITE)
    by += 50
    draw.text((bx, by), art, font=f_box_art, fill=GOLD)
    by += 46
    for line in wrap_text(draw, body, f_box_body, box_w - pad * 2):
        draw.text((bx, by), line, font=f_box_body, fill=LIGHT_GRAY)
        by += 40
    y += box_h + box_gap

y += 30

# --- CTA button, centered ---
f_cta = font(F_BOLD, 32)
cta_text = "Fala com a Domina →"
tw = draw.textlength(cta_text, font=f_cta)
btn_pad_x, btn_pad_y = 40, 22
btn_w = tw + btn_pad_x * 2
btn_h = f_cta.size + btn_pad_y * 2
bx0 = CX - btn_w / 2
draw.rounded_rectangle([bx0, y, bx0 + btn_w, y + btn_h], radius=btn_h // 2, fill=GOLD)
draw.text((bx0 + btn_pad_x, y + btn_pad_y - 4), cta_text, font=f_cta, fill=DARK_TEXT)

# ensure nothing crosses into bottom safe area
assert y + btn_h <= H - SAFE_BOTTOM, f"content extends into bottom safe area: {y + btn_h} > {H - SAFE_BOTTOM}"

img.save("/tmp/story.png")
print("saved", img.size, "content bottom:", y + btn_h, "limit:", H - SAFE_BOTTOM)
