from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1080

# Paleta branco gelo (oposta ao ultimo post, que foi navy)
BG = (247, 246, 240)
NAVY = (10, 20, 45)
NAVY_SOFT = (21, 39, 76)
GOLD = (196, 155, 58)
SUBTITLE = (90, 100, 120)
LINE = (210, 205, 190)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
def font(size, bold=True):
    path = FONT_DIR + ("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf")
    return ImageFont.truetype(path, size)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

MARGIN = 80

def text_w(s, f):
    bbox = d.textbbox((0, 0), s, font=f)
    return bbox[2] - bbox[0]

def wrap(text, f, max_w):
    words = text.split(" ")
    lines, cur = [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if text_w(trial, f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines

# ---- Logo (top-right) ----
logo = Image.open("/tmp/claude-0/-home-user-domina-posts/0d7437a2-de51-5a3c-94a3-87c43a74be28/scratchpad/assets/logo_domina.png").convert("RGBA")
logo_size = 100
logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
logo_x = W - MARGIN - logo_size
logo_y = 72
img.paste(logo, (logo_x, logo_y), logo)

# ---- Tag pill (top-left) ----
tag_text = "LEI 14.133/2021 · ART. 81"
f_tag = font(24, bold=True)
tw = text_w(tag_text, f_tag)
pad_x, pad_y = 26, 14
pill_x0, pill_y0 = MARGIN, 80
pill_x1, pill_y1 = pill_x0 + tw + pad_x * 2, pill_y0 + 24 + pad_y * 2
d.rounded_rectangle([pill_x0, pill_y0, pill_x1, pill_y1], radius=(pill_y1 - pill_y0) // 2, outline=GOLD, width=2)
d.text((pill_x0 + pad_x, pill_y0 + pad_y - 2), tag_text, font=f_tag, fill=GOLD)

# ---- Title ----
f_title = font(58, bold=True)
title_lines = [
    ("AJUDE A DESENHAR", NAVY),
    ("O EDITAL", GOLD),
    ("ANTES DELE EXISTIR.", NAVY),
]
title_y = 212
line_gap = 64
for i, (line, color) in enumerate(title_lines):
    d.text((MARGIN, title_y + i * line_gap), line, font=f_title, fill=color)

sub_y = title_y + len(title_lines) * line_gap + 22

# ---- Subtitle ----
f_sub = font(28, bold=False)
subtitle = "O Procedimento de Manifestação de Interesse (PMI) permite que sua empresa apresente estudos técnicos ao poder público — antes da licitação ser lançada."
sub_lines = wrap(subtitle, f_sub, W - 2 * MARGIN)
y = sub_y
for line in sub_lines:
    d.text((MARGIN, y), line, font=f_sub, fill=SUBTITLE)
    y += 38

# ---- Divider ----
y += 14
d.line([(MARGIN, y), (W - MARGIN, y)], fill=LINE, width=2)
y += 36

# ---- Sections ----
f_label = font(23, bold=True)
f_body = font(26, bold=False)

def section(label, body, y):
    d.text((MARGIN, y), label, font=f_label, fill=GOLD)
    y += 34
    lines = wrap(body, f_body, W - 2 * MARGIN)
    for line in lines:
        d.text((MARGIN, y), line, font=f_body, fill=NAVY_SOFT)
        y += 34
    return y + 22

y = section("O QUE É", "Por chamamento público, o governo convida empresas e especialistas a apresentar estudos e projetos para estruturar uma futura contratação.", y)
y = section("NA PRÁTICA", "Quem participa ajuda a moldar as especificações do edital e ganha visibilidade técnica antes da disputa abrir.", y)

# ---- CTA button ----
cta_text = "Fale com a Domina no direct  →"
f_cta = font(30, bold=True)
tw = text_w(cta_text, f_cta)
btn_pad_x, btn_pad_y = 40, 22
btn_y0 = max(y + 10, H - 150)
btn_x0 = MARGIN
btn_x1 = btn_x0 + tw + btn_pad_x * 2
btn_y1 = btn_y0 + 24 + btn_pad_y * 2
d.rounded_rectangle([btn_x0, btn_y0, btn_x1, btn_y1], radius=(btn_y1 - btn_y0) // 2, fill=GOLD)
d.text((btn_x0 + btn_pad_x, btn_y0 + btn_pad_y - 2), cta_text, font=f_cta, fill=NAVY)

# ---- Decorative corner bracket (bottom-right) ----
bx0, by0 = W - MARGIN, H - 60
d.line([(bx0 - 60, by0), (bx0, by0)], fill=GOLD, width=3)
d.line([(bx0, by0 - 60), (bx0, by0)], fill=GOLD, width=3)

img.save("/tmp/claude-0/-home-user-domina-posts/0d7437a2-de51-5a3c-94a3-87c43a74be28/scratchpad/post_feed.png")
print("saved", img.size)
