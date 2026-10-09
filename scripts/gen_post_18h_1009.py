import sys
from PIL import Image, ImageDraw, ImageFont

W = H = 1080
BG = (247, 246, 240)          # branco gelo
NAVY = (14, 23, 48)           # titulo
SUBTITLE = (91, 107, 134)     # cinza-azulado
GOLD = (212, 175, 55)
GOLD_DARK_TEXT = (24, 20, 4)
LINE = (214, 209, 194)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
def F(size):
    return ImageFont.truetype(FONT_DIR + "DejaVuSans-Bold.ttf", size)
def FR(size):
    return ImageFont.truetype(FONT_DIR + "DejaVuSans.ttf", size)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

def text_w(draw, s, font):
    bbox = draw.textbbox((0, 0), s, font=font)
    return bbox[2] - bbox[0]

def rounded_pill(draw, xy, radius, fill=None, outline=None, width=2):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)

# --- decorative corner bracket bottom-left ---
bx, by, bl = 56, H - 56, 46
d.line([(bx, by), (bx, by - bl)], fill=GOLD, width=3)
d.line([(bx, by), (bx + bl, by)], fill=GOLD, width=3)

# --- logo top-right ---
logo = Image.open("/tmp/claude-0/-home-user-domina-posts/372e0576-3c9a-5dd7-a76b-ca2d34273e3a/scratchpad/assets/logo_domina.png").convert("RGBA")
logo_size = 105
logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
logo_x = W - 70 - logo_size
logo_y = 64
img.paste(logo, (logo_x, logo_y), logo)

# --- badge top-left ---
badge_font = F(24)
badge_text = "LEI 14.133/2021 · ART. 64"
tw = text_w(d, badge_text, badge_font)
pad_x, pad_y = 26, 14
bx0, by0 = 64, 90
bx1, by1 = bx0 + tw + pad_x * 2, by0 + 24 + pad_y * 2
rounded_pill(d, (bx0, by0, bx1, by1), radius=(by1 - by0) // 2, outline=GOLD, width=2)
d.text((bx0 + pad_x, by0 + pad_y), badge_text, font=badge_font, fill=GOLD)

# --- title ---
title_font = F(70)
lines = [
    ("DESCLASSIFICADA POR", NAVY),
    ("UM ERRO QUE A LEI", NAVY),
    ("MANDA CORRIGIR.", GOLD),
]
ty = 230
line_gap = 82
for line, color in lines:
    d.text((64, ty), line, font=title_font, fill=color)
    ty += line_gap

# --- subtitle ---
sub_font = FR(30)
sub_lines = [
    "Pelo art. 64 da Lei 14.133/2021, falhas que não",
    "mudam a substância da proposta devem ser sanadas",
    "por diligência — não geram desclassificação automática.",
]
sy = ty + 28
for line in sub_lines:
    d.text((64, sy), line, font=sub_font, fill=SUBTITLE)
    sy += 42

# --- divider ---
dy = sy + 26
d.line([(64, dy), (W - 64, dy)], fill=LINE, width=2)

# --- erro comum block ---
label_font = F(26)
body_font = FR(29)
ly = dy + 38
d.text((64, ly), "ERRO COMUM", font=label_font, fill=GOLD)
ly += 42
erro_lines = [
    "Perder a disputa por um vício formal sanável —",
    "sem a comissão abrir diligência para corrigir,",
    "como manda o art. 64.",
]
for line in erro_lines:
    d.text((64, ly), line, font=body_font, fill=NAVY)
    ly += 40

# --- CTA pill ---
cta_font = F(30)
cta_text = "Fale com a Domina no direct  →"
tw2 = text_w(d, cta_text, cta_font)
pad_x2, pad_y2 = 40, 22
cx0, cy1 = 64, H - 90
cy0 = cy1 - (24 + pad_y2 * 2) - 10
cx1 = cx0 + tw2 + pad_x2 * 2
cy0 = H - 90 - (24 + pad_y2 * 2)
cy1 = H - 90
rounded_pill(d, (cx0, cy0, cx1, cy1), radius=(cy1 - cy0) // 2, fill=GOLD)
d.text((cx0 + pad_x2, cy0 + pad_y2 - 2), cta_text, font=cta_font, fill=GOLD_DARK_TEXT)

out_path = "/tmp/claude-0/-home-user-domina-posts/372e0576-3c9a-5dd7-a76b-ca2d34273e3a/scratchpad/post.png"
img.save(out_path)
print("saved", out_path, img.size)
