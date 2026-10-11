from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920

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

MARGIN = 90
SAFE_TOP = 250
SAFE_BOTTOM = 250

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

content_w = W - 2 * MARGIN

# ---- Logo (centered, in top safe area) ----
logo = Image.open("/tmp/claude-0/-home-user-domina-posts/0d7437a2-de51-5a3c-94a3-87c43a74be28/scratchpad/assets/logo_domina.png").convert("RGBA")
logo_size = 110
logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
logo_x = (W - logo_size) // 2
logo_y = SAFE_TOP - logo_size - 30
img.paste(logo, (logo_x, logo_y), logo)

y = SAFE_TOP

# ---- Tag pill (centered) ----
tag_text = "LEI 14.133/2021 · ART. 81"
f_tag = font(28, bold=True)
tw = text_w(tag_text, f_tag)
pad_x, pad_y = 30, 16
pill_w = tw + pad_x * 2
pill_h = 28 + pad_y * 2
pill_x0 = (W - pill_w) // 2
d.rounded_rectangle([pill_x0, y, pill_x0 + pill_w, y + pill_h], radius=pill_h // 2, outline=GOLD, width=2)
d.text((pill_x0 + pad_x, y + pad_y - 2), tag_text, font=f_tag, fill=GOLD)
y += pill_h + 70

# ---- Title (centered) ----
f_title = font(72, bold=True)
title_lines = [
    ("AJUDE A DESENHAR", NAVY),
    ("O EDITAL", GOLD),
    ("ANTES DELE", NAVY),
    ("EXISTIR.", NAVY),
]
for line, color in title_lines:
    tw = text_w(line, f_title)
    d.text(((W - tw) // 2, y), line, font=f_title, fill=color)
    y += 82

y += 36

# ---- Subtitle (centered) ----
f_sub = font(34, bold=False)
subtitle = "O Procedimento de Manifestação de Interesse (PMI) permite que sua empresa apresente estudos técnicos ao poder público — antes da licitação ser lançada."
sub_lines = wrap(subtitle, f_sub, content_w - 60)
for line in sub_lines:
    tw = text_w(line, f_sub)
    d.text(((W - tw) // 2, y), line, font=f_sub, fill=SUBTITLE)
    y += 48

y += 30
d.line([(MARGIN + 60, y), (W - MARGIN - 60, y)], fill=LINE, width=2)
y += 60

# ---- Sections (centered) ----
f_label = font(28, bold=True)
f_body = font(32, bold=False)

def section(label, body, y):
    tw = text_w(label, f_label)
    d.text(((W - tw) // 2, y), label, font=f_label, fill=GOLD)
    y += 46
    lines = wrap(body, f_body, content_w - 60)
    for line in lines:
        tw = text_w(line, f_body)
        d.text(((W - tw) // 2, y), line, font=f_body, fill=NAVY_SOFT)
        y += 44
    return y + 44

y = section("O QUE É", "Por chamamento público, o governo convida empresas e especialistas a apresentar estudos e projetos para estruturar uma futura contratação.", y)
y = section("NA PRÁTICA", "Quem participa ajuda a moldar as especificações do edital e ganha visibilidade técnica antes da disputa abrir.", y)

# ---- CTA button (centered, above bottom safe zone) ----
cta_text = "Fale com a Domina no direct  →"
f_cta = font(34, bold=True)
tw = text_w(cta_text, f_cta)
btn_pad_x, btn_pad_y = 44, 26
btn_w = tw + btn_pad_x * 2
btn_h = 30 + btn_pad_y * 2
btn_y0 = min(max(y + 20, H - SAFE_BOTTOM - btn_h - 40), H - SAFE_BOTTOM - btn_h)
btn_x0 = (W - btn_w) // 2
d.rounded_rectangle([btn_x0, btn_y0, btn_x0 + btn_w, btn_y0 + btn_h], radius=btn_h // 2, fill=GOLD)
d.text((btn_x0 + btn_pad_x, btn_y0 + btn_pad_y - 2), cta_text, font=f_cta, fill=NAVY)

img.save("/tmp/claude-0/-home-user-domina-posts/0d7437a2-de51-5a3c-94a3-87c43a74be28/scratchpad/post_story.png")
print("saved", img.size, "cta bottom:", btn_y0 + btn_h, "safe bottom line:", H - SAFE_BOTTOM)
