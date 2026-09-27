"""
Florya MEV Koleji - Eylül 2026 Kasa Defteri Veri Aktarım Aracı
Masaüstündeki 'BASINKÖY MEV KASA.xls' dosyasındaki Eylül verilerini veritabanına aktarır.
"""

import xlrd
from pathlib import Path
from database import get_sqlite_connection, trigger_auto_backup

EXCEL_PATH = Path(r"C:\Users\doruk\Desktop\BASINKÖY MEV KASA.xls")

def import_september_kasa():
    if not EXCEL_PATH.exists():
        print(f"[HATA] Dosya bulunamadı: {EXCEL_PATH}")
        return False

    wb = xlrd.open_workbook(str(EXCEL_PATH))
    sheet_candidates = [s for s in wb.sheet_names() if 'EYL' in s or 'eyl' in s]
    if not sheet_candidates:
        print("[HATA] 'EYLÜL' sayfası bulunamadı!")
        return False

    sheet = wb.sheet_by_name(sheet_candidates[0])
    print(f"[BİLGİ] '{sheet.name}' sayfası işleniyor...")

    conn = get_sqlite_connection()
    cursor = conn.cursor()

    # Önceki Eylül kayıtlarını temizleyelim (çift kayıt olmasın)
    cursor.execute("DELETE FROM kasa_transactions WHERE trans_date LIKE '2026-09%'")
    cursor.execute("DELETE FROM canteen_cash_records WHERE record_date LIKE '2026-09%'")
    conn.commit()

    # 1. NAKLİ YEKÛN (Ağustos'tan devreden kasa)
    try:
        nakli_yekun = float(sheet.cell_value(5, 20))
    except:
        nakli_yekun = 18845.0

    if nakli_yekun > 0:
        cursor.execute("""
            INSERT INTO kasa_transactions (
                trans_type, trans_date, order_no, description, category,
                amount, document_no, notes, recorded_by
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            "GELİR",
            "2026-09-01",
            0,
            "AĞUSTOS AYINDAN GELEN DEVİR (NAKLİ YEKÛN)",
            "Devreden Kasa",
            nakli_yekun,
            "",
            "Ağustos ayı kapanış bakiyesi devri",
            "Erva Yunus"
        ))

    # 2. GELİRLERİ AKTAR (Satır 6'dan 36'ya kadar)
    gelir_count = 0
    gelirler_by_date = {}
    for r in range(6, 37):
        sira = sheet.cell_value(r, 11)
        if not sira:
            continue
        try:
            tarih = xlrd.xldate_as_datetime(sheet.cell_value(r, 12), wb.datemode).strftime('%Y-%m-%d')
            aciklama = str(sheet.cell_value(r, 14)).strip()
            tutar = float(sheet.cell_value(r, 20))
        except Exception as e:
            continue

        if tutar > 0:
            cursor.execute("""
                INSERT INTO kasa_transactions (
                    trans_type, trans_date, order_no, description, category,
                    amount, document_no, notes, recorded_by
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                "GELİR",
                tarih,
                int(sira),
                aciklama if aciklama else "TÜM KASALAR",
                "Günlük Hasılat",
                tutar,
                "",
                f"Eylül Kasa Defteri Sıra No: {int(sira)}",
                "Erva Yunus"
            ))
            gelir_count += 1
            gelirler_by_date[tarih] = gelirler_by_date.get(tarih, 0.0) + tutar

    # 3. GİDERLERİ AKTAR (Satır 6'dan 36'ya kadar)
    gider_count = 0
    giderler_by_date = {}
    for r in range(6, 37):
        sira = sheet.cell_value(r, 0)
        if not sira:
            continue
        try:
            tarih = xlrd.xldate_as_datetime(sheet.cell_value(r, 1), wb.datemode).strftime('%Y-%m-%d')
            aciklama = str(sheet.cell_value(r, 3)).strip()
            tutar = float(sheet.cell_value(r, 9))
        except Exception as e:
            continue

        if tutar > 0:
            # Kategori belirleme
            cat = "Tedarikçi Ödemesi"
            if "MERKEZ" in aciklama.upper():
                cat = "Merkeze Teslim"
            elif "İTFAİYE" in aciklama.upper() or "ITFAIYE" in aciklama.upper():
                cat = "Resmi / Kurum Harcaması"

            cursor.execute("""
                INSERT INTO kasa_transactions (
                    trans_type, trans_date, order_no, description, category,
                    amount, document_no, notes, recorded_by
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                "GİDER",
                tarih,
                int(sira),
                aciklama,
                cat,
                tutar,
                "",
                f"Eylül Kasa Defteri Gider Sıra No: {int(sira)}",
                "Erva Yunus"
            ))
            gider_count += 1
            
            if tarih not in giderler_by_date:
                giderler_by_date[tarih] = {"merkez": 0.0, "vendor": 0.0, "other": 0.0, "notes": []}
            if cat == "Merkeze Teslim":
                giderler_by_date[tarih]["merkez"] += tutar
            elif cat == "Tedarikçi Ödemesi":
                giderler_by_date[tarih]["vendor"] += tutar
            else:
                giderler_by_date[tarih]["other"] += tutar
            giderler_by_date[tarih]["notes"].append(f"{aciklama} ({tutar:,.0f} TL)")

    # 4. GÜNLÜK ÖZETLERİ canteen_cash_records TABLOSUNA İŞLE
    all_dates = sorted(list(set(list(gelirler_by_date.keys()) + list(giderler_by_date.keys()))))
    for d in all_dates:
        rev = gelirler_by_date.get(d, 0.0)
        exp_info = giderler_by_date.get(d, {"merkez": 0.0, "vendor": 0.0, "other": 0.0, "notes": []})
        hq = exp_info["merkez"]
        ven = exp_info["vendor"]
        oth = exp_info["other"]
        tot_exp = hq + ven + oth
        net_rem = rev - tot_exp
        n_text = "; ".join(exp_info["notes"]) if exp_info["notes"] else "Günlük kasa hasılatı"

        # Mevcut POS tablosundan çekim varsa koru
        cursor.execute("SELECT total_pos FROM canteen_pos_devices WHERE record_date = ?", (d,))
        p_row = cursor.fetchone()
        pos_val = float(p_row[0]) if p_row and p_row[0] else 0.0
        tot_rev_combined = round(rev + pos_val, 2)

        cursor.execute("""
            INSERT INTO canteen_cash_records (
                record_date, cash_revenue, pos_revenue, total_revenue,
                transferred_to_hq, vendor_payouts, other_expenses,
                net_cash_remaining, z_report_no, notes, recorded_by
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            d,
            rev,
            pos_val,
            tot_rev_combined,
            hq,
            ven,
            oth,
            net_rem,
            f"KASA-{d[-5:]}",
            n_text,
            "Erva Yunus"
        ))

    conn.commit()
    conn.close()

    print("[BASARILI] Aktarim tamamlandi:")
    print(f"   - {gelir_count} Gelir kalemi (+1 Devir)")
    print(f"   - {gider_count} Gider kalemi")
    print(f"   - {len(all_dates)} Gunluk mutabakat kaydi")

    trigger_auto_backup()
    return True

if __name__ == "__main__":
    import_september_kasa()
