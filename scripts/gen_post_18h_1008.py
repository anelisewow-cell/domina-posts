#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Post 18h 2026-10-08: prazos minimos de publicacao do edital (art. 55,
Lei 14.133/2021) - quanto tempo a empresa tem entre a publicacao do edital
e a abertura das propostas. Angulo comercial: quem nao monitora o PNCP todo
dia pode perder editais mesmo dentro do prazo legal.

Paleta: branco gelo (oposta ao post das 9h de hoje, cuja capa/post
"mais recente" foi azul marinho).
Layout variado: tudo alinhado a esquerda, logo no topo esquerdo, kicker em
pill a direita (nao repete capa centralizada nem lista com circulos do post
das 9h); lista de prazos em duas colunas compactas (categoria x dias).
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1080

OFFWHITE = (247, 246, 240)
NAVY_TEXT = (16, 28, 58)
SUBTLE = (94, 104, 128)
GOLD_ON_LIGHT = (196, 154, 61)
LINE_ON_LIGHT = (214, 208, 190)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
F_BOLD = FONT_DIR + "DejaVuSans-Bold.ttf"
F_REG = FONT_DIR + "DejaVuSans.ttf"
LOGO_PATH = "/home/user/domina-posts/logo_domina.png"


def font(path, size):
    return ImageFont.truetype(path, size)


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


def paste_logo(img, size, pos):
    logo = Image.open(LOGO_PATH).convert("RGBA")
    logo = logo.resize((size, size), Image.LANCZOS)
    img.paste(logo, pos, logo)


def pill_right(draw, right_x, y, text, fnt, outline):
    tw = draw.textlength(text, font=fnt)
    pad_x, pad_y = 24, 12
    h = fnt.size + pad_y * 2
    x1 = right_x
    x0 = x1 - tw - pad_x * 2
    draw.rounded_rectangle([x0, y, x1, y + h], radius=h / 2, outline=outline, width=2)
    draw.text((x0 + pad_x, y + pad_y - 2), text, font=fnt, fill=outline)
    return h


def rounded_button(draw, xy, text, fnt, fill_btn, fill_text, pad_x=36, pad_y=20):
    x, y = xy
    tw = draw.textlength(text, font=fnt)
    th = fnt.size
    w = tw + pad_x * 2
    h = th + pad_y * 2
    draw.rounded_rectangle([x, y, x + w, y + h], radius=h // 2, fill=fill_btn)
    draw.text((x + pad_x, y + pad_y), text, font=fnt, fill=fill_text)
    return x, y, x + w, y + h


def build():
    img = Image.new("RGB", (W, H), OFFWHITE)
    draw = ImageDraw.Draw(img)

    MARGIN_L = 90
    MARGIN_R = 90
    content_w = W - MARGIN_L - MARGIN_R

    # top row: logo left, kicker pill right
    logo_size = 105
    paste_logo(img, size=logo_size, pos=(MARGIN_L, 64))

    f_pill = font(F_BOLD, 23)
    pill_right(draw, W - MARGIN_R, 64 + logo_size / 2 - 23, "LEI 14.133/2021 · ART. 55", f_pill, GOLD_ON_LIGHT)

    y = 64 + logo_size + 54

    f_head = font(F_BOLD, 66)
    draw.text((MARGIN_L, y), "SEU EDITAL PODE", font=f_head, fill=NAVY_TEXT)
    y += 76
    draw.text((MARGIN_L, y), "ABRIR EM SÓ", font=f_head, fill=NAVY_TEXT)
    y += 76

    f_head_big = font(F_BOLD, 78)
    draw.text((MARGIN_L, y), "8 DIAS ÚTEIS", font=f_head_big, fill=GOLD_ON_LIGHT)
    y += 100

    f_sub = font(F_REG, 28)
    sub_lines = wrap_text(
        draw,
        "Prazo mínimo entre a publicação do edital e a abertura das propostas, para compra de bens com menor preço (Lei 14.133/2021, art. 55).",
        f_sub,
        content_w,
    )
    for line in sub_lines:
        draw.text((MARGIN_L, y), line, font=f_sub, fill=SUBTLE)
        y += 38

    y += 34
    draw.line([(MARGIN_L, y), (W - MARGIN_R, y)], fill=LINE_ON_LIGHT, width=2)
    y += 38

    f_kicker = font(F_BOLD, 24)
    draw.text((MARGIN_L, y), "OUTROS PRAZOS MÍNIMOS DO ART. 55", font=f_kicker, fill=GOLD_ON_LIGHT)
    y += 46

    rows = [
        ("Bens — outros critérios de julgamento", "15 dias úteis"),
        ("Serviços e obras comuns — menor preço", "10 dias úteis"),
        ("Serviços e obras especiais — menor preço", "25 dias úteis"),
    ]
    f_row_label = font(F_REG, 25)
    f_row_val = font(F_BOLD, 25)
    for label, val in rows:
        draw.text((MARGIN_L, y), label, font=f_row_label, fill=NAVY_TEXT)
        vw = draw.textlength(val, font=f_row_val)
        draw.text((W - MARGIN_R - vw, y), val, font=f_row_val, fill=GOLD_ON_LIGHT)
        y += 40

    y += 28
    f_body = font(F_REG, 26)
    body_lines = wrap_text(
        draw,
        "São prazos mínimos, não médios: a abertura pode ocorrer em menos de duas semanas corridas. Quem não acompanha o PNCP todos os dias chega tarde.",
        f_body,
        content_w,
    )
    for line in body_lines:
        draw.text((MARGIN_L, y), line, font=f_body, fill=SUBTLE)
        y += 36

    y += 40
    f_btn = font(F_BOLD, 30)
    btn_text = "Fala com a Domina no direct →"
    rounded_button(draw, (MARGIN_L, y), btn_text, f_btn, GOLD_ON_LIGHT, NAVY_TEXT, pad_x=34, pad_y=20)

    return img


if __name__ == "__main__":
    out_dir = "/tmp/claude-0/-home-user-domina-posts/708d43d9-8468-5cd3-8b9e-c3551e78e844/scratchpad"
    build().save(f"{out_dir}/post-18h-1008.png")
    print("done")
