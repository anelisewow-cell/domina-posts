#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Post 09h 2026-10-08: sancoes da Lei 14.133/2021 (impedimento de licitar x
declaracao de inidoneidade, arts. 155 e 156).
Carrossel de 4 slides, paleta alternando a cada slide (azul/branco/azul/branco),
iniciando em azul marinho (oposto ao ultimo post publicado em 2026-10-07 18h,
que foi branco gelo).
Layout variado (nao repete capa direita / lista esquerda / stat gigante /
CTA centralizado do carrossel anterior): capa com headline centralizada e pill
dupla, slide 2 com lista numerada em circulos dourados, slide 3 em comparacao
split-screen (coluna esquerda x direita), slide 4 CTA alinhado a esquerda.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1080

NAVY_DARK = (8, 16, 40)
NAVY_LIGHT = (26, 46, 92)
OFFWHITE = (247, 246, 240)
NAVY_TEXT = (16, 28, 58)
SUBTLE = (94, 104, 128)
GRAY_ON_NAVY = (200, 210, 225)
GOLD = (212, 175, 55)
GOLD_ON_LIGHT = (196, 154, 61)
LINE_ON_NAVY = (60, 78, 118)
LINE_ON_LIGHT = (214, 208, 190)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
F_BOLD = FONT_DIR + "DejaVuSans-Bold.ttf"
F_REG = FONT_DIR + "DejaVuSans.ttf"
LOGO_PATH = "/home/user/domina-posts/logo_domina.png"


def font(path, size):
    return ImageFont.truetype(path, size)


def vertical_gradient(w, h, top, bottom):
    img = Image.new("RGB", (w, h), top)
    draw = ImageDraw.Draw(img)
    for y in range(h):
        t = y / (h - 1)
        r = int(top[0] + (bottom[0] - top[0]) * t)
        g = int(top[1] + (bottom[1] - top[1]) * t)
        b = int(top[2] + (bottom[2] - top[2]) * t)
        draw.line([(0, y), (w, y)], fill=(r, g, b))
    return img


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


def draw_center(draw, y, text, fnt, fill, cx):
    tw = draw.textlength(text, font=fnt)
    draw.text((cx - tw / 2, y), text, font=fnt, fill=fill)
    return tw


def paste_logo(img, size, pos):
    logo = Image.open(LOGO_PATH).convert("RGBA")
    logo = logo.resize((size, size), Image.LANCZOS)
    img.paste(logo, pos, logo)


def rounded_button(draw, xy, text, fnt, fill_btn, fill_text, pad_x=36, pad_y=20):
    x, y = xy
    tw = draw.textlength(text, font=fnt)
    th = fnt.size
    w = tw + pad_x * 2
    h = th + pad_y * 2
    draw.rounded_rectangle([x, y, x + w, y + h], radius=h // 2, fill=fill_btn)
    draw.text((x + pad_x, y + pad_y), text, font=fnt, fill=fill_text)
    return x, y, x + w, y + h


def pill(draw, cx, y, text, fnt, outline):
    tw = draw.textlength(text, font=fnt)
    pad_x, pad_y = 26, 12
    h = fnt.size + pad_y * 2
    x0 = cx - tw / 2 - pad_x
    x1 = cx + tw / 2 + pad_x
    draw.rounded_rectangle([x0, y, x1, y + h], radius=h / 2, outline=outline, width=2)
    draw.text((cx - tw / 2, y + pad_y - 2), text, font=fnt, fill=outline)
    return h


# ---------------- SLIDE 1: CAPA (azul marinho, centralizada) ----------------
def slide_capa():
    img = vertical_gradient(W, H, NAVY_DARK, NAVY_LIGHT)
    draw = ImageDraw.Draw(img)
    cx = W / 2

    logo_size = 100
    paste_logo(img, size=logo_size, pos=(int(cx - logo_size / 2), 86))

    y = 86 + logo_size + 44
    f_pill = font(F_BOLD, 24)
    ph = pill(draw, cx, y, "LEI 14.133/2021 · ARTS. 155 E 156", f_pill, GOLD)
    y += ph + 44

    f_head = font(F_BOLD, 60)
    head_lines = [
        ("SUA EMPRESA PODE", (255, 255, 255)),
        ("FICAR DE FORA DE", (255, 255, 255)),
        ("TODAS AS LICITAÇÕES", GOLD),
        ("DO PAÍS", GOLD),
    ]
    for text, color in head_lines:
        draw_center(draw, y, text, f_head, color, cx)
        y += 68

    y += 24
    f_sub = font(F_REG, 29)
    sub_lines = wrap_text(
        draw,
        "Entenda as sanções da Lei 14.133/2021 antes que uma delas tire sua empresa da disputa.",
        f_sub,
        740,
    )
    for line in sub_lines:
        draw_center(draw, y, line, f_sub, GRAY_ON_NAVY, cx)
        y += 40

    f_arrow = font(F_BOLD, 28)
    draw_center(draw, H - 90, "ARRASTE PARA VER →", f_arrow, GOLD, cx)

    return img


# ---------------- SLIDE 2: AS 4 SANCOES (branco gelo, lista numerada) ----------------
def slide_2():
    img = Image.new("RGB", (W, H), OFFWHITE)
    draw = ImageDraw.Draw(img)

    MARGIN_L = 96
    MARGIN_R = 96
    content_w = W - MARGIN_L - MARGIN_R

    f_prog = font(F_BOLD, 26)
    draw.text((MARGIN_L, 64), "2 DE 4", font=f_prog, fill=GOLD_ON_LIGHT)
    paste_logo(img, size=64, pos=(W - MARGIN_R - 64, 50))

    y = 150
    f_kicker = font(F_BOLD, 28)
    draw.text((MARGIN_L, y), "AS 4 SANÇÕES PREVISTAS", font=f_kicker, fill=GOLD_ON_LIGHT)
    y += 54

    f_head = font(F_BOLD, 46)
    draw.text((MARGIN_L, y), "O que a lei pode aplicar", font=f_head, fill=NAVY_TEXT)
    y += 56
    draw.text((MARGIN_L, y), "à sua empresa", font=f_head, fill=NAVY_TEXT)
    y += 66

    draw.line([(MARGIN_L, y), (W - MARGIN_R, y)], fill=LINE_ON_LIGHT, width=2)
    y += 40

    items = [
        ("1", "Advertência", "Alerta formal — reservada a falhas na execução do contrato."),
        ("2", "Multa", "Percentual sobre o valor do contrato ou do item, previsto no edital."),
        ("3", "Impedimento de licitar e contratar", "Suspensão temporária, no ente que aplicou a sanção."),
        ("4", "Declaração de inidoneidade", "A mais grave — suspensão em todo o país."),
    ]

    circ_d = 46
    text_x = MARGIN_L + circ_d + 24
    f_num = font(F_BOLD, 24)
    f_item_head = font(F_BOLD, 28)
    f_item_body = font(F_REG, 23)

    for num, title, body in items:
        draw.ellipse([MARGIN_L, y, MARGIN_L + circ_d, y + circ_d], outline=GOLD_ON_LIGHT, width=3)
        ntw = draw.textlength(num, font=f_num)
        draw.text((MARGIN_L + circ_d / 2 - ntw / 2, y + circ_d / 2 - 14), num, font=f_num, fill=GOLD_ON_LIGHT)

        draw.text((text_x, y - 2), title, font=f_item_head, fill=NAVY_TEXT)
        ty = y + 38
        for line in wrap_text(draw, body, f_item_body, content_w - circ_d - 24):
            draw.text((text_x, ty), line, font=f_item_body, fill=SUBTLE)
            ty += 30

        y = max(y + circ_d, ty) + 26

    return img


# ---------------- SLIDE 3: IMPEDIMENTO x INIDONEIDADE (azul, split screen) ----------------
def slide_3():
    img = vertical_gradient(W, H, NAVY_LIGHT, NAVY_DARK)
    draw = ImageDraw.Draw(img)
    cx = W / 2

    f_prog = font(F_BOLD, 26)
    draw.text((80, 64), "3 DE 4", font=f_prog, fill=GOLD)

    f_kicker = font(F_BOLD, 26)
    y0 = 150
    draw_center(draw, y0, "AS 2 SANÇÕES MAIS GRAVES", f_kicker, GOLD, cx)
    y0 += 54
    draw.line([(cx - 360, y0), (cx + 360, y0)], fill=LINE_ON_NAVY, width=2)

    col_top = y0 + 50
    col_w = 400
    left_cx = cx - 240
    right_cx = cx + 240

    draw.line([(cx, col_top), (cx, H - 130)], fill=LINE_ON_NAVY, width=2)

    f_col_head = font(F_BOLD, 34)
    f_label = font(F_REG, 22)
    f_stat = font(F_BOLD, 40)
    f_body = font(F_REG, 22)

    # LEFT: IMPEDIMENTO
    y = col_top
    draw_center(draw, y, "IMPEDIMENTO", f_col_head, (255, 255, 255), left_cx)
    y += 44
    draw_center(draw, y, "DE LICITAR", f_col_head, (255, 255, 255), left_cx)
    y += 62

    draw_center(draw, y, "PRAZO MÁXIMO", f_label, GRAY_ON_NAVY, left_cx)
    y += 32
    draw_center(draw, y, "3 ANOS", f_stat, GOLD, left_cx)
    y += 66

    draw_center(draw, y, "ALCANCE", f_label, GRAY_ON_NAVY, left_cx)
    y += 32
    for line in wrap_text(draw, "Só no ente que aplicou a sanção", f_body, col_w - 40):
        draw_center(draw, y, line, f_body, (255, 255, 255), left_cx)
        y += 30

    # RIGHT: INIDONEIDADE
    y = col_top
    draw_center(draw, y, "DECLARAÇÃO DE", f_col_head, (255, 255, 255), right_cx)
    y += 44
    draw_center(draw, y, "INIDONEIDADE", f_col_head, (255, 255, 255), right_cx)
    y += 62

    draw_center(draw, y, "PRAZO", f_label, GRAY_ON_NAVY, right_cx)
    y += 32
    draw_center(draw, y, "3 A 6 ANOS", f_stat, GOLD, right_cx)
    y += 66

    draw_center(draw, y, "ALCANCE", f_label, GRAY_ON_NAVY, right_cx)
    y += 32
    for line in wrap_text(draw, "Em todo o Brasil, qualquer órgão", f_body, col_w - 40):
        draw_center(draw, y, line, f_body, (255, 255, 255), right_cx)
        y += 30

    f_foot = font(F_REG, 22)
    draw_center(draw, H - 90, "Reservada a fraude, documento falso e conduta dolosa", f_foot, GRAY_ON_NAVY, cx)

    return img


# ---------------- SLIDE 4: CTA (branco gelo, alinhado a esquerda) ----------------
def slide_4():
    img = Image.new("RGB", (W, H), OFFWHITE)
    draw = ImageDraw.Draw(img)

    MARGIN_L = 96
    MARGIN_R = 96
    content_w = W - MARGIN_L - MARGIN_R

    f_prog = font(F_BOLD, 26)
    draw.text((MARGIN_L, 64), "4 DE 4", font=f_prog, fill=GOLD_ON_LIGHT)

    logo_size = 84
    paste_logo(img, size=logo_size, pos=(W - MARGIN_R - logo_size, 50))

    y = 220
    f_head = font(F_BOLD, 50)
    head_lines = ["NÃO ESPERE SER", "PENALIZADA PARA", "SE PROTEGER"]
    for line in head_lines:
        draw.text((MARGIN_L, y), line, font=f_head, fill=NAVY_TEXT)
        y += 60

    y += 24
    draw.line([(MARGIN_L, y), (W - MARGIN_R, y)], fill=LINE_ON_LIGHT, width=2)
    y += 40

    f_sub = font(F_REG, 29)
    sub_lines = wrap_text(
        draw,
        "A Domina Licitações acompanha a conformidade da sua empresa em cada etapa da licitação e do contrato — e prepara a defesa se uma sanção for aplicada indevidamente.",
        f_sub,
        content_w,
    )
    for line in sub_lines:
        draw.text((MARGIN_L, y), line, font=f_sub, fill=SUBTLE)
        y += 40

    y += 40
    f_btn = font(F_BOLD, 30)
    btn_text = "Fala com a Domina no direct →"
    rounded_button(draw, (MARGIN_L, y), btn_text, f_btn, GOLD_ON_LIGHT, (255, 255, 255), pad_x=34, pad_y=20)

    return img


# ---------------- STORY (vertical, capa) ----------------
def story_cover():
    SW, SH = 1080, 1920
    img = vertical_gradient(SW, SH, NAVY_DARK, NAVY_LIGHT)
    draw = ImageDraw.Draw(img)
    cx = SW / 2

    safe_top = 250
    safe_bottom = SH - 250

    logo_size = 130
    paste_logo(img, size=logo_size, pos=(int(cx - logo_size / 2), safe_top))

    y = safe_top + logo_size + 50
    f_pill = font(F_BOLD, 28)
    ph = pill(draw, cx, y, "LEI 14.133/2021 · ARTS. 155 E 156", f_pill, GOLD)
    y += ph + 50

    f_head = font(F_BOLD, 68)
    head_lines = [
        ("SUA EMPRESA PODE", (255, 255, 255)),
        ("FICAR DE FORA DE", (255, 255, 255)),
        ("TODAS AS LICITAÇÕES", GOLD),
        ("DO PAÍS", GOLD),
    ]
    for text, color in head_lines:
        draw_center(draw, y, text, f_head, color, cx)
        y += 80

    y += 24
    f_sub = font(F_REG, 34)
    sub_lines = wrap_text(
        draw,
        "Entenda as sanções da Lei 14.133/2021 antes que uma delas tire sua empresa da disputa. Arrasta pra ver no feed.",
        f_sub,
        760,
    )
    for line in sub_lines:
        draw_center(draw, y, line, f_sub, GRAY_ON_NAVY, cx)
        y += 46

    f_arrow = font(F_BOLD, 34)
    draw_center(draw, safe_bottom - 80, "ARRASTE PRA CIMA →", f_arrow, GOLD, cx)

    return img


if __name__ == "__main__":
    out_dir = "/tmp/claude-0/-home-user-domina-posts/30b1ef38-8432-5685-820a-ef90b4f1db33/scratchpad"

    slide_capa().save(f"{out_dir}/carousel-1.png")
    slide_2().save(f"{out_dir}/carousel-2.png")
    slide_3().save(f"{out_dir}/carousel-3.png")
    slide_4().save(f"{out_dir}/carousel-4.png")
    story_cover().save(f"{out_dir}/story-cover.png")

    print("done")
