#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Story 2026-09-27 (9h): Reequilibrio economico-financeiro - reajuste, repactuacao e revisao."""
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920

NAVY_TOP = (10, 22, 50)
NAVY_BOTTOM = (28, 58, 108)
GOLD = (212, 175, 55)
WHITE = (255, 255, 255)
LIGHT_GRAY = (198, 206, 224)
DARK_TEXT = (20, 24, 40)
LINE = (90, 108, 150)

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
MARGIN_L = 100
MARGIN_R = 100
content_w = W - MARGIN_L - MARGIN_R

y = SAFE_TOP

# --- Logo + kicker, centered as one unit ---
logo = Image.open("/tmp/logo_domina.png").convert("RGBA")
logo_size = 100
logo_resized = logo.resize((logo_size, logo_size), Image.LANCZOS)

f_kicker = font(F_BOLD, 28)
kicker_text = "CONTRATOS PÚBLICOS"
kicker_w = draw.textlength(kicker_text, font=f_kicker)
gap = 22
unit_w = logo_size + gap + kicker_w
unit_x = CX - unit_w / 2

img.paste(logo_resized, (int(unit_x), int(y)), logo_resized)
draw.text((unit_x + logo_size + gap, y + logo_size / 2 - f_kicker.size / 2), kicker_text, font=f_kicker, fill=GOLD)

y += logo_size + 66

# --- Headline, centered ---
f_head = font(F_BOLD, 54)
for line in wrap_text(draw, "SEU CONTRATO COM O GOVERNO ESTÁ DEFASADO?", f_head, content_w):
    center_text(draw, CX, y, line, f_head, WHITE)
    y += 64

y += 30
draw.line([(MARGIN_L, y), (W - MARGIN_R, y)], fill=LINE, width=2)
y += 46

f_sub = font(F_REG, 32)
for line in wrap_text(draw, "A Lei 14.133/2021 prevê 3 caminhos para o reequilíbrio econômico-financeiro:", f_sub, content_w):
    center_text(draw, CX, y, line, f_sub, LIGHT_GRAY)
    y += 42

y += 40

# --- 3 numbered rows with gold circle badges ---
items = [
    ("1", "REAJUSTE", "Aplica o índice previsto no contrato após 1 ano da proposta."),
    ("2", "REPACTUAÇÃO", "Comprova a variação real de custo em serviços com mão de obra."),
    ("3", "REVISÃO", "Recompõe o contrato diante de fatos imprevisíveis, como força maior."),
]

badge_r = 36
f_badge = font(F_BOLD, 36)
f_title = font(F_BOLD, 38)
f_body = font(F_REG, 30)

for num, title, body in items:
    cy = y + badge_r
    draw.ellipse([MARGIN_L, y, MARGIN_L + badge_r * 2, y + badge_r * 2], fill=GOLD)
    ntw = draw.textlength(num, font=f_badge)
    draw.text((MARGIN_L + badge_r - ntw / 2, cy - f_badge.size / 2 - 2), num, font=f_badge, fill=DARK_TEXT)

    tx = MARGIN_L + badge_r * 2 + 28
    draw.text((tx, y - 4), title, font=f_title, fill=GOLD)
    ty = y + 48
    for line in wrap_text(draw, body, f_body, content_w - (badge_r * 2 + 28)):
        draw.text((tx, ty), line, font=f_body, fill=WHITE)
        ty += 38

    y = max(ty, y + badge_r * 2) + 34

y += 20

# --- CTA button, centered ---
f_cta = font(F_BOLD, 33)
cta_text = "Fala com a Domina →"
tw = draw.textlength(cta_text, font=f_cta)
btn_pad_x, btn_pad_y = 40, 22
btn_w = tw + btn_pad_x * 2
btn_h = f_cta.size + btn_pad_y * 2
bx0 = CX - btn_w / 2
draw.rounded_rectangle([bx0, y, bx0 + btn_w, y + btn_h], radius=btn_h // 2, fill=GOLD)
draw.text((bx0 + btn_pad_x, y + btn_pad_y - 4), cta_text, font=f_cta, fill=DARK_TEXT)

assert y + btn_h <= H - SAFE_BOTTOM, f"content extends into bottom safe area: {y + btn_h} > {H - SAFE_BOTTOM}"

img.save("/tmp/story.png")
print("saved", img.size, "content bottom:", y + btn_h, "limit:", H - SAFE_BOTTOM)
