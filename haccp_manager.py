"""
Florya MEV Koleji - HACCP ve Gıda Güvenliği Yönetim Modülü (haccp_manager.py)
72 Saatlik Şahit Numune Takibi ve Buzdolabı/Depo Sıcaklık Kontrolleri
"""

import sqlite3
import datetime
from typing import List, Dict, Any, Tuple, Optional
import pandas as pd
from database import get_sqlite_connection, trigger_auto_backup

# Tanımlı Cihazlar ve Yasal Sıcaklık Limitleri (HACCP ve Tarım Bakanlığı Standartları)
TEMPERATURE_TARGETS = {
    "Soğuk Hava Deposu (+4°C)": {"min": 0.0, "max": 4.0, "unit": "°C"},
    "Donuk Depo (-18°C)": {"min": -25.0, "max": -18.0, "unit": "°C"},
    "Şahit Numune Dolabı (+4°C)": {"min": 0.0, "max": 4.0, "unit": "°C"},
    "Kuru Gıda Deposu": {"min": 15.0, "max": 22.0, "unit": "°C"},
    "Sıcak Yemek Servis Tezgahı (Benmari)": {"min": 65.0, "max": 95.0, "unit": "°C"},
    "Salatabar / Soğuk Servis Ünitesi": {"min": 0.0, "max": 10.0, "unit": "°C"}
}

MEAL_TYPES = ["Öğle Yemeği", "Sabah Kahvaltısı", "İkindi / Ara Öğün", "Özel Etkinlik"]
TIME_PERIODS = ["Sabah (09:00)", "Öğle (13:00)", "Akşam (17:00)"]

# ==========================================================
# 1. 72 SAATLİK ŞAHİT NUMUNE YÖNETİMİ
# ==========================================================

def add_haccp_sample(meal_name: str, meal_type: str, sample_date: datetime.date,
                     sample_time: str, sample_taken_by: str, notes: str = "") -> Tuple[bool, str]:
    """Yeni bir şahit numune kaydı ekler."""
    if not meal_name or not sample_taken_by:
        return False, "Yemek adı ve numuneyi alan personel bilgisi zorunludur."

    try:
        conn = get_sqlite_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO haccp_samples (
                meal_name, meal_type, sample_date, sample_time,
                sample_taken_by, status, notes
            ) VALUES (?, ?, ?, ?, ?, 'SAKLANIYOR', ?)
        """, (meal_name.strip(), meal_type, sample_date.strftime("%Y-%m-%d"),
              sample_time, sample_taken_by.strip(), notes.strip() if notes else None))
        conn.commit()
        conn.close()
        trigger_auto_backup()
        return True, f"'{meal_name}' numunesi başarıyla 72 saatlik takibe alındı."
    except Exception as e:
        return False, f"Numune ekleme hatası: {e}"

def get_haccp_samples_df(status_filter: str = "Tümü") -> pd.DataFrame:
    """Tüm şahit numuneleri ve kalan yasal saklama sürelerini hesaplayarak döndürür."""
    conn = get_sqlite_connection()
    query = "SELECT * FROM haccp_samples"
    params = []

    if status_filter == "Saklananlar":
        query += " WHERE status = 'SAKLANIYOR'"
    elif status_filter == "İmha Edilenler":
        query += " WHERE status = 'IMHA_EDILDI'"

    query += " ORDER BY sample_date DESC, sample_time DESC"
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()

    if df.empty:
        return df

    # 72 saatlik süre analizi
    now = datetime.datetime.now()
    remaining_hours_list = []
    status_labels = []

    for _, row in df.iterrows():
        if row['status'] == 'IMHA_EDILDI':
            remaining_hours_list.append(0)
            status_labels.append("✅ Güvenle İmha Edildi")
            continue

        try:
            # Alınış anı
            sample_dt_str = f"{row['sample_date']} {row['sample_time']}"
            sample_dt = datetime.datetime.strptime(sample_dt_str, "%Y-%m-%d %H:%M")
            expire_dt = sample_dt + datetime.timedelta(hours=72)
            diff = expire_dt - now
            rem_hours = diff.total_seconds() / 3600.0
            remaining_hours_list.append(round(rem_hours, 1))

            if rem_hours <= 0:
                status_labels.append("🟢 72 Saat Doldu (İmhaya Hazır)")
            elif rem_hours <= 12:
                status_labels.append(f"🟡 Dolmak Üzere ({rem_hours:.1f} sa)")
            else:
                status_labels.append(f"⏳ Saklanıyor ({rem_hours:.1f} sa kaldı)")
        except Exception:
            remaining_hours_list.append(0)
            status_labels.append("Bilinmiyor")

    df['remaining_hours'] = remaining_hours_list
    df['status_label'] = status_labels
    return df

def dispose_sample(sample_id: int, disposed_by: str) -> Tuple[bool, str]:
    """72 saati dolan numuneyi yasal olarak imha edildi şeklinde işaretler."""
    try:
        conn = get_sqlite_connection()
        cursor = conn.cursor()
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
            UPDATE haccp_samples
            SET status = 'IMHA_EDILDI', disposed_at = ?, disposed_by = ?
            WHERE id = ?
        """, (now_str, disposed_by.strip(), sample_id))
        conn.commit()
        conn.close()
        trigger_auto_backup()
        return True, "Numune başarıyla imha edildi olarak kaydedildi."
    except Exception as e:
        return False, f"İmha kaydı hatası: {e}"

# ==========================================================
# 2. DOLAP VE DEPO SICAKLIK TAKİBİ
# ==========================================================

def add_temperature_log(device_name: str, check_date: datetime.date,
                        check_time_period: str, temperature: float,
                        recorded_by: str, action_taken: str = "") -> Tuple[bool, str, bool]:
    """Yeni sıcaklık ölçümü ekler. Güvenli olup olmadığını denetler."""
    if device_name not in TEMPERATURE_TARGETS:
        return False, "Geçersiz cihaz seçimi.", False

    target = TEMPERATURE_TARGETS[device_name]
    t_min = target["min"]
    t_max = target["max"]

    # Sıcaklık yasal sınırlar içinde mi?
    is_safe = 1 if (t_min <= temperature <= t_max) else 0

    try:
        conn = get_sqlite_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO temperature_logs (
                device_name, check_date, check_time_period,
                temperature, target_min, target_max, is_safe,
                action_taken, recorded_by
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            device_name, check_date.strftime("%Y-%m-%d"), check_time_period,
            float(temperature), t_min, t_max, is_safe,
            action_taken.strip() if action_taken else None, recorded_by.strip()
        ))
        conn.commit()
        conn.close()
        trigger_auto_backup()

        if is_safe == 1:
            return True, f"Ölçüm kaydedildi: {temperature}°C (Uygun)", True
        else:
            return True, f"DİKKAT: {temperature}°C yasal sınır ({t_min}°C - {t_max}°C) DIŞINDA!", False
    except Exception as e:
        return False, f"Sıcaklık kaydı hatası: {e}", False

def get_temperature_logs_df(device_filter: str = "Tümü", days: int = 30) -> pd.DataFrame:
    """Son günlere ait sıcaklık kayıtlarını döndürür."""
    conn = get_sqlite_connection()
    cutoff_date = (datetime.datetime.now() - datetime.timedelta(days=days)).strftime("%Y-%m-%d")

    query = "SELECT * FROM temperature_logs WHERE check_date >= ?"
    params = [cutoff_date]

    if device_filter != "Tümü":
        query += " AND device_name = ?"
        params.append(device_filter)

    query += " ORDER BY check_date DESC, check_time_period DESC"
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df
