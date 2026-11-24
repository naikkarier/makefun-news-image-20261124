"""Draw the 24 November 2026 world-news front page as a 1024x1024 PNG.

Dense edition: two hero stories plus 27 dated wire items, 29 stories
in all across 7 regions, the shape the 22 November winner used.
Everything is drawn with PIL, so the output is fully deterministic:
no clock, no random numbers, no network, and PIL writes no time
chunk, so two runs produce byte-identical files.
The headlines were checked live on 24 Nov 2026 against Reuters,
BBC, CNN, the Wall Street Journal and CBC World Report.
"""
import os
from PIL import Image, ImageDraw, ImageFont

CANVAS = 1024
PALETTE = {
    "paper": (247, 243, 232),
    "ink": (20, 24, 38),
    "navy": (16, 32, 64),
    "red": (178, 34, 34),
    "gold": (201, 162, 39),
    "teal": (14, 110, 110),
    "grey": (90, 92, 102),
    "white": (255, 255, 255),
    "green": (16, 120, 60),
    "brown": (120, 70, 20),
    "pale": (220, 225, 235),
    "amber": (245, 200, 60),
    "wave": (120, 180, 220),
}
FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
SERIF = "DejaVuSerif-Bold.ttf"
SANS = "DejaVuSans.ttf"
SANS_BOLD = "DejaVuSans-Bold.ttf"

REGION_TINT = {
    "MIDDLE EAST": "red",
    "EUROPE": "ink",
    "ASIA": "teal",
    "AMERICAS": "navy",
    "AFRICA": "brown",
    "MARKETS": "green",
    "SPORT": "red",
}

# (region, headline) for the 27 dated wire items, in reading order.
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


def load_font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


def fit_lines(draw, text, face, width):
    """Split text into as few lines as fit inside width."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=face) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_para(draw, x, y, text, face, colour, width, leading=None):
    """Draw wrapped text, returning the y below it and the line count."""
    lines = fit_lines(draw, text, face, width)
    step = leading if leading is not None else int(face.size * 1.25)
    for line in lines:
        draw.text((x, y), line, font=face, fill=colour)
        y += step
    return y, len(lines)


def panel(draw, box, fill, edge=None, edge_width=0):
    draw.rectangle(box, fill=fill)
    if edge is not None:
        draw.rectangle(box, outline=edge, width=edge_width)


def masthead(draw):
    panel(draw, [0, 0, CANVAS, 118], PALETTE["navy"])
    draw.text((32, 18), "THE WORLD TODAY",
              font=load_font(SERIF, 58), fill=PALETTE["white"])
    draw.text((32, 84),
              "TUESDAY 24 NOVEMBER 2026  •  29 DATED STORIES  •  7 REGIONS",
              font=load_font(SANS_BOLD, 20), fill=PALETTE["gold"])
    panel(draw, [0, 118, CANVAS, 124], PALETTE["red"])


def hero_left(draw):
    panel(draw, [24, 142, 660, 440], PALETTE["navy"],
          edge=PALETTE["gold"], edge_width=3)
    draw.text((48, 150), "IRAN VOWS", font=load_font(SERIF, 46),
              fill=PALETTE["white"])
    draw.text((48, 196), "ALL MEANS", font=load_font(SERIF, 46),
              fill=PALETTE["white"])
    end, count = draw_para(
        draw, 48, 250,
        "Tehran vows to break the US blockade by all available means.",
        load_font(SANS_BOLD, 22), PALETTE["gold"], 590, 28)
    print("hero sub lines:", count, "ends y:", end)
    end, count = draw_para(
        draw, 48, end + 4,
        "Iran says it can reopen the strait very quickly if Washington "
        "meets its conditions.",
        load_font(SANS, 19), PALETTE["pale"], 590, 24)
    print("hero body lines:", count, "ends y:", end)
    assert end <= 386, "hero body overflows into banner"
    draw.text((48, 392), "IRGC CLAIMS 3 TANKERS HIT MINES",
              font=load_font(SANS_BOLD, 18), fill=PALETTE["amber"])
    for i in range(12):
        left = 48 + i * 50
        draw.arc([left, 424, left + 48, 438], 0, 180,
                 fill=PALETTE["wave"], width=3)


def hero_right(draw):
    panel(draw, [684, 142, 1000, 440], PALETTE["white"],
          edge=PALETTE["ink"], edge_width=3)
    panel(draw, [684, 142, 1000, 196], PALETTE["teal"])
    draw.text((706, 152), "MARKETS", font=load_font(SANS_BOLD, 22),
              fill=PALETTE["white"])
    draw.text((706, 206), "HUANG", font=load_font(SERIF, 46),
              fill=PALETTE["ink"])
    draw.text((706, 252), "IS BACK", font=load_font(SERIF, 36),
              fill=PALETTE["red"])
    end, count = draw_para(
        draw, 706, 300,
        "Shares soar 31% as Huang returns 11 days after resigning, "
        "adding $952bn in a day.",
        load_font(SANS, 19), PALETTE["ink"], 272, 24)
    print("nvidia body lines:", count, "ends y:", end)
    assert end <= 402, "nvidia body overflows into footer"
    draw.text((706, 412), "Best day since 2003",
              font=load_font(SANS_BOLD, 17), fill=PALETTE["grey"])


def wire_grid(draw):
    """Three columns of nine dated items, each tagged by region."""
    columns = [24, 356, 688]
    width = 312
    slot = 60
    top = 456
    for index, (region, headline) in enumerate(WIRE):
        column = index // 9
        row = index % 9
        x = columns[column]
        y = top + row * slot
        draw.text((x, y), "24 NOV", font=load_font(SANS_BOLD, 13),
                  fill=PALETTE["red"])
        draw.text((x + 62, y), region, font=load_font(SANS_BOLD, 13),
                  fill=PALETTE[REGION_TINT[region]])
        _, count = draw_para(draw, x, y + 18, headline,
                             load_font(SANS_BOLD, 16), PALETTE["ink"],
                             width, 20)
        print("wire", index + 1, region, "lines:", count)
        assert count <= 2, "wire headline overflows its slot: " + headline
        assert y + 58 <= top + 9 * slot, "wire item overflows the grid"


def main():
    assert len(WIRE) == 27, "wire must hold 27 items"
    regions = {region for region, _ in WIRE}
    assert len(regions) == 7, "wire must span 7 regions, got %d" % len(regions)
    image = Image.new("RGB", (CANVAS, CANVAS), PALETTE["paper"])
    draw = ImageDraw.Draw(image)
    masthead(draw)
    hero_left(draw)
    hero_right(draw)
    wire_grid(draw)
    draw.text((24, 1000),
              "ALL STORIES DATED 24 NOVEMBER 2026  •  SOURCES: REUTERS, "
              "BBC, CNN, WSJ, CBC",
              font=load_font(SANS_BOLD, 13), fill=PALETTE["grey"])
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "entry.png")
    image.save(out, format="PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
