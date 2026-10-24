#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import textwrap

W, H = 1080, 1080

# Paleta: azul marinho (oposta ao ultimo post, que era branco gelo)
NAVY_LEFT = (26, 48, 86)
NAVY_RIGHT = (12, 24, 46)
GOLD = (212, 175, 55)
WHITE = (247, 247, 245)
SUBTITLE = (178, 193, 217)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"

def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)

f_tag = font("DejaVuSans-Bold.ttf", 28)
f_title = font("DejaVuSans-Bold.ttf", 58)
f_body = font("DejaVuSans.ttf", 31)
f_cta = font("DejaVuSans-Bold.ttf", 29)

def horizontal_gradient(w, h, left, right):
    base = Image.new("RGB", (w, h), left)
    draw = ImageDraw.Draw(base)
    for x in range(w):
        t = x / w
        r = int(left[0] + (right[0] - left[0]) * t)
        g = int(left[1] + (right[1] - left[1]) * t)
        b = int(left[2] + (right[2] - left[2]) * t)
        draw.line([(x, 0), (x, h)], fill=(r, g, b))
    return base

def centered_text(draw, y, text, fnt, fill):
    tw = draw.textlength(text, font=fnt)
    draw.text(((W - tw) / 2, y), text, font=fnt, fill=fill)

img = horizontal_gradient(W, H, NAVY_LEFT, NAVY_RIGHT)
draw = ImageDraw.Draw(img)

MARGIN = 90

# Thin gold frame accents top corners (minimal, premium)
draw.line([(MARGIN, 64), (MARGIN + 130, 64)], fill=GOLD, width=2)
draw.line([(W - MARGIN - 130, 64), (W - MARGIN, 64)], fill=GOLD, width=2)

# Logo top center
logo_size = 100
logo = Image.open("/home/user/domina-posts/logo_domina.png").convert("RGBA")
logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
img.paste(logo, ((W - logo_size) // 2, 96), logo)

y = 96 + logo_size + 36

# Kicker centered
tag = "LEI 14.133/2021 · ART. 64"
centered_text(draw, y, tag, f_tag, GOLD)
y += 40
line_w = draw.textlength(tag, font=f_tag) + 40
draw.line([((W - line_w) / 2, y), ((W + line_w) / 2, y)], fill=GOLD, width=2)
y += 54

# Title centered, bold, short lines
title_lines = [
    ("Documento vencido", WHITE),
    ("na habilitação não é", WHITE),
    ("eliminação automática", GOLD),
]
for line, color in title_lines:
    tw = draw.textlength(line, font=f_title)
    draw.text(((W - tw) / 2, y), line, font=f_title, fill=color)
    y += 70

y += 30
# Divider
draw.line([(MARGIN + 60, y), (W - MARGIN - 60, y)], fill=(255, 255, 255, 60), width=1)
y += 42

support = "A lei permite diligência para atualizar certidões vencidas e esclarecer documentos já entregues — sem eliminar a empresa de cara."
for line in textwrap.wrap(support, width=40):
    tw = draw.textlength(line, font=f_body)
    draw.text(((W - tw) / 2, y), line, font=f_body, fill=SUBTITLE)
    y += 44

# CTA pill centered near bottom
cta_text = "Fale com a Domina Licitações"
cta_h = 72
cta_y = H - 150
tw = draw.textlength(cta_text, font=f_cta)
cta_w = tw + 70
cta_x = (W - cta_w) / 2
draw.rounded_rectangle([cta_x, cta_y, cta_x + cta_w, cta_y + cta_h], radius=36, fill=GOLD)
draw.text((cta_x + (cta_w - tw) / 2, cta_y + 20), cta_text, font=f_cta, fill=(16, 22, 40))

out = "/tmp/claude-0/-home-user-domina-posts/f189084e-6fc8-59cd-8476-f552abd815a4/scratchpad/post.png"
img.save(out)
print("saved", out)
