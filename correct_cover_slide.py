import os
import subprocess
from PIL import Image

# Let's inspect the dimensions of cover_image.png: 1536 x 1024
# We can do this at 2x resolution: 3072 x 2048, or at native 1536 x 1024!
# Let's write an HTML page where the base is cover_image.png,
# and we overlay corrected patches with perfect Arabic typography!

html_content = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@600;700;800;900&family=Tajawal:wght@500;700;800;900&display=swap" rel="stylesheet">
<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}
body {
    width: 1536px;
    height: 1024px;
    overflow: hidden;
    position: relative;
    background: #ffffff;
    font-family: 'Tajawal', 'Cairo', sans-serif;
    -webkit-font-smoothing: antialiased;
}
.bg-slide {
    position: absolute;
    top: 0;
    left: 0;
    width: 1536px;
    height: 1024px;
    z-index: 1;
}

/* ================= 1. PATCH FOR MAIN DESCRIPTION ================= */
/* The patch covers y: 78px to 154px, x: 200px to 1336px */
.desc-patch {
    position: absolute;
    top: 78px;
    left: 200px;
    width: 1136px;
    height: 76px;
    z-index: 10;
    background: linear-gradient(to bottom, #f3f6f9 0%, #edf2f6 100%);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 2px 10px;
}
.desc-patch .line-gold {
    font-size: 17px;
    font-weight: 800;
    color: #a27411;
    margin-bottom: 3px;
    letter-spacing: -0.2px;
}
.desc-patch .line-navy {
    font-size: 14.5px;
    font-weight: 700;
    color: #102a43;
    line-height: 1.45;
}

/* ================= 2. PATCH FOR SECTION SUBHEADER ================= */
/* Covers y: 184px to 212px, x: 380px to 1156px ("من التسجيل وحتى...") */
.subhead-patch {
    position: absolute;
    top: 185px;
    left: 400px;
    width: 736px;
    height: 26px;
    z-index: 10;
    background: #edf3f7;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
}
.subhead-patch p {
    font-size: 13.5px;
    font-weight: 700;
    color: #1e3a5f;
}

/* ================= 3. PATCH FOR SELLER OUTCOME TYPO ================= */
/* Fixes "تسريع دورة لتورة التوريد" -> "تسريع دورة التوريد" */
/* In Seller outcome box (left side in image layout): x: 55px to 120px, y: 720px to 746px */
.seller-outcome-patch {
    position: absolute;
    top: 718px;
    left: 60px;
    width: 80px;
    height: 28px;
    z-index: 10;
    background: #eef6f3;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
}
.seller-outcome-patch span {
    font-size: 12px;
    font-weight: 800;
    color: #015738;
    line-height: 1.2;
}

/* ================= 4. PATCH FOR ADMIN OUTCOME TYPO ================= */
/* Fixes "امتثال أعلي" -> "امتثال أعلى" */
/* x: 1370px to 1435px, y: 720px to 742px */
.admin-outcome-patch {
    position: absolute;
    top: 720px;
    left: 1370px;
    width: 65px;
    height: 22px;
    z-index: 10;
    background: #faf6eb;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
}
.admin-outcome-patch span {
    font-size: 12.5px;
    font-weight: 800;
    color: #015738;
}

</style>
</head>
<body>

    <!-- Base Official Slide -->
    <img src="static/images/cover_image.png" class="bg-slide" alt="المنصة الوطنية لأسواق النفع العام">

    <!-- 1. Corrected Description -->
    <div class="desc-patch">
        <div class="line-gold">منصة رقمية وطنية موحدة لإدارة وتنظيم وتشغيل أسواق النفع العام،</div>
        <div class="line-navy">تربط المنتجين والمزارع ومراكز الخدمة والمستهلكين والجهات الإشرافية ضمن منظومة رقمية متكاملة للحوكمة والتشغيل والرقابة، بما يعزز الشفافية ويرفع كفاءة الأسواق ويسهم في دعم الأمن الغذائي واستدامة القطاع الزراعي.</div>
    </div>

    <!-- 2. Corrected Subheader -->
    <div class="subhead-patch">
        <p>من التسجيل وحتى إتمام العمليات التشغيلية والخدمية لكل فئة من المستفيدين</p>
    </div>

    <!-- 3. Corrected Seller Outcome -->
    <div class="seller-outcome-patch">
        <span>تسريع دورة<br>التوريد</span>
    </div>

    <!-- 4. Corrected Admin Outcome -->
    <div class="admin-outcome-patch">
        <span>امتثال أعلى</span>
    </div>

</body>
</html>
"""

html_path = os.path.abspath("patch_cover_slide.html")
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print("Saved patch_cover_slide.html")

chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
out_img = os.path.abspath(r"static\images\cover_image_corrected.png")

cmd = [
    chrome_path,
    "--headless",
    "--disable-gpu",
    "--window-size=1536,1024",
    f"--screenshot={out_img}",
    "--virtual-time-budget=4000",
    f"file:///{html_path.replace(os.sep, '/')}"
]

print("Rendering corrected cover image...")
res = subprocess.run(cmd, capture_output=True)
print("Chrome exit code:", res.returncode)

if os.path.exists(out_img):
    im = Image.open(out_img)
    print("SUCCESS! Output image size:", im.size)
    # Also save as JPEG
    im.convert("RGB").save(r"static\images\cover_image_corrected.jpg", quality=98)
    print("Saved cover_image_corrected.jpg")
