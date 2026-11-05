import os
import sys
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding='utf-8')

# Load the pristine original image
orig_path = r"C:\Users\admin\Downloads\Designer (4).png"
im = Image.open(orig_path).convert("RGBA")
w, h = im.size
print(f"Loaded Designer (4).png: {w}x{h}")

draw = ImageDraw.Draw(im)

# =========================================================================
# 1. TOP HEADER: Smooth, seamless sky inpainting between logos
# Logos: Vision 2030 (x: 20 to 180), MEWA & NAAMA (x: 1328 to 1525)
# Inpaint x: 182 to 1324, y: 12 to 216
# =========================================================================
print("1. Inpainting top header...")
for y in range(12, 218):
    p_left = im.getpixel((178, y))
    p_right = im.getpixel((1326, y))
    for x in range(180, 1326):
        factor = (x - 180) / (1326 - 180)
        r = int(p_left[0] * (1 - factor) + p_right[0] * factor)
        g = int(p_left[1] * (1 - factor) + p_right[1] * factor)
        b = int(p_left[2] * (1 - factor) + p_right[2] * factor)
        im.putpixel((x, y), (r, g, b, 255))

# Clean small tagline beside Vision 2030: x: 156 to 179, y: 30 to 110
for y in range(30, 110):
    p = im.getpixel((152, y))
    for x in range(154, 180):
        im.putpixel((x, y), p)

# Clean small tagline under MEWA: x: 1115 to 1325, y: 70 to 105
for y in range(70, 105):
    p = im.getpixel((1330, y))
    for x in range(1115, 1326):
        im.putpixel((x, y), p)

# =========================================================================
# 2. CARD HEADERS: Clear text, keep circular icon badges
# =========================================================================
print("2. Inpainting card headers...")
# Card 1 (Seller): Green pill at x: 45 to 518, y: 215 to 286.
# Clear text at x: 142 to 510, y: 222 to 282
for y in range(222, 283):
    p_green = im.getpixel((138, y))
    for x in range(142, 512):
        im.putpixel((x, y), p_green)

# Card 2 (Consumer): Blue/teal pill at x: 560 to 982, y: 215 to 286.
# Clear text at x: 654 to 975, y: 222 to 282
for y in range(222, 283):
    p_blue = im.getpixel((650, y))
    for x in range(654, 976):
        im.putpixel((x, y), p_blue)

# Card 3 (Admin): Gold pill at x: 1015 to 1490, y: 215 to 286.
# Clear text at x: 1112 to 1482, y: 222 to 282
for y in range(222, 283):
    p_gold = im.getpixel((1108, y))
    for x in range(1112, 1484):
        im.putpixel((x, y), p_gold)

# =========================================================================
# 3. STEP PILLS: Clear text inside each step pill
# =========================================================================
print("3. Inpainting step pills...")

# --- Card 1 (Seller): 8 steps ---
# Card 1 base x = 45. Steps start at x = 45 + 250 = 295 to 45 + 420 = 465.
# Number badges on left (x ~ 276). Icons on right (x ~ 478).
for i in range(8):
    y0 = int(363 + i * 72.8 - 72.8) # 290, 363, 436...
    y1 = y0 + 44
    for y in range(y0, y1 + 1):
        f = (y - y0) / (y1 - y0)
        r = int(246 * (1 - f) + 228 * f)
        g = int(252 * (1 - f) + 240 * f)
        b = int(248 * (1 - f) + 234 * f)
        for x in range(300, 465):
            im.putpixel((x, y), (r, g, b, 255))

# --- Card 2 (Consumer): 7 steps ---
# Card 2 base x = 560. Number badge at x ~ 768. Icon at x ~ 945.
# Text is at x: 792 to 935.
for i in range(7):
    y0 = int(294 + i * 85.5)
    y1 = y0 + 44
    for y in range(y0, y1 + 1):
        f = (y - y0) / (y1 - y0)
        r = int(245 * (1 - f) + 230 * f)
        g = int(250 * (1 - f) + 242 * f)
        b = int(254 * (1 - f) + 250 * f)
        for x in range(792, 935):
            im.putpixel((x, y), (r, g, b, 255))

# --- Card 3 (Admin): 8 steps ---
# Card 3 base x = 1015. Number badge at x ~ 1248. Icon at x ~ 1450.
# Text is at x: 1272 to 1438.
for i in range(8):
    y0 = int(290 + i * 72.8)
    y1 = y0 + 44
    for y in range(y0, y1 + 1):
        f = (y - y0) / (y1 - y0)
        r = int(252 * (1 - f) + 244 * f)
        g = int(250 * (1 - f) + 242 * f)
        b = int(240 * (1 - f) + 232 * f)
        for x in range(1272, 1438):
            im.putpixel((x, y), (r, g, b, 255))

# =========================================================================
# 4. OUTCOME BOXES: Clear badges and outcome text
# =========================================================================
print("4. Inpainting outcome boxes...")
# Badges: "النتيجة للمستفيد"
# Card 1 badge: x: 195 to 358, y: 622 to 646
for y in range(622, 646):
    p = im.getpixel((192, y))
    for x in range(195, 358):
        im.putpixel((x, y), p)

# Card 2 badge: x: 672 to 835, y: 622 to 646
for y in range(622, 646):
    p = im.getpixel((668, y))
    for x in range(672, 835):
        im.putpixel((x, y), p)

# Card 3 badge: x: 1142 to 1305, y: 622 to 646
for y in range(622, 646):
    p = im.getpixel((1138, y))
    for x in range(1142, 1305):
        im.putpixel((x, y), p)

# Text under outcome icons:
# Card 1 (x: 48 to 175, 215 to 345, 380 to 510, y: 676 to 742)
for y in range(676, 742):
    p1 = im.getpixel((46, y))
    for x in range(48, 175): im.putpixel((x, y), p1)
    for x in range(215, 345): im.putpixel((x, y), p1)
    for x in range(380, 510): im.putpixel((x, y), p1)

# Card 2 (x: 570 to 680, 715 to 825, 860 to 970, y: 676 to 742)
for y in range(676, 742):
    p2 = im.getpixel((562, y))
    for x in range(570, 680): im.putpixel((x, y), p2)
    for x in range(715, 825): im.putpixel((x, y), p2)
    for x in range(860, 970): im.putpixel((x, y), p2)

# Card 3 (x: 1030 to 1160, 1190 to 1315, 1345 to 1475, y: 676 to 742)
for y in range(676, 742):
    p3 = im.getpixel((1018, y))
    for x in range(1030, 1160): im.putpixel((x, y), p3)
    for x in range(1190, 1315): im.putpixel((x, y), p3)
    for x in range(1345, 1475): im.putpixel((x, y), p3)

# =========================================================================
# 5. SHARED SERVICES DOCK: Clear badge and capsule texts
# =========================================================================
print("5. Inpainting shared services dock...")
# Dock badge: x: 558 to 975, y: 760 to 790
for y in range(760, 792):
    p_dock = im.getpixel((554, y))
    for x in range(558, 975):
        im.putpixel((x, y), p_dock)

# Text under icons in dock: y: 835 to 876
for y in range(835, 876):
    p_wh = im.getpixel((52, y))
    for x in range(52, 1480):
        im.putpixel((x, y), p_wh)

# Big "نفاذ" text: x: 80 to 185, y: 798 to 836
for y in range(798, 836):
    p_wh = im.getpixel((75, y))
    for x in range(80, 185):
        im.putpixel((x, y), p_wh)

# =========================================================================
# 6. FOOTER BANNER: Clear headline and pillar texts
# =========================================================================
print("6. Inpainting footer banner...")
# Headline: y: 896 to 938, x: 275 to 1250
for y in range(896, 938):
    p_foot = im.getpixel((270, y))
    for x in range(275, 1250):
        im.putpixel((x, y), p_foot)

# Pillars text (keep leaf, community, chart icons!):
for y in range(950, 988):
    p_f = im.getpixel((435, y))
    for x in range(440, 580): im.putpixel((x, y), p_f)
    for x in range(670, 800): im.putpixel((x, y), p_f)
    for x in range(890, 1030): im.putpixel((x, y), p_f)

# Save the professional blank template
out_png = os.path.abspath("executive_template_clean_pro.png")
im.save(out_png)
print("Saved executive_template_clean_pro.png successfully!")

# Save to project static/images as well
im.save(os.path.abspath("static/images/executive_template_clean_pro.png"))
im.convert("RGB").save(os.path.abspath("static/images/executive_template_clean_pro.jpg"), quality=98)

# Save 4K Ultra-HD version (3840 x 2560)
im_4k = im.resize((3840, 2560), Image.Resampling.LANCZOS)
im_4k.save(os.path.abspath("static/images/executive_template_clean_pro_4k.png"))
im_4k.convert("RGB").save(os.path.abspath("static/images/executive_template_clean_pro_4k.jpg"), quality=98)
print("Saved 4K versions successfully!")

# Save preview
thumb = im.resize((1024, int(1024 * h / w)))
thumb.convert("RGB").save("static/images/blank_pro_preview.jpg", quality=95)
print("Saved blank_pro_preview.jpg")
