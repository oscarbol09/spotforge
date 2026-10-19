"""Generate professional high-resolution cover image for SpotForge."""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

# Dimensions: 1200 x 630 (Standard OG / DEV.to cover ratio)
WIDTH = 1200
HEIGHT = 630

# Colors
BG_COLOR = (11, 15, 25)        # slate-950
PURPLE_PRIMARY = (147, 51, 234) # brand-600
INDIGO_ACCENT = (99, 102, 241)  # indigo-500
AMBER_ACCENT = (251, 191, 36)   # amber-400
TEXT_WHITE = (248, 250, 252)    # slate-50
TEXT_MUTED = (148, 163, 184)    # slate-400
CARD_BG = (19, 26, 42)          # slate-900 / dark card
CARD_BORDER = (45, 55, 78)      # border slate-700

img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
draw = ImageDraw.Draw(img)

# 1. Subtle radial gradient glow in the center-top
for r in range(400, 0, -5):
    alpha = int(35 * (1 - r / 400))
    glow_color = (alpha, alpha // 2, alpha + 15)
    draw.ellipse(
        [WIDTH // 2 - r, 80 - r // 2, WIDTH // 2 + r, 80 + r // 2],
        fill=glow_color,
    )

# 2. Top Badge
badge_text = "HACKTOBERFEST 2026  •  OPEN-SOURCE AI CHALLENGE (SIDE HUSTLE)"
try:
    font_badge = ImageFont.truetype("arial.ttf", 16)
    font_title = ImageFont.truetype("arialbd.ttf", 64)
    font_sub = ImageFont.truetype("arial.ttf", 26)
    font_card_title = ImageFont.truetype("arialbd.ttf", 22)
    font_card_sub = ImageFont.truetype("arial.ttf", 15)
    font_pill = ImageFont.truetype("arialbd.ttf", 15)
except Exception:
    font_badge = ImageFont.load_default()
    font_title = font_badge
    font_sub = font_badge
    font_card_title = font_badge
    font_card_sub = font_badge
    font_pill = font_badge

# Draw Top Badge pill
badge_bbox = draw.textbbox((0, 0), badge_text, font=font_badge)
badge_w = badge_bbox[2] - badge_bbox[0]
badge_x = (WIDTH - badge_w) // 2
badge_y = 60
draw.rounded_rectangle(
    [badge_x - 18, badge_y - 8, badge_x + badge_w + 18, badge_y + 24],
    radius=16,
    fill=(30, 27, 75),
    outline=(126, 34, 206),
    width=1,
)
draw.text((badge_x, badge_y), badge_text, font=font_badge, fill=AMBER_ACCENT)

# 3. Main Title
title = "SpotForge"
title_bbox = draw.textbbox((0, 0), title, font=font_title)
title_w = title_bbox[2] - title_bbox[0]
title_x = (WIDTH - title_w) // 2
title_y = 130
draw.text((title_x, title_y), title, font=font_title, fill=TEXT_WHITE)

# 4. Subtitle
sub = "Turn 3 Local Business Facts into a Broadcast-Ready Commercial Audio Ad"
sub_bbox = draw.textbbox((0, 0), sub, font=font_sub)
sub_w = sub_bbox[2] - sub_bbox[0]
sub_x = (WIDTH - sub_w) // 2
sub_y = 220
draw.text((sub_x, sub_y), sub, font=font_sub, fill=TEXT_MUTED)

# 5. Technology Stack Pills
pills = [
    "Google Gemma 4 (Open Weights)",
    "Deterministic Phonetic Normalizer",
    "ElevenLabs Voiceover",
    "FFmpeg Audio Mixer",
]
pills_str = "   •   ".join(pills)
pills_bbox = draw.textbbox((0, 0), pills_str, font=font_pill)
pills_w = pills_bbox[2] - pills_bbox[0]
pills_x = (WIDTH - pills_w) // 2
pills_y = 290
draw.text((pills_x, pills_y), pills_str, font=font_pill, fill=(192, 132, 252))

# 6. Metric Cards at bottom
cards = [
    ("~30s Ad Pacing", "Physics-based speech rate & duration calibration"),
    ("AIDA Copywriting", "Proven sales structure tailored to local retail"),
    ("97%+ Gross Margin", "Production for pennies; high-margin freelance side hustle"),
]

card_w = 340
card_h = 130
gap = 30
total_cards_w = len(cards) * card_w + (len(cards) - 1) * gap
cards_start_x = (WIDTH - total_cards_w) // 2
cards_y = 390

for i, (head, desc) in enumerate(cards):
    cx = cards_start_x + i * (card_w + gap)
    draw.rounded_rectangle(
        [cx, cards_y, cx + card_w, cards_y + card_h],
        radius=14,
        fill=CARD_BG,
        outline=CARD_BORDER,
        width=1,
    )
    # Accent top border
    draw.rounded_rectangle(
        [cx, cards_y, cx + card_w, cards_y + 4],
        radius=2,
        fill=PURPLE_PRIMARY if i % 2 == 0 else INDIGO_ACCENT,
    )
    draw.text((cx + 20, cards_y + 24), head, font=font_card_title, fill=TEXT_WHITE)

    # Word wrap description
    words = desc.split()
    line1 = " ".join(words[:5])
    line2 = " ".join(words[5:])
    draw.text((cx + 20, cards_y + 60), line1, font=font_card_sub, fill=TEXT_MUTED)
    if line2:
        draw.text((cx + 20, cards_y + 82), line2, font=font_card_sub, fill=TEXT_MUTED)

# 7. Footer
footer_text = "github.com/oscarbol09/spotforge  •  MIT License  •  FastAPI + Vanilla SPA"
footer_bbox = draw.textbbox((0, 0), footer_text, font=font_badge)
footer_w = footer_bbox[2] - footer_bbox[0]
draw.text(((WIDTH - footer_w) // 2, 570), footer_text, font=font_badge, fill=(100, 116, 139))

output_path = Path("docs/cover.png")
output_path.parent.mkdir(parents=True, exist_ok=True)
img.save(output_path, "PNG", quality=95)
print(f"[SUCCESS] Cover image generated at: {output_path.as_posix()} ({output_path.stat().st_size} bytes)")
