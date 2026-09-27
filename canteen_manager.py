"""
Florya MEV Koleji - Kantin Günlük Kasa & Z Raporu Mutabakat Yöneticisi (canteen_manager.py)
"""

import sqlite3
import pandas as pd
import datetime
from pathlib import Path
from database import get_sqlite_connection, trigger_auto_backup

def get_day_financial_snapshot(record_date: str):
    """Belirli bir güne ait tüm tablolardaki (POS, Kasa Defteri, Kasa Çizelgesi) mevcut verileri çeker."""
    conn = get_sqlite_connection()
    cursor = conn.cursor()

    # POS tablosundan çek
    cursor.execute("""
        SELECT pos_2127, pos_2128, pos_9188, total_pos, day_name, notes
        FROM canteen_pos_devices WHERE record_date = ?
    """, (record_date,))
    pos_row = cursor.fetchone()
    pos_data = {
        "pos_2127": float(pos_row[0]) if pos_row and pos_row[0] else 0.0,
        "pos_2128": float(pos_row[1]) if pos_row and pos_row[1] else 0.0,
        "pos_9188": float(pos_row[2]) if pos_row and pos_row[2] else 0.0,
        "total_pos": float(pos_row[3]) if pos_row and pos_row[3] else 0.0,
        "day_name": pos_row[4] if pos_row else "",
        "notes": pos_row[5] if pos_row else ""
    }

    # Kasa çizelgesi tablosundan çek
    cursor.execute("""
        SELECT cash_revenue, pos_revenue, total_revenue, transferred_to_hq, vendor_payouts, other_expenses, net_cash_remaining, z_report_no, notes, recorded_by
        FROM canteen_cash_records WHERE record_date = ?
    """, (record_date,))
    cash_row = cursor.fetchone()
    cash_data = {
        "cash_revenue": float(cash_row[0]) if cash_row and cash_row[0] else 0.0,
        "pos_revenue": float(cash_row[1]) if cash_row and cash_row[1] else 0.0,
        "total_revenue": float(cash_row[2]) if cash_row and cash_row[2] else 0.0,
        "transferred_to_hq": float(cash_row[3]) if cash_row and cash_row[3] else 0.0,
        "vendor_payouts": float(cash_row[4]) if cash_row and cash_row[4] else 0.0,
        "other_expenses": float(cash_row[5]) if cash_row and cash_row[5] else 0.0,
        "net_cash_remaining": float(cash_row[6]) if cash_row and cash_row[6] else 0.0,
        "z_report_no": cash_row[7] if cash_row and cash_row[7] else "",
        "notes": cash_row[8] if cash_row and cash_row[8] else "",
        "recorded_by": cash_row[9] if cash_row and cash_row[9] else "Kantin Sorumlusu"
    }

    conn.close()
    return pos_data, cash_data

def sync_cash_and_pos_for_date(record_date: str):
    """
    Belirli bir gün için tüm sekmelerin (POS, Kasa Defteri, Günlük Kasa Çizelgesi)
    verilerini tek bir çatı altında birleştirip eksiksiz eşitler.
    """
    conn = get_sqlite_connection()
    cursor = conn.cursor()

    # 1. POS Cihazları toplamını al
    cursor.execute("SELECT total_pos FROM canteen_pos_devices WHERE record_date = ?", (record_date,))
    p_row = cursor.fetchone()
    total_pos = float(p_row[0]) if p_row and p_row[0] is not None else 0.0

    # 2. Mevcut Kasa Çizelgesi kaydını al
    cursor.execute("""
        SELECT id, cash_revenue, transferred_to_hq, vendor_payouts, other_expenses, z_report_no, notes, recorded_by
        FROM canteen_cash_records WHERE record_date = ?
    """, (record_date,))
    c_row = cursor.fetchone()

    # 3. Kasa Defteri'ndeki (kasa_transactions) toplamları al
    cursor.execute("""
        SELECT 
            COALESCE(SUM(CASE WHEN trans_type = 'GELİR' AND description NOT LIKE '%DEVİR%' THEN amount ELSE 0 END), 0.0),
            COALESCE(SUM(CASE WHEN trans_type = 'GİDER' AND (category = 'Merkeze Teslim' OR description LIKE '%MERKEZ%') THEN amount ELSE 0 END), 0.0),
            COALESCE(SUM(CASE WHEN trans_type = 'GİDER' AND (category = 'Tedarikçi Ödemesi' OR description LIKE '%TATLI%') THEN amount ELSE 0 END), 0.0),
            COALESCE(SUM(CASE WHEN trans_type = 'GİDER' AND category NOT IN ('Merkeze Teslim', 'Tedarikçi Ödemesi') AND description NOT LIKE '%MERKEZ%' AND description NOT LIKE '%TATLI%' THEN amount ELSE 0 END), 0.0)
        FROM kasa_transactions
        WHERE trans_date = ?
    """, (record_date,))
    ledger_row = cursor.fetchone()
    led_cash = float(ledger_row[0]) if ledger_row else 0.0
    led_hq = float(ledger_row[1]) if ledger_row else 0.0
    led_ven = float(ledger_row[2]) if ledger_row else 0.0
    led_oth = float(ledger_row[3]) if ledger_row else 0.0

    if c_row:
        rec_id, cur_cash, cur_hq, cur_ven, cur_oth, cur_zno, cur_notes, cur_by = c_row
        final_cash = led_cash if led_cash > 0 else float(cur_cash or 0.0)
        final_hq = led_hq if led_hq > 0 else float(cur_hq or 0.0)
        final_ven = led_ven if led_ven > 0 else float(cur_ven or 0.0)
        final_oth = led_oth if led_oth > 0 else float(cur_oth or 0.0)

        final_tot_rev = round(final_cash + total_pos, 2)
        final_net = round(final_cash - (final_hq + final_ven + final_oth), 2)

        cursor.execute("""
            UPDATE canteen_cash_records
            SET cash_revenue = ?,
                pos_revenue = ?,
                total_revenue = ?,
                transferred_to_hq = ?,
                vendor_payouts = ?,
                other_expenses = ?,
                net_cash_remaining = ?
            WHERE id = ?
        """, (final_cash, total_pos, final_tot_rev, final_hq, final_ven, final_oth, final_net, rec_id))
    else:
        # Eğer çizelgede satır yok ama POS veya Defterde kayıt varsa, çizelgeye ekle
        if total_pos > 0 or led_cash > 0 or led_hq > 0 or led_ven > 0 or led_oth > 0:
            final_tot_rev = round(led_cash + total_pos, 2)
            final_net = round(led_cash - (led_hq + led_ven + led_oth), 2)
            cursor.execute("""
                INSERT INTO canteen_cash_records (
                    record_date, cash_revenue, pos_revenue, total_revenue,
                    transferred_to_hq, vendor_payouts, other_expenses,
                    net_cash_remaining, z_report_no, notes, recorded_by
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, '', 'Otomatik senkronize kayıt', 'Sistem')
            """, (record_date, led_cash, total_pos, final_tot_rev, led_hq, led_ven, led_oth, final_net))

    conn.commit()
    conn.close()

def add_canteen_cash_record(
    record_date: str,
    cash_revenue: float,
    pos_revenue: float,
    transferred_to_hq: float = 0.0,
    vendor_payouts: float = 0.0,
    other_expenses: float = 0.0,
    z_report_no: str = "",
    notes: str = "",
    recorded_by: str = "Kantin Sorumlusu"
):
    """
    Yeni bir günlük kasa ve Z raporu kaydı ekler veya günceller.
    POS Cihazları ve Kasa Defteri ile çift yönlü otomatik senkronizasyon sağlar.
    """
    cash_revenue = float(cash_revenue) if cash_revenue else 0.0
    pos_revenue = float(pos_revenue) if pos_revenue else 0.0
    transferred_to_hq = float(transferred_to_hq) if transferred_to_hq else 0.0
    vendor_payouts = float(vendor_payouts) if vendor_payouts else 0.0
    other_expenses = float(other_expenses) if other_expenses else 0.0

    conn = get_sqlite_connection()
    cursor = conn.cursor()

    # 1. Eğer POS girilmediyse (0 ise) POS tablosundan çek
    if pos_revenue == 0.0:
        cursor.execute("SELECT total_pos FROM canteen_pos_devices WHERE record_date = ?", (record_date,))
        row_pos = cursor.fetchone()
        if row_pos and row_pos[0]:
            pos_revenue = float(row_pos[0])
    elif pos_revenue > 0:
        # Eğer kullanıcı burada POS girdi ama POS tablosunda o günün kaydı yoksa veya 0 ise, POS tablosuna da işle
        cursor.execute("SELECT total_pos FROM canteen_pos_devices WHERE record_date = ?", (record_date,))
        row_p = cursor.fetchone()
        if not row_p or float(row_p[0] or 0.0) == 0.0:
            dt_obj = datetime.date.fromisoformat(record_date)
            day_names_tr = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
            d_name = day_names_tr[dt_obj.weekday()]
            cursor.execute("""
                INSERT INTO canteen_pos_devices (
                    record_date, day_name, pos_2127, pos_2128, pos_9188, total_pos, notes, recorded_by
                ) VALUES (?, ?, ?, 0.0, 0.0, ?, ?, ?)
                ON CONFLICT(record_date) DO UPDATE SET
                    pos_2127 = excluded.pos_2127,
                    total_pos = excluded.total_pos,
                    notes = excluded.notes
            """, (record_date, d_name, pos_revenue, pos_revenue, f"Kasa Girişinden Aktarıldı ({z_report_no})", recorded_by))

    total_revenue = round(cash_revenue + pos_revenue, 2)
    net_cash_remaining = round(cash_revenue - (transferred_to_hq + vendor_payouts + other_expenses), 2)

    # 2. Günlük Kasa Çizelgesi'nde mükerrer satır oluşmasın; varsa güncelle, yoksa ekle
    cursor.execute("SELECT id FROM canteen_cash_records WHERE record_date = ?", (record_date,))
    existing_row = cursor.fetchone()

    if existing_row:
        cursor.execute("""
            UPDATE canteen_cash_records
            SET cash_revenue = ?,
                pos_revenue = ?,
                total_revenue = ?,
                transferred_to_hq = ?,
                vendor_payouts = ?,
                other_expenses = ?,
                net_cash_remaining = ?,
                z_report_no = COALESCE(NULLIF(?, ''), z_report_no),
                notes = COALESCE(NULLIF(?, ''), notes),
                recorded_by = ?
            WHERE id = ?
        """, (cash_revenue, pos_revenue, total_revenue, transferred_to_hq, vendor_payouts, other_expenses, net_cash_remaining, z_report_no, notes, recorded_by, existing_row[0]))
    else:
        cursor.execute("""
            INSERT INTO canteen_cash_records (
                record_date, cash_revenue, pos_revenue, total_revenue,
                transferred_to_hq, vendor_payouts, other_expenses,
                net_cash_remaining, z_report_no, notes, recorded_by
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (record_date, cash_revenue, pos_revenue, total_revenue, transferred_to_hq, vendor_payouts, other_expenses, net_cash_remaining, z_report_no, notes, recorded_by))

    # 3. Kasa Defteri (kasa_transactions) ile de senkronize et
    # 3a. Nakit Gelir
    if cash_revenue > 0:
        cursor.execute("SELECT id FROM kasa_transactions WHERE trans_date = ? AND trans_type = 'GELİR' AND description NOT LIKE '%DEVİR%'", (record_date,))
        g_row = cursor.fetchone()
        if g_row:
            cursor.execute("UPDATE kasa_transactions SET amount = ?, notes = ? WHERE id = ?", (cash_revenue, f"Z No: {z_report_no}", g_row[0]))
        else:
            cursor.execute("""
                INSERT INTO kasa_transactions (trans_type, trans_date, description, category, amount, notes, recorded_by)
                VALUES ('GELİR', ?, 'TÜM KASALAR', 'Günlük Hasılat', ?, ?, ?)
            """, (record_date, cash_revenue, f"Z No: {z_report_no}", recorded_by))

    # 3b. Merkeze Teslim
    if transferred_to_hq > 0:
        cursor.execute("SELECT id FROM kasa_transactions WHERE trans_date = ? AND trans_type = 'GİDER' AND (category = 'Merkeze Teslim' OR description LIKE '%MERKEZ%')", (record_date,))
        hq_row = cursor.fetchone()
        if hq_row:
            cursor.execute("UPDATE kasa_transactions SET amount = ? WHERE id = ?", (transferred_to_hq, hq_row[0]))
        else:
            cursor.execute("""
                INSERT INTO kasa_transactions (trans_type, trans_date, description, category, amount, notes, recorded_by)
                VALUES ('GİDER', ?, 'MERKEZE GÖNDERİLDİ', 'Merkeze Teslim', ?, '', ?)
            """, (record_date, transferred_to_hq, recorded_by))

    # 3c. Tedarikçi Ödemesi
    if vendor_payouts > 0:
        cursor.execute("SELECT id FROM kasa_transactions WHERE trans_date = ? AND trans_type = 'GİDER' AND (category = 'Tedarikçi Ödemesi' OR description LIKE '%TATLI%')", (record_date,))
        v_row = cursor.fetchone()
        if v_row:
            cursor.execute("UPDATE kasa_transactions SET amount = ? WHERE id = ?", (vendor_payouts, v_row[0]))
        else:
            cursor.execute("""
                INSERT INTO kasa_transactions (trans_type, trans_date, description, category, amount, notes, recorded_by)
                VALUES ('GİDER', ?, 'TATLICIYA VERİLDİ', 'Tedarikçi Ödemesi', ?, '', ?)
            """, (record_date, vendor_payouts, recorded_by))

    # 3d. Diğer Giderler
    if other_expenses > 0:
        cursor.execute("SELECT id FROM kasa_transactions WHERE trans_date = ? AND trans_type = 'GİDER' AND category NOT IN ('Merkeze Teslim', 'Tedarikçi Ödemesi') AND description NOT LIKE '%MERKEZ%' AND description NOT LIKE '%TATLI%'", (record_date,))
        o_row = cursor.fetchone()
        if o_row:
            cursor.execute("UPDATE kasa_transactions SET amount = ? WHERE id = ?", (other_expenses, o_row[0]))
        else:
            cursor.execute("""
                INSERT INTO kasa_transactions (trans_type, trans_date, description, category, amount, notes, recorded_by)
                VALUES ('GİDER', ?, 'DİĞER GİDERLER', 'Resmi / Kurum Harcaması', ?, '', ?)
            """, (record_date, other_expenses, recorded_by))

    conn.commit()
    conn.close()

    # Çift yönlü kontrol
    sync_cash_and_pos_for_date(record_date)

    # Otomatik Bulut Yedekleme Tetikle
    trigger_auto_backup()
    return True

def get_canteen_records_df(start_date: str = None, end_date: str = None) -> pd.DataFrame:
    """Kasa kayıtlarını filtreli veya tüm liste olarak DataFrame formatında döndürür."""
    conn = get_sqlite_connection()
    query = "SELECT * FROM canteen_cash_records"
    params = []

    if start_date and end_date:
        query += " WHERE record_date BETWEEN ? AND ?"
        params.extend([start_date, end_date])
    elif start_date:
        query += " WHERE record_date >= ?"
        params.append(start_date)
    elif end_date:
        query += " WHERE record_date <= ?"
        params.append(end_date)

    query += " ORDER BY record_date DESC, id DESC"

    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

def delete_canteen_record(record_id: int):
    """Bir kasa kaydını siler ve otomatik yedeklemeyi tetikler."""
    conn = get_sqlite_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM canteen_cash_records WHERE id = ?", (record_id,))
    conn.commit()
    conn.close()
    trigger_auto_backup()
    return True

def get_canteen_summary_stats():
    """Kantin cirosu ve kasa durumuna ait KPI istatistiklerini hesaplar."""
    conn = get_sqlite_connection()
    cursor = conn.cursor()

    today_str = datetime.date.today().strftime("%Y-%m-%d")
    current_month_prefix = datetime.date.today().strftime("%Y-%m")

    # Bugünün durumu
    cursor.execute("""
        SELECT SUM(cash_revenue), SUM(pos_revenue), SUM(total_revenue), SUM(net_cash_remaining)
        FROM canteen_cash_records WHERE record_date = ?
    """, (today_str,))
    today_res = cursor.fetchone()
    today_cash = (today_res[0] if today_res and today_res[0] else 0.0)
    today_pos = (today_res[1] if today_res and today_res[1] else 0.0)
    today_total = (today_res[2] if today_res and today_res[2] else 0.0)
    today_net = (today_res[3] if today_res and today_res[3] else 0.0)

    # Bu ayın durumu
    cursor.execute("""
        SELECT SUM(total_revenue), SUM(cash_revenue), SUM(pos_revenue), SUM(transferred_to_hq), SUM(vendor_payouts + other_expenses)
        FROM canteen_cash_records WHERE record_date LIKE ?
    """, (f"{current_month_prefix}%",))
    month_res = cursor.fetchone()
    month_total = (month_res[0] if month_res and month_res[0] else 0.0)
    month_cash = (month_res[1] if month_res and month_res[1] else 0.0)
    month_pos = (month_res[2] if month_res and month_res[2] else 0.0)
    month_transferred = (month_res[3] if month_res and month_res[3] else 0.0)
    month_expenses = (month_res[4] if month_res and month_res[4] else 0.0)

    # Kasa Defterindeki guncel net bakiye (devir dahil gercek kasadaki nakit para)
    cursor.execute("""
        SELECT 
            COALESCE(SUM(CASE WHEN trans_type = 'GELİR' THEN amount ELSE 0 END), 0.0) -
            COALESCE(SUM(CASE WHEN trans_type = 'GİDER' THEN amount ELSE 0 END), 0.0)
        FROM kasa_transactions
        WHERE trans_date LIKE ?
    """, (f"{current_month_prefix}%",))
    ledger_net_row = cursor.fetchone()
    current_cash_balance = float(ledger_net_row[0]) if ledger_net_row else 0.0

    conn.close()

    return {
        "today_total": today_total,
        "today_cash": today_cash,
        "today_pos": today_pos,
        "today_net": today_net,
        "current_cash_balance": current_cash_balance,
        "month_total": month_total,
        "month_cash": month_cash,
        "month_pos": month_pos,
        "month_transferred": month_transferred,
        "month_expenses": month_expenses
    }

# ==========================================================
# TEKİL GELİR & GİDER HAREKETLERİ (KASA DEFTERİ)
# ==========================================================

def add_kasa_transaction(
    trans_type: str,
    trans_date: str,
    description: str,
    amount: float,
    category: str = "Genel",
    order_no: int = None,
    document_no: str = "",
    notes: str = "",
    recorded_by: str = "Erva Yunus"
):
    """Kasa defterine tekil gelir veya gider kaydı ekler."""
    conn = get_sqlite_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO kasa_transactions (
            trans_type, trans_date, order_no, description, category,
            amount, document_no, notes, recorded_by
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        trans_type.upper(),
        trans_date,
        order_no,
        description,
        category,
        float(amount),
        document_no,
        notes,
        recorded_by
    ))
    conn.commit()
    conn.close()

    # Günlük Kasa Çizelgesi'ni anında otomatik senkronize et
    sync_cash_and_pos_for_date(trans_date)

    trigger_auto_backup()
    return True

def get_kasa_transactions_df(month_prefix: str = None) -> pd.DataFrame:
    """Kasa hareketlerini döndürür."""
    conn = get_sqlite_connection()
    query = "SELECT * FROM kasa_transactions"
    params = []
    if month_prefix:
        query += " WHERE trans_date LIKE ?"
        params.append(f"{month_prefix}%")
    query += " ORDER BY trans_type DESC, trans_date ASC, order_no ASC, id ASC"
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

def get_kasa_ledger_summary(month_prefix: str = "2026-09"):
    """Seçili ay için toplam gelir, toplam gider ve bakiye özetini döndürür."""
    df = get_kasa_transactions_df(month_prefix)
    if df.empty:
        return {"total_gelir": 0.0, "total_gider": 0.0, "net_bakiye": 0.0, "count_gelir": 0, "count_gider": 0}

    gelirler = df[df["trans_type"] == "GELİR"]
    giderler = df[df["trans_type"] == "GİDER"]

    tot_gelir = float(gelirler["amount"].sum())
    tot_gider = float(giderler["amount"].sum())
    net = tot_gelir - tot_gider
    return {
        "total_gelir": tot_gelir,
        "total_gider": tot_gider,
        "net_bakiye": net,
        "count_gelir": len(gelirler),
        "count_gider": len(giderler)
    }

def delete_kasa_transaction(record_id: int):
    conn = get_sqlite_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT trans_date FROM kasa_transactions WHERE id = ?", (record_id,))
    row = cursor.fetchone()
    trans_date = row[0] if row else None

    cursor.execute("DELETE FROM kasa_transactions WHERE id = ?", (record_id,))
    conn.commit()
    conn.close()

    if trans_date:
        sync_cash_and_pos_for_date(trans_date)

    trigger_auto_backup()
    return True

# ==========================================================
# POS CİHAZLARI SERİ NO BAZLI GÜNLÜK TAKİP
# ==========================================================

POS_DEVICES = {
    "PAV210002127": {"name": "1. POS Cihazı (Ana Kasa)", "color": "#3b82f6"},
    "PAV210002128": {"name": "2. POS Cihazı (Hızlı Kasa)", "color": "#10b981"},
    "PAV210009188": {"name": "3. POS Cihazı (Mobil / Yedek)", "color": "#8b5cf6"}
}

def add_or_update_pos_record(
    record_date: str,
    day_name: str,
    pos_2127: float = 0.0,
    pos_2128: float = 0.0,
    pos_9188: float = 0.0,
    notes: str = "",
    recorded_by: str = "Erva Yunus"
):
    """Günlük POS cihazları hasılatını kaydeder veya günceller."""
    pos_2127 = float(pos_2127) if pos_2127 else 0.0
    pos_2128 = float(pos_2128) if pos_2128 else 0.0
    pos_9188 = float(pos_9188) if pos_9188 else 0.0
    total_pos = round(pos_2127 + pos_2128 + pos_9188, 2)

    conn = get_sqlite_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO canteen_pos_devices (
            record_date, day_name, pos_2127, pos_2128, pos_9188, total_pos, notes, recorded_by
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(record_date) DO UPDATE SET
            day_name = excluded.day_name,
            pos_2127 = excluded.pos_2127,
            pos_2128 = excluded.pos_2128,
            pos_9188 = excluded.pos_9188,
            total_pos = excluded.total_pos,
            notes = excluded.notes,
            recorded_by = excluded.recorded_by
    """, (
        record_date, day_name, pos_2127, pos_2128, pos_9188, total_pos, notes, recorded_by
    ))
    conn.commit()
    conn.close()

    # Günlük Kasa Çizelgesi'ni anında ve eksiksiz otomatik güncelle
    sync_cash_and_pos_for_date(record_date)

    trigger_auto_backup()
    return True

def get_pos_records_df(month_prefix: str = None) -> pd.DataFrame:
    """POS kayıtlarını döndürür."""
    conn = get_sqlite_connection()
    query = "SELECT * FROM canteen_pos_devices"
    params = []
    if month_prefix:
        query += " WHERE record_date LIKE ?"
        params.append(f"{month_prefix}%")
    query += " ORDER BY record_date ASC, id ASC"
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

def get_pos_summary_stats(month_prefix: str = "2026-09"):
    """Seçili ayın POS cihazları bazında toplamlarını döndürür."""
    df = get_pos_records_df(month_prefix)
    if df.empty:
        return {
            "total_2127": 0.0,
            "total_2128": 0.0,
            "total_9188": 0.0,
            "grand_total": 0.0,
            "active_days": 0
        }
    return {
        "total_2127": float(df["pos_2127"].sum()),
        "total_2128": float(df["pos_2128"].sum()),
        "total_9188": float(df["pos_9188"].sum()),
        "grand_total": float(df["total_pos"].sum()),
        "active_days": int((df["total_pos"] > 0).sum())
    }
