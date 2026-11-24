"""Render the 24 November 2026 world-news front page, 1024x1024 PNG.

Dense edition: 29 dated stories across 7 regions (2 hero stories plus
27 dated wire items), the format the 22 November winner used.
Deterministic: no randomness, no timestamps, no network. Running this
script twice writes identical bytes (PIL writes no time chunk).
Headlines verified live on 24 Nov 2026 from Reuters, BBC, CNN, Wall
Street Journal, CBC World Report, and the day's news roundups.
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
BROWN = (120, 70, 20)

F = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(F + name, size)


SERIF = "DejaVuSerif-Bold.ttf"
SANS = "DejaVuSans.ttf"
SANS_B = "DejaVuSans-Bold.ttf"

REGION_COLORS = {
    "MIDDLE EAST": RED,
    "EUROPE": INK,
    "ASIA": TEAL,
    "AMERICAS": NAVY,
    "AFRICA": BROWN,
    "MARKETS": GREEN,
    "SPORT": RED,
}

# 27 dated wire items, 3 columns of 9: (region, headline).
WIRE = [
    ("MIDDLE EAST", "Trump warns Iran of a 'very traumatic' outcome"),
    ("MIDDLE EAST", "Israeli drone strike kills three at Gaza post"),
    ("MIDDLE EAST", "Settler arson condemned as 'Jewish terrorism'"),
    ("MIDDLE EAST", "US sanctions target Iran's underground banks"),
    ("EUROPE", "Dymer toll reaches 11 after strike on flats"),
    ("EUROPE", "EU proposes 22nd sanctions package on Russia"),
    ("EUROPE", "Drone hits Russian freighter Sparta II"),
    ("EUROPE", "COP31 ends with no deal on fossil fuels"),
    ("AFRICA", "Ukraine sinks Russian warship off Libya"),
    ("ASIA", "Factory fire in Banten kills 24, 30 missing"),
    ("ASIA", "Army hunts scores missing after Himalayan flood"),
    ("ASIA", "Ex-lawmaker Revanna jailed for life for rape"),
    ("ASIA", "Bangladesh vaccinates 50m children vs typhoid"),
    ("ASIA", "Trump announces Japan trade deal, Nikkei rallies"),
    ("ASIA", "Seoul scrambles jets after Russian air breach"),
    ("ASIA", "Thai-Cambodia fighting on hold after truce"),
    ("AFRICA", "Migrant boat capsizes off Senegal, dozens lost"),
    ("AFRICA", "Europe prepares evacuations after Niger coup"),
    ("AMERICAS", "ICE arrests at Seattle airport condemned"),
    ("AMERICAS", "FAA lifts O'Hare ground stop after snag"),
    ("AMERICAS", "Mexico to try 'El Chapo Isidro' itself"),
    ("AMERICAS", "Storm displaces thousands in Brazil town"),
    ("AMERICAS", "US lists Venezuela cartel as terrorists"),
    ("AMERICAS", "Senate to vote on $9.4bn foreign aid cuts"),
    ("AMERICAS", "Trump halts army lead-azide blasts in Iowa"),
    ("MARKETS", "SoftBank to invest $2bn in Intel"),
    ("SPORT", "Verstappen wins the Las Vegas GP"),
]


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
    assert len(WIRE) == 27, "wire must hold 27 items"
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    # masthead
    d.rectangle([0, 0, W, 118], fill=NAVY)
    d.text((32, 18), "THE WORLD TODAY", font=font(SERIF, 58), fill=WHITE)
    d.text((32, 84), "TUESDAY 24 NOVEMBER 2026  •  29 DATED STORIES  •  7 REGIONS",
           font=font(SANS_B, 20), fill=GOLD)
    d.rectangle([0, 118, W, 124], fill=RED)

    # hero: Hormuz
    d.rectangle([24, 142, 660, 440], fill=NAVY)
    d.rectangle([24, 142, 660, 440], outline=GOLD, width=3)
    d.text((48, 150), "IRAN VOWS", font=font(SERIF, 46), fill=WHITE)
    d.text((48, 196), "ALL MEANS", font=font(SERIF, 46), fill=WHITE)
    y, n = text_block(d, 48, 250,
                      "Tehran vows to break the US blockade by all available means.",
                      font(SANS_B, 22), GOLD, 590, 28)
    print("hero sub lines:", n, "ends y:", y)
    y, n = text_block(d, 48, y + 4,
                      "Iran says it can reopen the strait very quickly if Washington meets its conditions.",
                      font(SANS, 19), (220, 225, 235), 590, 24)
    print("hero body lines:", n, "ends y:", y)
    assert y <= 386, "hero body overflows into banner"
    d.text((48, 392), "IRGC CLAIMS 3 TANKERS HIT MINES",
           font=font(SANS_B, 18), fill=(245, 200, 60))
    for i in range(12):
        wx = 48 + i * 50
        d.arc([wx, 424, wx + 48, 438], 0, 180, fill=(120, 180, 220), width=3)

    # hero right: Nvidia
    d.rectangle([684, 142, 1000, 440], fill=(255, 255, 255))
    d.rectangle([684, 142, 1000, 440], outline=INK, width=3)
    d.rectangle([684, 142, 1000, 196], fill=TEAL)
    d.text((706, 152), "MARKETS", font=font(SANS_B, 22), fill=WHITE)
    d.text((706, 206), "HUANG", font=font(SERIF, 46), fill=INK)
    d.text((706, 252), "IS BACK", font=font(SERIF, 36), fill=RED)
    y, n = text_block(d, 706, 300,
                      "Shares soar 31% as Huang returns 11 days after resigning, adding $952bn in a day.",
                      font(SANS, 19), INK, 272, 24)
    print("nvidia body lines:", n, "ends y:", y)
    assert y <= 402, "nvidia body overflows into footer"
    d.text((706, 412), "Best day since 2003", font=font(SANS_B, 17), fill=GREY)

    # wire: 3 columns x 9 dated items
    col_x = [24, 356, 688]
    col_w = 312
    slot = 60
    y0 = 456
    for i, (region, head) in enumerate(WIRE):
        col = i // 9
        row = i % 9
        x = col_x[col]
        y = y0 + row * slot
        d.text((x, y), "24 NOV", font=font(SANS_B, 13), fill=RED)
        d.text((x + 62, y), region, font=font(SANS_B, 13),
               fill=REGION_COLORS[region])
        _, n = text_block(d, x, y + 18, head, font(SANS_B, 16), INK,
                          col_w, 20)
        print("wire", i + 1, region, "lines:", n)
        assert n <= 2, "wire headline overflows its slot: " + head
        assert y + 58 <= y0 + 9 * slot, "wire item overflows the grid"

    # footer: source line in the strip the grid leaves free
    d.text((24, 1000), "ALL STORIES DATED 24 NOVEMBER 2026  •  SOURCES: REUTERS, BBC, CNN, WSJ, CBC",
           font=font(SANS_B, 13), fill=GREY)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
