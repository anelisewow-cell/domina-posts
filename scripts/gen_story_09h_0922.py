#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Story 2026-09-22 09h: Impugnacao de edital (vertical version of feed post)."""
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920

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

MARGIN_L = 96
MARGIN_R = 96
content_w = W - MARGIN_L - MARGIN_R

SAFE_TOP = 250
SAFE_BOTTOM = H - 250

y = SAFE_TOP + 20

# --- Logo top-center (in safe area) ---
logo = Image.open("/tmp/logo_domina.png").convert("RGBA")
logo_size = 120
logo_resized = logo.resize((logo_size, logo_size), Image.LANCZOS)
img.paste(logo_resized, (W // 2 - logo_size // 2, y), logo_resized)
y += logo_size + 40

# --- Ribbon label, centered ---
f_label = font(F_BOLD, 28)
label_text = "DIREITO DO LICITANTE"
tw = draw.textlength(label_text, font=f_label)
cx = W // 2
draw.text((cx - tw / 2, y), label_text, font=f_label, fill=GOLD)
y += 60

# --- Headline centered ---
f_head = font(F_BOLD, 56)
headline = "EDITAL COM EXIGÊNCIA ESTRANHA? DÁ PRA QUESTIONAR ANTES DA DISPUTA"
h_lines = wrap_text(draw, headline, f_head, content_w)
for line in h_lines:
    tw = draw.textlength(line, font=f_head)
    draw.text((cx - tw / 2, y), line, font=f_head, fill=WHITE)
    y += 66
y += 50

# --- Vertical timeline: 3 steps, left aligned block centered on canvas ---
steps = [
    ("ATÉ 3 DIAS ÚTEIS ANTES", "prazo para pedir esclarecimento ou impugnar o edital"),
    ("QUALQUER INTERESSADO", "pode protocolar — mesmo antes de estar inscrito na disputa"),
    ("RESPOSTA EM ATÉ 3 DIAS ÚTEIS", "a administração é obrigada a responder antes da abertura"),
]

f_step_title = font(F_BOLD, 34)
f_step_cap = font(F_REG, 28)

block_x = MARGIN_L + 40
dot_x = block_x
text_x = block_x + 50
text_w = content_w - 90

step_positions = []
line_top = y + 16
cy = y
for title, cap in steps:
    step_positions.append(cy + 16)
    draw.text((text_x, cy), title, font=f_step_title, fill=GOLD)
    cy += 46
    cap_lines = wrap_text(draw, cap, f_step_cap, text_w)
    for line in cap_lines:
        draw.text((text_x, cy), line, font=f_step_cap, fill=LIGHT_GRAY)
        cy += 36
    cy += 44

line_bottom = step_positions[-1]
draw.line([(dot_x, line_top), (dot_x, line_bottom)], fill=(120, 130, 160), width=3)
for i, pos in enumerate(step_positions):
    r = 12
    fill = GOLD if i != 1 else WHITE
    draw.ellipse([dot_x - r, pos - r, dot_x + r, pos + r], fill=fill)

y = cy + 10
draw.line([(MARGIN_L, y), (MARGIN_L + content_w, y)], fill=(90, 100, 130), width=2)
y += 44

# --- Support paragraph centered ---
f_support = font(F_REG, 32)
support_text = "Cláusula restritiva ou confusa no edital? Esse é o momento de agir — antes de perder tempo com uma disputa mal desenhada."
s_lines = wrap_text(draw, support_text, f_support, content_w)
for line in s_lines:
    tw = draw.textlength(line, font=f_support)
    draw.text((cx - tw / 2, y), line, font=f_support, fill=WHITE)
    y += 44

y += 40

# --- CTA button centered ---
f_cta = font(F_BOLD, 32)
cta_text = "Manda o edital pra Domina analisar"
tw = draw.textlength(cta_text, font=f_cta)
btn_pad_x, btn_pad_y = 36, 22
btn_w = tw + btn_pad_x * 2
btn_h = f_cta.size + btn_pad_y * 2
bx0 = cx - btn_w / 2
draw.rounded_rectangle([bx0, y, bx0 + btn_w, y + btn_h], radius=btn_h // 2, fill=GOLD)
draw.text((bx0 + btn_pad_x, y + btn_pad_y - 4), cta_text, font=f_cta, fill=DARK_TEXT)
y += btn_h

assert y < SAFE_BOTTOM, f"content overflows safe area: y={y}, safe_bottom={SAFE_BOTTOM}"

img.save("/tmp/story.png")
print("saved", img.size, "content_bottom_y=", y, "safe_bottom=", SAFE_BOTTOM)
