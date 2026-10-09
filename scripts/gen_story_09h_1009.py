#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import textwrap

W, H = 1080, 1920
GOLD = (212, 175, 55)
NAVY_TOP = (10, 18, 42)
NAVY_BOTTOM = (22, 36, 68)
WHITE = (255, 255, 255)
SUBTLE = (176, 188, 212)
DARK_TEXT = (16, 24, 48)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
def font(size, bold=True):
    path = FONT_DIR + ("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf")
    return ImageFont.truetype(path, size)

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

def right_align_text(draw, x_right, y, text, fnt, fill):
    bbox = draw.textbbox((0, 0), text, font=fnt)
    tw = bbox[2] - bbox[0]
    draw.text((x_right - tw, y), text, font=fnt, fill=fill)
    return tw

img = vertical_gradient(W, H, NAVY_TOP, NAVY_BOTTOM)
draw = ImageDraw.Draw(img)

MARGIN_R = 100
MARGIN_L = 100
SAFE_TOP = 250
SAFE_BOTTOM = H - 250

# thin gold vertical accent line on the left (within safe area)
draw.line([(MARGIN_L, SAFE_TOP + 40), (MARGIN_L, SAFE_BOTTOM - 40)], fill=GOLD, width=3)

# logo centered top, inside safe area
logo = Image.open("/home/user/domina-posts/logo_domina.png").convert("RGBA")
logo_size = 110
logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
logo_x = (W - logo_size) // 2
img.paste(logo, (logo_x, SAFE_TOP), logo)

# badge pill, right-aligned
badge_text = "LEI 14.133/2021 · ART. 61"
badge_font = font(28)
bbox = draw.textbbox((0, 0), badge_text, font=badge_font)
tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
pad_x, pad_y = 28, 16
badge_w = tw + pad_x * 2
badge_h = th + pad_y * 2
badge_x1 = W - MARGIN_R
badge_x0 = badge_x1 - badge_w
badge_y0 = SAFE_TOP + 190
badge_y1 = badge_y0 + badge_h
draw.rounded_rectangle([badge_x0, badge_y0, badge_x1, badge_y1], radius=badge_h // 2, outline=GOLD, width=2)
draw.text((badge_x0 + pad_x, badge_y0 + pad_y - bbox[1]), badge_text, font=badge_font, fill=GOLD)

# Title, right-aligned
title_font = font(74)
title_lines = [
    ("Vencer o preço", WHITE),
    ("não encerra", WHITE),
    ("a disputa.", GOLD),
]
y = badge_y1 + 90
line_gap = 92
for text, color in title_lines:
    right_align_text(draw, W - MARGIN_R, y, text, title_font, color)
    y += line_gap

# subtitle, right-aligned, wrapped
sub_font = font(33, bold=False)
subtitle = "Pelo art. 61 da Lei 14.133/2021, a Administração pode negociar um preço ainda melhor com quem fica em 1º lugar — antes de declarar o resultado final."
wrapped = textwrap.wrap(subtitle, width=36)
y += 40
for line in wrapped:
    right_align_text(draw, W - MARGIN_R, y, line, sub_font, SUBTLE)
    y += 48

# divider
y += 30
draw.line([(W - MARGIN_R - 200, y), (W - MARGIN_R, y)], fill=GOLD, width=3)

# CTA button, right-aligned, kept within safe bottom area
cta_text = "FALE COM A DOMINA"
cta_font = font(32)
bbox = draw.textbbox((0, 0), cta_text, font=cta_font)
tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
pad_x, pad_y = 46, 26
btn_w = tw + pad_x * 2
btn_h = th + pad_y * 2
btn_x1 = W - MARGIN_R
btn_x0 = btn_x1 - btn_w
btn_y0 = min(y + 60, SAFE_BOTTOM - btn_h - 20)
btn_y1 = btn_y0 + btn_h
draw.rounded_rectangle([btn_x0, btn_y0, btn_x1, btn_y1], radius=btn_h // 2, fill=GOLD)
draw.text((btn_x0 + pad_x, btn_y0 + pad_y - bbox[1]), cta_text, font=cta_font, fill=DARK_TEXT)

img.save("/tmp/story.png")
print("saved", img.size)
