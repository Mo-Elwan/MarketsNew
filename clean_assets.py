from PIL import Image, ImageDraw, ImageFilter
import os

im = Image.open('static/images/slide_official_hd.png')
w, h = im.size

# 1. Clean Farm Photo:
# In slide_official_hd.png, the farm greenhouse photo is between y: 480 and 1100, x: 120 and 520
farm = im.crop((140, 480, 520, 1100))
farm.save('static/images/clean_farm_photo.png')
print("Saved clean_farm_photo.png:", farm.size)

# 2. Clean Cart / Mobile Photo:
# The phone showing vegetables is between y: 560 and 1120, x: 1040 and 1380
cart = im.crop((1045, 560, 1375, 1120))
cart.save('static/images/clean_cart_photo.png')
print("Saved clean_cart_photo.png:", cart.size)

# 3. Clean Admin Photo:
# The operator with screens is between y: 460 and 1100, x: 2060 and 2490
admin = im.crop((2060, 460, 2480, 1100))
admin.save('static/images/clean_admin_photo.png')
print("Saved clean_admin_photo.png:", admin.size)

# 4. Clean Bottom Banner:
# The landscape is from y: 1680 to 2046
banner = im.crop((0, 1680, w, 2046)).convert("RGBA")
# Let's cover the old text in the upper half of the banner with a beautiful dark green gradient
bw, bh = banner.size
overlay = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
draw = ImageDraw.Draw(overlay)

# Fill top portion with solid/semi-transparent green matching the dark green (#004028)
for y in range(int(bh * 0.55)):
    alpha = int(240 * (1 - (y / (bh * 0.55)) * 0.3))
    draw.line([(0, y), (bw, y)], fill=(1, 64, 40, alpha))

banner = Image.alpha_composite(banner, overlay)
banner.save('static/images/clean_bottom_banner.png')
print("Saved clean_bottom_banner.png:", banner.size)

# 5. Extract circular medallion with transparent background:
# Center hub in slide_official_hd.png is roughly at center: x ~ 1536 (wait, in RTL, center is at x ~ 1536)
# Let's find the exact circle
# In slide_official_hd.png, width is 3072. Center is 1536.
# Let's crop a square around the center hub:
cx, cy, radius = 1536, 615, 260
circle_box = (cx - radius, cy - radius, cx + radius, cy + radius)
medallion = im.crop(circle_box).convert("RGBA")

# Create a circular mask
mask = Image.new("L", medallion.size, 0)
mask_draw = ImageDraw.Draw(mask)
mask_draw.ellipse((8, 8, medallion.size[0] - 8, medallion.size[1] - 8), fill=255)
medallion.putalpha(mask)
medallion.save('static/images/clean_center_hub.png')
print("Saved clean_center_hub.png:", medallion.size)
