from PIL import Image, ImageDraw, ImageFont
import os

# Load high-res cover_image
base = Image.open('static/images/cover_image.png').convert('RGBA')
bw, bh = base.size
print(f"Base size: {bw}x{bh}")

# Load the clean center hub
hub = Image.open('static/images/clean_center_hub.png').convert('RGBA')

# In cover_image.png (1536 x 1024):
# The consumer card header is at x ~ 768, y ~ 220 to 280
# The text "رحلة المستفيد في المنصة الوطنية لأسواق النفع العام" is at y ~ 160 to 200
# Center is x = 768.

# Let's resize hub to fit nicely between header and consumer card
# Hub diameter ~ 170 px
hub_size = 175
hub_resized = hub.resize((hub_size, hub_size), Image.Resampling.LANCZOS)

# Coordinates for center hub:
hx = int((bw - hub_size) / 2)
hy = 175  # slightly overlapping or sitting right above consumer card

# Create overlay for connecting golden lines and hub
overlay = Image.new('RGBA', (bw, bh), (0, 0, 0, 0))
draw = ImageDraw.Draw(overlay)

# Draw golden connecting lines from hub to left and right cards
# Gold color: #c59b27 -> RGB (197, 155, 39)
gold_color = (197, 155, 39, 230)
gold_glow = (197, 155, 39, 80)

# Line to Right Card (Seller: x ~ 480, y ~ 240)
# In cover_image:
# Left card is Seller (x ~ 60 to 520, header top ~ 220)
# Right card is Admin (x ~ 1020 to 1480, header top ~ 220)
# Center card is Consumer (x ~ 560 to 980, header top ~ 220)

# Wire 1: From hub center (768, 262) to Seller header (490, 240)
draw.line([(768, 262), (510, 240)], fill=gold_color, width=4)
draw.ellipse([505, 235, 515, 245], fill=gold_color)

# Wire 2: From hub center (768, 262) to Admin header (1030, 240)
draw.line([(768, 262), (1026, 240)], fill=gold_color, width=4)
draw.ellipse([1021, 235, 1031, 245], fill=gold_color)

# Wire 3: From hub center down to Consumer header
draw.line([(768, 262 + hub_size//2), (768, 305)], fill=gold_color, width=4)
draw.ellipse([763, 300, 773, 310], fill=gold_color)

# Paste the hub
overlay.paste(hub_resized, (hx, hy), hub_resized)

# Draw the small badge below hub: "تسجيل الدخول عبر نفاذ"
badge_w, badge_h = 160, 26
bx = int((bw - badge_w) / 2)
by = hy + hub_size - 14

draw.rounded_rectangle([bx, by, bx + badge_w, by + badge_h], radius=13, fill=(255, 255, 255, 245), outline=gold_color, width=2)

# Composite together
result = Image.alpha_composite(base, overlay)

# Save result
result.convert('RGB').save('static/images/infographic_composite_preview.jpg', quality=95)
print("Saved infographic_composite_preview.jpg")
