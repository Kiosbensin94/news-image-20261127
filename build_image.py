#!/usr/bin/env python3
"""Render THE WORLD TODAY - 27 November 2026 front page (1024x1024 PNG).

Flat-vector newspaper drawn with PIL: every word is real text, so nothing
is garbled. News verified against wire reports on the morning of 27 Nov 2026.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 232)
INK = (26, 26, 26)
RED = (164, 31, 31)
NAVY = (34, 64, 107)
GREY = (110, 108, 100)
LIGHT = (233, 227, 210)
MAPSEA = (232, 238, 242)
MAPLAND = (226, 219, 197)
MAPLINE = (180, 172, 150)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIFB = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIFI = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANSB = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill=INK, leading=None):
    if leading is None:
        leading = int(fnt.size * 1.18)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def hline(draw, x0, x1, y, fill=INK, width=1):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
M = 26                      # margin
CW = W - 2 * M              # content width = 972
y = 18

# ---------------------------------------------------------------- masthead
f_title = font(SERIFB, 56)
t = "THE WORLD TODAY"
tw = d.textlength(t, font=f_title)
d.text(((W - tw) / 2, y), t, font=f_title, fill=INK)
y += 66
hline(d, M, W - M, y, width=3)
y += 4
hline(d, M, W - M, y, width=1)
y += 8
f_date = font(SANSB, 15)
d.text((M, y), "FRIDAY, 27 NOVEMBER 2026", font=f_date, fill=RED)
r = "EDITION No. 27  •  2026"
d.text((W - M - d.textlength(r, font=f_date), y), r, font=f_date, fill=INK)
c = "ONE DAY  —  ONE PAGE  —  ALL THE NEWS"
d.text(((W - d.textlength(c, font=f_date)) / 2, y), c, font=f_date, fill=GREY)
y += 22
hline(d, M, W - M, y, width=1)
y += 7
f_counts = font(SANSB, 19)
c = "33 STORIES  •  7 REGIONS  •  15 SOURCES"
d.text(((W - d.textlength(c, font=f_counts)) / 2, y), c, font=f_counts, fill=NAVY)
y += 26

# ------------------------------------------------------------- region bar
regions = [("EUROPE", 11, (34, 64, 107)), ("ASIA", 8, (164, 31, 31)),
           ("MIDDLE EAST", 5, (146, 98, 24)), ("N. AMERICA", 5, (46, 110, 84)),
           ("S. AMERICA", 2, (110, 70, 130)), ("AFRICA", 1, (160, 90, 50)),
           ("OCEANIA", 1, (90, 110, 120))]
bar_h = 14
x = M
for name, n, col in regions:
    wseg = CW * n / 33
    d.rectangle([x, y, x + wseg - 1, y + bar_h], fill=col)
    x += wseg
y += bar_h + 5
f_leg = font(SANSB, 11)
parts = [(f"{name} {n}", col) for name, n, col in regions]
# each item: 9px colour square + 3px gap + text + 12px gap to next square
item_w = [12 + d.textlength(txt, font=f_leg) + 12 for txt, _ in parts]
total_w = sum(item_w) - 12
x = (W - total_w) / 2
for (txt, col), w in zip(parts, item_w):
    d.rectangle([x, y + 2, x + 9, y + 11], fill=col)
    d.text((x + 12, y), txt, font=f_leg, fill=INK)
    x += w
y += 18
hline(d, M, W - M, y, width=1)
y += 9

# ------------------------------------------------------------------- leads
LEADS = [
    dict(kicker="MIDDLE EAST  •  KUWAIT", head="DRONES KILL 2 ITALIANS IN KUWAIT",
         body=("Two Rheinmetall technicians die at an air-defence station hit "
               "by drones. Italy and Kuwait blame Iran; Tehran denies any role "
               "and offers a joint inquiry."),
         src="SOURCE: REUTERS / AP / BBC", status="CONFIRMED  •  CLAIM", art="drone"),
    dict(kicker="MIDDLE EAST  •  GAZA", head="10 KILLED IN GAZA AS CEASEFIRE FRAYS",
         body=("Overnight strikes hit Gaza City and Deir al-Balah. Hamas official "
               "Khaled Abu Nada is among the dead, and Hamas weighs its response."),
         src="SOURCE: REUTERS / AP", status="CONFIRMED", art="city"),
    dict(kicker="NORTH AMERICA  •  USA", head="STORM GROUNDS 100TH MACY'S PARADE",
         body=("A Thanksgiving nor'easter cuts power to 800,000+, cancels 400+ "
               "flights and strands 80m travellers. The parade moves to "
               "Saturday — a first in 100 years."),
         src="SOURCE: REUTERS / AP", status="ONGOING", art="storm"),
]
col_w = int((CW - 2 * 18) / 3)
lead_top = y
f_kick = font(SANSB, 12)
f_head = font(SERIFB, 23)
f_body = font(SERIF, 14)
f_src = font(SANSB, 11)
lead_bottom = y
for i, L in enumerate(LEADS):
    x0 = M + i * (col_w + 18)
    # flat illustration panel
    ax0, ay0, ax1, ay1 = x0, y, x0 + col_w, y + 64
    if L["art"] == "drone":
        d.rectangle([ax0, ay0, ax1, ay1], fill=(223, 232, 238))
        d.rectangle([ax0, ay1 - 26, ax1, ay1], fill=(224, 200, 152))  # desert
        # radar tower
        d.line([(ax0 + 52, ay1 - 26), (ax0 + 52, ay0 + 30)], fill=INK, width=3)
        d.line([(ax0 + 44, ay1 - 26), (ax0 + 60, ay1 - 26)], fill=INK, width=3)
        d.arc([ax0 + 38, ay0 + 14, ax0 + 66, ay0 + 42], 180, 360, fill=INK, width=3)
        # drone silhouette
        cx, cy = ax0 + col_w * 0.68, ay0 + 34
        d.ellipse([cx - 26, cy - 8, cx + 26, cy + 8], fill=(40, 40, 40))
        for sx in (-34, 34):
            d.line([(cx + sx * 0.7, cy), (cx + sx, cy - 12)], fill=(40, 40, 40), width=3)
            d.ellipse([cx + sx - 9, cy - 18, cx + sx + 9, cy - 6], outline=(40, 40, 40), width=3)
        d.line([(cx - 46, cy - 16), (cx + 46, cy - 16)], fill=(40, 40, 40), width=2)
    elif L["art"] == "city":
        d.rectangle([ax0, ay0, ax1, ay1], fill=(238, 228, 208))
        d.rectangle([ax0, ay1 - 18, ax1, ay1], fill=(200, 190, 168))
        for bx, bw, bh, col in [(0, 62, 40, (143, 133, 120)), (66, 48, 48, (120, 110, 96)),
                                (118, 58, 34, (160, 150, 134)), (180, 52, 46, (133, 122, 108)),
                                (236, 56, 30, (150, 140, 124))]:
            d.rectangle([ax0 + bx, ay1 - 18 - bh, ax0 + bx + bw, ay1 - 18], fill=col)
            for wy in range(ay1 - 18 - bh + 8, ay1 - 24, 12):
                for wx in range(ax0 + bx + 8, ax0 + bx + bw - 6, 14):
                    d.rectangle([wx, wy, wx + 6, wy + 7], fill=(248, 244, 232))
        # smoke plumes
        for sx, sy, r in [(ax0 + 92, ay0 + 26, 13), (ax0 + 100, ay0 + 14, 9),
                          (ax0 + 210, ay0 + 30, 11), (ax0 + 218, ay0 + 18, 8)]:
            d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(150, 148, 142))
    else:  # storm
        d.rectangle([ax0, ay0, ax1, ay1], fill=(216, 226, 234))
        # cloud
        cx, cy = ax0 + 110, ay0 + 34
        for ox, oy, r in [(-38, 6, 20), (-8, -8, 26), (26, 4, 22), (48, 12, 14)]:
            d.ellipse([cx + ox - r, cy + oy - r, cx + ox + r, cy + oy + r], fill=(90, 107, 125))
        d.rectangle([cx - 58, cy - 2, cx + 62, cy + 22], fill=(90, 107, 125))
        # rain
        for rx in range(0, 8):
            xx = ax0 + 40 + rx * 16
            d.line([(xx, ay0 + 52), (xx - 5, ay0 + 66)], fill=(127, 163, 192), width=2)
        # lightning
        d.polygon([(ax0 + 200, ay0 + 44), (ax0 + 212, ay0 + 44), (ax0 + 205, ay0 + 54),
                   (ax0 + 214, ay0 + 54), (ax0 + 198, ay0 + 68), (ax0 + 203, ay0 + 56),
                   (ax0 + 195, ay0 + 56)], fill=(232, 185, 59))
        # parade balloon
        bx, by = ax0 + col_w - 62, ay0 + 18
        d.ellipse([bx, by, bx + 46, by + 26], fill=(192, 57, 43))
        d.line([(bx + 15, by), (bx + 15, by + 26)], fill=(248, 244, 232), width=3)
        d.line([(bx + 31, by), (bx + 31, by + 26)], fill=(248, 244, 232), width=3)
        d.line([(bx + 23, by + 26), (bx + 23, by + 34)], fill=INK, width=2)
        d.rectangle([bx + 15, by + 34, bx + 31, by + 40], outline=INK, width=2)
    yy = y + 72
    d.text((x0, yy), L["kicker"], font=f_kick, fill=RED)
    yy += 17
    yy = text_block(d, x0, yy, wrap(d, L["head"], f_head, col_w), f_head, leading=26)
    yy += 2
    yy = text_block(d, x0, yy, wrap(d, L["body"], f_body, col_w), f_body, leading=17)
    yy += 4
    d.text((x0, yy), L["src"], font=f_src, fill=GREY)
    yy += 13
    d.text((x0, yy), L["status"], font=f_src, fill=RED)
    yy += 14
    lead_bottom = max(lead_bottom, yy)
    if i < 2:
        d.line([(x0 + col_w + 9, lead_top), (x0 + col_w + 9, lead_bottom)], fill=(200, 194, 176), width=1)
y = lead_bottom + 2
hline(d, M, W - M, y, width=1)
y += 7

# ------------------------------------------------------------ big numbers
stats = [("800,000+", "HOMES WITHOUT POWER"), ("80M", "THANKSGIVING TRAVELLERS"),
         ("400+", "FLIGHTS CANCELLED"), ("$96.57", "BRENT CRUDE, +1.2%"),
         ("100,000+ T", "GRAIN UNDER FIRE"), ("400,000", "WEDDING GUESTS"),
         ("7,000 T", "DIESEL ADRIFT"), ("€45BN", "UKRAINE LOAN ROW")]
strip_top = y
d.rectangle([M, y, W - M, y + 48], fill=NAVY)
f_num = font(SANSB, 18)
f_lab = font(SANS, 10)
cell_w = CW / 4
for i, (num, lab) in enumerate(stats):
    cx = M + (i % 4) * cell_w
    cy = strip_top + (i // 4) * 24
    d.text((cx + 10, cy + 3), num, font=f_num, fill=(255, 255, 255))
    d.text((cx + 10 + d.textlength(num, font=f_num) + 7, cy + 8), lab,
           font=f_lab, fill=(200, 210, 225))
y = strip_top + 48 + 6
hline(d, M, W - M, y, width=1)
y += 6

# ------------------------------------------------------- numbered 4 - 13
f_sec = font(SANSB, 13)
d.text((M, y), "THE DAY IN BRIEF", font=f_sec, fill=RED)
d.text((W - M - d.textlength("STORIES 4 – 13", font=f_sec), y), "STORIES 4 – 13",
       font=f_sec, fill=GREY)
y += 20
NUMBERED = [
    ("KYIV HIT BY BALLISTIC MISSILES",
     "Missiles hit a shopping centre; 7 hurt. Kyiv braces for a grid attack.",
     "REUTERS / AP — CONFIRMED"),
    ("GRAIN SHIPS ATTACKED OFF ODESA",
     "Two foreign bulk carriers hit; 100,000+ tonnes of wheat at risk.",
     "REUTERS — REPORTED"),
    ("HOUTHIS CLAIM SAUDI REFINERY HIT",
     "Rebels claim Ras Tanura hit; Riyadh says it downed two missiles.",
     "REUTERS — CLAIM / CONFIRMED"),
    ("TWO TANKERS HIT BY MINES IN GULF",
     "Two tankers strike sea mines off Oman; fires aboard both vessels.",
     "REUTERS / FARS — REPORTED"),
    ("BANGKOK REFINERY BLAST HURTS 9",
     "Blast at Bangchak plant; three critical. All production units shut.",
     "AP / BBC — CONFIRMED"),
    ("EU SPLIT OVER €45BN UKRAINE LOAN",
     "Leaders split at summit over a €45bn loan for 2027 and the budget.",
     "REUTERS — REPORTED"),
    ("SPAIN'S DE COS TO LEAD ECB",
     "First Spaniard to hold the job; he succeeds Christine Lagarde.",
     "AL JAZEERA / EURONEWS — OFFICIAL"),
    ("UK MIGRATION LOWEST SINCE 1997",
     "Net migration falls to its lowest outside the pandemic years.",
     "NYT — OFFICIAL"),
    ("KIM VOWS MORE NUCLEAR ARMS",
     "Leader pledges a bigger arsenal and wider tactical nuclear rollout.",
     "BBC / REUTERS — OFFICIAL"),
    ("GUINEA-BISSAU VOTE DELAYED TO 2028",
     "Junta postpones elections by two years, a year after seizing power.",
     "REUTERS / AP — OFFICIAL"),
]
f_nh = font(SERIFB, 15)
f_nb = font(SERIF, 13)
f_ns = font(SANS, 10)
ncol_w = int((CW - 24) / 2)
item_h = 41
for i, (head, body, src) in enumerate(NUMBERED):
    col = i % 2
    row = i // 2
    x0 = M + col * (ncol_w + 24)
    yy = y + row * item_h
    d.ellipse([x0, yy + 2, x0 + 21, yy + 23], fill=RED)
    num = str(i + 4)
    d.text((x0 + (21 - d.textlength(num, font=font(SANSB, 13))) / 2, yy + 4),
           num, font=font(SANSB, 13), fill=(255, 255, 255))
    tx = x0 + 28
    d.text((tx, yy), head, font=f_nh, fill=INK)
    blines = wrap(d, body, f_nb, ncol_w - 28)
    by = yy + 19
    for ln in blines[:1]:
        d.text((tx, by), ln, font=f_nb, fill=INK)
        by += 14
    d.text((tx, by + 1), src, font=f_ns, fill=GREY)
y += 5 * item_h + 4
hline(d, M, W - M, y, width=1)
y += 8

# -------------------------------------------------------------- also on
d.text((M, y), "ALSO ON 27 NOVEMBER", font=f_sec, fill=RED)
d.text((W - M - d.textlength("STORIES 14 – 33", font=f_sec), y), "STORIES 14 – 33",
       font=f_sec, fill=GREY)
y += 19
ALSO = [
    ("FRANCE", "Depardieu to stand trial over 2018 rape claim.", "AP", "OFFICIAL"),
    ("SPAIN", "Tanker Med Emre capsizes off Ibiza; 1 dead.", "REUTERS", "CONFIRMED"),
    ("NEW ZEALAND", "Final count due today; coalition on 67/131.", "REUTERS", "ONGOING"),
    ("VENEZUELA", "US, Qatar plan bridge loan to clear arrears.", "REUTERS", "REPORTED"),
    ("NORTH KOREA", "Missile shipments to Russia briefly halted.", "REUTERS", "REPORTED"),
    ("RUSSIA", "Drone strike sets Slavyansk refinery ablaze.", "REUTERS", "REPORTED"),
    ("USA", "Trump seeks probe of 'fake' GDP, revised to 4.3%.", "MINT", "REPORTED"),
    ("PERSIAN GULF", "Tanker reports blast nearby, west of Dubai.", "UKMTO", "REPORTED"),
    ("CHESS", "Gukesh, Sindarov draw marathon Game 3.", "INDIA TODAY", "CONFIRMED"),
    ("MARKETS", "Black Friday: shares rise; Wall St shut for holiday.", "AP", "REPORTED"),
    ("USA", "FDA clears Neuralink brain-implant trial for ALS.", "REUTERS", "OFFICIAL"),
    ("ARGENTINA", "Central bank barred from printing money.", "AP", "OFFICIAL"),
    ("INDIA", "Top court: judges must sit on seizure panels.", "TIMES OF INDIA", "OFFICIAL"),
    ("NEPAL", "Move to declare 213 missing Indians dead.", "MATHRUBHUMI", "OFFICIAL"),
    ("CHINA", "Border with India 'generally stable', Beijing says.", "BEIJING", "OFFICIAL"),
    ("INDIA", "Murder charge after 400,000-guest wedding.", "AL JAZEERA", "REPORTED"),
    ("USA", "Musk: every US child to get two SpaceX shares.", "THE HINDU", "CLAIM"),
    ("FRANCE", "Mainstream politics risks failing at election.", "BBC", "REPORTED"),
    ("OIL", "Brent closes at $96.57, up 1.2%.", "REUTERS", "CONFIRMED"),
    ("FOOTBALL", "AC Milan rally from 0\u20132 to beat Olympiacos 4\u20132.", "UEFA", "CONFIRMED"),
]
f_a = font(SERIF, 12.5)
f_ab = font(SERIFB, 12.5)
f_as = font(SANS, 10)
acol_w = int((CW - 24) / 2)
row_h = 12.5
for i, (place, txt, src, status) in enumerate(ALSO):
    col = i % 2
    row = i // 2
    x0 = M + col * (acol_w + 24)
    yy = y + row * row_h
    pre = f"{i + 14}. {place} — "
    d.text((x0, yy), pre, font=f_ab, fill=INK)
    px = x0 + d.textlength(pre, font=f_ab)
    d.text((px, yy), txt, font=f_a, fill=INK)
    sx = px + d.textlength(txt, font=f_a) + 6
    tag = f"[{src} • {status}]"
    d.text((sx, yy + 1), tag, font=f_as, fill=GREY)
    total = (sx - x0) + d.textlength(tag, font=f_as)
    if total > acol_w:
        print(f"OVERFLOW ALSO {i + 14}: {total:.0f}px > {acol_w}px :: {pre}{txt} {tag}")
y += 10 * row_h + 4
hline(d, M, W - M, y, width=1)
y += 6

# ------------------------------------------- bottom: map + timeline + date check
bot_top = y
map_w, tl_w, dc_w = 356, 296, 296
f_bh = font(SANSB, 12)
d.text((M, y), "WHERE IT HAPPENED", font=f_bh, fill=RED)
d.text((M + map_w + 12, y), "THE DAY IN UTC", font=f_bh, fill=RED)
d.text((M + map_w + 12 + tl_w + 12, y), "DATE CHECK — LEFT OUT ON PURPOSE", font=f_bh, fill=RED)
y += 17
map_h = 96
mx0, my0 = M, y
d.rectangle([mx0, my0, mx0 + map_w, my0 + map_h], fill=MAPSEA,
            outline=MAPLINE, width=1)
# continents as rough lon/lat polygons
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 73), (-75, 72),
     (-65, 60), (-55, 52), (-60, 45), (-70, 42), (-75, 35), (-80, 26), (-85, 30),
     (-90, 21), (-95, 18), (-100, 16), (-105, 20), (-110, 23), (-115, 30),
     (-125, 40), (-125, 48), (-135, 58), (-155, 58), (-165, 60)],
    [(-80, 10), (-75, 12), (-70, 12), (-60, 8), (-50, 5), (-40, 0), (-35, -8),
     (-40, -20), (-48, -28), (-55, -35), (-65, -45), (-70, -54), (-73, -40),
     (-72, -20), (-77, -12), (-80, -5)],
    [(-17, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (30, 31), (35, 28),
     (43, 12), (48, 11), (51, 10), (45, 0), (40, -10), (35, -20), (30, -30),
     (20, -35), (15, -30), (12, -18), (9, 0), (8, 4), (-8, 5), (-13, 8)],
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57), (10, 59), (18, 56),
     (21, 55), (24, 59), (28, 60), (30, 62), (32, 70), (40, 68), (45, 66),
     (40, 60), (35, 55), (30, 50), (28, 45), (23, 40), (19, 42), (12, 44),
     (8, 44), (3, 42), (0, 39), (-2, 37), (-6, 36)],
    [(30, 68), (40, 68), (50, 69), (60, 70), (70, 72), (80, 73), (90, 74),
     (100, 75), (110, 75), (120, 73), (130, 72), (140, 72), (150, 70), (160, 66),
     (170, 66), (162, 60), (158, 52), (150, 45), (142, 40), (135, 35), (127, 33),
     (122, 30), (120, 25), (110, 20), (105, 10), (100, 8), (95, 15), (90, 22),
     (85, 20), (80, 8), (75, 10), (70, 20), (65, 25), (60, 25), (55, 26),
     (50, 28), (45, 30), (40, 35), (35, 36), (32, 42), (30, 50), (30, 60)],
    [(113, -22), (114, -30), (115, -35), (125, -33), (130, -32), (135, -35),
     (140, -38), (145, -38), (150, -37), (153, -27), (150, -22), (146, -19),
     (142, -11), (136, -12), (132, -11), (126, -14), (122, -17), (118, -20)],
]
def proj(lon, lat):
    return (mx0 + (lon + 170) / 360 * map_w, my0 + (75 - lat) / 130 * map_h)
for poly in CONTINENTS:
    d.polygon([proj(lon, lat) for lon, lat in poly], fill=MAPLAND, outline=MAPLINE)
PINS = [  # (story no, lon, lat, dot_dx, dot_dy, lab_dx, lab_dy)
    (1, 47.5, 29.4, 0, 0, 7, -9), (2, 34.5, 31.5, -8, 2, -18, -5),
    (3, -74, 40.7, 0, 0, 6, -9), (4, 30.5, 50.4, 2, -6, 7, -3),
    (5, 30.7, 46.5, 6, 10, -15, 5), (6, 46.7, 24.6, -2, 8, 7, 3),
    (7, 56.5, 26.5, 0, 0, 8, -9), (8, 100.5, 13.8, 0, 0, 6, -9),
    (9, 4.4, 50.8, -4, 10, -17, 1), (10, 8.7, 50.1, 2, -8, 8, -5),
    (11, -0.1, 51.5, 0, 0, -15, -9), (12, 125.8, 39.0, 0, 0, 6, -9),
    (13, -15.6, 11.9, 0, 0, 6, -9),
]
f_pin = font(SANSB, 9)
for n, lon, lat, ddx, ddy, ldx, ldy in PINS:
    px, py = proj(lon, lat)
    qx, qy = px + ddx, py + ddy
    if (ddx, ddy) != (0, 0):
        d.line([(px, py), (qx, qy)], fill=(120, 118, 110), width=1)
    d.ellipse([qx - 3.5, qy - 3.5, qx + 3.5, qy + 3.5], fill=RED,
              outline=(255, 255, 255), width=1)
    lx, ly = qx + ldx, qy + ldy
    for ox, oy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        d.text((lx + ox, ly + oy), str(n), font=f_pin, fill=(255, 255, 255))
    d.text((lx, ly), str(n), font=f_pin, fill=RED)
# timeline
tl_x = M + map_w + 12
f_tt = font(SANSB, 12)
f_tb = font(SERIF, 12)
TIMELINE = [
    ("01:00", "NZ final count due."),
    ("02:11", "Depardieu ordered to trial."),
    ("02:26", "Hamas weighs response."),
    ("03:31", "Tanker capsizes off Ibiza."),
    ("06:03", "Kuwait deaths confirmed."),
]
ty = y
for t, txt in TIMELINE:
    d.text((tl_x, ty), t, font=f_tt, fill=NAVY)
    d.text((tl_x + 50, ty), txt, font=f_tb, fill=INK)
    ty += 18
# date check
dc_x = M + map_w + 12 + tl_w + 12
f_dc = font(SERIF, 11)
DATECHECK = [
    "Mali: 349 Russians died since 2023 — Guardian, 24 Nov.",
    "Nvidia brings back Jensen Huang — 24 Nov.",
    "Sudan: RSF strike kills 19 at hospital — 25 Nov.",
    "Yemen: Houthis advance ~50 km to Aden — 25 Nov.",
    "Cairo tanker crash kills 31 — 26 Nov.",
    "COP31 ends with no fossil-fuel deal — 26 Nov.",
]
dy = y
for item in DATECHECK:
    d.text((dc_x, dy), "•  " + item, font=f_dc, fill=(90, 88, 80))
    dy += 15
y = bot_top + 17 + map_h + 5
hline(d, M, W - M, y, width=1)
y += 5
f_foot = font(SANS, 10.5)
foot = "DRAWN, NOT PHOTOGRAPHED  •  SOURCES: REUTERS, AP, BBC, NYT, AL JAZEERA AND OTHERS  •  THE WORLD TODAY"
d.text(((W - d.textlength(foot, font=f_foot)) / 2, y), foot, font=f_foot, fill=GREY)
print("final y:", y, "of", H)
img.save("/home/hatch/workspace/makefun-news-image-20261127/entry.png", optimize=True)
import os
print("bytes:", os.path.getsize("/home/hatch/workspace/makefun-news-image-20261127/entry.png"))
