#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Story 09h 2026-10-28: mesma arte do feed (certificacao pontua x habilitacao elimina),
versao vertical 1080x1920, conteudo centralizado na area segura."""
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920

NAVY_TOP = (14, 27, 51)
NAVY_BOTTOM = (23, 43, 77)
GOLD = (212, 175, 55)
GOLD_SOFT = (224, 196, 110)
WHITE = (247, 247, 245)
SUBTITLE = (170, 184, 209)
CARD_LINE = (58, 78, 112)
SOURCE_GRAY = (140, 155, 180)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


f_tag = font("DejaVuSans-Bold.ttf", 30)
f_title = font("DejaVuSans-Bold.ttf", 64)
f_body = font("DejaVuSans.ttf", 33)
f_card_label = font("DejaVuSans-Bold.ttf", 31)
f_card_body = font("DejaVuSans.ttf", 28)
f_source = font("DejaVuSans.ttf", 23)
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
CENTER_X = W // 2
SAFE_TOP = 250
SAFE_BOTTOM = H - 250


def text_w(txt, fnt):
    bbox = draw.textbbox((0, 0), txt, font=fnt)
    return bbox[2] - bbox[0]


def draw_center(y, txt, fnt, fill):
    w = text_w(txt, fnt)
    draw.text((CENTER_X - w / 2, y), txt, font=fnt, fill=fill)
    return w


def draw_center_mixed(y, parts, fnt):
    total_w = sum(text_w(t, fnt) for t, _ in parts)
    x = CENTER_X - total_w / 2
    for t, c in parts:
        draw.text((x, y), t, font=fnt, fill=c)
        x += text_w(t, fnt)


# --- logo centralizada no topo da area segura ---
logo_size = 118
logo = Image.open("/home/user/domina-posts/logo_domina.png").convert("RGBA")
logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
logo_y = SAFE_TOP + 30
img.paste(logo, (CENTER_X - logo_size // 2, logo_y), logo)

y = logo_y + logo_size + 56

tag = "TCU · ACÓRDÃO 1.093/2026"
draw_center(y, tag, f_tag, GOLD_SOFT)
y += 68

title_lines = [
    [("CERTIFICAÇÃO ", WHITE), ("PONTUA.", GOLD)],
    [("NA HABILITAÇÃO,", WHITE)],
    [("NÃO PODE ", WHITE), ("ELIMINAR.", GOLD)],
]
for parts in title_lines:
    draw_center_mixed(y, parts, f_title)
    y += 78

y += 30
support = ["ISO, PBQP-H e certificações do tipo só", "podem valer ponto na proposta técnica —", "nunca tirar sua empresa da disputa."]
for line in support:
    draw_center(y, line, f_body, SUBTITLE)
    y += 46

y += 56

card_x0 = MARGIN
card_x1 = W - MARGIN
row_h = 110


def comparison_row(y0, icon, icon_color, label, desc):
    draw.rectangle([card_x0, y0, card_x1, y0 + row_h], outline=CARD_LINE, width=1)
    icon_cx = card_x0 + 66
    draw.text((icon_cx - text_w(icon, f_title) / 2, y0 + row_h / 2 - 38), icon, font=f_title, fill=icon_color)
    tx = card_x0 + 128
    draw.text((tx, y0 + 20), label, font=f_card_label, fill=WHITE)
    draw.text((tx, y0 + 60), desc, font=f_card_body, fill=SUBTITLE)


comparison_row(y, "✓", GOLD, "PONTUAÇÃO TÉCNICA", "Soma pontos — você segue na disputa")
y += row_h + 22
comparison_row(y, "✗", (210, 110, 110), "HABILITAÇÃO", "Eliminatória — edital não pode confundir")
y += row_h + 56

source_line = "Fonte: TCU, Acórdão 1.093/2026-Plenário; Lei nº 14.133/2021"
draw_center(y, source_line, f_source, SOURCE_GRAY)
y += 70

cta_text = "FALE COM A DOMINA LICITAÇÕES"
cta_w = text_w(cta_text, f_cta)
pad_x = 44
pad_y = 22
btn_w = cta_w + pad_x * 2
btn_h = f_cta.size + pad_y * 2
btn_x0 = CENTER_X - btn_w / 2
btn_y0 = y
draw.rounded_rectangle([btn_x0, btn_y0, btn_x0 + btn_w, btn_y0 + btn_h], radius=btn_h // 2, fill=GOLD)
draw.text((btn_x0 + pad_x, btn_y0 + pad_y - 2), cta_text, font=f_cta, fill=(16, 22, 40))

handle = "@domina.licitacao"
hw = text_w(handle, f_handle)
handle_y = SAFE_BOTTOM - 60
draw_center(handle_y, handle, f_handle, SUBTITLE)

out = "/tmp/claude-0/-home-user-domina-posts/0cc84516-e6e6-592d-8ec9-775c26144841/scratchpad/story.png"
img.save(out)
print("saved", out, img.size)
