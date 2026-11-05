from PIL import Image, ImageDraw

im = Image.open('static/images/slide_official_hd.png')
w, h = im.size

# Bottom banner is from y: 1680 to 2046 (height 366)
banner = im.crop((0, 1680, w, 2046)).convert("RGBA")
bw, bh = banner.size

# Draw completely solid dark green over the old text (y: 0 to 180)
# and smooth fade into the green lawn / trees below
overlay = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
draw = ImageDraw.Draw(overlay)

# Fill top portion with solid green #014327
for y in range(int(bh * 0.52)):
    draw.line([(0, y), (bw, y)], fill=(1, 67, 39, 255))

# Smooth fade from y = bh * 0.52 to bh * 0.70
fade_start = int(bh * 0.52)
fade_end = int(bh * 0.70)
for y in range(fade_start, fade_end):
    factor = 1.0 - ((y - fade_start) / (fade_end - fade_start))
    alpha = int(255 * factor)
    draw.line([(0, y), (bw, y)], fill=(1, 67, 39, alpha))

banner = Image.alpha_composite(banner, overlay)
banner.save('static/images/clean_bottom_banner.png')
print("Banner cleaned with 100% solid top!")
