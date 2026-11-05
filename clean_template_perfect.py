import os
import sys
from PIL import Image, ImageDraw, ImageFilter

sys.stdout.reconfigure(encoding='utf-8')

# Load the original pristine image
orig_path = r"C:\Users\admin\Downloads\Designer (4).png"
im = Image.open(orig_path).convert("RGBA")
w, h = im.size
print(f"Loaded Designer (4).png: {w}x{h}")

draw = ImageDraw.Draw(im)

# =========================================================================
# 1. TOP HEADER: Smooth, seamless sky inpainting between logos
# Logos: Vision 2030 (x: 20 to 180), MEWA & NAAMA (x: 1330 to 1520)
# Clear x: 180 to 1325, y: 12 to 215
# We can sample the vertical gradient from the clean sky on the left (x: 175)
# and right (x: 1330) and interpolate across the whole header!
# =========================================================================
print("Inpainting top header...")
for y in range(12, 215):
    # Left sky pixel at (175, y), Right sky pixel at (1330, y)
    p_left = im.getpixel((175, y))
    p_right = im.getpixel((1330, y))
    for x in range(180, 1325):
        factor = (x - 180) / (1325 - 180)
        r = int(p_left[0] * (1 - factor) + p_right[0] * factor)
        g = int(p_left[1] * (1 - factor) + p_right[1] * factor)
        b = int(p_left[2] * (1 - factor) + p_right[2] * factor)
        im.putpixel((x, y), (r, g, b, 255))

# Also clean the small texts under/beside logos:
# Beside Vision 2030: x: 155 to 178, y: 30 to 110
for y in range(30, 110):
    p = im.getpixel((150, y))
    for x in range(155, 179):
        im.putpixel((x, y), p)

# Beside/under MEWA: x: 1110 to 1330, y: 65 to 110
for y in range(65, 110):
    p = im.getpixel((1335, y))
    for x in range(1110, 1330):
        im.putpixel((x, y), p)

# =========================================================================
# 2. CARD HEADERS: Clear text, keep circular icon badges
# =========================================================================
print("Inpainting card headers...")
# Card 1 (Seller): Green pill at x: 45 to 518, y: 215 to 286.
# Icon circle is at x: 45 to 142.
# Clear x: 145 to 510, y: 224 to 282 with gradient matching header
for y in range(224, 282):
    p_green = im.getpixel((144, y))
    for x in range(145, 510):
        im.putpixel((x, y), p_green)

# Card 2 (Consumer): Blue pill at x: 560 to 982, y: 215 to 286.
# Icon circle is at x: 560 to 655.
# Clear x: 656 to 975, y: 224 to 282
for y in range(224, 282):
    p_blue = im.getpixel((654, y))
    for x in range(656, 975):
        im.putpixel((x, y), p_blue)

# Card 3 (Admin): Gold pill at x: 1015 to 1490, y: 215 to 286.
# Icon circle is at x: 1015 to 1115.
# Clear x: 1116 to 1482, y: 224 to 282
for y in range(224, 282):
    p_gold = im.getpixel((1114, y))
    for x in range(1116, 1482):
        im.putpixel((x, y), p_gold)

# =========================================================================
# 3. STEP PILLS: Clear text inside each step pill
# =========================================================================
print("Inpainting step pills...")

# --- Card 1 (Seller): 8 steps ---
# In Card 1: The step items are at x: 260 to 480.
# The number circle is at x ~ 276. The icon is at x ~ 478.
# The text is strictly between x: 295 and x: 460.
for step_idx in range(8):
    sy = int(292 + step_idx * 37.8)
    for y in range(sy + 3, sy + 33):
        # sample the pill background at (292, y)
        p_bg = im.getpixel((292, y))
        for x in range(295, 462):
            im.putpixel((x, y), p_bg)

# --- Card 2 (Consumer): 7 steps ---
# In Card 2: The phone photo is on left.
# The number circle is at x ~ 768. The icon is at x ~ 945.
# The text is strictly between x: 785 and x: 925.
for step_idx in range(7):
    sy = int(294 + step_idx * 42.6)
    for y in range(sy + 4, sy + 34):
        p_bg = im.getpixel((782, y))
        for x in range(785, 930):
            im.putpixel((x, y), p_bg)

# --- Card 3 (Admin): 8 steps ---
# In Card 3: The control room operator is on left.
# The number circle is at x ~ 1248. The icon is at x ~ 1450.
# The text is strictly between x: 1265 and x: 1435.
for step_idx in range(8):
    sy = int(292 + step_idx * 37.8)
    for y in range(sy + 3, sy + 33):
        p_bg = im.getpixel((1262, y))
        for x in range(1265, 1435):
            im.putpixel((x, y), p_bg)

# =========================================================================
# 4. OUTCOME BOXES: Clear badges and text inside chips
# =========================================================================
print("Inpainting outcome boxes...")
# Outcome top badges:
# Card 1 badge: x: 195 to 358, y: 622 to 646 (fill dark green)
for y in range(622, 646):
    p = im.getpixel((192, y))
    for x in range(195, 358):
        im.putpixel((x, y), p)

# Card 2 badge: x: 672 to 835, y: 622 to 646 (fill dark teal)
for y in range(622, 646):
    p = im.getpixel((668, y))
    for x in range(672, 835):
        im.putpixel((x, y), p)

# Card 3 badge: x: 1142 to 1305, y: 622 to 646 (fill dark olive)
for y in range(622, 646):
    p = im.getpixel((1138, y))
    for x in range(1142, 1305):
        im.putpixel((x, y), p)

# Outcome text under icons in Card 1 (x: 45 to 518, y: 676 to 740)
for y in range(676, 742):
    p1 = im.getpixel((46, y))
    for x in range(48, 175):
        im.putpixel((x, y), p1)
    for x in range(215, 345):
        im.putpixel((x, y), p1)
    for x in range(380, 510):
        im.putpixel((x, y), p1)

# Outcome text under icons in Card 2 (x: 560 to 982, y: 676 to 740)
for y in range(676, 742):
    p2 = im.getpixel((562, y))
    for x in range(570, 680):
        im.putpixel((x, y), p2)
    for x in range(715, 825):
        im.putpixel((x, y), p2)
    for x in range(860, 970):
        im.putpixel((x, y), p2)

# Outcome text under icons in Card 3 (x: 1015 to 1490, y: 676 to 740)
for y in range(676, 742):
    p3 = im.getpixel((1018, y))
    for x in range(1030, 1160):
        im.putpixel((x, y), p3)
    for x in range(1190, 1315):
        im.putpixel((x, y), p3)
    for x in range(1345, 1475):
        im.putpixel((x, y), p3)

# =========================================================================
# 5. SHARED SERVICES DOCK: Clear dock badge and text under capsules
# =========================================================================
print("Inpainting shared services dock...")
# Dock badge: x: 560 to 975, y: 760 to 790
for y in range(760, 792):
    p_dock = im.getpixel((555, y))
    for x in range(560, 975):
        im.putpixel((x, y), p_dock)

# Text under icons in dock: y: 835 to 876
for y in range(835, 876):
    p_wh = im.getpixel((55, y))
    for x in range(55, 1480):
        im.putpixel((x, y), p_wh)

# Big "نفاذ" text: x: 80 to 185, y: 798 to 836
for y in range(798, 836):
    p_wh = im.getpixel((75, y))
    for x in range(80, 185):
        im.putpixel((x, y), p_wh)

# =========================================================================
# 6. FOOTER BANNER: Clear headline and pillar texts
# =========================================================================
print("Inpainting footer banner...")
# Headline: y: 898 to 938, x: 280 to 1250
for y in range(898, 938):
    p_foot = im.getpixel((275, y))
    for x in range(280, 1250):
        im.putpixel((x, y), p_foot)

# Pillars text (keep leaf, community, and chart icons!):
# Leaf text "أمن غذائي مستدام": x: 440 to 580, y: 950 to 988
# Community text "مجتمع حيوي": x: 670 to 800, y: 950 to 988
# Chart text "اقتصاد مزدهر": x: 890 to 1030, y: 950 to 988
for y in range(950, 988):
    p_f = im.getpixel((435, y))
    for x in range(440, 580):
        im.putpixel((x, y), p_f)
    for x in range(670, 800):
        im.putpixel((x, y), p_f)
    for x in range(890, 1030):
        im.putpixel((x, y), p_f)

# Save the final pristine blank template:
out_png = os.path.abspath("executive_template_blank.png")
im.save(out_png)
print("Saved executive_template_blank.png successfully!")

# Also save 4K version for high-res presentations
im_4k = im.resize((3840, 2560), Image.Resampling.LANCZOS)
im_4k.save(os.path.abspath("executive_template_blank_4k.png"))
im_4k.convert("RGB").save(os.path.abspath("executive_template_blank_4k.jpg"), quality=98)
print("Saved 4K versions successfully!")

# Save preview
thumb = im.resize((1024, int(1024 * h / w)))
thumb.convert("RGB").save("static/images/blank_preview_perfect.jpg", quality=95)
print("Saved blank_preview_perfect.jpg")
