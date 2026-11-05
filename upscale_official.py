from PIL import Image, ImageEnhance, ImageFilter

# Load cover_image.png
im = Image.open('static/images/cover_image.png')
w, h = im.size

# Target 4K landscape: 3840 x 2560 (or 3840 x 2160)
# cover_image aspect ratio is 1536 / 1024 = 1.5 (which is 3840 x 2560)
target_w = 3840
target_h = int(target_w * h / w) # 2560

# High quality Lanczos resize
im_4k = im.resize((target_w, target_h), Image.Resampling.LANCZOS)

# Subtle unsharp mask to ensure text and lines are razor sharp
im_sharp = im_4k.filter(ImageFilter.UnsharpMask(radius=1.5, percent=120, threshold=3))

# Save PNG and JPG
im_sharp.save('static/images/executive_infographic_naama_official_4k.png')
im_sharp.convert('RGB').save('static/images/executive_infographic_naama_official_4k.jpg', quality=98)
print(f"Saved 4K official infographic: {im_sharp.size}")
