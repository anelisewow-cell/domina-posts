#!/usr/bin/env python3.13
from PIL import Image, ImageDraw, ImageFont
import textwrap

W, H = 1080, 1080

# Paleta: azul marinho (oposta ao ultimo post, que era branco gelo)
NAVY_TOP = (14, 30, 58)
NAVY_BOTTOM = (22, 44, 82)
GOLD = (212, 175, 55)
WHITE = (247, 247, 245)
SUBTITLE = (178, 193, 217)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"

def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)

f_tag = font("DejaVuSans-Bold.ttf", 30)
f_title = font("DejaVuSans-Bold.ttf", 64)
f_stat = font("DejaVuSans-Bold.ttf", 56)
f_body = font("DejaVuSans.ttf", 32)
f_cta = font("DejaVuSans-Bold.ttf", 30)

def vertical_gradient(w, h, top, bottom):
    base = Image.new("RGB", (w, h), top)
    draw = ImageDraw.Draw(base)
    for y in range(h):
        t = y / h
        r = int(top[0] + (bottom[0] - top[0]) * t)
        g = int(top[1] + (bottom[1] - top[1]) * t)
        b = int(top[2] + (bottom[2] - top[2]) * t)
        draw.line([(0, y), (w, y)], fill=(r, g, b))
    return base

img = vertical_gradient(W, H, NAVY_TOP, NAVY_BOTTOM)
draw = ImageDraw.Draw(img)

# Decorative thin gold corner accent (bottom-right), minimal/premium
draw.line([(W - 180, H - 40), (W - 40, H - 40)], fill=GOLD, width=2)
draw.line([(W - 40, H - 180), (W - 40, H - 40)], fill=GOLD, width=2)

MARGIN = 86

# Kicker
tag = "DECISÃO DO TCU"
draw.text((MARGIN, 88), tag, font=f_tag, fill=GOLD)
draw.line([(MARGIN, 134), (MARGIN + 215, 134)], fill=GOLD, width=3)

# Title block (left aligned, bold, short lines)
title_lines = [
    ("Cota de aprendizes", WHITE),
    ("na habilitação:", WHITE),
    ("TCU diz que isso", WHITE),
    ("não tem respaldo legal", GOLD),
]
y = 190
for line, color in title_lines:
    draw.text((MARGIN, y), line, font=f_title, fill=color)
    y += 76

# Support line
y += 24
support = "Essa exigência é condição de execução do contrato, não da fase de habilitação."
for line in textwrap.wrap(support, width=42):
    draw.text((MARGIN, y), line, font=f_body, fill=SUBTITLE)
    y += 42

# Divider
y += 28
draw.line([(MARGIN, y), (W - MARGIN, y)], fill=(255, 255, 255, 60), width=1)

# Stat highlight block
y += 36
draw.text((MARGIN, y), "Apenas 2", font=f_stat, fill=GOLD)
y += 72
stat_support = "reservas de vaga podem ser cobradas na habilitação: PCD e reabilitados da Previdência (art. 63, IV)."
for line in textwrap.wrap(stat_support, width=44):
    draw.text((MARGIN, y), line, font=f_body, fill=WHITE)
    y += 42

# CTA pill bottom-left
cta_text = "Fale com a Domina Licitações"
cta_h = 72
cta_y = H - 160
tw = draw.textlength(cta_text, font=f_cta)
cta_w = tw + 70
draw.rounded_rectangle([MARGIN, cta_y, MARGIN + cta_w, cta_y + cta_h], radius=36, fill=GOLD)
draw.text((MARGIN + (cta_w - tw) / 2, cta_y + 20), cta_text, font=f_cta, fill=(20, 24, 40))

# Logo bottom-right, vertically centered with CTA pill
logo_size = 105
logo = Image.open("/home/user/domina-posts/logo_domina.png").convert("RGBA")
logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
logo_x = W - MARGIN - logo_size
logo_y = cta_y + (cta_h - logo_size) // 2
img.paste(logo, (logo_x, logo_y), logo)

out = "/tmp/claude-0/-home-user-domina-posts/e9f92984-67f4-55e4-8070-9092cc390e9c/scratchpad/post.png"
img.save(out)
print("saved", out)
