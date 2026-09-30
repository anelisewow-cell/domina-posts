#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont

NAVY_DARK = (10, 20, 48)
NAVY_MID = (16, 33, 74)
NAVY_LIGHT = (30, 55, 110)
GOLD = (212, 175, 55)
WHITE = (255, 255, 255)
GRAY = (200, 210, 225)

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

W, H = 1080, 1080
LOGO_PATH = "/home/user/domina-posts/logo_domina.png"


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


def wrap_text(draw, text, font, max_width):
    words = text.split(" ")
    lines = []
    cur = ""
    for w in words:
        test = (cur + " " + w).strip()
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= max_width or not cur:
            cur = test
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_multiline(draw, xy, lines, font, fill, line_gap=14, anchor_center=False, img_width=W):
    x, y = xy
    for line in lines:
        if anchor_center:
            bbox = draw.textbbox((0, 0), line, font=font)
            lw = bbox[2] - bbox[0]
            draw.text(((img_width - lw) / 2, y), line, font=font, fill=fill)
        else:
            draw.text((x, y), line, font=font, fill=fill)
        bbox = draw.textbbox((0, 0), line, font=font)
        y += (bbox[3] - bbox[1]) + line_gap
    return y


def paste_logo(img, size=105, pos=None):
    logo = Image.open(LOGO_PATH).convert("RGBA")
    logo = logo.resize((size, size), Image.LANCZOS)
    if pos is None:
        pos = (W - size - 70, 60)
    img.paste(logo, pos, logo)


def rounded_button(draw, xy, text, font, pad_x=36, pad_y=20):
    x, y = xy
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    w = tw + pad_x * 2
    h = th + pad_y * 2
    draw.rounded_rectangle([x, y, x + w, y + h], radius=h // 2, fill=GOLD)
    draw.text((x + pad_x, y + pad_y - bbox[1]), text, font=font, fill=(30, 20, 5))
    return x, y, x + w, y + h


def deco_circles(img, cx, cy, color=GOLD):
    draw = ImageDraw.Draw(img)
    for r in (110, 155, 195):
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=3)


def deco_corner_lines(img, corner="tl", color=GOLD):
    draw = ImageDraw.Draw(img)
    if corner == "tl":
        draw.line([(0, 90), (90, 0)], fill=color, width=6)
        draw.line([(0, 40), (40, 0)], fill=color, width=6)
    elif corner == "br":
        draw.line([(W, H - 90), (W - 90, H)], fill=color, width=6)
        draw.line([(W, H - 40), (W - 40, H)], fill=color, width=6)


# ---------------- SLIDE 1: CAPA ----------------
def slide_capa():
    img = vertical_gradient(W, H, (8, 16, 40), (26, 46, 92))
    draw = ImageDraw.Draw(img)
    paste_logo(img, size=100, pos=(70, 65))

    tag_font = ImageFont.truetype(FONT_BOLD, 32)
    draw.text((70, 205), "TRATAMENTO DIFERENCIADO ME/EPP", font=tag_font, fill=GOLD)
    draw.line([(70, 255), (560, 255)], fill=GOLD, width=4)

    title_font = ImageFont.truetype(FONT_BOLD, 68)
    lines = ["3 REGRAS DA LEI", "QUE TODA ME/EPP", "PRECISA CONHECER"]
    y = 300
    for line in lines:
        draw.text((70, y), line, font=title_font, fill=WHITE)
        bbox = draw.textbbox((0, 0), line, font=title_font)
        y += (bbox[3] - bbox[1]) + 22

    sub_font = ImageFont.truetype(FONT_REG, 34)
    sub_lines = wrap_text(draw, "Para vender ao poder público com o benefício que a lei garante à sua empresa.", sub_font, 900)
    y += 20
    for line in sub_lines:
        draw.text((70, y), line, font=sub_font, fill=GRAY)
        bbox = draw.textbbox((0, 0), line, font=sub_font)
        y += (bbox[3] - bbox[1]) + 12

    deco_circles(img, W - 40, H - 40, GOLD)

    arrow_font = ImageFont.truetype(FONT_BOLD, 32)
    arrow_text = "ARRASTE PARA VER →"
    bbox = draw.textbbox((0, 0), arrow_text, font=arrow_font)
    tw = bbox[2] - bbox[0]
    draw.text((W - tw - 70, H - 100), arrow_text, font=arrow_font, fill=GOLD)
    return img


# ---------------- SLIDES 2-4: REGRAS ----------------
def slide_regra(num_label, kicker, title_lines, body_lines, bg_top, bg_bottom):
    img = vertical_gradient(W, H, bg_top, bg_bottom)
    draw = ImageDraw.Draw(img)

    num_font = ImageFont.truetype(FONT_BOLD, 200)
    draw.text((60, 40), num_label, font=num_font, fill=(255, 255, 255, 40))
    # overlay softer by drawing translucent-like effect: draw outline only
    draw.text((60, 40), num_label, font=num_font, fill=(38, 60, 105))

    kicker_font = ImageFont.truetype(FONT_BOLD, 30)
    draw.text((70, 270), kicker, font=kicker_font, fill=GOLD)

    title_font = ImageFont.truetype(FONT_BOLD, 58)
    y = 320
    for line in title_lines:
        draw.text((70, y), line, font=title_font, fill=WHITE)
        bbox = draw.textbbox((0, 0), line, font=title_font)
        y += (bbox[3] - bbox[1]) + 16

    draw.line([(70, y + 10), (1010, y + 10)], fill=(90, 110, 150), width=2)
    y += 50

    body_font = ImageFont.truetype(FONT_REG, 36)
    for para in body_lines:
        wrapped = wrap_text(draw, para, body_font, 920)
        for line in wrapped:
            draw.text((70, y), line, font=body_font, fill=(230, 235, 245))
            bbox = draw.textbbox((0, 0), line, font=body_font)
            y += (bbox[3] - bbox[1]) + 14
        y += 22

    paste_logo(img, size=80, pos=(W - 80 - 60, H - 80 - 55))
    progress_font = ImageFont.truetype(FONT_BOLD, 28)
    prog_text = f"{num_label} DE 3"
    draw.text((70, H - 95), prog_text, font=progress_font, fill=GOLD)
    return img


# ---------------- SLIDE 5: CTA ----------------
def slide_cta():
    img = vertical_gradient(W, H, (30, 55, 110), (8, 16, 40))
    draw = ImageDraw.Draw(img)
    deco_corner_lines(img, "tl", GOLD)
    deco_corner_lines(img, "br", GOLD)

    paste_logo(img, size=120, pos=((W - 120) // 2, 120))

    title_font = ImageFont.truetype(FONT_BOLD, 56)
    lines = ["SUA EMPRESA SE", "ENQUADRA NESSAS", "REGRAS?"]
    y = 300
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=title_font)
        lw = bbox[2] - bbox[0]
        draw.text(((W - lw) / 2, y), line, font=title_font, fill=WHITE)
        y += (bbox[3] - bbox[1]) + 18

    sub_font = ImageFont.truetype(FONT_REG, 32)
    sub_lines = wrap_text(draw, "A Domina Licitações identifica o enquadramento certo e cuida da estratégia e da documentação do início ao fim.", sub_font, 820)
    y += 30
    for line in sub_lines:
        bbox = draw.textbbox((0, 0), line, font=sub_font)
        lw = bbox[2] - bbox[0]
        draw.text(((W - lw) / 2, y), line, font=sub_font, fill=GRAY)
        y += (bbox[3] - bbox[1]) + 12

    btn_font = ImageFont.truetype(FONT_BOLD, 34)
    btn_text = "Fala com a Domina agora →"
    bbox = draw.textbbox((0, 0), btn_text, font=btn_font)
    tw = bbox[2] - bbox[0]
    pad_x = 40
    btn_w = tw + pad_x * 2
    rounded_button(draw, ((W - btn_w) / 2, y + 40), btn_text, btn_font, pad_x=pad_x, pad_y=24)
    return img


if __name__ == "__main__":
    out_dir = "/tmp/claude-0/-home-user-domina-posts/904583ad-8d82-5892-838f-ada9c0f13b49/scratchpad"

    slide_capa().save(f"{out_dir}/carousel-1.png")

    slide_regra(
        "1",
        "REGRA 1 · ART. 48, I DA LC 123/2006",
        ["LICITAÇÃO EXCLUSIVA", "ATÉ R$ 80 MIL"],
        [
            "Quando o valor do item ou lote é de até R$ 80.000, o órgão público é obrigado a licitar exclusivamente entre ME e EPP.",
            "Grandes empresas ficam de fora dessa disputa — o espaço é só das pequenas.",
        ],
        (10, 24, 55), (24, 44, 90),
    ).save(f"{out_dir}/carousel-2.png")

    slide_regra(
        "2",
        "REGRA 2 · ART. 48, III DA LC 123/2006",
        ["COTA DE ATÉ 25%", "RESERVADA PRA VOCÊ"],
        [
            "Acima de R$ 80 mil, se o objeto for divisível, o edital pode reservar até 25% da quantidade para disputa exclusiva entre ME e EPP.",
            "Ou seja: mesmo em contratos maiores, pode sobrar uma fatia só para pequenos fornecedores.",
        ],
        (12, 20, 48), (30, 52, 100),
    ).save(f"{out_dir}/carousel-3.png")

    slide_regra(
        "3",
        "REGRA 3 · ART. 4º DA LEI 14.133/2021",
        ["O BENEFÍCIO TEM", "UM TETO: R$ 4,8 MI"],
        [
            "As regras de tratamento favorecido só valem se o valor total orçado da contratação não ultrapassar R$ 4,8 milhões.",
            "Acima disso, a licitação segue as regras gerais — sem exclusividade nem cota para ME/EPP.",
        ],
        (8, 18, 44), (22, 38, 82),
    ).save(f"{out_dir}/carousel-4.png")

    slide_cta().save(f"{out_dir}/carousel-5.png")

    print("done")

def story_cover():
    SW, SH = 1080, 1920
    img = vertical_gradient(SW, SH, (8, 16, 40), (26, 46, 92))
    draw = ImageDraw.Draw(img)

    safe_top = 250
    safe_bottom = SH - 250

    logo_size = 130
    paste_logo(img, size=logo_size, pos=((SW - logo_size)//2, safe_top))

    tag_font = ImageFont.truetype(FONT_BOLD, 34)
    tag_text = "TRATAMENTO DIFERENCIADO ME/EPP"
    bbox = draw.textbbox((0,0), tag_text, font=tag_font)
    tw = bbox[2]-bbox[0]
    y = safe_top + logo_size + 60
    draw.text(((SW-tw)/2, y), tag_text, font=tag_font, fill=GOLD)
    y += (bbox[3]-bbox[1]) + 30
    draw.line([((SW-500)/2, y), ((SW+500)/2, y)], fill=GOLD, width=4)
    y += 50

    title_font = ImageFont.truetype(FONT_BOLD, 74)
    lines = ["3 REGRAS DA LEI", "QUE TODA ME/EPP", "PRECISA CONHECER"]
    for line in lines:
        bbox = draw.textbbox((0,0), line, font=title_font)
        lw = bbox[2]-bbox[0]
        draw.text(((SW-lw)/2, y), line, font=title_font, fill=WHITE)
        y += (bbox[3]-bbox[1]) + 26

    sub_font = ImageFont.truetype(FONT_REG, 38)
    sub_lines = wrap_text(draw, "Para vender ao poder público com o benefício que a lei garante à sua empresa.", sub_font, 820)
    y += 30
    for line in sub_lines:
        bbox = draw.textbbox((0,0), line, font=sub_font)
        lw = bbox[2]-bbox[0]
        draw.text(((SW-lw)/2, y), line, font=sub_font, fill=GRAY)
        y += (bbox[3]-bbox[1]) + 16

    deco_circles(img, SW - 60, safe_bottom - 60, GOLD)

    arrow_font = ImageFont.truetype(FONT_BOLD, 36)
    arrow_text = "ARRASTE PRA CIMA →"
    bbox = draw.textbbox((0,0), arrow_text, font=arrow_font)
    tw = bbox[2]-bbox[0]
    draw.text(((SW-tw)/2, safe_bottom - 120), arrow_text, font=arrow_font, fill=GOLD)

    return img

story_cover().save("/tmp/claude-0/-home-user-domina-posts/904583ad-8d82-5892-838f-ada9c0f13b49/scratchpad/story-cover.png")
print("story done")
