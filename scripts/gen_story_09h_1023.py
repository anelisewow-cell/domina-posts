#!/usr/bin/env python3.13
from PIL import Image, ImageDraw, ImageFont
import textwrap

W, H = 1080, 1920

NAVY_TOP = (14, 30, 58)
NAVY_BOTTOM = (22, 44, 82)
GOLD = (212, 175, 55)
WHITE = (247, 247, 245)
SUBTITLE = (178, 193, 217)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"

def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)

f_tag = font("DejaVuSans-Bold.ttf", 32)
f_title = font("DejaVuSans-Bold.ttf", 68)
f_stat = font("DejaVuSans-Bold.ttf", 76)
f_body = font("DejaVuSans.ttf", 34)
f_cta = font("DejaVuSans-Bold.ttf", 32)

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

MARGIN = 96
SAFE_TOP = 250
SAFE_BOTTOM = 250

# Decorative corner accents
draw.line([(MARGIN, SAFE_TOP - 60), (MARGIN + 140, SAFE_TOP - 60)], fill=GOLD, width=2)
draw.line([(W - MARGIN - 140, H - SAFE_BOTTOM + 60), (W - MARGIN, H - SAFE_BOTTOM + 60)], fill=GOLD, width=2)

y = SAFE_TOP

# Kicker
tag = "DECISÃO DO TCU"
draw.text((MARGIN, y), tag, font=f_tag, fill=GOLD)
y += 48
draw.line([(MARGIN, y), (MARGIN + 230, y)], fill=GOLD, width=3)
y += 70

# Title
title_lines = [
    ("Cota de aprendizes", WHITE),
    ("na habilitação:", WHITE),
    ("TCU diz que isso", WHITE),
    ("não tem respaldo", WHITE),
    ("legal", GOLD),
]
for line, color in title_lines:
    draw.text((MARGIN, y), line, font=f_title, fill=color)
    y += 82

y += 30
support = "Essa exigência é condição de execução do contrato, não da fase de habilitação."
for line in textwrap.wrap(support, width=36):
    draw.text((MARGIN, y), line, font=f_body, fill=SUBTITLE)
    y += 46

y += 50
draw.line([(MARGIN, y), (W - MARGIN, y)], fill=(255, 255, 255, 60), width=1)
y += 56

draw.text((MARGIN, y), "Apenas 2", font=f_stat, fill=GOLD)
y += 98
stat_support = "reservas de vaga podem ser cobradas na habilitação: PCD e reabilitados da Previdência (art. 63, IV)."
for line in textwrap.wrap(stat_support, width=36):
    draw.text((MARGIN, y), line, font=f_body, fill=WHITE)
    y += 46

# CTA pill + logo near bottom safe zone
cta_text = "Fale com a Domina Licitações"
cta_h = 80
cta_y = H - SAFE_BOTTOM - cta_h - 40
tw = draw.textlength(cta_text, font=f_cta)
cta_w = tw + 76
draw.rounded_rectangle([MARGIN, cta_y, MARGIN + cta_w, cta_y + cta_h], radius=40, fill=GOLD)
draw.text((MARGIN + (cta_w - tw) / 2, cta_y + 22), cta_text, font=f_cta, fill=(20, 24, 40))

logo_size = 110
logo = Image.open("/home/user/domina-posts/logo_domina.png").convert("RGBA")
logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
logo_x = W - MARGIN - logo_size
logo_y = cta_y + (cta_h - logo_size) // 2
img.paste(logo, (logo_x, logo_y), logo)

out = "/tmp/claude-0/-home-user-domina-posts/e9f92984-67f4-55e4-8070-9092cc390e9c/scratchpad/story.png"
img.save(out)
print("saved", out)
