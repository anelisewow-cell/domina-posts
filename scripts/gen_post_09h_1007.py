#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Post 9h 2026-10-07: marca especifica em edital - regra x excecao (art. 41, Lei 14.133/2021)."""
from PIL import Image, ImageDraw, ImageFont

W = H = 1080

NAVY_TOP = (9, 20, 46)
NAVY_BOTTOM = (26, 54, 102)
GOLD = (212, 175, 55)
WHITE = (255, 255, 255)
LIGHT_GRAY = (198, 206, 224)
DARK_TEXT = (20, 24, 40)
LINE = (90, 108, 150)

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


img = Image.new("RGB", (W, H), NAVY_TOP)
draw = ImageDraw.Draw(img)
vertical_gradient(draw, W, H, NAVY_TOP, NAVY_BOTTOM)

MARGIN_L = 94
MARGIN_R = 94
content_w = W - MARGIN_L - MARGIN_R

# --- decorative corner brackets ---
BR_LEN = 38
draw.line([(40, 40), (40, 40 + BR_LEN)], fill=GOLD, width=2)
draw.line([(40, 40), (40 + BR_LEN, 40)], fill=GOLD, width=2)
draw.line([(W - 40, H - 40), (W - 40, H - 40 - BR_LEN)], fill=GOLD, width=2)
draw.line([(W - 40, H - 40), (W - 40 - BR_LEN, H - 40)], fill=GOLD, width=2)

# --- Logo top-left ---
logo = Image.open("/tmp/logo_domina.png").convert("RGBA")
logo_size = 105
logo_resized = logo.resize((logo_size, logo_size), Image.LANCZOS)
logo_x = MARGIN_L
logo_y = 72
img.paste(logo_resized, (logo_x, logo_y), logo_resized)

y = logo_y + logo_size + 44

# --- pill badge, left aligned ---
f_badge_txt = font(F_BOLD, 24)
badge_text = "LEI 14.133/2021  ·  ART. 41"
btw = draw.textlength(badge_text, font=f_badge_txt)
pad_x, pad_y = 26, 14
bw = btw + pad_x * 2
bh = f_badge_txt.size + pad_y * 2
draw.rounded_rectangle([MARGIN_L, y, MARGIN_L + bw, y + bh], radius=bh // 2, outline=GOLD, width=2)
draw.text((MARGIN_L + pad_x, y + pad_y - 2), badge_text, font=f_badge_txt, fill=GOLD)

y += bh + 44

# --- Headline, left aligned, 3 short lines ---
f_head = font(F_BOLD, 54)
head_lines = [
    ("EDITAL EXIGINDO", WHITE),
    ("MARCA ESPECÍFICA?", GOLD),
    ("A REGRA É NÃO PODER.", WHITE),
]
for line, color in head_lines:
    draw.text((MARGIN_L, y), line, font=f_head, fill=color)
    y += 60

y += 18

f_sub = font(F_REG, 27)
sub_text = ("A Lei 14.133/2021 proíbe, por padrão, a exigência de marca ou modelo no edital. "
            "Ela só é permitida em hipóteses específicas — e sempre com justificativa técnica formal.")
for line in wrap_text(draw, sub_text, f_sub, content_w):
    draw.text((MARGIN_L, y), line, font=f_sub, fill=LIGHT_GRAY)
    y += 36

y += 26
draw.line([(MARGIN_L, y), (W - MARGIN_R, y)], fill=LINE, width=2)
y += 36

# --- label + body rows ---
f_label = font(F_BOLD, 27)
f_body = font(F_REG, 26)

rows = [
    ("QUANDO É PERMITIDO",
     "Padronização do objeto, compatibilidade com sistema já usado pelo órgão, exclusividade técnica comprovada ou mera referência, com “ou equivalente”."),
    ("SEM JUSTIFICATIVA FORMAL?",
     "A exigência é ilegal e pode ser impugnada e derrubada antes mesmo de a disputa começar."),
]

for label, body in rows:
    draw.text((MARGIN_L, y), label, font=f_label, fill=GOLD)
    y += f_label.size + 12
    for line in wrap_text(draw, body, f_body, content_w):
        draw.text((MARGIN_L, y), line, font=f_body, fill=WHITE)
        y += 33
    y += 16

# --- CTA button, left aligned ---
f_cta = font(F_BOLD, 29)
cta_text = "Fale com a Domina no direct  →"
tw = draw.textlength(cta_text, font=f_cta)
btn_pad_x, btn_pad_y = 32, 18
btn_w = tw + btn_pad_x * 2
btn_h = f_cta.size + btn_pad_y * 2
bx0 = MARGIN_L
draw.rounded_rectangle([bx0, y, bx0 + btn_w, y + btn_h], radius=btn_h // 2, fill=GOLD)
draw.text((bx0 + btn_pad_x, y + btn_pad_y - 4), cta_text, font=f_cta, fill=DARK_TEXT)

assert y + btn_h <= H - 40, f"content overflow: {y + btn_h}"

img.save("/tmp/post.png")
print("saved", img.size, "bottom:", y + btn_h)
