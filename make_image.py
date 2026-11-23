"""
make_image.py – Generates entry.png (1024×1024, < 1 MiB)
Newspaper front-page: THE WORLD HERALD · 22 NOVEMBER 2026
Requires: Pillow
"""
from PIL import Image, ImageDraw, ImageFont
import os, sys, textwrap

# ── Constants ────────────────────────────────────────────────────────────────
W, H         = 1024, 1024
BG           = (255, 255, 255)
INK          = (12,  12,  12)
GREY         = (80,  80,  80)
LIGHT_GREY   = (170, 170, 170)
ACCENT       = (180, 20,  20)   # deep red for headline rule

SIZE_TITLE   = 66
SIZE_DATE    = 20
SIZE_HL      = 32
SIZE_SH      = 19
SIZE_BODY    = 22

# ── Font loader ───────────────────────────────────────────────────────────────
_BOLD_CANDIDATES = [
    "C:/Windows/Fonts/arialbd.ttf",
    "C:/Windows/Fonts/Arial Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/msttcorefonts/Arial_Bold.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
]
_REG_CANDIDATES = [
    "C:/Windows/Fonts/arial.ttf",
    "C:/Windows/Fonts/Arial.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    "/usr/share/fonts/truetype/msttcorefonts/Arial.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
]

def _load(candidates, size):
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            pass
    # Pillow ≥ 10.1 supports size= in load_default
    try:
        return ImageFont.load_default(size=size)
    except TypeError:
        return ImageFont.load_default()


def _wrap(draw, text, font, max_px):
    """Word-wrap text to fit within max_px pixels wide."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_px:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def _story_block(draw, story, x, y, col_w, fonts, sizes):
    f_hl, f_sh, f_body = fonts
    s_hl, s_sh, s_body = sizes

    # Red accent bar
    draw.rectangle([(x, y), (x + col_w - 2, y + 4)], fill=ACCENT)
    y += 10

    # Headline
    for line in _wrap(draw, story["headline"], f_hl, col_w - 4):
        draw.text((x, y), line, font=f_hl, fill=INK)
        y += s_hl + 6
    y += 4

    # Subhead (grey, italic-ish)
    for line in _wrap(draw, story["subhead"], f_sh, col_w - 4):
        draw.text((x, y), line, font=f_sh, fill=GREY)
        y += s_sh + 4
    y += 2

    # Thin rule under subhead
    draw.line([(x, y), (x + col_w - 4, y)], fill=LIGHT_GREY, width=1)
    y += 8

    # Body
    for line in _wrap(draw, story["body"], f_body, col_w - 4):
        draw.text((x, y), line, font=f_body, fill=INK)
        y += s_body + 5

    return y


# ── Main ─────────────────────────────────────────────────────────────────────
def create_newspaper(out_path="entry.png"):
    img  = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    f_title = _load(_BOLD_CANDIDATES, SIZE_TITLE)
    f_date  = _load(_REG_CANDIDATES,  SIZE_DATE)
    f_hl    = _load(_BOLD_CANDIDATES, SIZE_HL)
    f_sh    = _load(_REG_CANDIDATES,  SIZE_SH)
    f_body  = _load(_REG_CANDIDATES,  SIZE_BODY)

    # ── Masthead ─────────────────────────────────────────────────────────────
    MAST_H = 88
    draw.rectangle([(0, 0), (W, MAST_H)], fill=INK)
    draw.text((W // 2, 8), "THE WORLD HERALD",
              font=f_title, fill="white", anchor="mt")

    y = MAST_H + 6
    draw.text((14, y), "SUNDAY, 22 NOVEMBER 2026",
              font=f_date, fill=INK)
    draw.text((W - 14, y), "SPECIAL EDITION",
              font=f_date, fill=INK, anchor="ra")
    y += SIZE_DATE + 8

    # Double rule
    draw.line([(10, y), (W - 10, y)], fill=INK, width=3)
    y += 5
    draw.line([(10, y), (W - 10, y)], fill=INK, width=1)
    y += 14

    # ── Two-column layout ─────────────────────────────────────────────────────
    MARGIN = 12
    GAP    = 16
    col_w  = (W - 2 * MARGIN - GAP) // 2
    col_x  = [MARGIN, MARGIN + col_w + GAP]

    stories = [
        {
            "headline": "COP31 ANTALYA ENDS WITHOUT DEAL",
            "subhead":  "First failure since 2009 · 'Fossil fuels' erased · Two-day overrun",
            "body":     (
                "The COP31 climate summit closed in Antalya Saturday without a binding "
                "agreement — the first UN climate collapse since Copenhagen 2009. 'Fossil "
                "fuels' was stripped from the final text, breaking with every accord since "
                "Glasgow 2021. Talks ran two days beyond schedule as blocs clashed over "
                "finance targets and emissions timelines. Observers called the outcome a "
                "historic setback for multilateral climate action."
            ),
        },
        {
            "headline": "IRAN ESCALATES IN STRAIT OF HORMUZ",
            "subhead":  "~25 tankers struck since Nov 14 · US MQ-1 drone downed, Iran claims",
            "body":     (
                "Iranian forces have struck roughly 25 oil tankers in the Strait of Hormuz "
                "since 14 November in what analysts call a coordinated pressure campaign. "
                "Tehran separately claimed to have shot down a US MQ-1 Predator drone over "
                "the Persian Gulf; Washington has not confirmed the loss. Marine insurance "
                "premiums hit record highs and Brent crude briefly topped $105 per barrel."
            ),
        },
        {
            "headline": "ZELENSKY: RELEASE PATRIOTS NOW",
            "subhead":  "Ukraine presses US to free Patriot batteries from strategic reserve",
            "body":     (
                "President Volodymyr Zelensky called on Washington to release Patriot "
                "air-defence batteries from US strategic reserves, warning Ukraine's air "
                "shield is 'running on fumes'. The appeal follows fresh Russian drone "
                "strikes on energy infrastructure in Kharkiv and Zaporizhzhia. The "
                "administration has not responded publicly, citing allied consultations."
            ),
        },
        {
            "headline": "CHESS: GUKESH VS SINDAROV BEGINS",
            "subhead":  "World Championship opens in Geneva · Game 1: Monday 24 November",
            "body":     (
                "The 2026 World Chess Championship between reigning champion D Gukesh "
                "(India, 20) and challenger Nodirbek Sindarov (Uzbekistan, 19) opened "
                "ceremonially in Geneva on Saturday. Swiss Federal President "
                "Karin Keller-Sutter played the first symbolic move. Game 1 is set for "
                "Monday 24 November. Sindarov is the youngest challenger in championship "
                "history."
            ),
        },
    ]

    fonts = (f_hl, f_sh, f_body)
    sizes = (SIZE_HL, SIZE_SH, SIZE_BODY)

    col_y = [y, y]
    for idx, story in enumerate(stories):
        col  = idx % 2
        cx   = col_x[col]
        cy   = col_y[col]

        # Separator between stories in the same column
        if idx >= 2:
            cy += 10
            draw.line([(cx, cy), (cx + col_w - 2, cy)], fill=LIGHT_GREY, width=1)
            cy += 10

        end_y = _story_block(draw, story, cx, cy, col_w, fonts, sizes)
        col_y[col] = end_y

    # Vertical column divider
    div_x = MARGIN + col_w + GAP // 2
    draw.line([(div_x, y - 10), (div_x, max(col_y) + 10)], fill=LIGHT_GREY, width=1)

    # ── Footer ────────────────────────────────────────────────────────────────
    fy = H - 28
    draw.line([(10, fy), (W - 10, fy)], fill=INK, width=1)
    draw.text((W // 2, fy + 4),
              "make.fun/bounty/news-image-20261122",
              font=f_date, fill=GREY, anchor="mt")

    # ── Save ──────────────────────────────────────────────────────────────────
    img.save(out_path, "PNG", optimize=True)
    size = os.path.getsize(out_path)
    print(f"Saved {out_path}  ({size:,} bytes / {size / 1024:.1f} KiB)")
    if size >= 1 * 1024 * 1024:
        raise RuntimeError(f"entry.png is {size} bytes — exceeds 1 MiB limit!")
    return out_path


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(script_dir, "entry.png")
    create_newspaper(out)
