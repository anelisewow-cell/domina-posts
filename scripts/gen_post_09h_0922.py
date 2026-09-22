#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Post 9h 2026-09-22: Impugnacao de edital e pedido de esclarecimento (art. 164, Lei 14.133/2021)."""
from PIL import Image, ImageDraw, ImageFont

W = H = 1080

NAVY_TOP = (12, 18, 46)
NAVY_BOTTOM = (30, 40, 88)
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


img = Image.new("RGB", (W, H), NAVY_TOP)
draw = ImageDraw.Draw(img)
vertical_gradient(draw, W, H, NAVY_TOP, NAVY_BOTTOM)

# thin gold frame accent (variation vs. corner triangles / top-bottom bars used previously)
draw.rectangle([28, 28, W - 28, H - 28], outline=GOLD, width=3)

MARGIN_L = 96
MARGIN_R = 96
content_w = W - MARGIN_L - MARGIN_R

y = 96

# --- Ribbon label, left aligned near top ---
f_label = font(F_BOLD, 25)
label_text = "DIREITO DO LICITANTE"
draw.line([(MARGIN_L, y + 17), (MARGIN_L + 46, y + 17)], fill=GOLD, width=4)
draw.text((MARGIN_L + 62, y), label_text, font=f_label, fill=GOLD)
y += 62

# --- Headline, left aligned ---
f_head = font(F_BOLD, 50)
headline = "EDITAL COM EXIGÊNCIA ESTRANHA? DÁ PRA QUESTIONAR ANTES DA DISPUTA"
h_lines = wrap_text(draw, headline, f_head, content_w)
for line in h_lines:
    draw.text((MARGIN_L, y), line, font=f_head, fill=WHITE)
    y += 58
y += 34

# --- Vertical timeline: 3 steps ---
steps = [
    ("ATÉ 3 DIAS ÚTEIS ANTES", "prazo para pedir esclarecimento ou impugnar o edital"),
    ("QUALQUER INTERESSADO", "pode protocolar — mesmo antes de estar inscrito na disputa"),
    ("RESPOSTA EM ATÉ 3 DIAS ÚTEIS", "a administração é obrigada a responder antes da abertura"),
]

f_step_title = font(F_BOLD, 30)
f_step_cap = font(F_REG, 25)

dot_x = MARGIN_L + 14
text_x = MARGIN_L + 56
line_top = y + 14
step_positions = []

cy = y
for i, (title, cap) in enumerate(steps):
    step_positions.append(cy + 14)
    draw.text((text_x, cy), title, font=f_step_title, fill=GOLD)
    cy += 40
    cap_lines = wrap_text(draw, cap, f_step_cap, content_w - 56)
    for line in cap_lines:
        draw.text((text_x, cy), line, font=f_step_cap, fill=LIGHT_GRAY)
        cy += 32
    cy += 34

line_bottom = step_positions[-1]
draw.line([(dot_x, line_top), (dot_x, line_bottom)], fill=(120, 130, 160), width=3)

for i, pos in enumerate(step_positions):
    r = 11
    fill = GOLD if i != 1 else WHITE
    draw.ellipse([dot_x - r, pos - r, dot_x + r, pos + r], fill=fill)

y = cy - 12
draw.line([(MARGIN_L, y), (MARGIN_L + content_w, y)], fill=(90, 100, 130), width=2)
y += 34

# --- Support paragraph ---
f_support = font(F_REG, 29)
support_text = "Cláusula restritiva ou confusa no edital? Esse é o momento de agir — antes de perder tempo com uma disputa mal desenhada."
s_lines = wrap_text(draw, support_text, f_support, content_w)
for line in s_lines:
    draw.text((MARGIN_L, y), line, font=f_support, fill=WHITE)
    y += 40

y += 30

# --- CTA button, left aligned ---
f_cta = font(F_BOLD, 29)
cta_text = "Manda o edital pra Domina analisar"
tw = draw.textlength(cta_text, font=f_cta)
btn_pad_x, btn_pad_y = 32, 18
btn_w = tw + btn_pad_x * 2
btn_h = f_cta.size + btn_pad_y * 2
draw.rounded_rectangle([MARGIN_L, y, MARGIN_L + btn_w, y + btn_h], radius=btn_h // 2, fill=GOLD)
draw.text((MARGIN_L + btn_pad_x, y + btn_pad_y - 4), cta_text, font=f_cta, fill=DARK_TEXT)

# --- Logo bottom-right (variation vs. top-center/top-right used previously) ---
logo = Image.open("/tmp/logo_domina.png").convert("RGBA")
logo_size = 100
logo_resized = logo.resize((logo_size, logo_size), Image.LANCZOS)
logo_x = W - MARGIN_R - logo_size
logo_y = H - 96 - logo_size
img.paste(logo_resized, (logo_x, logo_y), logo_resized)

img.save("/tmp/post.png")
print("saved", img.size)
