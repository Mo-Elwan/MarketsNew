/**
 * المنصة الوطنية لأسواق النفع العام - مستودع البيانات التفاعلي الثابت (FutureStaticStore)
 * متوافق 100% مع التشغيل الثابت بدون خادم (Static HTML / Offline) والتشغيل مع خادم FastAPI.
 * هوية وطنية سعودية خالصة وفق معايير وزارة البيئة والمياه والزراعة ومنصة نماء ورؤية 2030.
 */

(function() {
    const STORAGE_KEY = 'SA_FUTURE_MARKETS_STORE_V1';

    const DEFAULT_SEED_DATA = {
        lots: [
            {
                lot_id: "LOT-SA-2026-0101",
                farmer_name: "مزارع الوادي الوطنية",
                farmer_phone: "0501234567",
                farm_name: "مزارع الوادي بالخرج",
                farm_location: "الخرج - منطقة الرياض",
                saudi_gap_cert: "GAP-SA-2026-8812",
                commodity: "طماطم محمية قطاف اليوم",
                category: "خضار وفواكه",
                spoilage_tier: "المرحلة 1: سريع التلف",
                quantity: 1500,
                unit: "صندوق (6 كجم)",
                target_market: "سوق العزيزية المركزي - الرياض",
                scheduled_arrival: "2026-11-04 06:30",
                status: "auction_active",
                created_at: "2026-11-04 05:00",
                image_url: "https://images.unsplash.com/photo-1592924357228-91a4daadcfea?w=600",
                assaying: {
                    certificate_no: "CER-2026-9811",
                    inspector_name: "م. فهد القحطاني",
                    lab_name: "مختبر الجودة المركزي - الرياض",
                    moisture_pct: 89.2,
                    purity_pct: 99.4,
                    defect_pct: 1.1,
                    sugar_brix: 5.6,
                    quality_grade: "نخب أول (Grade A)",
                    reference_price: 18.50,
                    inspection_notes: "مطابق لاشتراطات سعودي جاب، صلابة ممتازة، لا توجد لسعات شمس، جاهز للتبريد المباشر.",
                    tested_at: "2026-11-04 07:15"
                },
                auction: {
                    auction_id: "AUC-2026-4401",
                    start_price: 18.50,
                    reserve_price: 17.00,
                    current_bid: 19.50,
                    highest_bidder_name: "شركة التميمي للأسواق",
                    highest_bidder_org: "أسواق التميمي الفاخرة",
                    highest_bidder_city: "الرياض",
                    bid_count: 7,
                    auction_status: "active",
                    time_remaining: "14 دقيقة و 20 ثانية",
                    starts_at: "2026-11-04 08:00",
                    ends_at: "2026-11-04 09:30"
                },
                coldchain: {
                    cold_window_hours: 4,
                    current_temp: 9.2,
                    target_temp_range: "8°C - 10°C",
                    current_humidity: 88,
                    temp_status: "normal",
                    truck_plate: "أ ب د 1234",
                    driver_name: "سعد الشمري",
                    driver_phone: "0559988771",
                    current_location: "بوابة فحص سوق العزيزية",
                    destination_market: "سوق العزيزية المركزي - الرياض",
                    eta: "تم الوصول وتفريغ العينة"
                }
            },
            {
                lot_id: "LOT-SA-2026-0102",
                farmer_name: "مؤسسة حائل للتنمية الزراعية",
                farmer_phone: "0554433221",
                farm_name: "مزارع بقعاء النموذجية",
                farm_location: "بقعاء - منطقة حائل",
                saudi_gap_cert: "GAP-SA-2026-4190",
                commodity: "بطاطس مائدة صنف سبونتا",
                category: "خضار وفواكه",
                spoilage_tier: "المرحلة 2: متوسط التلف",
                quantity: 12000,
                unit: "كيس شبكي (15 كجم)",
                target_market: "سوق الخضار والفواكه المركزي - بريدة",
                scheduled_arrival: "2026-11-04 07:45",
                status: "auction_active",
                created_at: "2026-11-04 04:30",
                image_url: "https://images.unsplash.com/photo-1518977676601-b53f82aba655?w=600",
                assaying: {
                    certificate_no: "CER-2026-9812",
                    inspector_name: "م. تركي الشمري",
                    lab_name: "مختبر فحص القصيم المعتمد",
                    moisture_pct: 78.5,
                    purity_pct: 98.8,
                    defect_pct: 1.8,
                    sugar_brix: 0.0,
                    quality_grade: "نخب ثاني (Grade B)",
                    reference_price: 2.40,
                    inspection_notes: "درنات مائدة صلبة خالية من العفن، أقطار متجانسة بين 70-85 ملم.",
                    tested_at: "2026-11-04 08:00"
                },
                auction: {
                    auction_id: "AUC-2026-4402",
                    start_price: 2.40,
                    reserve_price: 2.20,
                    current_bid: 2.75,
                    highest_bidder_name: "مؤسسة النخبة للتوريدات الغذائية",
                    highest_bidder_org: "النخبة للخدمات التموينية",
                    highest_bidder_city: "بريدة",
                    bid_count: 12,
                    auction_status: "active",
                    time_remaining: "08 دقائق و 45 ثانية",
                    starts_at: "2026-11-04 08:15",
                    ends_at: "2026-11-04 09:15"
                },
                coldchain: {
                    cold_window_hours: 6,
                    current_temp: 14.5,
                    target_temp_range: "12°C - 15°C",
                    current_humidity: 75,
                    temp_status: "normal",
                    truck_plate: "ح ل ق 9876",
                    driver_name: "محمد العتيبي",
                    driver_phone: "0561122334",
                    current_location: "طريق حائل - بريدة السريع",
                    destination_market: "سوق الخضار المركزي - بريدة",
                    eta: "خلال 45 دقيقة"
                }
            },
            {
                lot_id: "LOT-SA-2026-0103",
                farmer_name: "جمعية عنيزة الزراعية التعاونية",
                farmer_phone: "0543322119",
                farm_name: "مزارع الجمعية التعاونية",
                farm_location: "عنيزة - منطقة القصيم",
                saudi_gap_cert: "GAP-SA-2026-7731",
                commodity: "بصل أحمر قصيمي مجفف",
                category: "خضار وفواكه",
                spoilage_tier: "المرحلة 2: متوسط التلف",
                quantity: 8000,
                unit: "كيس شبكي (15 كجم)",
                target_market: "سوق الخضار المركزي بالصفا - جدة",
                scheduled_arrival: "2026-11-04 11:30",
                status: "in_transit",
                created_at: "2026-11-04 03:00",
                image_url: "https://images.unsplash.com/photo-1618512496248-a07fe83aa8cb?w=600",
                assaying: {
                    certificate_no: "CER-2026-9813",
                    inspector_name: "د. خالد السليمان",
                    lab_name: "مختبر جودة القصيم",
                    moisture_pct: 12.8,
                    purity_pct: 99.1,
                    defect_pct: 0.9,
                    sugar_brix: 0.0,
                    quality_grade: "نخب أول (Grade A)",
                    reference_price: 3.20,
                    inspection_notes: "بصل أحمر متماسك مجفف طبيعياً، جفاف مثالي، خالٍ من التبرعم، جاهز للشحن بين المدن.",
                    tested_at: "2026-11-04 05:40"
                },
                coldchain: {
                    cold_window_hours: 6,
                    current_temp: 12.2,
                    target_temp_range: "10°C - 14°C",
                    current_humidity: 65,
                    temp_status: "normal",
                    truck_plate: "ع ن ز 5544",
                    driver_name: "فايز الحربي",
                    driver_phone: "0509988112",
                    current_location: "طريق المدينة - مكة السريع",
                    destination_market: "سوق الخضار المركزي بالصفا - جدة",
                    eta: "خلال ساعة و 20 دقيقة"
                }
            },
            {
                lot_id: "LOT-SA-2026-0104",
                farmer_name: "مزارع النخيل الذهبي",
                farmer_phone: "0508877665",
                farm_name: "نخيل الهفوف المباركة",
                farm_location: "الهفوف - الأحساء",
                saudi_gap_cert: "GAP-SA-2026-9901",
                commodity: "تمر خلاص الأحساء الفاخر",
                category: "تمور",
                spoilage_tier: "المرحلة 3: قابل للتخزين",
                quantity: 3000,
                unit: "كرتون (8 كجم)",
                target_market: "سوق التمور والخضار المركزي - الأحساء",
                scheduled_arrival: "2026-11-04 08:00",
                status: "auction_active",
                created_at: "2026-11-04 06:00",
                image_url: "https://images.unsplash.com/photo-1596483739943-431f41b4b1a4?w=600",
                assaying: {
                    certificate_no: "CER-2026-9814",
                    inspector_name: "م. إبراهيم الدوسري",
                    lab_name: "مختبر مركز التمور بالأحساء",
                    moisture_pct: 14.5,
                    purity_pct: 99.7,
                    defect_pct: 0.4,
                    sugar_brix: 68.0,
                    quality_grade: "نخب أول ملكي (Grade A+)",
                    reference_price: 185.00,
                    inspection_notes: "خلاص فاخر مكنوز بحبة ملكية جامبو، لون أشقر متجانس ونسبة سكر ممتازة.",
                    tested_at: "2026-11-04 08:10"
                },
                auction: {
                    auction_id: "AUC-2026-4404",
                    start_price: 185.00,
                    reserve_price: 180.00,
                    current_bid: 195.00,
                    highest_bidder_name: "سلسلة مطاعم الرومانسية",
                    highest_bidder_org: "شركة الرومانسية المحدودة",
                    highest_bidder_city: "الرياض",
                    bid_count: 15,
                    auction_status: "active",
                    time_remaining: "05 دقائق و 10 ثواني",
                    starts_at: "2026-11-04 08:30",
                    ends_at: "2026-11-04 09:30"
                }
            },
            {
                lot_id: "LOT-SA-2026-0105",
                farmer_name: "مزارع أسترا الزراعية",
                farmer_phone: "0532211445",
                farm_name: "مزارع تيماء الخضراء",
                farm_location: "تيماء - منطقة تبوك",
                saudi_gap_cert: "GAP-SA-2026-3321",
                commodity: "خيار بيوت محمية نخب أول",
                category: "خضار وفواكه",
                spoilage_tier: "المرحلة 1: سريع التلف",
                quantity: 2500,
                unit: "صندوق (6 كجم)",
                target_market: "سوق العزيزية المركزي - الرياض",
                scheduled_arrival: "2026-11-04 10:00",
                status: "registered",
                created_at: "2026-11-04 06:45",
                image_url: "https://images.unsplash.com/photo-1604977042946-1eecc30f269e?w=600"
            }
        ],
        disputes: [
            {
                dispute_id: "DIS-2026-101",
                lot_id: "LOT-SA-2026-0099",
                claimant_name: "أسواق عبد الله العثيم",
                defendant_name: "مزارع القصيم للخضار",
                dispute_type: "خرق سلسلة التبريد وتلف 8%",
                dispute_status: "under_review",
                claim_amount: 8400.0,
                details: "ارتفعت درجة حرارة شاحنة الطماطم إلى 16.4 مئوية لأكثر من 3 ساعات أثناء النقل مما تسبب في ليونة مفرطة وظهور بقع تلف.",
                evidence_attachment: "سجل حساس IoT للشاحنة رقم 4423",
                committee_decision: null,
                created_at: "اليوم - قبل ساعة و 15 دقيقة"
            },
            {
                dispute_id: "DIS-2026-102",
                lot_id: "LOT-SA-2026-0098",
                claimant_name: "شركة لولو هايبرماركت السعودية",
                defendant_name: "مزارع تبوك الزراعية",
                dispute_type: "عدم مطابقة رتبة الفحص",
                dispute_status: "resolved",
                claim_amount: 3200.0,
                details: "تم توريد جزء من الشحنة بدرجة ثانية بدلاً من درجة أولى المعتمدة في المزاد.",
                evidence_attachment: "محضر فحص عينة الاستلام رقم L-440",
                committee_decision: "إلزام البائع بخصم 15% من قيمة الفاتورة الصافية وصرف المبلغ المتبقي للمزارع فوراً مع تحديث سجل الموثوقية.",
                created_at: "أمس - تم الحل خلال 38 دقيقة"
            }
        ],
        escrow: [
            {
                escrow_no: "ESC-2026-8801",
                lot_id: "LOT-SA-2026-0101",
                commodity: "طماطم محمية قطاف اليوم",
                quantity: 1500,
                buyer_name: "شركة التميمي للأسواق",
                seller_name: "مزارع الوادي الوطنية",
                total_amount: 29250.0,
                platform_fee: 1462.5,
                seller_net: 27787.5,
                escrow_status: "held_in_escrow",
                created_at: "2026-11-04 08:30"
            },
            {
                escrow_no: "ESC-2026-8802",
                lot_id: "LOT-SA-2026-0102",
                commodity: "بطاطس مائدة صنف سبونتا",
                quantity: 12000,
                buyer_name: "مؤسسة النخبة للتوريدات الغذائية",
                seller_name: "مؤسسة حائل للتنمية الزراعية",
                total_amount: 33000.0,
                platform_fee: 1650.0,
                seller_net: 31350.0,
                escrow_status: "held_in_escrow",
                created_at: "2026-11-04 08:15"
            },
            {
                escrow_no: "ESC-2026-8803",
                lot_id: "LOT-SA-2026-0103",
                commodity: "بصل أحمر قصيمي مجفف",
                quantity: 8000,
                buyer_name: "شركة أسواق بن داود",
                seller_name: "جمعية عنيزة الزراعية التعاونية",
                total_amount: 45000.0,
                platform_fee: 2250.0,
                seller_net: 42750.0,
                escrow_status: "held_in_escrow",
                created_at: "2026-11-04 07:00"
            },
            {
                escrow_no: "ESC-2026-8800",
                lot_id: "LOT-SA-2026-0097",
                commodity: "تمر خلاص الأحساء الفاخر",
                quantity: 1200,
                buyer_name: "تموين كارفور السعودية",
                seller_name: "مزارع النخيل الذهبي",
                total_amount: 188250.0,
                platform_fee: 9412.5,
                seller_net: 178837.5,
                escrow_status: "released_to_seller",
                created_at: "2026-11-03 14:00"
            }
        ],
        referencePrices: [
            { commodity: "طماطم محمية قطاف اليوم", region: "منطقة الرياض", market_name: "سوق العزيزية المركزي", grade_a_price: 18.50, grade_b_price: 15.00, grade_c_price: 11.50 },
            { commodity: "خيار بيوت محمية نخب أول", region: "منطقة الرياض", market_name: "سوق العزيزية المركزي", grade_a_price: 16.00, grade_b_price: 13.00, grade_c_price: 9.50 },
            { commodity: "بطاطس مائدة صنف سبونتا", region: "منطقة القصيم", market_name: "سوق بريدة المركزي", grade_a_price: 2.80, grade_b_price: 2.40, grade_c_price: 1.80 },
            { commodity: "بصل أحمر قصيمي مجفف", region: "منطقة القصيم", market_name: "سوق عنيزة المركزي", grade_a_price: 3.50, grade_b_price: 3.10, grade_c_price: 2.20 },
            { commodity: "تمر خلاص الأحساء الفاخر", region: "المنطقة الشرقية", market_name: "سوق الأحساء المركزي", grade_a_price: 185.00, grade_b_price: 145.00, grade_c_price: 110.00 },
            { commodity: "حبحب وادي الدواسر أحمر", region: "منطقة الرياض", market_name: "سوق وادي الدواسر", grade_a_price: 3.20, grade_b_price: 2.50, grade_c_price: 1.90 }
        ]
    };

    class Store {
        constructor() {
            this.load();
        }

        load() {
            try {
                const stored = localStorage.getItem(STORAGE_KEY);
                if (stored) {
                    this.data = JSON.parse(stored);
                    // التحقق من اكتمال الجداول
                    if (!this.data.lots || this.data.lots.length === 0) {
                        this.data = JSON.parse(JSON.stringify(DEFAULT_SEED_DATA));
                        this.save();
                    }
                } else {
                    this.data = JSON.parse(JSON.stringify(DEFAULT_SEED_DATA));
                    this.save();
                }
            } catch (e) {
                this.data = JSON.parse(JSON.stringify(DEFAULT_SEED_DATA));
            }
        }

        save() {
            try {
                localStorage.setItem(STORAGE_KEY, JSON.stringify(this.data));
            } catch (e) {
                console.warn('LocalStorage save failed:', e);
            }
        }

        reset() {
            this.data = JSON.parse(JSON.stringify(DEFAULT_SEED_DATA));
            this.save();
            return this.data;
        }

        // --- عمليات الدفعات (Lots) ---
        getLots() {
            return this.data.lots;
        }

        addLot(lot) {
            const nextIndex = this.data.lots.length + 101;
            const lotId = `LOT-SA-2026-${String(nextIndex).padStart(4, '0')}`;
            const newLot = Object.assign({
                lot_id: lotId,
                status: 'registered',
                created_at: new Date().toISOString().slice(0, 16).replace('T', ' '),
                image_url: 'https://images.unsplash.com/photo-1592924357228-91a4daadcfea?w=600'
            }, lot);
            this.data.lots.unshift(newLot);
            this.save();
            return newLot;
        }

        // --- عمليات الفحص (Assaying) ---
        addAssaying(assay) {
            const lot = this.data.lots.find(l => l.lot_id === assay.lot_id);
            if (!lot) throw new Error('الدفعة غير موجودة');
            
            const certNo = `CER-2026-${Math.floor(1000 + Math.random() * 9000)}`;
            lot.assaying = {
                certificate_no: certNo,
                inspector_name: assay.inspector_name,
                lab_name: assay.lab_name,
                moisture_pct: assay.moisture_pct,
                purity_pct: assay.purity_pct,
                defect_pct: assay.defect_pct,
                sugar_brix: assay.sugar_brix,
                quality_grade: assay.quality_grade,
                reference_price: assay.reference_price,
                inspection_notes: assay.inspection_notes,
                tested_at: new Date().toISOString().slice(0, 16).replace('T', ' ')
            };
            lot.status = 'graded';
            this.save();
            return lot.assaying;
        }

        // --- عمليات المزاد (Auctions) ---
        getAuctions() {
            return this.data.lots
                .filter(l => l.auction)
                .map(l => ({
                    auction_id: l.auction.auction_id,
                    lot_id: l.lot_id,
                    start_price: l.auction.start_price,
                    reserve_price: l.auction.reserve_price,
                    current_bid: l.auction.current_bid,
                    highest_bidder_name: l.auction.highest_bidder_name,
                    highest_bidder_city: l.auction.highest_bidder_city,
                    bid_count: l.auction.bid_count,
                    auction_status: l.auction.auction_status,
                    time_remaining: l.auction.time_remaining || '12 دقيقة',
                    lot: {
                        commodity: l.commodity,
                        farmer_name: l.farmer_name,
                        farm_location: l.farm_location,
                        quantity: l.quantity,
                        unit: l.unit,
                        image_url: l.image_url
                    },
                    assaying: l.assaying
                }));
        }

        placeBid(auctionId, bid) {
            const lot = this.data.lots.find(l => l.auction && l.auction.auction_id === auctionId);
            if (!lot) throw new Error('المزاد غير موجود');
            if (bid.bid_amount <= lot.auction.current_bid) {
                throw new Error('قيمة المزايدة يجب أن تكون أعلى من السعر الحالي');
            }

            lot.auction.current_bid = bid.bid_amount;
            lot.auction.highest_bidder_name = bid.bidder_name;
            lot.auction.highest_bidder_city = bid.bidder_city;
            lot.auction.highest_bidder_org = bid.bidder_org;
            lot.auction.bid_count = (lot.auction.bid_count || 0) + 1;
            this.save();
            return lot.auction;
        }

        closeAndEscrow(auctionId) {
            const lot = this.data.lots.find(l => l.auction && l.auction.auction_id === auctionId);
            if (!lot) throw new Error('المزاد غير موجود');
            
            lot.auction.auction_status = 'closed';
            lot.status = 'in_transit';

            const total = lot.auction.current_bid * lot.quantity;
            const fee = total * 0.05;
            const net = total - fee;
            const escrowNo = `ESC-2026-${Math.floor(8800 + Math.random() * 900)}`;

            const escrowRecord = {
                escrow_no: escrowNo,
                lot_id: lot.lot_id,
                commodity: lot.commodity,
                quantity: lot.quantity,
                buyer_name: lot.auction.highest_bidder_name,
                seller_name: lot.farmer_name,
                total_amount: total,
                platform_fee: fee,
                seller_net: net,
                escrow_status: "held_in_escrow",
                created_at: new Date().toISOString().slice(0, 16).replace('T', ' ')
            };

            this.data.escrow.unshift(escrowRecord);
            this.save();
            return { lot, escrow: escrowRecord };
        }

        // --- عمليات سلاسل التبريد (Cold Chain) ---
        getColdChain() {
            return this.data.lots
                .filter(l => l.coldchain)
                .map(l => Object.assign({
                    lot_id: l.lot_id,
                    commodity: l.commodity,
                    farmer_name: l.farmer_name,
                    quantity: l.quantity,
                    unit: l.unit
                }, l.coldchain));
        }

        updateColdChainSensor(lotId, update) {
            const lot = this.data.lots.find(l => l.lot_id === lotId);
            if (!lot || !lot.coldchain) throw new Error('سجل التبريد غير موجود');
            Object.assign(lot.coldchain, update);
            this.save();
            return lot.coldchain;
        }

        // --- عمليات فض النزاعات (Disputes) ---
        getDisputes() {
            return this.data.disputes;
        }

        resolveDispute(disputeId, decision, text) {
            const d = this.data.disputes.find(x => x.dispute_id === disputeId);
            if (!d) throw new Error('النزاع غير موجود');
            d.dispute_status = 'resolved';
            d.committee_decision = text || decision;
            this.save();
            return d;
        }

        // --- عمليات حساب الضمان (Escrow) ---
        getEscrow() {
            return this.data.escrow;
        }

        releaseEscrow(escrowNo) {
            const e = this.data.escrow.find(x => x.escrow_no === escrowNo);
            if (!e) throw new Error('طلب الضمان غير موجود');
            e.escrow_status = 'released_to_seller';
            const lot = this.data.lots.find(l => l.lot_id === e.lot_id);
            if (lot) lot.status = 'accepted';
            this.save();
            return e;
        }

        // --- الأسعار المرجعية والإحصائيات ---
        getReferencePrices() {
            return this.data.referencePrices;
        }

        getAnalytics() {
            let graded = 0;
            let activeAuc = 0;
            this.data.lots.forEach(l => {
                if (l.assaying) graded++;
                if (l.auction && l.auction.auction_status === 'active') activeAuc++;
            });
            const escrowTotal = this.data.escrow.reduce((sum, e) => sum + (e.total_amount || 0), 0);
            return {
                graded_count: graded,
                active_auctions: activeAuc,
                escrow_total: escrowTotal,
                average_dispute_resolution_minutes: 42
            };
        }
    }

    window.FutureStaticStore = new Store();
})();
