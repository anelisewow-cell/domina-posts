#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Post 18h 2026-10-13: licitacao exclusiva para ME/EPP até R$80 mil
(art. 48, I, LC 123/2006, aplicado via art. 4o da Lei 14.133/2021).
Angulo comercial/leve: empresa pequena tem prioridade legal em compras
publicas de menor valor - oportunidade que muita empresa nao conhece.
CTA direto para contratar a Domina.

Paleta: azul marinho solido (oposta ao post das 9h de hoje, que foi
branco gelo). Layout variado: logo no topo ESQUERDO (nos ultimos posts
estava no topo direito), badge no topo DIREITO, titulo em formato de
ESTATISTICA GRANDE centralizada (R$ 80 MIL em destaque), fileira
horizontal de 3 recursos com marcador - nao repete a timeline vertical
de hoje de manha nem o bloco MITO/VERDADE alinhado a esquerda de dois
dias atras.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1080

NAVY = (12, 22, 46)
WHITE = (247, 246, 240)
SUBTITLE = (164, 177, 203)
GOLD = (212, 175, 55)
GOLD_DARK_TEXT = (24, 20, 4)
LINE = (54, 68, 100)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
def F(size):
    return ImageFont.truetype(FONT_DIR + "DejaVuSans-Bold.ttf", size)
def FR(size):
    return ImageFont.truetype(FONT_DIR + "DejaVuSans.ttf", size)

img = Image.new("RGB", (W, H), NAVY)
d = ImageDraw.Draw(img)
MARGIN = 72

def text_w(s, font):
    bbox = d.textbbox((0, 0), s, font=font)
    return bbox[2] - bbox[0]

def wrap(text, font, max_w):
    words = text.split(" ")
    lines, cur = [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if text_w(trial, font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines

def center_text(y, text, font, fill):
    tw = text_w(text, font)
    d.text(((W - tw) / 2, y), text, font=font, fill=fill)

def rounded_pill(xy, radius, fill=None, outline=None, width=2):
    d.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)

# --- logo, top-left ---
logo = Image.open("/home/user/domina-posts/logo_domina.png").convert("RGBA")
logo_size = 105
logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
img.paste(logo, (MARGIN, 54), logo)

# --- badge pill, top-right ---
badge_font = F(22)
badge_text = "LC 123/2006 · ART. 48"
tw = text_w(badge_text, badge_font)
pad_x, pad_y = 22, 12
bx1, by0 = W - MARGIN, 72
bx0 = bx1 - (tw + pad_x * 2)
by1 = by0 + 22 + pad_y * 2
rounded_pill((bx0, by0, bx1, by1), radius=(by1 - by0) // 2, outline=GOLD, width=2)
d.text((bx0 + pad_x, by0 + pad_y - 1), badge_text, font=badge_font, fill=GOLD)

# --- eyebrow, centered ---
eyebrow_font = F(26)
eyebrow = "COMPRAS PÚBLICAS ATÉ"
ey = 218
center_text(ey, eyebrow, eyebrow_font, SUBTITLE)

# --- big stat, centered ---
stat_font = F(142)
stat_text = "R$ 80 MIL"
sy = ey + 54
center_text(sy, stat_text, stat_font, GOLD)

# --- stat caption, centered ---
cap_font = F(40)
cap_lines = ["SÃO SÓ PARA", "EMPRESA PEQUENA."]
cy = sy + 162
for line in cap_lines:
    center_text(cy, line, cap_font, WHITE)
    cy += 52

# --- subtitle, centered ---
sub_font = FR(26)
subtitle = "A lei reserva essas disputas para micro e pequenas empresas — sem concorrer com as grandes. Muita empresa nem sabe que já pode entrar nelas."
sub_lines = wrap(subtitle, sub_font, 820)
suby = cy + 28
for line in sub_lines:
    center_text(suby, line, sub_font, SUBTITLE)
    suby += 34

# --- divider ---
dy = suby + 20
d.line([(MARGIN, dy), (W - MARGIN, dy)], fill=LINE, width=2)

# --- 3 features, horizontal row ---
features = [
    "Disputa exclusiva ME/EPP até R$ 80 mil",
    "Cota de até 25% do objeto reservada",
    "Subcontratação de ME/EPP garantida",
]
label_font = F(22)
col_w = (W - 2 * MARGIN) / 3
col_pad = 22
fy = dy + 40
for i, feat in enumerate(features):
    cx = MARGIN + col_w * i + col_w / 2
    lines = wrap(feat, label_font, col_w - 2 * col_pad)
    d.text((cx - 10, fy - 8), "•", font=F(30), fill=GOLD)
    yy = fy + 10
    for ln in lines:
        lw = text_w(ln, label_font)
        d.text((cx - lw / 2, yy), ln, font=label_font, fill=WHITE)
        yy += 30
    if i < 2:
        sep_x = MARGIN + col_w * (i + 1)
        d.line([(sep_x, fy - 6), (sep_x, fy + 78)], fill=LINE, width=2)

# --- CTA pill, centered, bottom ---
cta_font = F(29)
cta_text = "Fale com a Domina no direct  →"
tw3 = text_w(cta_text, cta_font)
pad_x3, pad_y3 = 38, 21
cy1 = H - 80
cy0 = cy1 - (24 + pad_y3 * 2)
cx0 = (W - (tw3 + pad_x3 * 2)) / 2
cx1 = cx0 + tw3 + pad_x3 * 2
rounded_pill((cx0, cy0, cx1, cy1), radius=(cy1 - cy0) // 2, fill=GOLD)
d.text((cx0 + pad_x3, cy0 + pad_y3 - 2), cta_text, font=cta_font, fill=GOLD_DARK_TEXT)

out_path = "/home/user/domina-posts/images/post-2026-10-13-18h-licitacao-exclusiva-me-epp-art48.png"
img.save(out_path)
print("saved", out_path, img.size)
