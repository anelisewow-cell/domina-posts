#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Post 18h 2026-09-23: Carrossel SICAF - cadastro de fornecedores (compras.gov.br)."""
from PIL import Image, ImageDraw, ImageFont

W = H = 1080

NAVY_TOP = (12, 18, 42)
NAVY_BOTTOM = (30, 42, 88)
GOLD = (212, 175, 55)
WHITE = (255, 255, 255)
LIGHT_GRAY = (198, 206, 224)
DARK_TEXT = (20, 24, 40)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
F_BOLD = FONT_DIR + "DejaVuSans-Bold.ttf"
F_REG = FONT_DIR + "DejaVuSans.ttf"

LOGO = Image.open("/tmp/logo_domina.png").convert("RGBA")


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


def center_text(draw, cy, text, fnt, fill, cx=W // 2):
    tw = draw.textlength(text, font=fnt)
    draw.text((cx - tw / 2, cy), text, font=fnt, fill=fill)


def new_canvas():
    img = Image.new("RGB", (W, H), NAVY_TOP)
    draw = ImageDraw.Draw(img)
    vertical_gradient(draw, W, H, NAVY_TOP, NAVY_BOTTOM)
    return img, draw


def paste_logo(img, cx, cy, size=105):
    logo_resized = LOGO.resize((size, size), Image.LANCZOS)
    img.paste(logo_resized, (int(cx - size / 2), int(cy - size / 2)), logo_resized)


def corner_deco(draw, corner="tl"):
    # thin gold triangle-corner accent, varies per slide
    L = 130
    if corner == "tl":
        draw.line([(0, L), (L, 0)], fill=GOLD, width=6)
    elif corner == "br":
        draw.line([(W - L, H), (W, H - L)], fill=GOLD, width=6)
    elif corner == "tr":
        draw.line([(W - L, 0), (W, L)], fill=GOLD, width=6)
    elif corner == "bl":
        draw.line([(0, H - L), (L, H)], fill=GOLD, width=6)


# ---------------------------------------------------------------- SLIDE 1 (capa)
def slide_capa():
    img, draw = new_canvas()
    corner_deco(draw, "tl")
    corner_deco(draw, "br")
    paste_logo(img, W // 2, 150)

    f_kicker = font(F_BOLD, 30)
    center_text(draw, 235, "GUIA RÁPIDO", f_kicker, GOLD)

    f_head = font(F_BOLD, 66)
    lines = ["O CADASTRO QUE", "ABRE AS PORTAS DAS", "LICITAÇÕES PRA VOCÊ"]
    y = 300
    for line in lines:
        center_text(draw, y, line, f_head, WHITE)
        y += 76

    f_sicaf = font(F_BOLD, 130)
    center_text(draw, y + 30, "SICAF", f_sicaf, GOLD)
    y += 30 + 150

    f_sub = font(F_REG, 30)
    sub = "o que é, quem precisa e como funcionar sem dor de cabeça"
    sub_lines = wrap_text(draw, sub, f_sub, W - 200)
    for line in sub_lines:
        center_text(draw, y, line, f_sub, LIGHT_GRAY)
        y += 40

    f_swipe = font(F_BOLD, 28)
    center_text(draw, H - 100, "ARRASTE PARA VER →", f_swipe, GOLD)
    img.save("/tmp/carousel_1.png")


# ---------------------------------------------------------------- numbered slide
def slide_step(n_total, n, kicker, title_lines, big_stat, stat_cap, body_lines, corner):
    img, draw = new_canvas()
    corner_deco(draw, corner)

    MARGIN_L = 100
    MARGIN_R = 100
    content_w = W - MARGIN_L - MARGIN_R

    # top: step badge left, logo right
    y = 90
    f_badge = font(F_BOLD, 30)
    badge_text = f"{n} DE {n_total}"
    draw.text((MARGIN_L, y), badge_text, font=f_badge, fill=GOLD)
    paste_logo(img, W - MARGIN_R - 45, y + 45, size=90)

    y += 70
    f_kicker = font(F_BOLD, 26)
    draw.text((MARGIN_L, y), kicker, font=f_kicker, fill=LIGHT_GRAY)
    y += 46

    f_head = font(F_BOLD, 50)
    for line in title_lines:
        draw.text((MARGIN_L, y), line, font=f_head, fill=WHITE)
        y += 58
    y += 26

    if big_stat:
        f_stat = font(F_BOLD, 110)
        draw.text((MARGIN_L, y), big_stat, font=f_stat, fill=GOLD)
        stat_w = draw.textlength(big_stat, font=f_stat)
        f_stat_cap = font(F_BOLD, 28)
        cap_lines = wrap_text(draw, stat_cap, f_stat_cap, content_w - stat_w - 30)
        cy = y + 20
        for line in cap_lines:
            draw.text((MARGIN_L + stat_w + 24, cy), line, font=f_stat_cap, fill=WHITE)
            cy += 36
        y += 130

    y += 20
    draw.line([(MARGIN_L, y), (W - MARGIN_R, y)], fill=(90, 100, 130), width=2)
    y += 40

    f_body = font(F_REG, 31)
    for b in body_lines:
        lines = wrap_text(draw, b, f_body, content_w)
        for line in lines:
            draw.text((MARGIN_L, y), line, font=f_body, fill=WHITE)
            y += 42
        y += 20

    img.save(f"/tmp/carousel_{n + 1}.png")


# ---------------------------------------------------------------- CTA final
def slide_cta():
    img, draw = new_canvas()
    corner_deco(draw, "tr")
    corner_deco(draw, "bl")

    paste_logo(img, W // 2, 300, size=150)

    f_head = font(F_BOLD, 56)
    lines = ["DEIXA A BUROCRACIA", "DO SICAF COM QUEM", "ENTENDE DO ASSUNTO"]
    y = 470
    for line in lines:
        center_text(draw, y, line, f_head, WHITE)
        y += 64
    y += 30

    f_sub = font(F_REG, 30)
    sub_lines = wrap_text(
        draw,
        "A Domina Licitações cuida do seu cadastro, das certidões e da renovação anual — enquanto você foca no seu negócio.",
        f_sub,
        W - 220,
    )
    for line in sub_lines:
        center_text(draw, y, line, f_sub, LIGHT_GRAY)
        y += 40
    y += 40

    f_cta = font(F_BOLD, 32)
    cta_text = "Fala com a Domina agora →"
    tw = draw.textlength(cta_text, font=f_cta)
    btn_pad_x, btn_pad_y = 40, 22
    btn_w = tw + btn_pad_x * 2
    btn_h = f_cta.size + btn_pad_y * 2
    bx0 = W / 2 - btn_w / 2
    draw.rounded_rectangle([bx0, y, bx0 + btn_w, y + btn_h], radius=btn_h // 2, fill=GOLD)
    draw.text((bx0 + btn_pad_x, y + btn_pad_y - 4), cta_text, font=f_cta, fill=DARK_TEXT)

    img.save("/tmp/carousel_6.png")


slide_capa()

slide_step(
    4, 1,
    "PASSO 1",
    ["O QUE É O SICAF"],
    None, "",
    [
        "É o cadastro único de fornecedores do governo federal — uma espécie de \"RG\" da sua empresa perante a administração pública.",
        "Uma vez cadastrada e regular no SICAF, sua empresa não precisa reapresentar os mesmos documentos em cada licitação de que participar.",
    ],
    "tl",
)

slide_step(
    4, 2,
    "PASSO 2",
    ["CADASTRO GRATUITO", "E 100% DIGITAL"],
    None, "",
    [
        "O cadastramento é feito pelo portal Compras.gov.br, sem custo em nenhuma etapa e sem necessidade de ir a um órgão público.",
        "É necessário certificado digital e-CPF (representante) ou e-CNPJ (empresa), padrão ICP-Brasil, para acessar o sistema.",
    ],
    "tr",
)

slide_step(
    4, 3,
    "PASSO 3",
    ["OS NÍVEIS DE", "CADASTRAMENTO"],
    None, "",
    [
        "O SICAF é organizado em níveis: dados societários, regularidade fiscal federal, estadual/municipal, qualificação técnica e qualificação econômico-financeira.",
        "Quanto mais níveis sua empresa mantiver em dia, para mais licitações ela fica habilitada a disputar.",
    ],
    "br",
)

slide_step(
    4, 4,
    "PASSO 4",
    ["FIQUE DE OLHO NA", "VALIDADE"],
    "1", "ANO DE VALIDADE — renovação obrigatória para manter o cadastro ativo",
    [
        "Certidões vencidas ou cadastro desatualizado são motivo comum de inabilitação — mesmo para empresas com a melhor proposta de preço.",
        "Manter o SICAF sempre regular evita perder disputa por um detalhe burocrático.",
    ],
    "bl",
)

slide_cta()
print("done")
