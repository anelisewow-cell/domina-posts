#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import textwrap

W, H = 1080, 1080

# Paleta: azul marinho (oposta ao ultimo post, que foi branco gelo)
NAVY_TOP = (14, 27, 51)
NAVY_BOTTOM = (23, 43, 77)
GOLD = (212, 175, 55)
GOLD_SOFT = (224, 196, 110)
WHITE = (247, 247, 245)
SUBTITLE = (170, 184, 209)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"

def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)

f_tag = font("DejaVuSans-Bold.ttf", 26)
f_title = font("DejaVuSans-Bold.ttf", 60)
f_body = font("DejaVuSans.ttf", 30)
f_cta = font("DejaVuSans-Bold.ttf", 28)
f_handle = font("DejaVuSans-Bold.ttf", 22)

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

# --- logo pequena no topo-direita ---
logo_size = 92
logo = Image.open("/home/user/domina-posts/logo_domina.png").convert("RGBA")
logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
img.paste(logo, (W - MARGIN - logo_size, 84), logo)

# --- barra dourada vertical decorativa a esquerda do bloco de titulo ---
bar_x = MARGIN
bar_top = 300
bar_bottom = 620
draw.rectangle([bar_x, bar_top, bar_x + 5, bar_bottom], fill=GOLD)

text_x = bar_x + 38

# --- kicker alinhado a esquerda ---
y = bar_top - 6
tag = "TCU · ACÓRDÃO 1.064/2026"
draw.text((text_x, y), tag, font=f_tag, fill=GOLD_SOFT)
y += 58

# --- titulo alinhado a esquerda, 3 linhas curtas ---
title_lines = [
    [("EXIGIR QUITAÇÃO", WHITE)],
    [("DO CONSELHO NA", WHITE)],
    [("HABILITAÇÃO É ", WHITE), ("ILEGAL", GOLD)],
]
for parts in title_lines:
    x = text_x
    for t, c in parts:
        draw.text((x, y), t, font=f_title, fill=c)
        x += draw.textlength(t, font=f_title)
    y += 72

y += 28
support = "Só pode ser exigida prova de registro ou inscrição no conselho profissional — não comprovação de anuidades pagas (art. 67, Lei 14.133/2021)."
for line in textwrap.wrap(support, width=42):
    draw.text((text_x, y), line, font=f_body, fill=SUBTITLE)
    y += 44

# --- CTA pill alinhado a esquerda ---
cta_text = "FALE COM A DOMINA LICITAÇÕES"
cta_h = 72
cta_y = 840
tw = draw.textlength(cta_text, font=f_cta)
cta_w = tw + 68
cta_x = text_x
draw.rounded_rectangle([cta_x, cta_y, cta_x + cta_w, cta_y + cta_h], radius=36, fill=GOLD)
draw.text((cta_x + (cta_w - tw) / 2, cta_y + 21), cta_text, font=f_cta, fill=(16, 22, 40))

# --- linha fina dourada e handle no rodape ---
foot_y = H - 70
draw.line([(MARGIN, foot_y - 24), (W - MARGIN, foot_y - 24)], fill=(255, 255, 255), width=0)
handle = "@domina.licitacao"
hw = draw.textlength(handle, font=f_handle)
draw.text(((W - hw) / 2, foot_y), handle, font=f_handle, fill=SUBTITLE)

out = "/tmp/claude-0/-home-user-domina-posts/b406b6d9-c995-5a91-bf78-f3605f5a1af5/scratchpad/post.png"
img.save(out)
print("saved", out, img.size)
