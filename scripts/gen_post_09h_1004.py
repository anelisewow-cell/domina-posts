#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Post 09h 2026-10-04: novos valores de dispensa de licitacao em 2026
(Decreto no 12.807/2025, que reajusta os valores de referencia da Lei 14.133/2021).
Carrossel de 4 slides, paleta alternando a cada slide (azul/branco/azul/branco),
iniciando em azul marinho (oposto ao ultimo post publicado, que foi branco gelo).
Layout variado: capa com headline alinhada a direita (nao usada nos posts recentes),
slide 2 em lista numerada a esquerda, slide 3 em estatistica gigante centralizada,
slide 4 CTA centralizado em branco gelo.
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


def draw_right(draw, y, text, fnt, fill, right_x):
    tw = draw.textlength(text, font=fnt)
    draw.text((right_x - tw, y), text, font=fnt, fill=fill)
    return tw


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


# ---------------- SLIDE 1: CAPA (azul marinho, headline alinhada a direita) ----------------
def slide_capa():
    img = vertical_gradient(W, H, NAVY_DARK, NAVY_LIGHT)
    draw = ImageDraw.Draw(img)

    MARGIN_R = 80
    right_x = W - MARGIN_R

    paste_logo(img, size=90, pos=(70, 60))

    draw.line([(W - 6, 0), (W - 6, H)], fill=GOLD, width=6)

    f_kicker = font(F_BOLD, 28)
    y = 210
    draw_right(draw, y, "ATUALIZAÇÃO · DECRETO Nº 12.807/2025", f_kicker, GOLD, right_x)
    y += 54
    draw.line([(right_x - 460, y), (right_x, y)], fill=GOLD, width=3)
    y += 46

    f_head = font(F_BOLD, 70)
    head_lines = [
        ("DISPENSA DE", (255, 255, 255)),
        ("LICITAÇÃO TEM", (255, 255, 255)),
        ("NOVOS VALORES", GOLD),
    ]
    for text, color in head_lines:
        draw_right(draw, y, text, f_head, color, right_x)
        y += 82

    y += 20
    f_sub = font(F_REG, 32)
    sub_lines = wrap_text(
        draw,
        "Os limites para contratação direta subiram em 2026. Veja o que muda pra sua empresa.",
        f_sub,
        640,
    )
    for line in sub_lines:
        draw_right(draw, y, line, f_sub, GRAY_ON_NAVY, right_x)
        y += 42

    f_arrow = font(F_BOLD, 30)
    arrow_text = "ARRASTE PARA VER →"
    draw_right(draw, H - 95, arrow_text, f_arrow, GOLD, right_x)

    return img


# ---------------- SLIDE 2: O QUE MUDOU (branco gelo, lista a esquerda) ----------------
def slide_2():
    img = Image.new("RGB", (W, H), OFFWHITE)
    draw = ImageDraw.Draw(img)

    MARGIN_L = 90
    MARGIN_R = 90
    content_w = W - MARGIN_L - MARGIN_R

    f_prog = font(F_BOLD, 26)
    draw.text((MARGIN_L, 64), "2 DE 4", font=f_prog, fill=GOLD_ON_LIGHT)
    paste_logo(img, size=64, pos=(W - MARGIN_R - 64, 50))

    y = 150
    f_kicker = font(F_BOLD, 28)
    draw.text((MARGIN_L, y), "O QUE MUDOU", font=f_kicker, fill=GOLD_ON_LIGHT)
    y += 52

    f_head = font(F_BOLD, 50)
    head_lines = ["Reajuste de 4,41%", "pela inflação (IPCA-E)"]
    for line in head_lines:
        draw.text((MARGIN_L, y), line, font=f_head, fill=NAVY_TEXT)
        y += 60

    y += 20
    draw.line([(MARGIN_L, y), (W - MARGIN_R, y)], fill=LINE_ON_LIGHT, width=2)
    y += 44

    f_body = font(F_REG, 30)
    paragraphs = [
        "O Decreto nº 12.807/2025 atualizou os valores de referência da Lei 14.133/2021 e está em vigor desde 1º de janeiro de 2026, substituindo o Decreto nº 12.343/2024.",
        "A regra não mudou — só os limites em reais ficaram maiores, abrindo mais espaço pra contratação direta, sem disputa de edital.",
    ]
    for para in paragraphs:
        lines = wrap_text(draw, para, f_body, content_w)
        for line in lines:
            draw.text((MARGIN_L, y), line, font=f_body, fill=SUBTLE)
            y += 40
        y += 26

    return img


# ---------------- SLIDE 3: OS NOVOS VALORES (azul marinho, estatistica gigante) ----------------
def slide_3():
    img = vertical_gradient(W, H, NAVY_LIGHT, NAVY_DARK)
    draw = ImageDraw.Draw(img)
    cx = W / 2

    f_prog = font(F_BOLD, 26)
    draw.text((80, 64), "3 DE 4", font=f_prog, fill=GOLD)

    f_kicker = font(F_BOLD, 26)
    y = 150
    draw_center(draw, y, "OS NOVOS VALORES DA DISPENSA (ART. 75)", f_kicker, GOLD, cx)
    y += 70

    draw.line([(cx - 420, y), (cx + 420, y)], fill=LINE_ON_NAVY, width=2)
    y += 60

    f_label = font(F_BOLD, 28)
    f_stat = font(F_BOLD, 76)

    draw_center(draw, y, "COMPRAS E SERVIÇOS", f_label, GRAY_ON_NAVY, cx)
    y += 46
    draw_center(draw, y, "R$ 65.492,11", f_stat, (255, 255, 255), cx)
    y += 120

    draw.line([(cx - 260, y), (cx + 260, y)], fill=LINE_ON_NAVY, width=1)
    y += 50

    draw_center(draw, y, "OBRAS E SERVIÇOS DE ENGENHARIA", f_label, GRAY_ON_NAVY, cx)
    y += 46
    draw_center(draw, y, "R$ 130.984,20", f_stat, GOLD, cx)
    y += 120

    f_foot = font(F_REG, 26)
    draw_center(draw, y, "Valores em vigor desde 1º/01/2026", f_foot, GRAY_ON_NAVY, cx)

    paste_logo(img, size=76, pos=(W - 76 - 60, H - 76 - 55))

    return img


# ---------------- SLIDE 4: CTA (branco gelo, centralizado) ----------------
def slide_4():
    img = Image.new("RGB", (W, H), OFFWHITE)
    draw = ImageDraw.Draw(img)
    cx = W / 2

    f_prog = font(F_BOLD, 26)
    draw.text((90, 64), "4 DE 4", font=f_prog, fill=GOLD_ON_LIGHT)

    logo_size = 110
    paste_logo(img, size=logo_size, pos=(int(cx - logo_size / 2), 150))

    y = 150 + logo_size + 54
    f_head = font(F_BOLD, 50)
    head_lines = ["SUA EMPRESA JÁ", "CONTRATA DENTRO", "DESSES LIMITES?"]
    for line in head_lines:
        draw_center(draw, y, line, f_head, NAVY_TEXT, cx)
        y += 60

    y += 24
    f_sub = font(F_REG, 30)
    sub_lines = wrap_text(
        draw,
        "A Domina Licitações mapeia as oportunidades de contratação direta com órgãos públicos e cuida de toda a documentação.",
        f_sub,
        780,
    )
    for line in sub_lines:
        draw_center(draw, y, line, f_sub, SUBTLE, cx)
        y += 40

    y += 36
    f_btn = font(F_BOLD, 32)
    btn_text = "Fala com a Domina no direct →"
    tw = draw.textlength(btn_text, font=f_btn)
    pad_x = 38
    btn_w = tw + pad_x * 2
    rounded_button(draw, (cx - btn_w / 2, y), btn_text, f_btn, GOLD_ON_LIGHT, (255, 255, 255), pad_x=pad_x, pad_y=22)

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

    y = safe_top + logo_size + 60
    f_kicker = font(F_BOLD, 32)
    draw_center(draw, y, "ATUALIZAÇÃO · DECRETO Nº 12.807/2025", f_kicker, GOLD, cx)
    y += 56
    draw.line([(cx - 320, y), (cx + 320, y)], fill=GOLD, width=3)
    y += 56

    f_head = font(F_BOLD, 72)
    head_lines = [
        ("DISPENSA DE", (255, 255, 255)),
        ("LICITAÇÃO TEM", (255, 255, 255)),
        ("NOVOS VALORES", GOLD),
    ]
    for text, color in head_lines:
        draw_center(draw, y, text, f_head, color, cx)
        y += 86

    y += 24
    f_sub = font(F_REG, 36)
    sub_lines = wrap_text(
        draw,
        "Os limites para contratação direta subiram em 2026. Arrasta pra ver no feed.",
        f_sub,
        780,
    )
    for line in sub_lines:
        draw_center(draw, y, line, f_sub, GRAY_ON_NAVY, cx)
        y += 48

    f_arrow = font(F_BOLD, 36)
    draw_center(draw, safe_bottom - 90, "ARRASTE PRA CIMA →", f_arrow, GOLD, cx)

    return img


if __name__ == "__main__":
    out_dir = "/tmp/claude-0/-home-user-domina-posts/69150f0d-75b9-571c-bc84-2805dffc4345/scratchpad"

    slide_capa().save(f"{out_dir}/carousel-1.png")
    slide_2().save(f"{out_dir}/carousel-2.png")
    slide_3().save(f"{out_dir}/carousel-3.png")
    slide_4().save(f"{out_dir}/carousel-4.png")
    story_cover().save(f"{out_dir}/story-cover.png")

    print("done")
