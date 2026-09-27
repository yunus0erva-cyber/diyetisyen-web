"""
Florya MEV Koleji - Depo ve Stok Takip Sistemi
Stok Yönetimi, Hareketler ve İş Mantığı Modülü
"""

import sqlite3
import datetime
from typing import Optional, Dict, List, Tuple, Any
import pandas as pd
from database import get_sqlite_connection, is_supabase_active, get_supabase_client, trigger_auto_backup

LOCATIONS = [
    "Kuru Depo",
    "Soğuk Hava Deposu (+4°C)",
    "Donuk Depo (-18°C)",
    "Kantin Deposu",
    "Mutfak Hazırlık",
    "Yemekhane Servis"
]

UNITS = [
    "Adet",
    "Kg",
    "Litre",
    "Koli",
    "Teneke",
    "Çuval",
    "Kova",
    "Kalıp",
    "Paket",
    "Blok",
    "Kasa"
]

def get_categories() -> List[str]:
    """Kayıtlı kategori isimlerini döndürür."""
    conn = get_sqlite_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM categories ORDER BY name ASC")
    rows = cursor.fetchall()
    conn.close()
    return [r[0] for r in rows]

def get_products_df(
    search_query: str = "",
    category: str = "Tümü",
    location: str = "Tümü",
    only_low_stock: bool = False
) -> pd.DataFrame:
    """Filtrelere göre ürün listesini Pandas DataFrame olarak döndürür."""
    conn = get_sqlite_connection()
    
    query = """
        SELECT 
            id,
            barcode AS "Barkod",
            product_code AS "Ürün Kodu",
            name AS "Ürün Adı",
            category AS "Kategori",
            unit AS "Birim",
            current_stock AS "Mevcut Stok",
            critical_threshold AS "Kritik Eşik",
            unit_price AS "Birim Fiyat (TL)",
            (current_stock * unit_price) AS "Toplam Değer (TL)",
            storage_location AS "Depo Lokasyonu",
            expiry_date AS "Son Tüketim (SKT)",
            lot_no AS "Parti / Lot No",
            notes AS "Açıklama / Notlar",
            updated_at AS "Son Güncelleme"
        FROM products
        WHERE 1=1
    """
    params = []

    if search_query:
        query += " AND (name LIKE ? OR barcode LIKE ? OR product_code LIKE ? OR lot_no LIKE ?)"
        q = f"%{search_query.strip()}%"
        params.extend([q, q, q, q])

    if category != "Tümü":
        query += " AND category = ?"
        params.append(category)

    if location != "Tümü":
        query += " AND storage_location = ?"
        params.append(location)

    if only_low_stock:
        query += " AND current_stock <= critical_threshold"

    query += " ORDER BY CASE WHEN current_stock <= critical_threshold THEN 0 ELSE 1 END, name ASC"

    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

def get_product_by_id(product_id: int) -> Optional[Dict]:
    """Tek bir ürünün detaylarını döndürür."""
    conn = get_sqlite_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None

def add_product(
    barcode: str,
    product_code: str,
    name: str,
    category: str,
    unit: str,
    initial_stock: float,
    critical_threshold: float,
    unit_price: float,
    storage_location: str,
    expiry_date: Optional[str],
    lot_no: str,
    notes: str,
    user_name: str
) -> Tuple[bool, str]:
    """Yeni bir ürün kartı açar ve açılış stok hareketini kaydeder."""
    if not name.strip():
        return False, "Ürün adı zorunludur!"

    conn = get_sqlite_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO products (
                barcode, product_code, name, category, unit, 
                current_stock, critical_threshold, unit_price, 
                storage_location, expiry_date, lot_no, notes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            barcode.strip() if barcode else None,
            product_code.strip() if product_code else None,
            name.strip(),
            category,
            unit,
            float(initial_stock),
            float(critical_threshold),
            float(unit_price),
            storage_location,
            expiry_date if expiry_date else None,
            lot_no.strip() if lot_no else None,
            notes.strip() if notes else None
        ))
        product_id = cursor.lastrowid

        # Açılış hareketi
        if initial_stock > 0:
            cursor.execute("""
                INSERT INTO stock_movements (
                    product_id, product_name, movement_type, quantity, 
                    previous_stock, new_stock, unit, document_no, reason, created_by
                )
                VALUES (?, ?, 'GİRİŞ', ?, 0, ?, ?, 'YENİ-KART', 'Yeni ürün açılış stoğu', ?)
            """, (product_id, name.strip(), initial_stock, initial_stock, unit, user_name))

        conn.commit()
        trigger_auto_backup()
        return True, "Ürün başarıyla eklendi."
    except sqlite3.IntegrityError:
        return False, f"Bu barkod ({barcode}) ile kayıtlı başka bir ürün zaten var!"
    except Exception as e:
        return False, f"Kayıt hatası: {str(e)}"
    finally:
        conn.close()

def update_product(
    product_id: int,
    barcode: str,
    product_code: str,
    name: str,
    category: str,
    unit: str,
    critical_threshold: float,
    unit_price: float,
    storage_location: str,
    expiry_date: Optional[str],
    lot_no: str,
    notes: str
) -> Tuple[bool, str]:
    """Ürün kartı bilgilerini günceller (stok miktarı buradan değil, hareketlerle değişir)."""
    if not name.strip():
        return False, "Ürün adı zorunludur!"

    conn = get_sqlite_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE products
            SET barcode = ?,
                product_code = ?,
                name = ?,
                category = ?,
                unit = ?,
                critical_threshold = ?,
                unit_price = ?,
                storage_location = ?,
                expiry_date = ?,
                lot_no = ?,
                notes = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (
            barcode.strip() if barcode else None,
            product_code.strip() if product_code else None,
            name.strip(),
            category,
            unit,
            float(critical_threshold),
            float(unit_price),
            storage_location,
            expiry_date if expiry_date else None,
            lot_no.strip() if lot_no else None,
            notes.strip() if notes else None,
            product_id
        ))
        conn.commit()
        trigger_auto_backup()
        return True, "Ürün bilgileri başarıyla güncellendi."
    except sqlite3.IntegrityError:
        return False, f"Bu barkod ({barcode}) başka bir ürüne ait!"
    except Exception as e:
        return False, f"Güncelleme hatası: {str(e)}"
    finally:
        conn.close()

def record_stock_movement(
    product_id: int,
    movement_type: str,
    quantity: float,
    document_no: str,
    reason: str,
    user_name: str
) -> Tuple[bool, str]:
    """
    Stok Girişi, Çıkışı, Sayım Düzeltmesi veya Fire kaydı yapar.
    Mevcut stoğu günceller ve denetim izi (audit log) oluşturur.
    """
    if quantity <= 0:
        return False, "İşlem miktarı sıfırdan büyük olmalıdır!"

    conn = get_sqlite_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT name, current_stock, unit FROM products WHERE id = ?", (product_id,))
        row = cursor.fetchone()
        if not row:
            return False, "Ürün bulunamadı!"

        prod_name = row["name"]
        current_stock = float(row["current_stock"])
        unit = row["unit"]

        if movement_type in ["ÇIKIŞ", "FİRE / İMHA"]:
            if current_stock < quantity:
                return False, f"Yetersiz stok! Mevcut stok: {current_stock} {unit}, Çıkış istenen: {quantity} {unit}"
            new_stock = current_stock - quantity
        elif movement_type == "GİRİŞ":
            new_stock = current_stock + quantity
        elif movement_type == "SAYIM DÜZELTME":
            # Sayım düzeltmede girilen miktar doğrudan yeni stok olarak atanır
            new_stock = quantity
            quantity = abs(new_stock - current_stock)
        else:
            return False, f"Geçersiz hareket türü: {movement_type}"

        # 1. Ürünün mevcut stoğunu güncelle
        cursor.execute("""
            UPDATE products 
            SET current_stock = ?, updated_at = CURRENT_TIMESTAMP 
            WHERE id = ?
        """, (new_stock, product_id))

        # 2. Hareket kaydı ekle
        cursor.execute("""
            INSERT INTO stock_movements (
                product_id, product_name, movement_type, quantity, 
                previous_stock, new_stock, unit, document_no, reason, created_by
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            product_id,
            prod_name,
            movement_type,
            quantity,
            current_stock,
            new_stock,
            unit,
            document_no.strip() if document_no else "BELGESİZ",
            reason.strip() if reason else None,
            user_name
        ))

        conn.commit()
        trigger_auto_backup()
        return True, f"{prod_name} için {movement_type} işlemi kaydedildi. Yeni Stok: {new_stock} {unit}"
    except Exception as e:
        return False, f"İşlem hatası: {str(e)}"
    finally:
        conn.close()

def delete_product(product_id: int) -> Tuple[bool, str]:
    """Ürünü veritabanından siler."""
    conn = get_sqlite_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
        conn.commit()
        trigger_auto_backup()
        return True, "Ürün başarıyla silindi."
    except Exception as e:
        return False, f"Silme hatası: {str(e)}"
    finally:
        conn.close()

def get_low_stock_alerts_df() -> pd.DataFrame:
    """Kritik seviyenin altına düşmüş ürünleri ve gereken sipariş miktarını hesaplar."""
    conn = get_sqlite_connection()
    query = """
        SELECT 
            id,
            barcode AS "Barkod",
            product_code AS "Kod",
            name AS "Ürün Adı",
            category AS "Kategori",
            storage_location AS "Depo Lokasyonu",
            current_stock AS "Mevcut Stok",
            critical_threshold AS "Kritik Eşik",
            unit AS "Birim",
            (critical_threshold - current_stock) AS "Eksik Miktar",
            unit_price AS "Birim Fiyat",
            ((critical_threshold - current_stock) * unit_price) AS "Tahmini Sipariş Tutarı (TL)",
            CASE 
                WHEN current_stock = 0 THEN '🚨 TÜKENDİ (STOK YOK)'
                WHEN current_stock < (critical_threshold * 0.5) THEN '🔴 ÇOK ACİL (KRİTİK)'
                ELSE '🟡 DİKKAT (EŞİK ALTI)'
            END AS "Durum Seviyesi"
        FROM products
        WHERE current_stock <= critical_threshold
        ORDER BY current_stock ASC, (critical_threshold - current_stock) DESC
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def get_expiring_soon_alerts_df(days: int = 30) -> pd.DataFrame:
    """FEFO kuralına göre SKT'si yaklaşan veya geçmiş ürünleri döndürür."""
    conn = get_sqlite_connection()
    query = """
        SELECT 
            id,
            barcode AS "Barkod",
            name AS "Ürün Adı",
            category AS "Kategori",
            storage_location AS "Lokasyon",
            current_stock AS "Stok",
            unit AS "Birim",
            lot_no AS "Parti / Lot",
            expiry_date AS "Son Tüketim (SKT)"
        FROM products
        WHERE expiry_date IS NOT NULL AND expiry_date != '' AND current_stock > 0
        ORDER BY expiry_date ASC
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    if df.empty:
        return df

    today = datetime.date.today()
    df["Son Tüketim (SKT)"] = pd.to_datetime(df["Son Tüketim (SKT)"]).dt.date
    df["Kalan Gün"] = df["Son Tüketim (SKT)"].apply(lambda x: (x - today).days)
    
    # Sadece belirtilen gün eşiğindekileri filtrele
    filtered_df = df[df["Kalan Gün"] <= days].copy()

    def determine_fefo_status(days_left):
        if days_left < 0:
            return f"❌ SKT GEÇTİ ({abs(days_left)} gün önce) - İMHA EDİN"
        elif days_left <= 7:
            return f"🚨 ACİL TÜKETİM / FEFO (Kalan {days_left} gün)"
        elif days_left <= 15:
            return f"⚠️ DİKKAT (Kalan {days_left} gün)"
        else:
            return f"ℹ️ Yaklaşıyor (Kalan {days_left} gün)"

    filtered_df["FEFO Öncelik Durumu"] = filtered_df["Kalan Gün"].apply(determine_fefo_status)
    return filtered_df.sort_values(by="Kalan Gün", ascending=True)

def get_stock_movements_df(limit: int = 200, movement_type: str = "Tümü") -> pd.DataFrame:
    """Stok giriş/çıkış hareket geçmişini Pandas DataFrame olarak döndürür."""
    conn = get_sqlite_connection()
    query = """
        SELECT 
            id,
            created_at AS "Tarih & Saat",
            movement_type AS "Hareket Türü",
            product_name AS "Ürün Adı",
            quantity AS "İşlem Miktarı",
            unit AS "Birim",
            previous_stock AS "Önceki Stok",
            new_stock AS "Kalan Stok",
            document_no AS "İrsaliye / Belge No",
            reason AS "Açıklama",
            created_by AS "İşlemi Yapan"
        FROM stock_movements
        WHERE 1=1
    """
    params = []
    if movement_type != "Tümü":
        query += " AND movement_type = ?"
        params.append(movement_type)

    query += " ORDER BY id DESC LIMIT ?"
    params.append(limit)

    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

def get_inventory_summary_stats() -> Dict[str, Any]:
    """Ana sayfa KPI istatistiklerini hesaplar."""
    conn = get_sqlite_connection()
    cursor = conn.cursor()

    # Toplam ürün çeşidi
    cursor.execute("SELECT COUNT(*) FROM products")
    total_sku = cursor.fetchone()[0]

    # Toplam stok kalemi ve toplam envanter değeri
    cursor.execute("SELECT SUM(current_stock), SUM(current_stock * unit_price) FROM products")
    row_sum = cursor.fetchone()
    total_quantity = row_sum[0] if row_sum[0] else 0.0
    total_value = row_sum[1] if row_sum[1] else 0.0

    # Kritik stok sayısındaki ürünler
    cursor.execute("SELECT COUNT(*) FROM products WHERE current_stock <= critical_threshold")
    critical_count = cursor.fetchone()[0]

    # Stokta tamamen tükenenler
    cursor.execute("SELECT COUNT(*) FROM products WHERE current_stock = 0")
    out_of_stock_count = cursor.fetchone()[0]

    # Bugünkü hareket sayısı
    today_str = datetime.date.today().isoformat()
    cursor.execute("SELECT COUNT(*) FROM stock_movements WHERE DATE(created_at) = ?", (today_str,))
    today_movements = cursor.fetchone()[0]

    conn.close()

    return {
        "total_sku": total_sku,
        "total_quantity": total_quantity,
        "total_value": total_value,
        "critical_count": critical_count,
        "out_of_stock_count": out_of_stock_count,
        "today_movements": today_movements
    }
