from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import sqlite3
import os
import datetime
from database import get_connection

future_router = APIRouter(tags=["الوضع المستقبلي"])

# === نماذج البيانات (Pydantic Models) ===

class CreateLotRequest(BaseModel):
    farmer_name: str
    farmer_phone: str
    farm_name: str
    farm_location: str
    saudi_gap_cert: Optional[str] = "غير حاصل على شهادة"
    commodity: str
    category: str
    spoilage_tier: str
    quantity: float
    unit: str
    target_market: str
    scheduled_arrival: str
    image_url: Optional[str] = "https://images.unsplash.com/photo-1592924357228-91a4daadcfea?w=600&auto=format&fit=crop&q=80"

class SubmitAssayingRequest(BaseModel):
    lot_id: str
    inspector_name: str
    lab_name: str
    moisture_pct: float
    purity_pct: float
    defect_pct: float
    sugar_brix: Optional[float] = 0.0
    quality_grade: str # درجة ممتازة A, درجة أولى B, درجة ثانية C
    reference_price: float
    inspection_notes: Optional[str] = ""

class PlaceBidRequest(BaseModel):
    auction_id: str
    lot_id: str
    bidder_name: str
    bidder_org: str
    bidder_city: str
    bid_amount: float

class CreateDisputeRequest(BaseModel):
    lot_id: str
    escrow_no: str
    complainant_name: str
    complainant_role: str
    dispute_type: str
    description: str

class ResolveDisputeRequest(BaseModel):
    dispute_id: int
    decision: str # resolved_full_payout, resolved_partial_discount, resolved_refund
    committee_decision: str
    partial_discount_amount: Optional[float] = 0.0

class UpdateColdChainRequest(BaseModel):
    lot_id: str
    current_temp: float
    current_humidity: float
    temp_status: str
    current_location: str
    eta: str


# === واجهات الـ API للوضع المستقبلي ===

@future_router.get("/api/future/lots")
def get_future_lots(status: Optional[str] = None):
    conn = get_connection()
    if status:
        query = "SELECT * FROM future_lots WHERE status = ? ORDER BY id DESC"
        rows = conn.execute(query, (status,)).fetchall()
    else:
        query = "SELECT * FROM future_lots ORDER BY id DESC"
        rows = conn.execute(query).fetchall()
    
    result = []
    for r in rows:
        d = dict(r)
        # جلب الفحص المخبري إن وجد
        assay = conn.execute("SELECT * FROM future_assaying WHERE lot_id = ?", (d["lot_id"],)).fetchone()
        d["assaying"] = dict(assay) if assay else None
        
        # جلب المزاد إن وجد
        auction = conn.execute("SELECT * FROM future_auctions WHERE lot_id = ?", (d["lot_id"],)).fetchone()
        d["auction"] = dict(auction) if auction else None

        # جلب التتبع المبرد إن وجد
        cold = conn.execute("SELECT * FROM future_coldchain WHERE lot_id = ?", (d["lot_id"],)).fetchone()
        d["coldchain"] = dict(cold) if cold else None

        result.append(d)
    conn.close()
    return result

@future_router.get("/api/future/lots/{lot_id}")
def get_future_lot_detail(lot_id: str):
    conn = get_connection()
    lot = conn.execute("SELECT * FROM future_lots WHERE lot_id = ?", (lot_id,)).fetchone()
    if not lot:
        conn.close()
        raise HTTPException(status_code=404, detail="الدفعة غير موجودة")
    
    d = dict(lot)
    assay = conn.execute("SELECT * FROM future_assaying WHERE lot_id = ?", (lot_id,)).fetchone()
    d["assaying"] = dict(assay) if assay else None

    auction = conn.execute("SELECT * FROM future_auctions WHERE lot_id = ?", (lot_id,)).fetchone()
    d["auction"] = dict(auction) if auction else None

    bids = conn.execute("SELECT * FROM future_bids WHERE lot_id = ? ORDER BY id DESC", (lot_id,)).fetchall()
    d["bids"] = [dict(b) for b in bids]

    cold = conn.execute("SELECT * FROM future_coldchain WHERE lot_id = ?", (lot_id,)).fetchone()
    d["coldchain"] = dict(cold) if cold else None

    escrow = conn.execute("SELECT * FROM future_escrow_orders WHERE lot_id = ?", (lot_id,)).fetchone()
    d["escrow"] = dict(escrow) if escrow else None

    conn.close()
    return d

@future_router.post("/api/future/lots")
def create_future_lot(data: CreateLotRequest):
    conn = get_connection()
    cursor = conn.cursor()

    # توليد كود دفعة جديد
    count = cursor.execute("SELECT COUNT(*) as c FROM future_lots").fetchone()["c"] + 1
    lot_id = f"SA-2026-{count:04d}"

    cursor.execute("""
    INSERT INTO future_lots (
        lot_id, farmer_name, farmer_phone, farm_name, farm_location, saudi_gap_cert,
        commodity, category, spoilage_tier, quantity, unit, target_market, scheduled_arrival,
        status, image_url
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'registered', ?)
    """, (
        lot_id, data.farmer_name, data.farmer_phone, data.farm_name, data.farm_location,
        data.saudi_gap_cert, data.commodity, data.category, data.spoilage_tier,
        data.quantity, data.unit, data.target_market, data.scheduled_arrival, data.image_url
    ))

    conn.commit()
    conn.close()
    return {
        "status": "success",
        "lot_id": lot_id,
        "message": f"تم تسجيل الدفعة وإصدار الهوية الرقمية الموحدة {lot_id} بنجاح وحجز موعد الوصول"
    }

@future_router.post("/api/future/assaying")
def submit_future_assaying(data: SubmitAssayingRequest):
    conn = get_connection()
    cursor = conn.cursor()

    lot = cursor.execute("SELECT * FROM future_lots WHERE lot_id = ?", (data.lot_id,)).fetchone()
    if not lot:
        conn.close()
        raise HTTPException(status_code=404, detail="الدفعة غير موجودة")

    cert_count = cursor.execute("SELECT COUNT(*) as c FROM future_assaying").fetchone()["c"] + 1
    cert_no = f"CERT-MEWA-2026-{8800 + cert_count:04d}"

    cursor.execute("""
    INSERT INTO future_assaying (
        lot_id, certificate_no, inspector_name, lab_name, moisture_pct, purity_pct,
        defect_pct, sugar_brix, quality_grade, reference_price, inspection_notes
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data.lot_id, cert_no, data.inspector_name, data.lab_name, data.moisture_pct,
        data.purity_pct, data.defect_pct, data.sugar_brix, data.quality_grade,
        data.reference_price, data.inspection_notes
    ))

    # إنشاء جلسة مزاد آلياً للدفعة
    auc_count = cursor.execute("SELECT COUNT(*) as c FROM future_auctions").fetchone()["c"] + 1
    auc_id = f"AUC-2026-{100 + auc_count:03d}"
    start_price = round(data.reference_price * 0.85, 2)
    closing_time = (datetime.datetime.now() + datetime.timedelta(hours=4)).strftime("%Y-%m-%d %H:%M")

    cursor.execute("""
    INSERT INTO future_auctions (
        auction_id, lot_id, start_price, current_bid, highest_bidder_name,
        highest_bidder_city, bid_count, auction_status, closing_time
    ) VALUES (?, ?, ?, ?, 'في انتظار المزايدات الأولى', 'سوق وطني موحد', 0, 'active', ?)
    """, (auc_id, data.lot_id, start_price, start_price, closing_time))

    cursor.execute("UPDATE future_lots SET status = 'auction_active' WHERE lot_id = ?", (data.lot_id,))

    conn.commit()
    conn.close()
    return {
        "status": "success",
        "certificate_no": cert_no,
        "auction_id": auc_id,
        "message": f"تم إصدار شهادة الفحص المعتمدة {cert_no} وإدراج الدفعة في قاعة المزاد الوطني بنجاح"
    }

@future_router.get("/api/future/auctions")
def get_future_auctions():
    conn = get_connection()
    auctions = conn.execute("SELECT * FROM future_auctions ORDER BY id DESC").fetchall()
    res = []
    for a in auctions:
        ad = dict(a)
        lot = conn.execute("SELECT * FROM future_lots WHERE lot_id = ?", (ad["lot_id"],)).fetchone()
        ad["lot"] = dict(lot) if lot else None
        assay = conn.execute("SELECT * FROM future_assaying WHERE lot_id = ?", (ad["lot_id"],)).fetchone()
        ad["assaying"] = dict(assay) if assay else None
        bids = conn.execute("SELECT * FROM future_bids WHERE auction_id = ? ORDER BY bid_amount DESC", (ad["auction_id"],)).fetchall()
        ad["bids"] = [dict(b) for b in bids]
        res.append(ad)
    conn.close()
    return res

@future_router.post("/api/future/auctions/{auction_id}/bid")
def place_future_bid(auction_id: str, data: PlaceBidRequest):
    conn = get_connection()
    cursor = conn.cursor()

    auc = cursor.execute("SELECT * FROM future_auctions WHERE auction_id = ?", (auction_id,)).fetchone()
    if not auc:
        conn.close()
        raise HTTPException(status_code=404, detail="المزاد غير موجود")

    if auc["auction_status"] != "active":
        conn.close()
        raise HTTPException(status_code=400, detail="المزاد مغلق")

    if data.bid_amount <= auc["current_bid"]:
        conn.close()
        raise HTTPException(status_code=400, detail=f"قيمة المزايدة يجب أن تتجاوز السعر الحالي ({auc['current_bid']} ريال)")

    cursor.execute("""
    INSERT INTO future_bids (auction_id, lot_id, bidder_name, bidder_org, bidder_city, bid_amount)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (auction_id, data.lot_id, data.bidder_name, data.bidder_org, data.bidder_city, data.bid_amount))

    new_count = auc["bid_count"] + 1
    cursor.execute("""
    UPDATE future_auctions 
    SET current_bid = ?, highest_bidder_name = ?, highest_bidder_city = ?, bid_count = ?
    WHERE auction_id = ?
    """, (data.bid_amount, f"{data.bidder_name} ({data.bidder_org})", data.bidder_city, new_count, auction_id))

    conn.commit()
    conn.close()
    return {
        "status": "success",
        "current_bid": data.bid_amount,
        "bid_count": new_count,
        "message": f"تم تسجيل مزايدتك بنجاح بمبلغ {data.bid_amount} ريال"
    }

@future_router.post("/api/future/auctions/{auction_id}/close-and-escrow")
def close_auction_and_create_escrow(auction_id: str):
    conn = get_connection()
    cursor = conn.cursor()

    auc = cursor.execute("SELECT * FROM future_auctions WHERE auction_id = ?", (auction_id,)).fetchone()
    if not auc:
        conn.close()
        raise HTTPException(status_code=404, detail="المزاد غير موجود")

    lot = cursor.execute("SELECT * FROM future_lots WHERE lot_id = ?", (auc["lot_id"],)).fetchone()
    if not lot:
        conn.close()
        raise HTTPException(status_code=404, detail="الدفعة غير موجودة")

    cursor.execute("UPDATE future_auctions SET auction_status = 'closed' WHERE auction_id = ?", (auction_id,))

    esc_count = cursor.execute("SELECT COUNT(*) as c FROM future_escrow_orders").fetchone()["c"] + 1
    esc_no = f"ESC-2026-{700 + esc_count:03d}"

    winning_rate = auc["current_bid"]
    total = round(winning_rate * lot["quantity"], 2)
    platform_fee = round(total * 0.05, 2)
    seller_net = round(total - platform_fee, 2)
    verify_code = f"VERIFY-{1000 + esc_count:04d}"

    cursor.execute("""
    INSERT INTO future_escrow_orders (
        escrow_no, lot_id, buyer_name, buyer_phone, seller_name, commodity,
        quantity, unit_price, total_amount, platform_fee, seller_net,
        escrow_status, delivery_confirmation_code
    ) VALUES (?, ?, ?, '0550000000', ?, ?, ?, ?, ?, ?, ?, 'held_in_escrow', ?)
    """, (
        esc_no, lot["lot_id"], auc["highest_bidder_name"], lot["farmer_name"],
        lot["commodity"], lot["quantity"], winning_rate, total, platform_fee, seller_net, verify_code
    ))

    cursor.execute("UPDATE future_lots SET status = 'in_transit' WHERE lot_id = ?", (lot["lot_id"],))

    # إنشاء سجل تتبع مبرد أولي للشحنة
    permit_no = f"PERMIT-SA-2026-{120 + esc_count:03d}"
    cursor.execute("""
    INSERT OR REPLACE INTO future_coldchain (
        lot_id, transporter_company, truck_plate, driver_name, driver_phone,
        transit_permit_no, cold_window_hours, target_temp_range, current_temp,
        current_humidity, temp_status, current_location, destination_market, eta
    ) VALUES (?, 'سلاسل النقل المبرد المعتمدة', 'س ع د 2030', 'سائق معتمد', '0551122334',
              ?, 4.0, '8°C - 12°C', 9.5, 84.0, 'normal', 'بوابة خروج السوق المركزي',
              ?, 'خلال ساعتين')
    """, (lot["lot_id"], permit_no, auc["highest_bidder_city"]))

    conn.commit()
    conn.close()
    return {
        "status": "success",
        "escrow_no": esc_no,
        "total_amount": total,
        "message": f"تم إغلاق المزاد وتفعيل حساب الضمان الرقمي {esc_no} وإصدار تصريح العبور المبرد"
    }

@future_router.get("/api/future/escrow")
def get_future_escrow_orders():
    conn = get_connection()
    orders = conn.execute("SELECT * FROM future_escrow_orders ORDER BY id DESC").fetchall()
    conn.close()
    return [dict(o) for o in orders]

@future_router.post("/api/future/escrow/{escrow_no}/release")
def release_escrow(escrow_no: str):
    conn = get_connection()
    cursor = conn.cursor()

    order = cursor.execute("SELECT * FROM future_escrow_orders WHERE escrow_no = ?", (escrow_no,)).fetchone()
    if not order:
        conn.close()
        raise HTTPException(status_code=404, detail="سجل الضمان غير موجود")

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    cursor.execute("""
    UPDATE future_escrow_orders 
    SET escrow_status = 'released_to_seller', released_at = ?
    WHERE escrow_no = ?
    """, (now, escrow_no))

    cursor.execute("UPDATE future_lots SET status = 'accepted' WHERE lot_id = ?", (order["lot_id"],))

    conn.commit()
    conn.close()
    return {
        "status": "success",
        "message": f"تمت مطابقة الاستلام والإفراج الفوري عن مبلغ {order['seller_net']} ريال لحساب المزارع البنكي"
    }

@future_router.get("/api/future/coldchain")
def get_future_coldchain():
    conn = get_connection()
    logs = conn.execute("""
    SELECT c.*, l.commodity, l.farmer_name, l.quantity, l.unit
    FROM future_coldchain c
    JOIN future_lots l ON c.lot_id = l.lot_id
    ORDER BY c.id DESC
    """).fetchall()
    conn.close()
    return [dict(l) for l in logs]

@future_router.post("/api/future/coldchain/update")
def update_future_coldchain(data: UpdateColdChainRequest):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE future_coldchain
    SET current_temp = ?, current_humidity = ?, temp_status = ?, current_location = ?, eta = ?
    WHERE lot_id = ?
    """, (data.current_temp, data.current_humidity, data.temp_status, data.current_location, data.eta, data.lot_id))

    conn.commit()
    conn.close()
    return {"status": "success", "message": "تم تحديث قراءات حساسات التبريد بنجاح"}

@future_router.get("/api/future/disputes")
def get_future_disputes():
    conn = get_connection()
    disputes = conn.execute("SELECT * FROM future_disputes ORDER BY id DESC").fetchall()
    conn.close()
    return [dict(d) for d in disputes]

@future_router.post("/api/future/disputes")
def create_future_dispute(data: CreateDisputeRequest):
    conn = get_connection()
    cursor = conn.cursor()

    count = cursor.execute("SELECT COUNT(*) as c FROM future_disputes").fetchone()["c"] + 1
    disp_no = f"DISP-2026-{40 + count:03d}"

    cursor.execute("""
    INSERT INTO future_disputes (
        dispute_no, lot_id, escrow_no, complainant_name, complainant_role,
        dispute_type, description, status
    ) VALUES (?, ?, ?, ?, ?, ?, ?, 'under_review')
    """, (disp_no, data.lot_id, data.escrow_no, data.complainant_name, data.complainant_role, data.dispute_type, data.description))

    cursor.execute("UPDATE future_escrow_orders SET escrow_status = 'disputed_held' WHERE escrow_no = ?", (data.escrow_no,))
    cursor.execute("UPDATE future_lots SET status = 'disputed' WHERE lot_id = ?", (data.lot_id,))

    conn.commit()
    conn.close()
    return {
        "status": "success",
        "dispute_no": disp_no,
        "message": f"تم تسجيل النزاع برقم {disp_no} وتجميد الضمان وإحالته فوراً للجنة التحكيم السريع"
    }

@future_router.post("/api/future/disputes/resolve")
def resolve_future_dispute(data: ResolveDisputeRequest):
    conn = get_connection()
    cursor = conn.cursor()

    disp = cursor.execute("SELECT * FROM future_disputes WHERE id = ?", (data.dispute_id,)).fetchone()
    if not disp:
        conn.close()
        raise HTTPException(status_code=404, detail="النزاع غير موجود")

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    cursor.execute("""
    UPDATE future_disputes
    SET status = ?, committee_decision = ?, resolved_at = ?
    WHERE id = ?
    """, (data.decision, data.committee_decision, now, data.dispute_id))

    if data.decision == "resolved_full_payout":
        cursor.execute("UPDATE future_escrow_orders SET escrow_status = 'released_to_seller', released_at = ? WHERE escrow_no = ?", (now, disp["escrow_no"]))
    elif data.decision == "resolved_refund":
        cursor.execute("UPDATE future_escrow_orders SET escrow_status = 'refunded_to_buyer', released_at = ? WHERE escrow_no = ?", (now, disp["escrow_no"]))
    elif data.decision == "resolved_partial_discount":
        cursor.execute("UPDATE future_escrow_orders SET escrow_status = 'released_to_seller', released_at = ? WHERE escrow_no = ?", (now, disp["escrow_no"]))

    cursor.execute("UPDATE future_lots SET status = 'accepted' WHERE lot_id = ?", (disp["lot_id"],))

    conn.commit()
    conn.close()
    return {"status": "success", "message": "تم اعتماد قرار لجنة فض النزاعات وتنفيذ التسوية المالية فوراً"}

class DisputeBuyerOrderRequest(BaseModel):
    reason: str
    details: Optional[str] = ""
    evidence: Optional[str] = ""

class PayBuyerOrderRequest(BaseModel):
    payment_method: Optional[str] = "مدى (Mada)"

@future_router.get("/api/future/reference-prices")
def get_future_reference_prices():
    conn = get_connection()
    prices = conn.execute("SELECT * FROM future_reference_prices ORDER BY id ASC").fetchall()
    conn.close()
    return [dict(p) for p in prices]

@future_router.get("/api/future/analytics")
def get_future_analytics():
    conn = get_connection()
    lots_count = conn.execute("SELECT COUNT(*) as c FROM future_lots").fetchone()["c"]
    graded_count = conn.execute("SELECT COUNT(*) as c FROM future_assaying").fetchone()["c"]
    active_auctions = conn.execute("SELECT COUNT(*) as c FROM future_auctions WHERE auction_status = 'active'").fetchone()["c"]
    escrow_total = conn.execute("SELECT COALESCE(SUM(total_amount), 0) as s FROM future_escrow_orders").fetchone()["s"]
    disputes_count = conn.execute("SELECT COUNT(*) as c FROM future_disputes").fetchone()["c"]
    resolved_disputes = conn.execute("SELECT COUNT(*) as c FROM future_disputes WHERE status != 'under_review'").fetchone()["c"]
    conn.close()

    return {
        "lots_count": lots_count,
        "graded_count": graded_count,
        "active_auctions": active_auctions,
        "escrow_total": round(escrow_total, 2),
        "disputes_count": disputes_count,
        "resolved_disputes": resolved_disputes,
        "coldchain_compliance": 99.4,
        "average_dispute_resolution_minutes": 42
    }

# قائمة طلبات المشتري الثابتة والمتوافقة
BUYER_SEED_ORDERS = [
    {
        "order_id": "ORD-2026-701",
        "lot_id": "SA-2026-0101",
        "auction_id": "AUC-2026-4401",
        "commodity": "طماطم محمية قطاف اليوم",
        "farmer_name": "مزارع الوادي بالخرج",
        "farm_location": "الخرج - منطقة الرياض",
        "quantity": 1500,
        "unit": "صندوق (6 كجم)",
        "unit_price": 19.50,
        "total_product": 29250.0,
        "fee": 1462.5,
        "vat": 219.38,
        "total_invoice": 30931.88,
        "status": "awaiting_payment",
        "invoice_no": "INV-SA-2026-9011",
        "created_at": "2026-11-04 09:30",
        "image_url": "static/images/products/tomatoes.jpg",
        "quality_grade": "نخب أول (Grade A)",
        "saudi_gap": "معتمد (Saudi G.A.P.)",
        "target_market": "سوق العزيزية المركزي - الرياض",
        "buyer_name": "شركة التميمي للأسواق",
        "tracking": {
            "step": 1,
            "step_title": "تمت الترسية وبانتظار سداد الفاتورة",
            "current_temp": None,
            "truck_plate": None,
            "driver_name": None,
            "driver_phone": None,
            "eta": "بانتظار السداد لبدء التحميل والتبريد"
        }
    },
    {
        "order_id": "ORD-2026-702",
        "lot_id": "SA-2026-0102",
        "auction_id": "AUC-2026-4402",
        "commodity": "بطاطس مائدة صنف سبونتا",
        "farmer_name": "مؤسسة حائل للتنمية الزراعية",
        "farm_location": "بقعاء - منطقة حائل",
        "quantity": 12000,
        "unit": "كيس شبكي (15 كجم)",
        "unit_price": 2.75,
        "total_product": 33000.0,
        "fee": 1650.0,
        "vat": 247.50,
        "total_invoice": 34897.50,
        "status": "in_transit",
        "escrow_no": "ESC-2026-8802",
        "invoice_no": "INV-SA-2026-9012",
        "payment_method": "مدى (Mada) •••• 4012",
        "paid_at": "2026-11-04 08:30",
        "created_at": "2026-11-04 08:15",
        "image_url": "static/images/products/potatoes.jpg",
        "quality_grade": "نخب ثاني (Grade B)",
        "saudi_gap": "معتمد (Saudi G.A.P.)",
        "target_market": "سوق بريدة المركزي - القصيم",
        "buyer_name": "شركة التميمي للأسواق",
        "tracking": {
            "step": 4,
            "step_title": "في الطريق إلى سوق بريدة المركزي",
            "current_temp": 14.2,
            "target_temp": "12°C - 15°C",
            "humidity": 76,
            "temp_status": "normal",
            "truck_plate": "ح ل ق 9876",
            "driver_name": "خالد المطيري",
            "driver_phone": "0556677889",
            "current_location": "طريق حائل - القصيم السريع (كم 140)",
            "eta": "خلال 45 دقيقة (09:45 ص)"
        }
    },
    {
        "order_id": "ORD-2026-703",
        "lot_id": "SA-2026-0103",
        "auction_id": "AUC-2026-4403",
        "commodity": "بصل أحمر قصيمي مجفف",
        "farmer_name": "جمعية عنيزة الزراعية التعاونية",
        "farm_location": "عنيزة - منطقة القصيم",
        "quantity": 8000,
        "unit": "كيس شبكي (10 كجم)",
        "unit_price": 3.20,
        "total_product": 25600.0,
        "fee": 1280.0,
        "vat": 192.00,
        "total_invoice": 27072.00,
        "status": "arrived",
        "escrow_no": "ESC-2026-8803",
        "invoice_no": "INV-SA-2026-9013",
        "payment_method": "سداد (SADAD - الحساب التجاري)",
        "paid_at": "2026-11-04 07:15",
        "created_at": "2026-11-04 07:00",
        "image_url": "static/images/products/zucchini.jpg",
        "quality_grade": "نخب أول (Grade A)",
        "saudi_gap": "معتمد (Saudi G.A.P.)",
        "target_market": "سوق عنيزة المركزي",
        "buyer_name": "شركة التميمي للأسواق",
        "tracking": {
            "step": 5,
            "step_title": "وصلت رصيف التفريغ بالسوق وبانتظار الاستلام أو الاعتراض",
            "current_temp": 19.5,
            "target_temp": "18°C - 22°C",
            "humidity": 62,
            "temp_status": "normal",
            "truck_plate": "ص ع ط 5511",
            "driver_name": "سلمان الحربي",
            "driver_phone": "0501144778",
            "current_location": "رصيف تفريغ رقم 4 - سوق عنيزة",
            "eta": "تم الوصول بنجاح"
        }
    }
]

@future_router.get("/api/future/buyer/orders")
def get_future_buyer_orders():
    return BUYER_SEED_ORDERS

@future_router.post("/api/future/buyer/orders/{order_id}/pay")
def pay_future_buyer_order(order_id: str, data: PayBuyerOrderRequest):
    order = next((o for o in BUYER_SEED_ORDERS if o["order_id"] == order_id), None)
    if not order:
        raise HTTPException(status_code=404, detail="الطلب غير موجود")
    order["status"] = "in_transit"
    order["payment_method"] = data.payment_method
    order["paid_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    if not order.get("escrow_no"):
        order["escrow_no"] = f"ESC-2026-{datetime.datetime.now().strftime('%S%M')}"
    return {"status": "success", "message": "تم سداد الفاتورة وإيداع المبلغ في حساب الضمان", "order": order}

@future_router.post("/api/future/buyer/orders/{order_id}/confirm")
def confirm_future_buyer_order(order_id: str):
    order = next((o for o in BUYER_SEED_ORDERS if o["order_id"] == order_id), None)
    if not order:
        raise HTTPException(status_code=404, detail="الطلب غير موجود")
    order["status"] = "completed"
    order["completed_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    return {"status": "success", "message": "تم تأكيد الاستلام بنجاح وصرف مستحقات المزارع", "order": order}

@future_router.post("/api/future/buyer/orders/{order_id}/dispute")
def dispute_future_buyer_order(order_id: str, data: DisputeBuyerOrderRequest):
    order = next((o for o in BUYER_SEED_ORDERS if o["order_id"] == order_id), None)
    if not order:
        raise HTTPException(status_code=404, detail="الطلب غير موجود")
    disp_id = f"DIS-2026-{datetime.datetime.now().strftime('%S%M')}"
    order["status"] = "disputed"
    order["dispute_id"] = disp_id
    order["dispute_reason"] = data.reason
    return {"status": "success", "message": f"تم تسجيل الاعتراض برقم {disp_id} وتجميد الضمان", "dispute_id": disp_id}
