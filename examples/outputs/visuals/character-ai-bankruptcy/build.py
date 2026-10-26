"""Build the Character.AI filing excerpts image (1080 x 1350 PNG).

Crops three passages from the public court PDFs, unchanged, and highlights
the sentences the post quotes. Run with PyMuPDF and Pillow installed:

  python build.py <doc18.pdf> <doc15.pdf> <out.png>

doc18: CEO's first-day declaration, Doc 18, case 26-11603 (D. Del.)
  https://cases.stretto.com/public/x936/14939/PLEADINGS/1493910132680000000119.pdf
doc15: bidding procedures motion, Doc 15
  https://storage.courtlistener.com/recap/gov.uscourts.deb.203004/gov.uscourts.deb.203004.15.0.pdf
"""
import sys

import fitz
from PIL import Image, ImageChops, ImageDraw, ImageFont

W, H = 1080, 1350
BG = (239, 237, 232)
INK = (28, 28, 28)
HIGHLIGHT = (255, 226, 77)
LABEL = (100, 100, 100)
MARGIN, PAD, PADY, GAP = 30, 22, 26, 36
X0, X1 = 70, 546  # text column on the court's letter pages, in points
HEADER = (8, 29)  # the "Case 26-11603-BLS Doc .. Page .." line
FONT = '/System/Library/Fonts/Helvetica.ttc'

# Diana's title (2026-10-22); the highlighted part matches the first excerpt
TITLE = [('Character.AI files for bankruptcy', None), ('with ', '$57 million'), (' left, why?', None)]
SUBTITLE = 'from its court filings, October 2026'

# (pdf, page index, (top, bottom) of the lines, phrases to highlight)
EXCERPTS = [
    (0, 7, (566, 641), ['Character has no funded debt and approximately $57 million in unrestricted cash']),
    (0, 8, (124, 199), ['in exchange for approximately $2.7 billion in total consideration',
                        'Google rehired the founders', 'of Character']),
    (1, 6, (207, 282), ['Disney required that the transaction be fully consummated in a chapter 11 sale',
                        'process.']),
]


def render(page, clip, scale, marks):
    pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale), clip=clip, alpha=False)
    img = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
    layer = Image.new('RGB', img.size, (255, 255, 255))
    draw = ImageDraw.Draw(layer)
    for r in marks:
        box = [(r.x0 - clip.x0) * scale - 3, (r.y0 - clip.y0) * scale - 1,
               (r.x1 - clip.x0) * scale + 3, (r.y1 - clip.y0) * scale + 2]
        draw.rectangle(box, fill=HIGHLIGHT)
    # multiply keeps the black text on top of the yellow
    return ImageChops.multiply(img, layer)


def draw_title(draw, y):
    bold = ImageFont.truetype(FONT, 64, index=1)
    line_h = 78
    x = MARGIN + 4
    draw.text((x, y), TITLE[0][0], font=bold, fill=INK)
    y += line_h
    for plain, marked in TITLE[1:]:
        if plain:
            draw.text((x, y), plain, font=bold, fill=INK)
            x += draw.textlength(plain, font=bold)
        if marked:
            w = draw.textlength(marked, font=bold)
            draw.rectangle([x - 4, y + 2, x + w + 4, y + 70], fill=HIGHLIGHT)
            draw.text((x, y), marked, font=bold, fill=INK)
            x += w
    y += line_h + 6
    draw.text((MARGIN + 4, y), SUBTITLE, font=ImageFont.truetype(FONT, 30), fill=LABEL)
    return y + 30 + 34


def main(doc18_path, doc15_path, out_path):
    docs = [fitz.open(doc18_path), fitz.open(doc15_path)]
    scale = (W - 2 * MARGIN - 2 * PAD) / (X1 - X0)
    canvas = Image.new('RGB', (W, H), BG)
    draw = ImageDraw.Draw(canvas)

    cards = []
    for d, pno, (top, bottom), phrases in EXCERPTS:
        page = docs[d][pno]
        marks = []
        for phrase in phrases:
            hits = [r for r in page.search_for(phrase) if top <= r.y0 <= bottom]
            if not hits:
                raise SystemExit(f'not found on page {pno + 1}: {phrase}')
            marks += hits
        header = render(page, fitz.Rect(X0, HEADER[0], X1, HEADER[1]), scale, [])
        body = render(page, fitz.Rect(X0, top, X1, bottom), scale, marks)
        cards.append((header, body))

    title_h = 78 * 2 + 6 + 30 + 34
    total = title_h + sum(h.height + 14 + b.height + 2 * PADY for h, b in cards) + GAP * (len(cards) - 1)
    y = draw_title(draw, (H - total) // 2)
    for header, body in cards:
        card_h = header.height + 14 + body.height + 2 * PADY
        draw.rectangle([MARGIN, y, W - MARGIN, y + card_h], fill=(255, 255, 255), outline=(214, 211, 204), width=2)
        canvas.paste(header, (MARGIN + PAD, y + PADY))
        canvas.paste(body, (MARGIN + PAD, y + PADY + header.height + 14))
        y += card_h + GAP
    canvas.save(out_path, optimize=True)
    print(out_path, canvas.size, f'scale {scale:.2f} px/pt')


if __name__ == '__main__':
    main(*sys.argv[1:4])
