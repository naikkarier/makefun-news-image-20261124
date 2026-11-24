"""Render the 24 November 2026 world-news front page, 1024x1024 PNG.

Deterministic: no randomness, no timestamps, no network. Running this
script twice writes identical bytes (PIL writes no time chunk).
Headlines verified live on 24 Nov 2026 from Reuters, BBC/France 24 via
One Turn, BusinessWorld/Reuters, CNN and the Wall Street Journal.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BG = (247, 243, 232)
INK = (20, 24, 38)
NAVY = (16, 32, 64)
RED = (178, 34, 34)
GOLD = (201, 162, 39)
TEAL = (14, 110, 110)
GREY = (90, 92, 102)
WHITE = (255, 255, 255)
GREEN = (16, 120, 60)

F = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(F + name, size)


SERIF = "DejaVuSerif-Bold.ttf"
SANS = "DejaVuSans.ttf"
SANS_B = "DejaVuSans-Bold.ttf"


def wrap(draw, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, color, width, leading=None):
    lines = wrap(draw, text, fnt, width)
    lh = leading or int(fnt.size * 1.25)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=color)
        y += lh
    return y, len(lines)


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    # masthead
    d.rectangle([0, 0, W, 118], fill=NAVY)
    d.text((32, 18), "THE WORLD TODAY", font=font(SERIF, 58), fill=WHITE)
    d.text((32, 84), "TUESDAY 24 NOVEMBER 2026  •  WORLD NEWS IN ONE IMAGE",
           font=font(SANS_B, 20), fill=GOLD)
    d.rectangle([0, 118, W, 124], fill=RED)

    # hero: Hormuz
    d.rectangle([24, 142, 660, 470], fill=NAVY)
    d.rectangle([24, 142, 660, 470], outline=GOLD, width=3)
    d.text((48, 150), "IRAN VOWS", font=font(SERIF, 48), fill=WHITE)
    d.text((48, 202), "ALL MEANS", font=font(SERIF, 48), fill=WHITE)
    y, n = text_block(d, 48, 258,
                      "Tehran vows to break the US blockade by all available means.",
                      font(SANS_B, 24), GOLD, 590, 30)
    print("hero sub lines:", n, "ends y:", y)
    y, n = text_block(d, 48, y + 6,
                      "Iran says it can reopen the strait very quickly if Washington meets its conditions.",
                      font(SANS, 21), (220, 225, 235), 590, 26)
    print("hero body lines:", n, "ends y:", y)
    assert y <= 410, "hero body overflows into banner"
    d.text((48, 420), "IRGC CLAIMS 3 TANKERS HIT MINES",
           font=font(SANS_B, 20), fill=(245, 200, 60))
    for i in range(12):
        wx = 48 + i * 50
        d.arc([wx, 452, wx + 48, 468], 0, 180, fill=(120, 180, 220), width=3)

    # right panel: Nvidia
    d.rectangle([684, 142, 1000, 470], fill=(255, 255, 255))
    d.rectangle([684, 142, 1000, 470], outline=INK, width=3)
    d.rectangle([684, 142, 1000, 196], fill=TEAL)
    d.text((706, 152), "MARKETS", font=font(SANS_B, 22), fill=WHITE)
    d.text((706, 206), "HUANG", font=font(SERIF, 48), fill=INK)
    d.text((706, 258), "IS BACK", font=font(SERIF, 38), fill=RED)
    y, n = text_block(d, 706, 316,
                      "Shares soar 31% as Huang returns 11 days after resigning, adding $952bn in a day.",
                      font(SANS, 20), INK, 272, 26)
    print("nvidia body lines:", n, "ends y:", y)
    assert y <= 432, "nvidia body overflows into footer"
    d.text((706, 440), "Best day since 2003", font=font(SANS_B, 18), fill=GREY)

    # middle grid: 4 stories, 2x2
    stories = [
        ("LIBYA", RED, "Ukraine sinks Russian warship",
         "Seven sea drones sank the corvette Merkury at Benghazi, Kyiv says. 10 injured."),
        ("UKRAINE", INK, "Dymer toll reaches 11",
         "Russian strike on flats near Kyiv kills at least 11. A boy, 7, and a woman, 79, pulled alive."),
        ("INDONESIA", NAVY, "Factory fire kills 24",
         "Candy factory blaze in Banten leaves about 30 missing. DNA tests to identify the dead."),
        ("FINLAND", TEAL, "Drone hits Russian freighter",
         "Sparta II is towed to St Petersburg after a drone strike in the Gulf of Finland."),
    ]
    x0, y0, cw, ch, gap = 24, 494, 476, 200, 24
    for i, (tag, col, head, body) in enumerate(stories):
        x = x0 + (i % 2) * (cw + gap)
        y = y0 + (i // 2) * (ch + gap)
        d.rectangle([x, y, x + cw, y + ch], fill=WHITE)
        d.rectangle([x, y, x + cw, y + ch], outline=INK, width=2)
        d.rectangle([x, y, x + cw, y + 40], fill=col)
        d.text((x + 16, y + 8), tag, font=font(SANS_B, 20), fill=WHITE)
        y2, n1 = text_block(d, x + 16, y + 52, head, font(SANS_B, 24), INK, cw - 32, 30)
        y3, n2 = text_block(d, x + 16, y + 116, body, font(SANS, 19), GREY, cw - 32, 25)
        print("panel", tag, "headline lines:", n1, "body lines:", n2, "body ends y:", y3)
        assert n1 <= 2 and y3 <= y + ch - 8, "panel overflows: " + tag

    # bottom strip: sport + Gaza + COP31
    strip = "SPORT  Verstappen wins Las Vegas GP  •  GAZA  3 killed, incl. UNRWA worker  •  COP31  No deal"
    sw = d.textlength(strip, font=font(SANS_B, 17))
    print("strip width:", sw, "limit:", 1000 - 40)
    assert sw <= 1000 - 40, "bottom strip overflows"
    d.rectangle([24, 942, 1000, 1000], fill=INK)
    d.text((40, 962), strip, font=font(SANS_B, 17), fill=WHITE)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
