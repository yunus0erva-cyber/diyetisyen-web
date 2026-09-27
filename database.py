"""
Florya MEV Koleji - Depo ve Stok Takip Sistemi
Veritabanı Katmanı (SQLite / Supabase Desteği)
"""

import os
import sqlite3
import hashlib
import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
import shutil
import pandas as pd
from dotenv import load_dotenv

# .env dosyasını yükle (varsa)
load_dotenv()

DB_PATH = Path(__file__).parent / "depo_stok.db"
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
DB_TYPE = os.getenv("DB_TYPE", "sqlite").lower()

def trigger_auto_backup():
    """Her veri değişikliğinde anında ve sessizce OneDrive, Google Drive ve D diskine güncel kopyayı aktarır."""
    try:
        if not DB_PATH.exists():
            return
        # 1. OneDrive
        onedrive_base = Path(os.environ.get("OneDrive", r"C:\Users\doruk\OneDrive"))
        onedrive_target = onedrive_base / "Florya_MEV_Yedekler"
        if onedrive_base.exists():
            onedrive_target.mkdir(parents=True, exist_ok=True)
            shutil.copy2(DB_PATH, onedrive_target / "depo_stok_GUNCEL.db")
        # 2. D: Sürücüsü
        d_drive = Path(r"D:\Florya_MEV_Yedekler")
        if Path("D:").exists():
            d_drive.mkdir(parents=True, exist_ok=True)
            shutil.copy2(DB_PATH, d_drive / "depo_stok_GUNCEL.db")
        # 3. Google Drive (Varsa)
        import string
        g_candidates = [
            Path(r"G:\Drive'ım"),
            Path(r"G:\My Drive"),
            Path("G:/"),
            Path(os.path.expanduser(r"~\Google Drive")),
            Path(os.path.expanduser(r"~\My Drive"))
        ]
        for letter in string.ascii_uppercase:
            p1 = Path(f"{letter}:\\Drive'ım")
            p2 = Path(f"{letter}:\\My Drive")
            if p1.exists(): g_candidates.append(p1)
            if p2.exists(): g_candidates.append(p2)
        for gc in g_candidates:
            if gc.exists():
                targets = [gc / "UYGULAMA WEB SİTESİ", gc / "Florya_MEV_Yedekler"]
                for tdir in targets:
                    try:
                        tdir.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(DB_PATH, tdir / "depo_stok_GUNCEL.db")
                    except Exception:
                        pass
                break
    except Exception:
        pass

def get_hash(password: str) -> str:
    """Parolayı SHA-256 ve statik tuz ile hashler."""
    salt = "florya_mev_stok_salt_2026"
    return hashlib.sha256((password + salt).encode('utf-8')).hexdigest()

def get_sqlite_connection():
    """Thread-safe SQLite bağlantısı oluşturur."""
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def get_supabase_client():
    """Supabase istemcisini döndürür (yapılandırılmışsa)."""
    if SUPABASE_URL and SUPABASE_KEY and SUPABASE_URL != "https://your-project.supabase.co":
        try:
            from supabase import create_client
            return create_client(SUPABASE_URL, SUPABASE_KEY)
        except Exception as e:
            print(f"Supabase bağlantı hatası: {e}")
            return None
    return None

def is_supabase_active() -> bool:
    """Supabase'in aktif ve kullanılabilir olup olmadığını kontrol eder."""
    return DB_TYPE == "supabase" and get_supabase_client() is not None

# ==========================================================
# VERİTABANI İLK KURULUM VE TABLO OLUŞTURMA
# ==========================================================

def init_db():
    """SQLite veritabanı tablolarını oluşturur ve başlangıç verilerini yükler."""
    conn = get_sqlite_connection()
    cursor = conn.cursor()

    # 1. Kullanıcılar tablosu
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'personel',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 2. Kategoriler tablosu
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    """)

    # 3. Ürünler tablosu
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            barcode TEXT UNIQUE,
            product_code TEXT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            unit TEXT NOT NULL DEFAULT 'Adet',
            current_stock REAL NOT NULL DEFAULT 0.0,
            critical_threshold REAL NOT NULL DEFAULT 5.0,
            unit_price REAL DEFAULT 0.0,
            storage_location TEXT DEFAULT 'Kuru Depo',
            expiry_date DATE,
            lot_no TEXT,
            notes TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 4. Stok hareketleri tablosu (Audit Log)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stock_movements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            product_name TEXT NOT NULL,
            movement_type TEXT NOT NULL,
            quantity REAL NOT NULL,
            previous_stock REAL NOT NULL,
            new_stock REAL NOT NULL,
            unit TEXT NOT NULL,
            document_no TEXT,
            reason TEXT,
            created_by TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE SET NULL
        )
    """)

    # 5. HACCP 72 Saatlik Şahit Numune Tablosu
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS haccp_samples (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            meal_name TEXT NOT NULL,
            meal_type TEXT NOT NULL DEFAULT 'Öğle Yemeği',
            sample_date DATE NOT NULL,
            sample_time TEXT NOT NULL,
            sample_taken_by TEXT NOT NULL,
            storage_location TEXT DEFAULT 'Şahit Numune Dolabı (+4°C)',
            status TEXT DEFAULT 'SAKLANIYOR',
            disposed_at TIMESTAMP,
            disposed_by TEXT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 6. Buzdolabı ve Depo Sıcaklık Takip Tablosu
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS temperature_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_name TEXT NOT NULL,
            check_date DATE NOT NULL,
            check_time_period TEXT NOT NULL,
            temperature REAL NOT NULL,
            target_min REAL NOT NULL,
            target_max REAL NOT NULL,
            is_safe INTEGER NOT NULL DEFAULT 1,
            action_taken TEXT,
            recorded_by TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 7. Kantin Günlük Kasa & Z Raporu Mutabakat Tablosu
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS canteen_cash_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            record_date DATE NOT NULL,
            cash_revenue REAL NOT NULL DEFAULT 0.0,
            pos_revenue REAL NOT NULL DEFAULT 0.0,
            total_revenue REAL NOT NULL DEFAULT 0.0,
            transferred_to_hq REAL NOT NULL DEFAULT 0.0,
            vendor_payouts REAL NOT NULL DEFAULT 0.0,
            other_expenses REAL NOT NULL DEFAULT 0.0,
            net_cash_remaining REAL NOT NULL DEFAULT 0.0,
            z_report_no TEXT,
            notes TEXT,
            recorded_by TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 8. Kasa Defteri - Tek Tek Gelir ve Gider Hareketleri Tablosu
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS kasa_transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trans_type TEXT NOT NULL,
            trans_date DATE NOT NULL,
            order_no INTEGER,
            description TEXT NOT NULL,
            category TEXT DEFAULT 'Genel',
            amount REAL NOT NULL,
            document_no TEXT,
            notes TEXT,
            recorded_by TEXT NOT NULL DEFAULT 'Erva Yunus',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 9. Kantin POS Cihazları Seri No Bazlı Günlük Takip Tablosu
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS canteen_pos_devices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            record_date DATE UNIQUE NOT NULL,
            day_name TEXT,
            pos_2127 REAL DEFAULT 0.0,
            pos_2128 REAL DEFAULT 0.0,
            pos_9188 REAL DEFAULT 0.0,
            total_pos REAL DEFAULT 0.0,
            notes TEXT,
            recorded_by TEXT NOT NULL DEFAULT 'Erva Yunus',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()

    # Başlangıç kullanıcılarını kontrol et ve ekle
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("""
            INSERT INTO users (username, password_hash, full_name, role)
            VALUES (?, ?, ?, ?)
        """, [
            ("admin", get_hash("admin123"), "Erva Yunus (Yönetici)", "admin"),
            ("depo", get_hash("depo123"), "Ahmet Yılmaz (Depo Sorumlusu)", "personel"),
            ("kantin", get_hash("kantin123"), "Merve Kaya (Kantin Sorumlusu)", "personel")
        ])
        conn.commit()

    # Başlangıç kategorilerini ekle
    cursor.execute("SELECT COUNT(*) FROM categories")
    if cursor.fetchone()[0] == 0:
        default_categories = [
            ("Kuru Gıda & Bakliyat",),
            ("Süt ve Süt Ürünleri",),
            ("Et ve Şarküteri",),
            ("Sıvı Yağlar",),
            ("Kantin İçecek",),
            ("Kantin Atıştırmalık",),
            ("Temizlik ve Hijyen",),
            ("Ambalaj ve Sarf",)
        ]
        cursor.executemany("INSERT INTO categories (name) VALUES (?)", default_categories)
        conn.commit()

    conn.close()

# Otomatik olarak modül ilk yüklendiğinde tabloları oluştur
init_db()
