#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Post 18h 2026-09-20: Mito x Verdade - pequenas empresas em licitações."""
from PIL import Image, ImageDraw, ImageFont

W = H = 1080

NAVY_TOP = (8, 20, 46)
NAVY_BOTTOM = (18, 40, 82)
GOLD = (212, 175, 55)
WHITE = (255, 255, 255)
LIGHT_GRAY = (198, 206, 224)
DARK_TEXT = (20, 24, 40)

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


def draw_pill(draw, xy, text, fnt, pad_x=22, pad_y=12, outline=GOLD, textcolor=GOLD, width=2):
    x, y = xy
    tw = draw.textlength(text, font=fnt)
    th = fnt.size
    x0, y0 = x, y
    x1, y1 = x + tw + pad_x * 2, y + th + pad_y * 2
    radius = (y1 - y0) // 2
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, outline=outline, width=width)
    draw.text((x0 + pad_x, y0 + pad_y - 2), text, font=fnt, fill=textcolor)
    return x1 - x0, y1 - y0


img = Image.new("RGB", (W, H), NAVY_TOP)
draw = ImageDraw.Draw(img)
vertical_gradient(draw, W, H, NAVY_TOP, NAVY_BOTTOM)

# thin gold accent line on right edge (decorative, varies layout from previous posts)
draw.rectangle([W - 14, 0, W - 8, H], fill=GOLD)

MARGIN_L = 84
MARGIN_R = 130
content_w = W - MARGIN_L - MARGIN_R

# --- Logo top-left (varied position vs previous bottom-center placements) ---
logo = Image.open("/tmp/logo_domina.png").convert("RGBA")
logo_size = 100
logo_resized = logo.resize((logo_size, logo_size), Image.LANCZOS)
logo_y = 70
img.paste(logo_resized, (MARGIN_L, logo_y), logo_resized)

f_brand = font(F_BOLD, 30)
draw.text((MARGIN_L + logo_size + 20, logo_y + 30), "DOMINA", font=f_brand, fill=WHITE)
f_brand_sub = font(F_REG, 16)
draw.text((MARGIN_L + logo_size + 20, logo_y + 65), "LICITAÇÕES", font=f_brand_sub, fill=LIGHT_GRAY)

# --- Pill badge ---
f_pill = font(F_BOLD, 24)
pill_y = logo_y + logo_size + 40
draw_pill(draw, (MARGIN_L, pill_y), "MITO x VERDADE", f_pill)

# --- MITO block ---
y = pill_y + 90
f_label = font(F_BOLD, 30)
draw.text((MARGIN_L, y), "MITO", font=f_label, fill=GOLD)
y += 46

f_mito = font(F_BOLD, 46)
mito_text = "Empresa pequena não tem chance em licitação pública."
lines = wrap_text(draw, mito_text, f_mito, content_w)
for line in lines:
    draw.text((MARGIN_L, y), line, font=f_mito, fill=WHITE)
    y += 56

# strike-through effect on first line to reinforce "myth" visually
if lines:
    first_w = draw.textlength(lines[0], font=f_mito)
    strike_y = y - len(lines) * 56 + 28
    draw.line([(MARGIN_L, strike_y), (MARGIN_L + first_w, strike_y)], fill=(180, 60, 60), width=5)

y += 26

# --- VERDADE block ---
f_label2 = font(F_BOLD, 30)
draw.text((MARGIN_L, y), "VERDADE", font=f_label2, fill=GOLD)
y += 46

f_verdade = font(F_BOLD, 46)
verdade_line1 = "A Lei 14.133/2021 reserva "
verdade_highlight = "25% das compras"
verdade_line1b = " e"

# Build multi-run wrapped text manually for highlight control
full_text_parts = [
    ("A Lei 14.133/2021 reserva até 25% das compras públicas divisíveis e itens de até R$ 80 mil só para ME/EPP.", WHITE),
]
verdade_full = "A Lei 14.133/2021 reserva até 25% das compras públicas divisíveis e itens de até R$ 80 mil só para ME/EPP."
v_lines = wrap_text(draw, verdade_full, f_verdade, content_w)
for line in v_lines:
    # highlight numbers in gold by drawing word by word
    words = line.split(" ")
    cursor_x = MARGIN_L
    for w in words:
        clean = w.strip(".,")
        is_gold = any(ch.isdigit() for ch in w) or w in ("ME/EPP.", "ME/EPP")
        color = GOLD if is_gold else WHITE
        draw.text((cursor_x, y), w, font=f_verdade, fill=color)
        cursor_x += draw.textlength(w + " ", font=f_verdade)
    y += 56

y += 20
f_support = font(F_REG, 30)
support_text = "Vale também o \"empate ficto\": até 10% de diferença de preço e sua empresa pode cobrir a proposta e vencer."
s_lines = wrap_text(draw, support_text, f_support, content_w)
for line in s_lines:
    draw.text((MARGIN_L, y), line, font=f_support, fill=LIGHT_GRAY)
    y += 40

# --- CTA button ---
y += 40
f_cta = font(F_BOLD, 32)
cta_text = "Fale com a Domina e garanta seu espaço →"
tw = draw.textlength(cta_text, font=f_cta)
btn_pad_x, btn_pad_y = 34, 22
btn_w = tw + btn_pad_x * 2
btn_h = f_cta.size + btn_pad_y * 2
draw.rounded_rectangle([MARGIN_L, y, MARGIN_L + btn_w, y + btn_h], radius=btn_h // 2, fill=GOLD)
draw.text((MARGIN_L + btn_pad_x, y + btn_pad_y - 4), cta_text, font=f_cta, fill=DARK_TEXT)

img.save("/tmp/post.png")
print("saved", img.size)
