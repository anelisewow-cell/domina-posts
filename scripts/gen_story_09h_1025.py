#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import textwrap

W, H = 1080, 1920

NAVY_TOP = (14, 27, 51)
NAVY_BOTTOM = (23, 43, 77)
GOLD = (212, 175, 55)
GOLD_SOFT = (224, 196, 110)
WHITE = (247, 247, 245)
SUBTITLE = (170, 184, 209)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"

def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)

f_tag = font("DejaVuSans-Bold.ttf", 30)
f_title = font("DejaVuSans-Bold.ttf", 66)
f_body = font("DejaVuSans.ttf", 33)
f_cta = font("DejaVuSans-Bold.ttf", 32)
f_handle = font("DejaVuSans-Bold.ttf", 26)

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

MARGIN = 100
SAFE_TOP = 250
SAFE_BOTTOM = H - 250

# --- logo centralizada dentro da area segura superior ---
logo_size = 120
logo = Image.open("/home/user/domina-posts/logo_domina.png").convert("RGBA")
logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
logo_y = SAFE_TOP + 20
img.paste(logo, ((W - logo_size) // 2, logo_y), logo)

y = logo_y + logo_size + 50

# --- barra dourada vertical decorativa ---
bar_x = MARGIN
bar_top = y
bar_bottom = y + 420
draw.rectangle([bar_x, bar_top, bar_x + 6, bar_bottom], fill=GOLD)

text_x = bar_x + 44

tag = "TCU · ACÓRDÃO 1.064/2026"
draw.text((text_x, y + 4), tag, font=f_tag, fill=GOLD_SOFT)
y += 68

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
    y += 80

y += 36
support = "Só pode ser exigida prova de registro ou inscrição no conselho profissional — não comprovação de anuidades pagas (art. 67, Lei 14.133/2021)."
for line in textwrap.wrap(support, width=38):
    draw.text((text_x, y), line, font=f_body, fill=SUBTITLE)
    y += 48

# --- CTA pill ---
cta_text = "FALE COM A DOMINA LICITAÇÕES"
cta_h = 80
cta_y = y + 70
tw = draw.textlength(cta_text, font=f_cta)
cta_w = tw + 72
cta_x = text_x
draw.rounded_rectangle([cta_x, cta_y, cta_x + cta_w, cta_y + cta_h], radius=40, fill=GOLD)
draw.text((cta_x + (cta_w - tw) / 2, cta_y + 23), cta_text, font=f_cta, fill=(16, 22, 40))

# --- handle dentro da area segura inferior ---
handle = "@domina.licitacao"
hw = draw.textlength(handle, font=f_handle)
handle_y = SAFE_BOTTOM - 70
draw.text(((W - hw) / 2, handle_y), handle, font=f_handle, fill=SUBTITLE)

out = "/tmp/claude-0/-home-user-domina-posts/b406b6d9-c995-5a91-bf78-f3605f5a1af5/scratchpad/story.png"
img.save(out)
print("saved", out, img.size)
