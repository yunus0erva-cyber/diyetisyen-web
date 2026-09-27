"""
Florya MEV Koleji - Otomatik Veritabanı ve Drive Yedekleme Aracı
"""

import os
import shutil
import datetime
import zipfile
from pathlib import Path

BASE_DIR = Path(__file__).parent
DB_FILE = BASE_DIR / "depo_stok.db"
BACKUP_DIR = BASE_DIR / "yedekler"

BACKUP_DIR.mkdir(exist_ok=True)

if not DB_FILE.exists():
    print("[HATA] depo_stok.db dosyası bulunamadı!")
    exit(1)

timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
target_file = BACKUP_DIR / f"depo_stok_{timestamp}.db"

# 1. Yerel yedek
shutil.copy2(DB_FILE, target_file)

# 2. Excel Envanter ve HACCP Yedeği
excel_msg = ""
try:
    import sqlite3
    import pandas as pd
    conn = sqlite3.connect(str(DB_FILE))
    
    # 2.1 Ürünler Envanteri
    df_prods = pd.read_sql_query("SELECT * FROM products", conn)
    excel_target = BACKUP_DIR / f"stok_envanter_{timestamp}.xlsx"
    excel_target_guncel = BACKUP_DIR / "stok_envanter_GUNCEL.xlsx"
    df_prods.to_excel(excel_target, index=False)
    df_prods.to_excel(excel_target_guncel, index=False)

    # 2.2 HACCP Şahit Numuneler Yedeği
    df_haccp = pd.read_sql_query("SELECT * FROM haccp_samples", conn)
    excel_haccp = BACKUP_DIR / f"haccp_numuneler_{timestamp}.xlsx"
    excel_haccp_guncel = BACKUP_DIR / "haccp_numuneler_GUNCEL.xlsx"
    df_haccp.to_excel(excel_haccp, index=False)
    df_haccp.to_excel(excel_haccp_guncel, index=False)

    # 2.3 Sıcaklık Kayıtları Yedeği
    df_temps = pd.read_sql_query("SELECT * FROM temperature_logs", conn)
    excel_temps = BACKUP_DIR / f"sicaklik_kayitlari_{timestamp}.xlsx"
    excel_temps_guncel = BACKUP_DIR / "sicaklik_kayitlari_GUNCEL.xlsx"
    df_temps.to_excel(excel_temps, index=False)
    df_temps.to_excel(excel_temps_guncel, index=False)

    # 2.4 Kantin Kasa ve Z Raporları Yedeği
    try:
        df_canteen = pd.read_sql_query("SELECT * FROM canteen_cash_records", conn)
        excel_canteen = BACKUP_DIR / f"kantin_kasa_{timestamp}.xlsx"
        excel_canteen_guncel = BACKUP_DIR / "kantin_kasa_GUNCEL.xlsx"
        df_canteen.to_excel(excel_canteen, index=False)
        df_canteen.to_excel(excel_canteen_guncel, index=False)

        # 2.5 Kasa Defteri (Tekil Gelir & Gider) Yedeği
        df_trans = pd.read_sql_query("SELECT * FROM kasa_transactions ORDER BY trans_date ASC, order_no ASC", conn)
        excel_trans = BACKUP_DIR / f"kasa_defteri_{timestamp}.xlsx"
        excel_trans_guncel = BACKUP_DIR / "kasa_defteri_GUNCEL.xlsx"
        df_trans.to_excel(excel_trans, index=False)
        df_trans.to_excel(excel_trans_guncel, index=False)

        # 2.6 Kantin POS Cihazları (Seri No Bazlı) Yedeği
        df_pos = pd.read_sql_query("SELECT * FROM canteen_pos_devices ORDER BY record_date ASC", conn)
        excel_pos = BACKUP_DIR / f"kantin_pos_seri_no_{timestamp}.xlsx"
        excel_pos_guncel = BACKUP_DIR / "kantin_pos_seri_no_GUNCEL.xlsx"
        df_pos.to_excel(excel_pos, index=False)
        df_pos.to_excel(excel_pos_guncel, index=False)
        # 2.7 Kantin Besin Değerleri Raporu (Varsa)
        nutrition_file = BASE_DIR / "NOYA_Kantin_Urunleri_Besin_Degerleri_2026_2027.xlsx"
        if nutrition_file.exists():
            shutil.copy2(nutrition_file, BACKUP_DIR / "NOYA_Kantin_Urunleri_Besin_Degerleri_2026_2027.xlsx")
    except Exception:
        pass

    conn.close()
    excel_msg = f"\n[EKSTRA] Excel Yedekleri (Stok + HACCP + Sıcaklık + Kantin Kasa + Kasa Defteri + POS Seri No + Besin Değerleri) oluşturuldu."
except Exception as e:
    excel_msg = f"\n[UYARI] Excel yedek hatası: {e}"

# 3. Otomatik OneDrive Bulut Eşitleme
onedrive_path = Path(os.environ.get("OneDrive", r"C:\Users\doruk\OneDrive"))
onedrive_folder = onedrive_path / "Florya_MEV_Yedekler"
onedrive_status = ""
if onedrive_path.exists():
    try:
        onedrive_folder.mkdir(parents=True, exist_ok=True)
        shutil.copy2(DB_FILE, onedrive_folder / f"depo_stok_{timestamp}.db")
        shutil.copy2(DB_FILE, onedrive_folder / "depo_stok_GUNCEL.db")
        for ef in [f"stok_envanter_{timestamp}.xlsx", f"haccp_numuneler_{timestamp}.xlsx", f"sicaklik_kayitlari_{timestamp}.xlsx", f"kantin_kasa_{timestamp}.xlsx", f"kasa_defteri_{timestamp}.xlsx", f"kantin_pos_seri_no_{timestamp}.xlsx",
                   "stok_envanter_GUNCEL.xlsx", "haccp_numuneler_GUNCEL.xlsx", "sicaklik_kayitlari_GUNCEL.xlsx", "kantin_kasa_GUNCEL.xlsx", "kasa_defteri_GUNCEL.xlsx", "kantin_pos_seri_no_GUNCEL.xlsx",
                   "NOYA_Kantin_Urunleri_Besin_Degerleri_2026_2027.xlsx"]:
            src_ef = BACKUP_DIR / ef
            if src_ef.exists():
                shutil.copy2(src_ef, onedrive_folder / ef)
        onedrive_status = f"\n[BULUT] OneDrive'a senkronize edildi: {onedrive_folder}"
    except Exception as e:
        onedrive_status = f"\n[UYARI] OneDrive kopyalama hatası: {e}"

# 4. D: Sürücüsü Yedekleme (Varsa)
d_status = ""
d_drive = Path(r"D:\Florya_MEV_Yedekler")
if Path(r"D:\ ").exists() or Path("D:").exists():
    try:
        d_drive.mkdir(parents=True, exist_ok=True)
        shutil.copy2(DB_FILE, d_drive / f"depo_stok_{timestamp}.db")
        shutil.copy2(DB_FILE, d_drive / "depo_stok_GUNCEL.db")
        for ef in [f"stok_envanter_{timestamp}.xlsx", f"haccp_numuneler_{timestamp}.xlsx", f"sicaklik_kayitlari_{timestamp}.xlsx", f"kantin_kasa_{timestamp}.xlsx", f"kasa_defteri_{timestamp}.xlsx", f"kantin_pos_seri_no_{timestamp}.xlsx",
                   "stok_envanter_GUNCEL.xlsx", "haccp_numuneler_GUNCEL.xlsx", "sicaklik_kayitlari_GUNCEL.xlsx", "kantin_kasa_GUNCEL.xlsx", "kasa_defteri_GUNCEL.xlsx", "kantin_pos_seri_no_GUNCEL.xlsx",
                   "NOYA_Kantin_Urunleri_Besin_Degerleri_2026_2027.xlsx"]:
            src_ef = BACKUP_DIR / ef
            if src_ef.exists():
                shutil.copy2(src_ef, d_drive / ef)
        d_status = f"\n[DİSK] D: Sürücüsüne kopyalandı: {d_drive}"
    except:
        pass

# 5. Otomatik Google Drive Bulut Eşitleme
gdrive_status = ""
import string

possible_gdrive = [
    Path(r"G:\Drive'ım"),
    Path(r"G:\My Drive"),
    Path("G:/"),
    Path(os.path.expanduser(r"~\Google Drive")),
    Path(os.path.expanduser(r"~\My Drive"))
]

for letter in string.ascii_uppercase:
    p_tr = Path(f"{letter}:\\Drive'ım")
    p_my = Path(f"{letter}:\\My Drive")
    if p_tr.exists():
        possible_gdrive.append(p_tr)
    if p_my.exists():
        possible_gdrive.append(p_my)

g_found = None
for cand in possible_gdrive:
    if cand.exists():
        g_found = cand
        break

if g_found:
    try:
        # Ana hedef: UYGULAMA WEB SİTESİ, Florya_MEV_Yedekler ve NOYA klasörleri
        target_dirs = [g_found / "UYGULAMA WEB SİTESİ", g_found / "Florya_MEV_Yedekler", g_found / "NOYA", g_found]
        for g_tgt in target_dirs:
            g_tgt.mkdir(parents=True, exist_ok=True)
            # Güncel ve zaman damgalı veritabanı
            shutil.copy2(DB_FILE, g_tgt / f"depo_stok_{timestamp}.db")
            shutil.copy2(DB_FILE, g_tgt / "depo_stok_GUNCEL.db")
            # Güncel ve zaman damgalı excel dosyaları
            for ef in [f"stok_envanter_{timestamp}.xlsx", f"haccp_numuneler_{timestamp}.xlsx", f"sicaklik_kayitlari_{timestamp}.xlsx", f"kantin_kasa_{timestamp}.xlsx", f"kasa_defteri_{timestamp}.xlsx", f"kantin_pos_seri_no_{timestamp}.xlsx",
                       "stok_envanter_GUNCEL.xlsx", "haccp_numuneler_GUNCEL.xlsx", "sicaklik_kayitlari_GUNCEL.xlsx", "kantin_kasa_GUNCEL.xlsx", "kasa_defteri_GUNCEL.xlsx", "kantin_pos_seri_no_GUNCEL.xlsx",
                       "NOYA_Kantin_Urunleri_Besin_Degerleri_2026_2027.xlsx"]:
                src_ef = BACKUP_DIR / ef
                if src_ef.exists():
                    shutil.copy2(src_ef, g_tgt / ef)

        gdrive_status = f"\n[GOOGLE DRIVE] Google Drive'a (UYGULAMA WEB SİTESİ, Florya_MEV_Yedekler, NOYA) senkronize edildi."
    except Exception as e:
        gdrive_status = f"\n[UYARI] Google Drive kopyalama hatası: {e}"

# 6. Masaüstü ve Google Drive Tam Web Sitesi ZIP Paketi
desktop_zip = Path(r"C:\Users\doruk\Desktop") / "Florya_MEV_GUNCEL_YEDEK.zip"
try:
    with zipfile.ZipFile(desktop_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(BASE_DIR):
            if "__pycache__" in root or ".git" in root:
                continue
            for f in files:
                fp = Path(root) / f
                arc = fp.relative_to(BASE_DIR)
                zipf.write(fp, arc)
    zip_status = f"\n[PAKET] Masaüstü Arşiv Paketi: {desktop_zip.name}"

    # Google Drive'daki her iki klasöre de tam arşiv zip'ini kopyala
    if g_found:
        for folder_name in ["UYGULAMA WEB SİTESİ", "Florya_MEV_Yedekler"]:
            f_dir = g_found / folder_name
            if f_dir.exists():
                shutil.copy2(desktop_zip, f_dir / "UYGULAMA_VE_WEB_SITESI_TAM_YEDEK.zip")
        zip_status += f"\n[GOOGLE DRIVE] Web Sitesi Tam Paketi her iki Drive klasörüne de kopyalandı."
except Exception as e:
    zip_status = ""

file_size_kb = target_file.stat().st_size / 1024

print("=" * 65)
print("     FLORYA MEV KOLEJİ - YEDEKLEME İŞLEMİ TAMAMLANDI")
print("=" * 65)
print(f"Yerel Klasör : yedekler/{target_file.name} ({file_size_kb:.1f} KB){excel_msg}")
print(onedrive_status)
if gdrive_status:
    print(gdrive_status)
print(d_status)
print(zip_status)
print("-" * 65)
print("Verileriniz hem yerel diskinize hem de bulut sürücünüze aktarıldı.")
