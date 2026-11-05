from PIL import Image
import os

im = Image.open('static/images/slide_official_hd.png')
w, h = im.size
print(f"Image dimensions: {w}x{h}")

# Let's crop key assets so we can reuse them seamlessly:
# 1. Farm photo (roughly in the left third, middle)
# 2. Cart photo (center card)
# 3. Admin photo (right card)
# 4. Central circular hub
# 5. Bottom panoramic farm & truck banner (bottom 20%)

# In slide_official_hd.png (3072 x 2046):
# Header: 0 to ~350 px
# Cards: ~350 to ~1300 px
# Bottom banner: ~1650 to 2046 px

# Let's save a crop of the bottom panorama (farm landscape with truck)
bottom_crop = im.crop((0, int(h * 0.82), w, h))
bottom_crop.save('static/images/asset_bottom_banner.png')
print("Saved bottom banner crop:", bottom_crop.size)

# Let's crop the central medallion
# Center is at x = 1536, y roughly around 600-800
# Let's find the circle
circle_crop = im.crop((int(w * 0.38), int(h * 0.16), int(w * 0.62), int(h * 0.44)))
circle_crop.save('static/images/asset_center_hub.png')
print("Saved center hub crop:", circle_crop.size)

# Farm photo crop
farm_crop = im.crop((int(w * 0.05), int(h * 0.22), int(w * 0.19), int(h * 0.52)))
farm_crop.save('static/images/asset_farm_photo.png')
print("Saved farm crop:", farm_crop.size)

# Cart photo crop
cart_crop = im.crop((int(w * 0.34), int(h * 0.45), int(w * 0.45), int(h * 0.62)))
cart_crop.save('static/images/asset_cart_photo.png')
print("Saved cart crop:", cart_crop.size)

# Admin photo crop
admin_crop = im.crop((int(w * 0.66), int(h * 0.22), int(w * 0.81), int(h * 0.53)))
admin_crop.save('static/images/asset_admin_photo.png')
print("Saved admin crop:", admin_crop.size)
