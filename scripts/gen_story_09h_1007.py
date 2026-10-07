#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Story 2026-10-07 (9h): marca especifica em edital - regra x excecao (art. 41, Lei 14.133/2021)."""
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920

NAVY_TOP = (9, 20, 46)
NAVY_BOTTOM = (24, 50, 96)
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

# --- decorative corner brackets within safe area ---
BR_LEN = 40
draw.line([(60, SAFE_TOP), (60, SAFE_TOP + BR_LEN)], fill=GOLD, width=2)
draw.line([(60, SAFE_TOP), (60 + BR_LEN, SAFE_TOP)], fill=GOLD, width=2)
draw.line([(W - 60, H - SAFE_BOTTOM), (W - 60, H - SAFE_BOTTOM - BR_LEN)], fill=GOLD, width=2)
draw.line([(W - 60, H - SAFE_BOTTOM), (W - 60 - BR_LEN, H - SAFE_BOTTOM)], fill=GOLD, width=2)

y = SAFE_TOP + 20

# --- Logo centered ---
logo = Image.open("/tmp/logo_domina.png").convert("RGBA")
logo_size = 110
logo_resized = logo.resize((logo_size, logo_size), Image.LANCZOS)
img.paste(logo_resized, (int(CX - logo_size / 2), int(y)), logo_resized)

y += logo_size + 46

# --- pill badge, centered ---
f_badge_txt = font(F_BOLD, 26)
badge_text = "LEI 14.133/2021  ·  ART. 41"
btw = draw.textlength(badge_text, font=f_badge_txt)
pad_x, pad_y = 28, 15
bw = btw + pad_x * 2
bh = f_badge_txt.size + pad_y * 2
bx0 = CX - bw / 2
draw.rounded_rectangle([bx0, y, bx0 + bw, y + bh], radius=bh // 2, outline=GOLD, width=2)
draw.text((bx0 + pad_x, y + pad_y - 2), badge_text, font=f_badge_txt, fill=GOLD)

y += bh + 56

# --- Headline, centered, 3 lines ---
f_head = font(F_BOLD, 60)
head_lines = [
    ("EDITAL EXIGINDO", WHITE),
    ("MARCA ESPECÍFICA?", GOLD),
    ("A REGRA É", WHITE),
    ("NÃO PODER.", WHITE),
]
for line, color in head_lines:
    center_text(draw, CX, y, line, f_head, color)
    y += 70

y += 34

f_sub = font(F_REG, 31)
sub_text = ("A Lei 14.133/2021 proíbe, por padrão, a exigência de marca ou modelo no "
            "edital. Ela só é permitida em hipóteses específicas, sempre com "
            "justificativa técnica formal.")
for line in wrap_text(draw, sub_text, f_sub, content_w):
    center_text(draw, CX, y, line, f_sub, LIGHT_GRAY)
    y += 40

y += 40
draw.line([(MARGIN_L, y), (W - MARGIN_R, y)], fill=LINE, width=2)
y += 54

# --- label + body blocks, centered ---
f_label = font(F_BOLD, 31)
f_body = font(F_REG, 29)

rows = [
    ("QUANDO É PERMITIDO",
     "Padronização do objeto, compatibilidade com sistema já usado, exclusividade técnica comprovada ou mera referência com “ou equivalente”."),
    ("SEM JUSTIFICATIVA FORMAL?",
     "A exigência é ilegal e pode ser impugnada e derrubada antes mesmo de a disputa começar."),
]

for label, body in rows:
    center_text(draw, CX, y, label, f_label, GOLD)
    y += f_label.size + 18
    for line in wrap_text(draw, body, f_body, content_w):
        center_text(draw, CX, y, line, f_body, WHITE)
        y += 40
    y += 36

y += 6

# --- CTA button, centered ---
f_cta = font(F_BOLD, 33)
cta_text = "Fale com a Domina no direct  →"
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
