from PIL import Image, ImageDraw
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Load the original pristine image
orig_path = r"C:\Users\admin\Downloads\Designer (4).png"
im = Image.open(orig_path).convert("RGBA")
w, h = im.size
print(f"Loaded image: {w}x{h}")

draw = ImageDraw.Draw(im)

# =========================================================================
# 1. TOP HEADER: Remove Title, Subtitle, Description, Section Title
# Logos: Vision 2030 (x: 20 to 180), MEWA & NAAMA (x: 1330 to 1520)
# So we can cleanly clear x: 190 to 1320, y: 15 to 215 with the sky gradient!
# =========================================================================
print("Clearing top header text...")
# Sample sky background colors from top to bottom
for y in range(15, 218):
    # interpolate color from y=15 (#fbfdfd) to y=215 (#edf3f7)
    factor = (y - 15) / (218 - 15)
    r = int(251 * (1 - factor) + 237 * factor)
    g = int(253 * (1 - factor) + 243 * factor)
    b = int(253 * (1 - factor) + 247 * factor)
    draw.line([(190, y), (1320, y)], fill=(r, g, b, 255), width=1)

# Also clear text on the left/right of logos if any:
# "مستقبل مستدام لبيئة مزدهرة" next to Vision 2030: x: 175 to 225, y: 30 to 110
# "بيئة .. غذاء .. حياة أفضل" / "نماء .. لمستقبل مستدام" under logos: x: 1100 to 1330, y: 70 to 100
for y in range(30, 115):
    draw.line([(160, y), (210, y)], fill=(248, 251, 253, 255), width=1)
for y in range(65, 110):
    draw.line([(1110, y), (1330, y)], fill=(248, 251, 253, 255), width=1)

# =========================================================================
# 2. CARD HEADERS: Clear text inside the top pills, keep icon circles
# =========================================================================
print("Clearing card header text...")
# Card 1 (Seller): Header pill is at x: 48 to 516, y: 220 to 286.
# Icon circle is at x: 48 to 140. Text is at x: 145 to 500, y: 228 to 280.
# Color is dark green #015738 -> RGB(1, 87, 56)
for y in range(226, 282):
    draw.line([(145, y), (500, y)], fill=(1, 87, 56, 255), width=1)

# Card 2 (Consumer): Header pill at x: 564 to 980, y: 220 to 286.
# Icon circle is at x: 564 to 650. Text is at x: 655 to 965, y: 228 to 280.
# Color is teal #026b45 -> RGB(2, 107, 69)
for y in range(226, 282):
    draw.line([(655, y), (965, y)], fill=(2, 107, 69, 255), width=1)

# Card 3 (Admin): Header pill at x: 1020 to 1488, y: 220 to 286.
# Icon circle is at x: 1020 to 1110. Text is at x: 1115 to 1475, y: 228 to 280.
# Color is gold/olive #a27411 -> RGB(162, 116, 17)
for y in range(226, 282):
    draw.line([(1115, y), (1475, y)], fill=(162, 116, 17, 255), width=1)

# =========================================================================
# 3. PHOTO OVERLAYS: Clear text over photos if any
# =========================================================================
# Card 1 Photo overlay at bottom: "من المنتج إلى السوق .. فرص أكبر"
# Let's inspect if there is text over the photos:
# In Card 1, photo is at x: 48 to 240, y: 290 to 600.
# In Card 3, photo is at x: 1020 to 1220, y: 290 to 600.

# =========================================================================
# 4. STEP PILLS: Clear text inside each step pill (8 steps per card)
# Inside Card 1 (Seller):
# Steps are at x: 250 to 515.
# Icon is at left (x: 480 to 510). Number is at right (x: 255 to 285).
# In between (x: 290 to 475) is the text!
# =========================================================================
print("Clearing step pills text...")
# In Card 1 (Seller): steps are 8 rows between y: 295 and 600
# Step pill background in Card 1: #f3faf6
card1_step_bg = (243, 250, 246, 255)
# Let's clean the text area inside each of the 8 steps:
# y ranges for each step roughly every 37px
for step_idx in range(8):
    sy = int(298 + step_idx * 37.8)
    for y in range(sy, sy + 28):
        draw.line([(300, y), (475, y)], fill=card1_step_bg, width=1)

# Card 2 (Consumer): 7 steps between y: 295 and 595
# Step pill background in Card 2: #f2f8fc
card2_step_bg = (242, 248, 252, 255)
for step_idx in range(7):
    sy = int(298 + step_idx * 42.5)
    for y in range(sy, sy + 30):
        draw.line([(705, y), (885, y)], fill=card2_step_bg, width=1)

# Card 3 (Admin): 8 steps between y: 295 and 600
# Step pill background in Card 3: #faf8f0
card3_step_bg = (250, 248, 240, 255)
for step_idx in range(8):
    sy = int(298 + step_idx * 37.8)
    for y in range(sy, sy + 28):
        draw.line([(1270, y), (1445, y)], fill=card3_step_bg, width=1)

# =========================================================================
# 5. OUTCOME BOXES: Clear text inside outcome boxes, keep container and icons
# =========================================================================
print("Clearing outcome boxes text...")
# "النتيجة للمستفيد" badges:
# Card 1 badge: x: 195 to 350, y: 622 to 644 (fill dark green #015738)
draw.rectangle([195, 622, 350, 644], fill=(1, 87, 56, 255))
# Card 2 badge: x: 675 to 830, y: 622 to 644 (fill dark teal #026b45)
draw.rectangle([675, 622, 830, 644], fill=(2, 107, 69, 255))
# Card 3 badge: x: 1145 to 1300, y: 622 to 644 (fill dark olive/green #014327)
draw.rectangle([1145, 622, 1300, 644], fill=(1, 67, 39, 255))

# Outcome items text:
# Card 1 items (3 slots):
# Background: #f2faf6
for y in range(676, 736):
    draw.line([(50, y), (170, y)], fill=(242, 250, 246, 255), width=1)
    draw.line([(220, y), (340, y)], fill=(242, 250, 246, 255), width=1)
    draw.line([(380, y), (500, y)], fill=(242, 250, 246, 255), width=1)

# Card 2 items (3 slots):
# Background: #f2f8fc
for y in range(676, 736):
    draw.line([(575, y), (675, y)], fill=(242, 248, 252, 255), width=1)
    draw.line([(720, y), (820, y)], fill=(242, 248, 252, 255), width=1)
    draw.line([(860, y), (960, y)], fill=(242, 248, 252, 255), width=1)

# Card 3 items (3 slots):
# Background: #faf7ee
for y in range(676, 736):
    draw.line([(1030, y), (1160, y)], fill=(250, 247, 238, 255), width=1)
    draw.line([(1190, y), (1310, y)], fill=(250, 247, 238, 255), width=1)
    draw.line([(1340, y), (1470, y)], fill=(250, 247, 238, 255), width=1)

# =========================================================================
# 6. SHARED SERVICES DOCK: Clear text under each icon
# Dock is at y: 760 to 885.
# Header pill "خدمات مشتركة تدعم جميع المستفيدين": x: 560 to 975, y: 760 to 790
# =========================================================================
print("Clearing shared services text...")
draw.rectangle([560, 760, 975, 790], fill=(1, 87, 56, 255))

# Text under icons in dock: y: 840 to 876
# Background is clean white/near-white: #fafcfb
for y in range(836, 876):
    draw.line([(60, y), (1476, y)], fill=(252, 254, 253, 255), width=1)

# Also clear the large bold "نفاذ" text above "نفاذ الوطني": x: 90 to 180, y: 800 to 836
for y in range(800, 836):
    draw.line([(90, y), (180, y)], fill=(252, 254, 253, 255), width=1)

# =========================================================================
# 7. FOOTER BANNER: Clear all text lines, keep landscape and pillars icons
# =========================================================================
print("Clearing footer banner text...")
# Main footer headline: "منصة واحدة • ثلاث رحلات مترابطة • قيمة مستدامة للقطاع الزراعي"
# y: 900 to 935, x: 300 to 1236
# Fill with the exact dark green #014327
for y in range(898, 938):
    draw.line([(280, y), (1250, y)], fill=(1, 67, 39, 255), width=1)

# Text of pillars:
# Leaf pillar text: "أمن غذائي مستدام" -> x: 440 to 580, y: 955 to 985
# Community pillar text: "مجتمع حيوي" -> x: 670 to 800, y: 955 to 985
# Economy pillar text: "اقتصاد مزدهر" -> x: 890 to 1020, y: 955 to 985
for y in range(952, 988):
    draw.line([(440, y), (580, y)], fill=(1, 67, 39, 255), width=1)
    draw.line([(670, y), (800, y)], fill=(1, 67, 39, 255), width=1)
    draw.line([(890, y), (1030, y)], fill=(1, 67, 39, 255), width=1)

# Text on the right market entrance: "أسواق النفع العام" over the building: x: 1370 to 1470, y: 895 to 925
# (we can leave building sign or clear it)

# Save the blank template
out_path = os.path.abspath("infographic_template_blank.png")
im.save(out_path)
print("Saved infographic_template_blank.png successfully!")

# Also save a preview
thumb = im.resize((1024, int(1024 * h / w)))
thumb.convert("RGB").save(os.path.abspath("static/images/blank_template_preview.jpg"), quality=95)
print("Saved blank_template_preview.jpg")
