import os
import subprocess
from PIL import Image

# Ensure static/images paths exist and are absolute or relative
html_content = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<title>المنصة الوطنية لأسواق النفع العام</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&family=Tajawal:wght@400;500;700;800;900&display=swap" rel="stylesheet">
<style>
* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    -webkit-font-smoothing: antialiased;
}
body {
    width: 2560px;
    height: 1440px;
    overflow: hidden;
    background: #f4f6f8;
    font-family: 'Cairo', 'Tajawal', 'Segoe UI', Tahoma, sans-serif;
    color: #1e293b;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

/* Header */
.header {
    background: #ffffff;
    height: 190px;
    padding: 16px 48px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 3px solid #e2e8f0;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
    position: relative;
    z-index: 20;
}
.header-right {
    display: flex;
    align-items: center;
    gap: 24px;
}
.header-right img.mewa {
    height: 80px;
}
.header-right img.naama {
    height: 75px;
}
.header-right .tagline {
    font-size: 17px;
    font-weight: 700;
    color: #015738;
    border-right: 2px solid #cbd5e1;
    padding-right: 18px;
    line-height: 1.4;
}
.header-center {
    text-align: center;
    flex: 1;
    max-width: 1400px;
    margin: 0 auto;
}
.header-center h1 {
    font-size: 40px;
    font-weight: 900;
    color: #015738;
    letter-spacing: -0.5px;
    margin-bottom: 4px;
}
.header-center .sub-gold {
    font-size: 24px;
    font-weight: 800;
    color: #b8860b;
    margin-bottom: 6px;
}
.header-center p {
    font-size: 16px;
    font-weight: 600;
    color: #475569;
    line-height: 1.4;
}
.header-left {
    display: flex;
    align-items: center;
    gap: 20px;
}
.header-left img.v2030 {
    height: 80px;
}
.header-left .vision-text {
    font-size: 16px;
    font-weight: 700;
    color: #015738;
    border-left: 2px solid #cbd5e1;
    padding-left: 16px;
    line-height: 1.3;
}

/* Main Swimlanes Container */
.main-container {
    height: 850px;
    padding: 16px 40px;
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 28px;
    position: relative;
    z-index: 10;
}

/* Connecting Lines from Central Hub */
.hub-connector {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 260px;
    height: 260px;
    z-index: 30;
    pointer-events: none;
}
.hub-img {
    width: 100%;
    height: 100%;
    object-fit: contain;
    filter: drop-shadow(0 12px 25px rgba(0, 87, 56, 0.35));
}
.hub-badge {
    position: absolute;
    bottom: -18px;
    left: 50%;
    transform: translateX(-50%);
    background: #ffffff;
    border: 2px solid #015738;
    border-radius: 20px;
    padding: 6px 18px;
    white-space: nowrap;
    font-size: 15px;
    font-weight: 800;
    color: #015738;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

/* Swimlane Card */
.lane-card {
    background: #ffffff;
    border-radius: 24px;
    border: 2px solid #e2e8f0;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.05);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 18px 20px;
    position: relative;
    overflow: hidden;
}

/* Card Header Banner */
.lane-header {
    background: linear-gradient(135deg, #015738 0%, #004028 100%);
    border-radius: 18px;
    padding: 12px 20px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    color: #ffffff;
    margin-bottom: 14px;
    box-shadow: 0 4px 15px rgba(1, 87, 56, 0.2);
}
.lane-header .title-box {
    display: flex;
    align-items: center;
    gap: 14px;
}
.lane-header .icon-circle {
    width: 44px;
    height: 44px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.15);
    border: 1.5px solid rgba(255, 255, 255, 0.3);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
}
.lane-header h2 {
    font-size: 21px;
    font-weight: 800;
    letter-spacing: -0.2px;
}
.lane-header .subtitle {
    font-size: 13px;
    font-weight: 500;
    color: #a7f3d0;
}

/* Card Body: Photo + Steps */
.lane-body {
    display: flex;
    gap: 16px;
    flex: 1;
}
.lane-photo-container {
    width: 200px;
    border-radius: 16px;
    overflow: hidden;
    position: relative;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    border: 1.5px solid #e2e8f0;
    display: flex;
    flex-direction: column;
}
.lane-photo-container img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}
.lane-photo-overlay {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    background: linear-gradient(to top, rgba(1, 87, 56, 0.95), rgba(1, 87, 56, 0.4) 70%, transparent);
    color: #ffffff;
    padding: 12px 10px;
    font-size: 13px;
    font-weight: 700;
    text-align: center;
    line-height: 1.3;
}

/* Steps Stack */
.steps-stack {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    gap: 6px;
}
.step-item {
    background: #f8fafc;
    border: 1.5px solid #e2e8f0;
    border-radius: 12px;
    padding: 7px 14px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    transition: all 0.15s ease;
}
.step-item:hover {
    border-color: #015738;
    background: #f0fdf4;
}
.step-item .step-text {
    font-size: 15px;
    font-weight: 700;
    color: #1e293b;
    display: flex;
    align-items: center;
    gap: 10px;
}
.step-item .step-num {
    width: 26px;
    height: 26px;
    border-radius: 50%;
    background: #015738;
    color: #ffffff;
    font-size: 13px;
    font-weight: 800;
    display: flex;
    align-items: center;
    justify-content: center;
}
.step-item .step-icon {
    font-size: 16px;
    color: #015738;
}

/* Outcome Bar */
.outcome-bar {
    margin-top: 12px;
    background: #f8fafc;
    border: 2px solid #b8860b;
    border-radius: 16px;
    padding: 10px 16px;
    display: flex;
    flex-direction: column;
    gap: 6px;
}
.outcome-title {
    font-size: 14px;
    font-weight: 800;
    color: #b8860b;
    display: flex;
    align-items: center;
    gap: 6px;
}
.outcome-chips {
    display: flex;
    gap: 8px;
    justify-content: space-between;
}
.outcome-chip {
    flex: 1;
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 10px;
    padding: 6px 8px;
    font-size: 12.5px;
    font-weight: 700;
    color: #015738;
    text-align: center;
    box-shadow: 0 2px 5px rgba(0,0,0,0.03);
}

/* Shared Services Dock */
.services-dock {
    height: 85px;
    background: #ffffff;
    margin: 0 40px;
    border-radius: 20px;
    border: 2px solid #e2e8f0;
    box-shadow: 0 4px 20px rgba(0,0,0,0.04);
    display: flex;
    align-items: center;
    padding: 0 24px;
    gap: 20px;
    position: relative;
    z-index: 15;
}
.dock-label {
    background: #015738;
    color: #ffffff;
    padding: 10px 20px;
    border-radius: 14px;
    font-size: 16px;
    font-weight: 800;
    white-space: nowrap;
    display: flex;
    align-items: center;
    gap: 8px;
}
.dock-capsules {
    display: flex;
    flex: 1;
    justify-content: space-between;
    gap: 14px;
}
.dock-capsule {
    flex: 1;
    background: #f8fafc;
    border: 1.5px solid #cbd5e1;
    border-radius: 12px;
    padding: 10px 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    font-size: 15px;
    font-weight: 700;
    color: #1e293b;
    box-shadow: 0 2px 6px rgba(0,0,0,0.02);
}
.dock-capsule .cap-icon {
    font-size: 18px;
    color: #015738;
}

/* Footer Banner */
.footer-banner {
    height: 150px;
    position: relative;
    background: url('static/images/asset_bottom_banner.png') center/cover no-repeat;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 16px 48px;
    color: #ffffff;
    border-top: 3px solid #b8860b;
}
.footer-top {
    text-align: center;
}
.footer-top h3 {
    font-size: 26px;
    font-weight: 900;
    text-shadow: 0 2px 8px rgba(0,0,0,0.7);
    margin-bottom: 2px;
}
.footer-top p {
    font-size: 16px;
    font-weight: 700;
    color: #a7f3d0;
    text-shadow: 0 2px 6px rgba(0,0,0,0.7);
}
.footer-pillars {
    display: flex;
    justify-content: center;
    gap: 60px;
    background: rgba(1, 40, 25, 0.65);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 14px;
    padding: 8px 32px;
    max-width: 900px;
    margin: 0 auto;
}
.pillar-item {
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 17px;
    font-weight: 800;
    color: #ffffff;
}
.pillar-item span.icon {
    font-size: 22px;
}
</style>
</head>
<body>

    <!-- 1. HEADER -->
    <header class="header">
        <!-- MEWA & NAAMA LOGOS (Right side in RTL) -->
        <div class="header-right">
            <img class="mewa" src="static/images/mewa_logo_hd.png" alt="وزارة البيئة والمياه والزراعة">
            <img class="naama" src="static/images/naama_logo_hd.png" alt="منصة نما">
            <div class="tagline">
                وزارة البيئة والمياه والزراعة<br>
                <span style="color:#2e7d32; font-weight:600;">نماء .. لمستقبل مستدام</span>
            </div>
        </div>

        <!-- CENTER TITLE & NARRATIVE -->
        <div class="header-center">
            <h1>المنصة الوطنية لأسواق النفع العام</h1>
            <div class="sub-gold">واجهة ذكية موحدة لخدمة جميع المستفيدين</div>
            <p>منصة رقمية وطنية موحدة لإدارة وتنظيم وتشغيل أسواق النفع العام، تربط المنتجين والمزارع ومراكز الخدمة والمستهلكين والجهات الإشرافية ضمن منظومة رقمية متكاملة للحوكمة والتشغيل والرقابة.</p>
        </div>

        <!-- VISION 2030 (Left side in RTL) -->
        <div class="header-left">
            <div class="vision-text">
                مستقبل مستدام<br>
                لبيئة مزدهرة
            </div>
            <img class="v2030" src="static/images/asset_v2030_logo.png" alt="رؤية السعودية 2030">
        </div>
    </header>

    <!-- 2. MAIN 3 PARALLEL SWIMLANES -->
    <main class="main-container">

        <!-- CENTRAL OVERLAPPING MEDALLION -->
        <div class="hub-connector">
            <img class="hub-img" src="static/images/asset_center_hub.png" alt="منصة أسواق النفع العام">
            <div class="hub-badge">🛡️ الدخول الموحد عبر نفاذ</div>
        </div>

        <!-- ================= LANE 1: SELLER / FARMER / SERVICE CENTER ================= -->
        <section class="lane-card">
            <!-- Header -->
            <div class="lane-header">
                <div class="title-box">
                    <div class="icon-circle">🌾</div>
                    <div>
                        <h2>البائع / المزرعة / مركز الخدمة</h2>
                        <div class="subtitle">من المنتج إلى السوق .. بخطوات أسهل</div>
                    </div>
                </div>
            </div>

            <!-- Body: Photo + Steps -->
            <div class="lane-body">
                <div class="lane-photo-container">
                    <img src="static/images/asset_farm_photo.png" alt="المزارع والمنتج">
                    <div class="lane-photo-overlay">ندعم منتجاتك لنصل بها إلى كافة الأسواق</div>
                </div>

                <div class="steps-stack">
                    <div class="step-item">
                        <div class="step-text"><span class="step-num">1</span> التسجيل والاعتماد</div>
                        <span class="step-icon">📋</span>
                    </div>
                    <div class="step-item">
                        <div class="step-text"><span class="step-num">2</span> إضافة المنتجات</div>
                        <span class="step-icon">📦</span>
                    </div>
                    <div class="step-item">
                        <div class="step-text"><span class="step-num">3</span> إدارة المخزون</div>
                        <span class="step-icon">🏢</span>
                    </div>
                    <div class="step-item">
                        <div class="step-text"><span class="step-num">4</span> استقبال الطلبات</div>
                        <span class="step-icon">🔔</span>
                    </div>
                    <div class="step-item">
                        <div class="step-text"><span class="step-num">5</span> تجهيز الطلبات</div>
                        <span class="step-icon">⚙️</span>
                    </div>
                    <div class="step-item">
                        <div class="step-text"><span class="step-num">6</span> التسليم والشحن</div>
                        <span class="step-icon">🚚</span>
                    </div>
                    <div class="step-item">
                        <div class="step-text"><span class="step-num">7</span> استلام المستحقات</div>
                        <span class="step-icon">💳</span>
                    </div>
                    <div class="step-item">
                        <div class="step-text"><span class="step-num">8</span> التقارير والإحصائيات</div>
                        <span class="step-icon">📊</span>
                    </div>
                </div>
            </div>

            <!-- Outcome Bar -->
            <div class="outcome-bar">
                <div class="outcome-title">🎯 القيمة المحققة للبائع والمزرعة:</div>
                <div class="outcome-chips">
                    <div class="outcome-chip">📈 زيادة المبيعات</div>
                    <div class="outcome-chip">📦 تحسين إدارة المخزون</div>
                    <div class="outcome-chip">⚡ تسريع دورة التوريد</div>
                </div>
            </div>
        </section>

        <!-- ================= LANE 2: CONSUMER ================= -->
        <section class="lane-card">
            <!-- Header -->
            <div class="lane-header" style="background: linear-gradient(135deg, #026b45 0%, #014e32 100%);">
                <div class="title-box">
                    <div class="icon-circle">🛒</div>
                    <div>
                        <h2>المستهلك</h2>
                        <div class="subtitle">منتجات وطنية موثوقة .. بين يديك</div>
                    </div>
                </div>
            </div>

            <!-- Body: Photo + Steps -->
            <div class="lane-body">
                <div class="lane-photo-container">
                    <img src="static/images/asset_cart_photo.png" alt="تسوق المستهلك">
                    <div class="lane-photo-overlay">منتجات وطنية طازجة بجودة عالية وأسعار عادلة</div>
                </div>

                <div class="steps-stack">
                    <div class="step-item">
                        <div class="step-text"><span class="step-num">1</span> استعراض الأسواق</div>
                        <span class="step-icon">🏪</span>
                    </div>
                    <div class="step-item">
                        <div class="step-text"><span class="step-num">2</span> البحث عن المنتجات</div>
                        <span class="step-icon">🔍</span>
                    </div>
                    <div class="step-item">
                        <div class="step-text"><span class="step-num">3</span> إضافة للسلة</div>
                        <span class="step-icon">🛍️</span>
                    </div>
                    <div class="step-item">
                        <div class="step-text"><span class="step-num">4</span> الدفع الإلكتروني</div>
                        <span class="step-icon">💳</span>
                    </div>
                    <div class="step-item">
                        <div class="step-text"><span class="step-num">5</span> متابعة الطلب</div>
                        <span class="step-icon">📍</span>
                    </div>
                    <div class="step-item">
                        <div class="step-text"><span class="step-num">6</span> استلام المنتج</div>
                        <span class="step-icon">📦</span>
                    </div>
                    <div class="step-item">
                        <div class="step-text"><span class="step-num">7</span> التقييم والملاحظات</div>
                        <span class="step-icon">⭐</span>
                    </div>
                    <!-- Extra space filler to match height -->
                    <div class="step-item" style="background:#f0fdf4; border-color:#86efac;">
                        <div class="step-text" style="color:#015738;"><span class="step-num" style="background:#16a34a;">✓</span> ضمان جودة وسلامة الغذاء</div>
                        <span class="step-icon">🛡️</span>
                    </div>
                </div>
            </div>

            <!-- Outcome Bar -->
            <div class="outcome-bar" style="border-color:#015738;">
                <div class="outcome-title" style="color:#015738;">🎯 القيمة المحققة للمستهلك:</div>
                <div class="outcome-chips">
                    <div class="outcome-chip">🛡️ شراء موثوق</div>
                    <div class="outcome-chip">✨ تجربة سهلة</div>
                    <div class="outcome-chip">🚀 وصول أسرع للمنتجات</div>
                </div>
            </div>
        </section>

        <!-- ================= LANE 3: SYSTEM ADMINISTRATOR ================= -->
        <section class="lane-card">
            <!-- Header -->
            <div class="lane-header" style="background: linear-gradient(135deg, #004d2c 0%, #01331d 100%);">
                <div class="title-box">
                    <div class="icon-circle">📊</div>
                    <div>
                        <h2>مدير النظام والرقابة</h2>
                        <div class="subtitle">إدارة شاملة .. وحوكمة أسواق أكثر كفاءة</div>
                    </div>
                </div>
            </div>

            <!-- Body: Photo + Steps -->
            <div class="lane-body">
                <div class="lane-photo-container">
                    <img src="static/images/asset_admin_photo.png" alt="غرفة العمليات المركزية">
                    <div class="lane-photo-overlay">رؤية مركزية شاملة لإدارة وحوكمة المنظومة</div>
                </div>

                <div class="steps-stack">
                    <div class="step-item">
                        <div class="step-text"><span class="step-num">1</span> استقبال الطلبات</div>
                        <span class="step-icon">📥</span>
                    </div>
                    <div class="step-item">
                        <div class="step-text"><span class="step-num">2</span> مراجعة البيانات</div>
                        <span class="step-icon">🔍</span>
                    </div>
                    <div class="step-item">
                        <div class="step-text"><span class="step-num">3</span> اعتماد الأنشطة</div>
                        <span class="step-icon">✅</span>
                    </div>
                    <div class="step-item">
                        <div class="step-text"><span class="step-num">4</span> إدارة المستخدمين</div>
                        <span class="step-icon">👥</span>
                    </div>
                    <div class="step-item">
                        <div class="step-text"><span class="step-num">5</span> متابعة العمليات</div>
                        <span class="step-icon">⚙️</span>
                    </div>
                    <div class="step-item">
                        <div class="step-text"><span class="step-num">6</span> معالجة النزاعات</div>
                        <span class="step-icon">⚖️</span>
                    </div>
                    <div class="step-item">
                        <div class="step-text"><span class="step-num">7</span> الرقابة والحوكمة</div>
                        <span class="step-icon">🛡️</span>
                    </div>
                    <div class="step-item">
                        <div class="step-text"><span class="step-num">8</span> المؤشرات والتقارير</div>
                        <span class="step-icon">📈</span>
                    </div>
                </div>
            </div>

            <!-- Outcome Bar -->
            <div class="outcome-bar">
                <div class="outcome-title">🎯 القيمة المحققة للمنظومة والوزارة:</div>
                <div class="outcome-chips">
                    <div class="outcome-chip">📋 امتثال أعلى</div>
                    <div class="outcome-chip">👁️ رقابة أفضل</div>
                    <div class="outcome-chip">🏛️ حوكمة فعالة</div>
                </div>
            </div>
        </section>

    </main>

    <!-- 3. BOTTOM SHARED SERVICES LAYER -->
    <div class="services-dock">
        <div class="dock-label">
            <span>⚙️</span>
            <span>الخدمات المشتركة</span>
        </div>
        <div class="dock-capsules">
            <div class="dock-capsule"><span class="cap-icon">🛡️</span> نفاذ الوطني</div>
            <div class="dock-capsule"><span class="cap-icon">🔑</span> إدارة الصلاحيات</div>
            <div class="dock-capsule"><span class="cap-icon">🔔</span> منظومة الإشعارات</div>
            <div class="dock-capsule"><span class="cap-icon">💳</span> المدفوعات الإلكترونية</div>
            <div class="dock-capsule"><span class="cap-icon">📍</span> التتبع واللوجستيات</div>
            <div class="dock-capsule"><span class="cap-icon">📊</span> التقارير والتحليلات</div>
        </div>
    </div>

    <!-- 4. FOOTER BANNER -->
    <footer class="footer-banner">
        <div class="footer-top">
            <h3>منصة واحدة • ثلاث رحلات مترابطة • قيمة مستدامة للقطاع الزراعي</h3>
            <p>معاً لأسواق نفع عام أكثر كفاءة وازدهاراً واستدامة ضمن رؤية السعودية 2030</p>
        </div>
        <div class="footer-pillars">
            <div class="pillar-item"><span class="icon">🌱</span> أمن غذائي مستدام</div>
            <div class="pillar-item"><span class="icon">🏪</span> أسواق أكثر كفاءة</div>
            <div class="pillar-item"><span class="icon">📈</span> اقتصاد مزدهر</div>
        </div>
    </footer>

</body>
</html>
"""

html_path = os.path.abspath("infographic_naama_master.html")
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print("Generated infographic_naama_master.html")

# Render to 4K / 2560x1440 image using Chrome headless!
chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
out_img = os.path.abspath(r"static\images\executive_infographic_naama_4k.png")

cmd = [
    chrome_path,
    "--headless",
    "--disable-gpu",
    "--window-size=2560,1440",
    f"--screenshot={out_img}",
    "--virtual-time-budget=5000",
    f"file:///{html_path.replace(os.sep, '/')}"
]

print("Rendering high-res infographic with Chrome headless...")
res = subprocess.run(cmd, capture_output=True)
print("Chrome finished with exit code:", res.returncode)

if os.path.exists(out_img):
    im = Image.open(out_img)
    print("SUCCESS! Output image size:", im.size)
    # Also save a high quality JPG
    im.convert("RGB").save(r"static\images\executive_infographic_naama_master.jpg", quality=95)
    print("Saved executive_infographic_naama_master.jpg")
else:
    print("Failed to produce image.")
