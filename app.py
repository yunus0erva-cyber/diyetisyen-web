"""
Florya MEV Koleji - Depo ve Stok Takip Web Uygulaması
Ana Streamlit Giriş Noktası (app.py)
"""

import streamlit as st
import pandas as pd
import datetime

# Sayfa Yapılandırması (Geniş ekran, sekme başlığı ve ikon)
st.set_page_config(
    page_title="Florya MEV - Depo & Stok Takip",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

from database import init_db, is_supabase_active, DB_PATH
from auth import (
    authenticate,
    login_user,
    logout_user,
    get_current_user,
    is_authenticated,
    is_admin,
    render_login_page,
    get_all_users,
    create_user,
    delete_user
)
from stock_manager import (
    LOCATIONS,
    UNITS,
    get_categories,
    get_products_df,
    get_product_by_id,
    add_product,
    update_product,
    delete_product,
    record_stock_movement,
    get_low_stock_alerts_df,
    get_expiring_soon_alerts_df,
    get_stock_movements_df,
    get_inventory_summary_stats
)
from excel_utils import (
    generate_import_template,
    parse_and_import_excel,
    export_dataframe_to_excel
)
from components import inject_custom_css, render_mev_header, render_kpi_card
from haccp_manager import (
    TEMPERATURE_TARGETS,
    MEAL_TYPES,
    TIME_PERIODS,
    add_haccp_sample,
    get_haccp_samples_df,
    dispose_sample,
    add_temperature_log,
    get_temperature_logs_df
)
from menu_data import WEEKLY_MENU, auto_register_day_samples, MENU_WEEKS
from canteen_manager import (
    add_canteen_cash_record,
    get_canteen_records_df,
    delete_canteen_record,
    get_canteen_summary_stats,
    add_kasa_transaction,
    get_kasa_transactions_df,
    get_kasa_ledger_summary,
    delete_kasa_transaction,
    POS_DEVICES,
    add_or_update_pos_record,
    get_pos_records_df,
    get_pos_summary_stats,
    get_day_financial_snapshot,
    sync_cash_and_pos_for_date
)

# CSS ve Stil Enjeksiyonu
inject_custom_css()

# ==========================================================
# 1. GİRİŞ KONTROLÜ (AUTHENTICATION GUARD)
# ==========================================================
if not is_authenticated():
    render_login_page()
    st.stop()

# Oturum açmış kullanıcı
current_user = get_current_user()

# ==========================================================
# 2. SOL MENÜ (SIDEBAR NAVIGATION)
# ==========================================================
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding-bottom: 12px; border-bottom: 1px solid #e2e8f0;">
        <h3 style="color: #1e3a8a; margin: 0; font-weight: 800;">📦 FLORYA MEV</h3>
        <p style="font-size: 12px; color: #64748b; margin: 0;">Depo & Stok Portalı</p>
    </div>
    """, unsafe_allow_html=True)

    # Kullanıcı Profil Kartı
    role_badge = "🔴 Yönetici" if current_user['role'] == "admin" else "🔵 Personel"
    st.markdown(f"""
    <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 10px 12px; margin: 12px 0;">
        <div style="font-size: 11px; color: #64748b; text-transform: uppercase;">Giriş Yapan:</div>
        <div style="font-weight: 700; color: #0f172a; font-size: 14px;">{current_user['full_name']}</div>
        <div style="font-size: 11px; margin-top: 2px;">{role_badge} <span style="color: #94a3b8;">(@{current_user['username']})</span></div>
    </div>
    """, unsafe_allow_html=True)

    # Menü Seçenekleri
    menu_items = [
        "🚨 Kritik Stok & Uyarı Paneli",
        "📋 Stok Listesi & Yönetimi",
        "➕ Hızlı Stok Giriş / Çıkış",
        "🍽️ Yemekhane & Menü Yönetimi",
        "🛡️ HACCP & Gıda Güvenliği",
        "💰 Kantin Kasa & Z Raporu",
        "📥 Excel ile Toplu Yükleme",
        "🔄 Hareket Geçmişi (Loglar)",
    ]

    if is_admin():
        menu_items.append("👥 Kullanıcı Yönetimi")
        menu_items.append("⚙️ Veritabanı & Ayarlar")

    selected_menu = st.radio("MENÜ", menu_items, index=0)

    st.markdown("---")
    if st.button("💾 Tek Tıkla Sistemi Yedekle", use_container_width=True, type="primary"):
        import subprocess, sys
        py_exec = sys.executable
        res = subprocess.run([py_exec, "yedekle.py"], capture_output=True, text=True)
        st.success("✅ Tüm veritabanı, numuneler ve Excel tabloları OneDrive, D: diski ve Masaüstüne yedeklendi!")

    if st.button("🚪 Güvenli Çıkış Yap", use_container_width=True, type="secondary"):
        logout_user()

    # Alt Bilgi
    st.markdown("""
    <div style="text-align: center; font-size: 10px; color: #94a3b8; margin-top: 20px;">
        Florya MEV Koleji Operasyon v1.0<br>
        HACCP & FEFO Uyumlu
    </div>
    """, unsafe_allow_html=True)

def render_yemekhane_menu_section(context_id: str = "main"):
    """Eylül ve Ekim 2026 dönemi 9 haftalık yemekhane menüsünü, kalorilerini ve numune alma işlevini görüntüler."""
    st.markdown("### 📅 Florya MEV Koleji - Yemekhane Menüsü ve Kalori Cetveli")
    st.caption("Eylül ve Ekim 2026 dönemi 9 haftalık resmi yemekhane menüsü (500 kişilik mutfak üretimi). Kalori değerleri ve 72 saatlik şahit numune kayıt durumu aşağıda listelenmiştir.")

    # 4'lü Üst Bilgi Kartları
    c_m1, c_m2, c_m3, c_m4 = st.columns(4)
    with c_m1:
        st.markdown("""
        <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:10px; text-align:center;">
            <div style="font-size:12px; color:#64748b; font-weight:600;">Planlanan Dönem</div>
            <div style="font-size:16px; color:#1e3a8a; font-weight:800; margin-top:2px;">Eylül & Ekim 2026</div>
        </div>
        """, unsafe_allow_html=True)
    with c_m2:
        st.markdown("""
        <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:10px; text-align:center;">
            <div style="font-size:12px; color:#64748b; font-weight:600;">Porsiyon Kapasitesi</div>
            <div style="font-size:16px; color:#10b981; font-weight:800; margin-top:2px;">500 Kişilik</div>
        </div>
        """, unsafe_allow_html=True)
    with c_m3:
        st.markdown("""
        <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:10px; text-align:center;">
            <div style="font-size:12px; color:#64748b; font-weight:600;">Kapsam</div>
            <div style="font-size:16px; color:#f59e0b; font-weight:800; margin-top:2px;">9 Hafta / 44 Gün</div>
        </div>
        """, unsafe_allow_html=True)
    with c_m4:
        st.markdown("""
        <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:10px; text-align:center;">
            <div style="font-size:12px; color:#64748b; font-weight:600;">Mevzuat Uyumu</div>
            <div style="font-size:16px; color:#8b5cf6; font-weight:800; margin-top:2px;">72 Saat Şahit Numune</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    today_iso = datetime.date.today().isoformat()
    all_week_titles = list(MENU_WEEKS.keys())

    # Dönem Filtresi (Tümü, Eylül 2026, Ekim 2026)
    c_f1, c_f2 = st.columns([1, 2])
    with c_f1:
        month_filter = st.radio(
            "Ay Filtresi:",
            ["Tümü (Eylül & Ekim)", "🍇 Eylül 2026 (5 Hafta)", "🍂 Ekim 2026 (4 Hafta)"],
            index=0,
            key=f"mf_{context_id}"
        )

    if "Eylül" in month_filter:
        active_week_titles = [w for w in all_week_titles if "Eylül" in w]
    elif "Ekim" in month_filter:
        active_week_titles = [w for w in all_week_titles if "Ekim" in w]
    else:
        active_week_titles = all_week_titles

    # Otomatik olarak bugünün haftasını tespit et
    default_w_idx = 0
    for w_idx, w_title in enumerate(active_week_titles):
        if today_iso in MENU_WEEKS[w_title]:
            default_w_idx = w_idx
            break
    if default_w_idx == 0:
        for w_idx, w_title in enumerate(active_week_titles):
            if "Eylül 4. Hafta" in w_title:
                default_w_idx = w_idx
                break

    with c_f2:
        selected_week_title = st.selectbox(
            "🗓️ Görüntülenecek Menü Haftasını Seçin:",
            active_week_titles,
            index=default_w_idx,
            key=f"sw_{context_id}"
        )

    day_keys = MENU_WEEKS[selected_week_title]
    cols_menu = st.columns(5)

    # Veritabanındaki tüm şahit numuneleri al (alınan günleri dinamik tespit etmek için)
    df_all_haccp = get_haccp_samples_df("Tümü")

    for idx, d_key in enumerate(day_keys):
        d_info = WEEKLY_MENU.get(d_key)
        if not d_info:
            continue
        with cols_menu[idx]:
            is_today = (d_key == today_iso)
            border_color = "#3b82f6" if is_today else "#e2e8f0"
            bg_color = "#eff6ff" if is_today else "#ffffff"
            badge_text = " 📍 BUGÜN" if is_today else ""

            # Tatil Kontrolü
            is_holiday = False
            lunch_meals = d_info['meals'].get('ÖĞLE YEMEĞİ', [])
            if lunch_meals and "TATİL" in lunch_meals[0]['name']:
                is_holiday = True

            st.markdown(f"""
            <div style="background:{bg_color}; border: 2px solid {border_color}; border-radius: 10px; padding: 12px; margin-bottom: 12px;">
                <h4 style="margin:0; color:#1e3a8a; text-align:center;">{d_info['day_name']}</h4>
                <div style="text-align:center; font-size:12px; color:#64748b; font-weight:700;">{d_info['date_str']}{badge_text}</div>
            </div>
            """, unsafe_allow_html=True)

            if is_holiday:
                st.info("🇹🇷 **29 EKİM CUMHURİYET BAYRAMI**\n\nResmi Tatil nedeniyle yemekhane kapalıdır.")
                continue

            # Toplam Kalori Hesabı
            total_kcal = sum(sum(item['kcal'] for item in meal_list) for meal_list in d_info['meals'].values())
            st.metric("Günlük Toplam", f"{total_kcal} kcal")

            # Öğünler
            for meal_name, items in d_info['meals'].items():
                if items:
                    with st.expander(f"{meal_name} ({len(items)})", expanded=(meal_name == "ÖĞLE YEMEĞİ")):
                        for it in items:
                            st.markdown(f"• **{it['name']}** <span style='color:#ef4444; font-size:11px;'>({it['kcal']} kcal)</span>", unsafe_allow_html=True)
                else:
                    with st.expander(f"{meal_name}", expanded=False):
                        st.caption("Bu öğün için servis bulunmuyor.")

            # Numune Durumu & Otomatik Kayıt Butonu
            st.markdown("---")
            has_sample = False
            if not df_all_haccp.empty and "sample_date" in df_all_haccp.columns:
                has_sample = (df_all_haccp["sample_date"] == d_key).any()

            if has_sample:
                st.success("✅ Numuneler Alındı")
            else:
                if st.button(f"🧪 Numuneleri Kaydet", key=f"btn_auto_{d_key}_{context_id}", use_container_width=True, type="secondary"):
                    res_msgs = auto_register_day_samples(d_key, current_user["full_name"])
                    st.success(f"{d_info['day_name']} günü için {len(res_msgs)} adet şahit numune dolaba kaydedildi!")
                    st.rerun()

    st.markdown("---")
    # Menü Excel Export
    st.markdown("#### 📥 Resmi Menü Dökümü ve Rapor İndirme")
    c_exp1, c_exp2, c_exp3, c_exp4 = st.columns(4)

    # 1. Seçili Hafta
    with c_exp1:
        sel_rows = []
        for d_k in day_keys:
            d_v = WEEKLY_MENU[d_k]
            for m_cat, m_items in d_v["meals"].items():
                for it in m_items:
                    sel_rows.append({
                        "Tarih": d_v["date_str"],
                        "Gün": d_v["day_name"],
                        "Öğün": m_cat,
                        "Yemek Adı": it["name"],
                        "Kalori (kcal)": it["kcal"]
                    })
        df_sel = pd.DataFrame(sel_rows)
        b_sel = export_dataframe_to_excel(df_sel)
        st.download_button(
            label="📄 Seçili Haftayı İndir",
            data=b_sel,
            file_name=f"Florya_MEV_Menu_{selected_week_title.split('(')[0].strip().replace(' ', '_')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
            key=f"btn_dl_sel_{context_id}"
        )

    # 2. Eylül Ayı
    with c_exp2:
        eylul_rows = []
        for w_title, w_days in MENU_WEEKS.items():
            if "Eylül" in w_title:
                for d_k in w_days:
                    d_v = WEEKLY_MENU[d_k]
                    for m_cat, m_items in d_v["meals"].items():
                        for it in m_items:
                            eylul_rows.append({
                                "Hafta": w_title.split("(")[0].strip(),
                                "Tarih": d_v["date_str"],
                                "Gün": d_v["day_name"],
                                "Öğün": m_cat,
                                "Yemek Adı": it["name"],
                                "Kalori (kcal)": it["kcal"]
                            })
        df_eylul = pd.DataFrame(eylul_rows)
        b_eylul = export_dataframe_to_excel(df_eylul)
        st.download_button(
            label="🍇 Eylül Ayı Menüsü (.xlsx)",
            data=b_eylul,
            file_name="Florya_MEV_Eylul_2026_Aylik_Menu.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
            key=f"btn_dl_eylul_{context_id}"
        )

    # 3. Ekim Ayı
    with c_exp3:
        ekim_rows = []
        for w_title, w_days in MENU_WEEKS.items():
            if "Ekim" in w_title:
                for d_k in w_days:
                    d_v = WEEKLY_MENU[d_k]
                    for m_cat, m_items in d_v["meals"].items():
                        for it in m_items:
                            ekim_rows.append({
                                "Hafta": w_title.split("(")[0].strip(),
                                "Tarih": d_v["date_str"],
                                "Gün": d_v["day_name"],
                                "Öğün": m_cat,
                                "Yemek Adı": it["name"],
                                "Kalori (kcal)": it["kcal"]
                            })
        df_ekim = pd.DataFrame(ekim_rows)
        b_ekim = export_dataframe_to_excel(df_ekim)
        st.download_button(
            label="🍂 Ekim Ayı Menüsü (.xlsx)",
            data=b_ekim,
            file_name="Florya_MEV_Ekim_2026_Aylik_Menu.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
            key=f"btn_dl_ekim_{context_id}"
        )

    # 4. Tam Liste (Eylül + Ekim)
    with c_exp4:
        all_rows = []
        for w_title, w_days in MENU_WEEKS.items():
            for d_k in w_days:
                d_v = WEEKLY_MENU[d_k]
                for m_cat, m_items in d_v["meals"].items():
                    for it in m_items:
                        all_rows.append({
                            "Hafta": w_title.split("(")[0].strip(),
                            "Tarih": d_v["date_str"],
                            "Gün": d_v["day_name"],
                            "Öğün": m_cat,
                            "Yemek Adı": it["name"],
                            "Kalori (kcal)": it["kcal"]
                        })
        df_all = pd.DataFrame(all_rows)
        b_all = export_dataframe_to_excel(df_all)
        st.download_button(
            label="📑 2 Aylık Tam Menü (.xlsx)",
            data=b_all,
            file_name="Florya_MEV_Eylul_Ekim_2026_Tam_Menu.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
            key=f"btn_dl_all_{context_id}"
        )

# ----------------------------------------------------------
# SAYFA: 🍽️ YEMEKHANE & MENÜ YÖNETİMİ
# ----------------------------------------------------------

# ==========================================================
# 3. SAYFA İÇERİKLERİ
# ==========================================================

# ----------------------------------------------------------
# SAYFA 1: 🚨 KRİTİK STOK & UYARI PANELİ
# ----------------------------------------------------------
if selected_menu == "🚨 Kritik Stok & Uyarı Paneli":
    render_mev_header("KRİTİK STOK VE UYARI PANELİ", "Kritik eşik altına düşen ve SKT'si yaklaşan ürünler")

    stats = get_inventory_summary_stats()
    
    # KPI Kartları
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_kpi_card("Toplam Ürün Çeşidi", f"{stats['total_sku']:,} Adet", "Kayıtlı aktif stok kartı", "📦", "#3b82f6")
    with c2:
        render_kpi_card("Kritik Eşik Altında", f"{stats['critical_count']} Ürün", "Acil tedarik bekleniyor", "🚨", "#ef4444")
    with c3:
        render_kpi_card("Tamamen Tükenen", f"{stats['out_of_stock_count']} Ürün", "Mevcut stok sıfır!", "⛔", "#dc2626")
    with c4:
        render_kpi_card("Bugünkü Hareketler", f"{stats['today_movements']} İşlem", "Giriş / Çıkış kayıtları", "🔄", "#10b981")

    st.markdown("### ⚠️ Kritik Seviyedeki ve Tükenen Ürünler")
    low_stock_df = get_low_stock_alerts_df()

    if low_stock_df.empty:
        st.success("🎉 Harika haber! Şu anda kritik stok seviyesinin altında veya tükenmiş hiçbir ürün bulunmuyor.")
    else:
        st.warning(f"Dikkat: Toplam **{len(low_stock_df)}** ürün kritik eşiğin altına inmiş durumda. Aşağıdaki tablodan eksik miktarları görebilir ve doğrudan satınalma listesini indirebilirsiniz.")

        # Excel Export Butonu
        col_btn1, col_btn2 = st.columns([2, 5])
        with col_btn1:
            excel_bytes = export_dataframe_to_excel(
                low_stock_df.drop(columns=["id"]),
                sheet_name="Siparis_Listesi",
                report_title="Kritik Stok ve Satınalma İhtiyaç Raporu"
            )
            st.download_button(
                label="📥 Satınalma Sipariş Listesini İndir (Excel)",
                data=excel_bytes,
                file_name=f"Florya_MEV_Siparis_Listesi_{datetime.date.today().isoformat()}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
                type="primary"
            )

        # Tablo Gösterimi
        display_cols = ["Barkod", "Ürün Adı", "Kategori", "Depo Lokasyonu", "Mevcut Stok", "Kritik Eşik", "Birim", "Eksik Miktar", "Durum Seviyesi"]
        st.dataframe(
            low_stock_df[display_cols],
            use_container_width=True,
            hide_index=True
        )

    st.markdown("---")
    st.markdown("### ⏳ FEFO Kuralı: Son Tüketim Tarihi (SKT) Yaklaşan Gıdalar")
    st.caption("Gıda güvenliği ve HACCP gereği, son tüketim tarihi yaklaşan ürünler öncelikle tüketime (FEFO) verilmelidir.")

    days_filter = st.slider("İncelemek istediğiniz gün aralığı:", min_value=7, max_value=90, value=30, step=7)
    expiring_df = get_expiring_soon_alerts_df(days=days_filter)

    if expiring_df.empty:
        st.info(f"Önümüzdeki {days_filter} gün içinde son kullanma tarihi dolacak ürün bulunmamaktadır.")
    else:
        st.dataframe(
            expiring_df[["Barkod", "Ürün Adı", "Kategori", "Lokasyon", "Stok", "Birim", "Parti / Lot", "Son Tüketim (SKT)", "Kalan Gün", "FEFO Öncelik Durumu"]],
            use_container_width=True,
            hide_index=True
        )

# ----------------------------------------------------------
# SAYFA 2: 📋 STOK LİSTESİ & YÖNETİMİ
# ----------------------------------------------------------
elif selected_menu == "📋 Stok Listesi & Yönetimi":
    render_mev_header("STOK LİSTESİ VE YÖNETİMİ", "Depolardaki tüm ürünlerin detaylı takibi ve düzenlenmesi")

    # Arama ve Filtreleme Çubuğu
    f_col1, f_col2, f_col3, f_col4 = st.columns([3, 2, 2, 2])
    with f_col1:
        search_txt = st.text_input("🔍 Ürün Ara (Ad, Barkod, Kod, Lot)", placeholder="Örn: Salça, Pirinç veya 869...")
    with f_col2:
        cat_list = ["Tümü"] + get_categories()
        selected_cat = st.selectbox("Kategori Filtresi", cat_list)
    with f_col3:
        loc_list = ["Tümü"] + LOCATIONS
        selected_loc = st.selectbox("Lokasyon Filtresi", loc_list)
    with f_col4:
        st.write("")
        st.write("")
        only_crit = st.checkbox("Sadece Kritik Stoklar", value=False)

    # Veriyi Çek
    products_df = get_products_df(
        search_query=search_txt,
        category=selected_cat,
        location=selected_loc,
        only_low_stock=only_crit
    )

    # Üst İstatistik & İndirme Butonları
    b_col1, b_col2 = st.columns([4, 2])
    with b_col1:
        st.info(f"Bulunan Ürün Sayısı: **{len(products_df)}** | Toplam Stok Miktarı: **{products_df['Mevcut Stok'].sum():,.2f}** | Toplam Parasal Değer: **{products_df['Toplam Değer (TL)'].sum():,.2f} ₺**")
    with b_col2:
        if not products_df.empty:
            export_data = export_dataframe_to_excel(
                products_df.drop(columns=["id"]),
                sheet_name="Stok_Listesi",
                report_title="Güncel Stok ve Envanter Durumu"
            )
            st.download_button(
                label="📥 Filtrelenen Listeyi Excel İndir (.xlsx)",
                data=export_data,
                file_name=f"Florya_MEV_Stok_Listesi_{datetime.date.today().isoformat()}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
                type="primary"
            )

    # Tablo
    display_table = products_df.drop(columns=["id"])
    st.dataframe(
        display_table,
        use_container_width=True,
        hide_index=True
    )

    # Ürün İşlemleri Sekmesi
    st.markdown("---")
    tab1, tab2 = st.tabs(["➕ Yeni Ürün Kartı Aç", "✏️ Mevcut Ürün Bilgilerini Düzenle / Sil"])

    with tab1:
        st.markdown("#### Yeni Ürün Kartı Tanımlama")
        with st.form("new_product_form", clear_on_submit=True):
            np1, np2, np3 = st.columns(3)
            with np1:
                p_name = st.text_input("Ürün Adı *", placeholder="Örn: Un (50kg Çuval)")
                p_cat = st.selectbox("Kategori *", get_categories())
                p_loc = st.selectbox("Depo Lokasyonu *", LOCATIONS)
            with np2:
                p_barcode = st.text_input("Barkod", placeholder="869...")
                p_code = st.text_input("Ürün Kodu", placeholder="KD-006")
                p_unit = st.selectbox("Birim *", UNITS)
            with np3:
                p_stock = st.number_input("Açılış Stok Miktarı", min_value=0.0, value=0.0, step=1.0)
                p_crit = st.number_input("Kritik Eşik Seviyesi *", min_value=0.0, value=5.0, step=1.0)
                p_price = st.number_input("Birim Fiyat (TL)", min_value=0.0, value=0.0, step=5.0)

            np4, np5, np6 = st.columns(3)
            with np4:
                p_skt = st.date_input("Son Tüketim Tarihi (SKT)", value=None)
            with np5:
                p_lot = st.text_input("Parti / Lot No", placeholder="LOT-...")
            with np6:
                p_notes = st.text_input("Notlar / Açıklama", placeholder="Alerjen vb.")

            add_btn = st.form_submit_button("Ürün Kartını Kaydet 💾", type="primary")
            if add_btn:
                if not p_name:
                    st.error("Lütfen ürün adını giriniz!")
                else:
                    success, msg = add_product(
                        barcode=p_barcode,
                        product_code=p_code,
                        name=p_name,
                        category=p_cat,
                        unit=p_unit,
                        initial_stock=p_stock,
                        critical_threshold=p_crit,
                        unit_price=p_price,
                        storage_location=p_loc,
                        expiry_date=p_skt.isoformat() if p_skt else None,
                        lot_no=p_lot,
                        notes=p_notes,
                        user_name=current_user["full_name"]
                    )
                    if success:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)

    with tab2:
        st.markdown("#### Ürün Bilgisi Düzenleme")
        if products_df.empty:
            st.info("Düzenlenecek ürün bulunamadı.")
        else:
            product_dict = {f"{row['Ürün Adı']} ({row['Barkod'] or 'Barkodsuz'}) - ID: {row['id']}": row['id'] for _, row in products_df.iterrows()}
            selected_label = st.selectbox("Düzenlenecek Ürünü Seçin:", list(product_dict.keys()))
            sel_id = product_dict[selected_label]
            prod_info = get_product_by_id(sel_id)

            if prod_info:
                with st.form("edit_product_form"):
                    ep1, ep2, ep3 = st.columns(3)
                    with ep1:
                        e_name = st.text_input("Ürün Adı", value=prod_info["name"])
                        e_cat = st.selectbox("Kategori", get_categories(), index=get_categories().index(prod_info["category"]) if prod_info["category"] in get_categories() else 0)
                        e_loc = st.selectbox("Depo Lokasyonu", LOCATIONS, index=LOCATIONS.index(prod_info["storage_location"]) if prod_info["storage_location"] in LOCATIONS else 0)
                    with ep2:
                        e_barcode = st.text_input("Barkod", value=prod_info["barcode"] or "")
                        e_code = st.text_input("Ürün Kodu", value=prod_info["product_code"] or "")
                        e_unit = st.selectbox("Birim", UNITS, index=UNITS.index(prod_info["unit"]) if prod_info["unit"] in UNITS else 0)
                    with ep3:
                        e_crit = st.number_input("Kritik Eşik", min_value=0.0, value=float(prod_info["critical_threshold"]), step=1.0)
                        e_price = st.number_input("Birim Fiyat (TL)", min_value=0.0, value=float(prod_info["unit_price"]), step=5.0)
                        
                        existing_date = None
                        if prod_info["expiry_date"]:
                            try:
                                existing_date = datetime.date.fromisoformat(prod_info["expiry_date"])
                            except:
                                existing_date = None
                        e_skt = st.date_input("Son Tüketim Tarihi", value=existing_date)

                    ep4, ep5 = st.columns(2)
                    with ep4:
                        e_lot = st.text_input("Parti / Lot No", value=prod_info["lot_no"] or "")
                    with ep5:
                        e_notes = st.text_input("Açıklama", value=prod_info["notes"] or "")

                    btn_c1, btn_c2 = st.columns([4, 1])
                    with btn_c1:
                        update_btn = st.form_submit_button("Bilgileri Güncelle 🔄", type="primary", use_container_width=True)
                    with btn_c2:
                        delete_btn = st.form_submit_button("Ürünü Sil 🗑️", type="secondary", use_container_width=True)

                    if update_btn:
                        succ, upd_msg = update_product(
                            product_id=sel_id,
                            barcode=e_barcode,
                            product_code=e_code,
                            name=e_name,
                            category=e_cat,
                            unit=e_unit,
                            critical_threshold=e_crit,
                            unit_price=e_price,
                            storage_location=e_loc,
                            expiry_date=e_skt.isoformat() if e_skt else None,
                            lot_no=e_lot,
                            notes=e_notes
                        )
                        if succ:
                            st.success(upd_msg)
                            st.rerun()
                        else:
                            st.error(upd_msg)

                    if delete_btn:
                        succ, del_msg = delete_product(sel_id)
                        if succ:
                            st.warning(del_msg)
                            st.rerun()
                        else:
                            st.error(del_msg)

# ----------------------------------------------------------
# SAYFA 3: ➕ HIZLI STOK GİRİŞ / ÇIKIŞ
# ----------------------------------------------------------
elif selected_menu == "➕ Hızlı Stok Giriş / Çıkış":
    render_mev_header("HIZLI STOK HAREKETİ", "Stok girişi, çıkışı, sayım düzeltmesi veya fire kaydı")

    all_prods = get_products_df()
    if all_prods.empty:
        st.warning("Henüz veritabanında ürün bulunmuyor. Önce ürün ekleyin veya Excel yükleyin.")
    else:
        prod_map = {f"{row['Ürün Adı']} [Mevcut: {row['Mevcut Stok']} {row['Birim']}]": row['id'] for _, row in all_prods.iterrows()}
        
        col_m1, col_m2 = st.columns([3, 2])
        with col_m1:
            with st.form("quick_movement_form"):
                selected_prod_label = st.selectbox("İşlem Yapılacak Ürünü Seçin *", list(prod_map.keys()))
                prod_id = prod_map[selected_prod_label]
                prod_item = get_product_by_id(prod_id)

                mov_type = st.radio(
                    "Hareket Türü *",
                    ["GİRİŞ", "ÇIKIŞ", "SAYIM DÜZELTME", "FİRE / İMHA"],
                    horizontal=True
                )

                q1, q2 = st.columns(2)
                with q1:
                    qty = st.number_input(f"İşlem Miktarı ({prod_item['unit']}) *", min_value=0.01, value=1.0, step=1.0)
                with q2:
                    doc_no = st.text_input("İrsaliye / Fatura / Fiş No", placeholder="Örn: IRS-2026-0042")

                reason_txt = st.text_input("Açıklama / Not", placeholder="Örn: Yemekhane mutfak tüketimi, haftalık irsaliye girişi vb.")

                submit_mov = st.form_submit_button("Hareketi Onayla ve Kaydet ⚡", type="primary", use_container_width=True)

                if submit_mov:
                    succ, res_msg = record_stock_movement(
                        product_id=prod_id,
                        movement_type=mov_type,
                        quantity=qty,
                        document_no=doc_no,
                        reason=reason_txt,
                        user_name=current_user["full_name"]
                    )
                    if succ:
                        st.success(res_msg)
                        st.rerun()
                    else:
                        st.error(res_msg)

        with col_m2:
            st.markdown("#### 📌 Seçili Ürün Kartı Özeti")
            if prod_item:
                is_crit = prod_item['current_stock'] <= prod_item['critical_threshold']
                status_color = "#ef4444" if is_crit else "#10b981"
                status_text = "🚨 KRİTİK SEVİYE" if is_crit else "✅ YETERLİ SEVİYE"

                st.markdown(f"""
                <div style="background: white; border: 1px solid #e2e8f0; border-radius: 10px; padding: 16px; box-shadow: 0 2px 4px rgba(0,0,0,0.03);">
                    <h3 style="margin-top:0; color:#1e3a8a;">{prod_item['name']}</h3>
                    <p style="margin:4px 0; color:#64748b;"><b>Barkod:</b> {prod_item['barcode'] or '-'}</p>
                    <p style="margin:4px 0; color:#64748b;"><b>Lokasyon:</b> {prod_item['storage_location']}</p>
                    <p style="margin:4px 0; color:#64748b;"><b>Kategori:</b> {prod_item['category']}</p>
                    <hr style="margin:10px 0; border:none; border-top:1px solid #f1f5f9;">
                    <div style="font-size:24px; font-weight:800; color:{status_color};">
                        {prod_item['current_stock']} {prod_item['unit']}
                    </div>
                    <div style="font-size:12px; color:#64748b;">Kritik Eşik Sınırı: {prod_item['critical_threshold']} {prod_item['unit']} ({status_text})</div>
                    <div style="font-size:12px; color:#64748b; margin-top:6px;">Birim Fiyat: {prod_item['unit_price']} TL</div>
                </div>
                """, unsafe_allow_html=True)

# ----------------------------------------------------------

elif selected_menu == "🍽️ Yemekhane & Menü Yönetimi":
    render_mev_header("FLORYA MEV KOLEJİ - YEMEKHANE & MENÜ YÖNETİMİ", "Eylül ve Ekim 2026 Resmi Okul Yemek Menüleri, Kalori Değerleri ve Şahit Numune Kayıtları")
    render_yemekhane_menu_section(context_id="page")

# SAYFA: 🛡️ HACCP & GIDA GÜVENLİĞİ
# ----------------------------------------------------------
elif selected_menu == "🛡️ HACCP & Gıda Güvenliği":
    render_mev_header("HACCP & GIDA GÜVENLİĞİ MERKEZİ", "72 Saatlik Şahit Numune Takibi ve Günlük Sıcaklık Çizelgesi")

    tab_h1, tab_h2, tab_h3 = st.tabs(["🧪 72 Saatlik Şahit Numune Takip Masası", "🍽️ Yemekhane Menüsü & Kalori Cetveli", "🌡️ Buzdolabı & Depo Sıcaklık Çizelgesi"])

    # ------------------------------------------------------
    # TAB 1: 72 SAATLİK ŞAHİT NUMUNE TAKİBİ
    # ------------------------------------------------------
    with tab_h1:
        st.markdown("### 🧪 Şahit Numune Geri Sayım ve Takip Paneli")
        st.caption("Tarım Bakanlığı ve MEB mevzuatına göre mutfakta pişen her öğünün şahit numunesi en az 72 saat +4°C'de saklanmak zorundadır.")

        df_all_samples = get_haccp_samples_df("Tümü")
        
        # Metrik Kartları
        total_samples_count = len(df_all_samples) if not df_all_samples.empty else 0
        if not df_all_samples.empty:
            active_s = df_all_samples[df_all_samples['status'] == 'SAKLANIYOR']
            ready_s = active_s[active_s['remaining_hours'] <= 0]
            urgent_s = active_s[(active_s['remaining_hours'] > 0) & (active_s['remaining_hours'] <= 12)]
            active_count = len(active_s)
            ready_count = len(ready_s)
            urgent_count = len(urgent_s)
        else:
            active_count = 0
            ready_count = 0
            urgent_count = 0

        c_k1, c_k2, c_k3, c_k4 = st.columns(4)
        with c_k1:
            render_kpi_card("Aktif Saklanan Numune", f"{active_count} Adet", "Dolapta yasal süresi sürenler", "🧪", "#3b82f6")
        with c_k2:
            render_kpi_card("72 Saati Dolan (İmhaya Hazır)", f"{ready_count} Adet", "Yasal süresi tamamlandı", "🟢", "#10b981")
        with c_k3:
            render_kpi_card("Dolmak Üzere (<12 Saat)", f"{urgent_count} Adet", "Bugün süresi dolacaklar", "🟡", "#f59e0b")
        with c_k4:
            render_kpi_card("Yasal Kural Standartı", "72 Saat (+4°C)", "MEB & HACCP zorunluluğu", "⚖️", "#8b5cf6")

        st.markdown("---")

        # Yeni Numune Ekleme Formu
        with st.expander("➕ Yeni Şahit Numune Kaydı Ekle", expanded=(active_count == 0)):
            with st.form("add_new_sample_form"):
                col_n1, col_n2 = st.columns(2)
                with col_n1:
                    new_meal_name = st.text_input("Yemek / Menü Adı *", placeholder="Örn: Mercimek Çorbası + Orman Kebabı + Pilav")
                    new_meal_type = st.selectbox("Öğün Türü", MEAL_TYPES, index=0)
                with col_n2:
                    col_dt1, col_dt2 = st.columns(2)
                    with col_dt1:
                        new_sample_date = st.date_input("Yemek Tarihi", value=datetime.date.today())
                    with col_dt2:
                        new_sample_time = st.text_input("Alınış Saati", value=datetime.datetime.now().strftime("%H:%M"))
                    new_taken_by = st.text_input("Numuneyi Alan Personel *", value=current_user["full_name"])

                new_notes = st.text_input("Açıklama / Not", placeholder="Örn: 250g steril kavanozda +4°C numune dolabına konuldu")
                submit_new_sample = st.form_submit_button("🧪 Numuneyi Kaydet ve 72 Saatlik Sayacı Başlat", type="primary", use_container_width=True)

                if submit_new_sample:
                    s_ok, s_msg = add_haccp_sample(
                        meal_name=new_meal_name,
                        meal_type=new_meal_type,
                        sample_date=new_sample_date,
                        sample_time=new_sample_time,
                        sample_taken_by=new_taken_by,
                        notes=new_notes
                    )
                    if s_ok:
                        st.success(s_msg)
                        st.rerun()
                    else:
                        st.error(s_msg)

        # 72 Saati Dolan Numuneleri İmha Etme Paneli
        if ready_count > 0:
            st.info(f"🟢 **Bilgi:** Dolapta yasal 72 saatlik saklama süresini tamamlamış **{ready_count} adet** numune bulunmaktadır. Bunları imha edip dolapta yer açabilirsiniz.")
            ready_options = {f"#{row['id']} - {row['meal_name']} ({row['sample_date']} {row['sample_time']})": row['id'] for _, row in ready_s.iterrows()}
            
            c_disp1, c_disp2 = st.columns([3, 1])
            with c_disp1:
                selected_dispose_label = st.selectbox("İmha Edilecek Numuneyi Seçin:", list(ready_options.keys()))
            with c_disp2:
                st.write("")
                st.write("")
                if st.button("🗑️ İmha Edildi Olarak Onayla", type="primary", use_container_width=True):
                    disp_id = ready_options[selected_dispose_label]
                    disp_ok, disp_msg = dispose_sample(disp_id, current_user["full_name"])
                    if disp_ok:
                        st.success(disp_msg)
                        st.rerun()
                    else:
                        st.error(disp_msg)

        # Numune Listesi ve Filtreleme
        st.markdown("#### 📋 Şahit Numune Kayıt Defteri")
        filter_col, export_col = st.columns([2, 1])
        with filter_col:
            status_filter = st.radio("Filtrele:", ["Saklananlar", "Tümü", "İmha Edilenler"], horizontal=True)

        df_filtered_samples = get_haccp_samples_df(status_filter)

        if df_filtered_samples.empty:
            st.info("Bu filtreye uygun numune kaydı bulunamadı.")
        else:
            with export_col:
                st.write("")
                excel_bytes = export_dataframe_to_excel(df_filtered_samples)
                st.download_button(
                    label="📥 Numune Defterini İndir (Excel)",
                    data=excel_bytes,
                    file_name=f"Florya_MEV_Sahit_Numune_Defteri_{datetime.date.today().isoformat()}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )

            # Tablo gösterimi
            view_cols = {
                "id": "No",
                "meal_name": "Yemek Adı",
                "meal_type": "Öğün",
                "sample_date": "Tarih",
                "sample_time": "Saat",
                "sample_taken_by": "Alan Personel",
                "status_label": "Yasal Durum / Kalan Süre",
                "disposed_by": "İmha Eden Personel",
                "notes": "Notlar"
            }
            existing_cols = [c for c in view_cols.keys() if c in df_filtered_samples.columns]
            df_display = df_filtered_samples[existing_cols].rename(columns=view_cols)
            st.dataframe(df_display, use_container_width=True, hide_index=True)

    # ------------------------------------------------------
    # TAB 2: AYLIK & HAFTALIK YEMEK MENÜSÜ VE KALORİ TAKİBİ
    # ------------------------------------------------------
    with tab_h2:
        render_yemekhane_menu_section(context_id="haccp_tab")

    # ------------------------------------------------------
    # TAB 3: BUZDOLABI & DEPO SICAKLIK ÇİZELGESİ
    # ------------------------------------------------------
    with tab_h3:
        st.markdown("### 🌡️ Günlük Dolap ve Depo Isı Takip Çizelgesi")
        st.caption("HACCP ve Gıda Güvenliği mevzuatına göre soğuk depoların ve numune dolaplarının dereceleri günde en az iki defa kaydedilmelidir.")

        # Cihaz Standartları Bilgi Şeridi
        with st.expander("ℹ️ Yasal Sıcaklık Standartları Tablosu", expanded=False):
            st.markdown("""
            * **Soğuk Hava Deposu:** `0.0°C` ile `4.0°C` arası *(Et, süt, şarküteri için)*
            * **Donuk Depo:** `-25.0°C` ile `-18.0°C` arası *(Dondurulmuş ürünler için)*
            * **Şahit Numune Dolabı:** `0.0°C` ile `4.0°C` arası *(72 saatlik numuneler için)*
            * **Kuru Gıda Deposu:** `15.0°C` ile `22.0°C` arası *(Bakliyat, un, yağ için)*
            * **Sıcak Yemek Servis Tezgahı (Benmari):** `65.0°C` ile `95.0°C` arası
            """)

        c_tform1, c_tform2 = st.columns([1, 1])

        with c_tform1:
            st.markdown("#### 📝 Yeni Sıcaklık Ölçümü Kaydet")
            with st.form("add_temperature_form"):
                dev_name = st.selectbox("Ölçüm Yapılan Cihaz / Depo *", list(TEMPERATURE_TARGETS.keys()))
                target_range = TEMPERATURE_TARGETS[dev_name]
                st.caption(f"Yasal Standart: **{target_range['min']}°C** ile **{target_range['max']}°C** arası")

                col_c1, col_c2 = st.columns(2)
                with col_c1:
                    t_date = st.date_input("Ölçüm Tarihi", value=datetime.date.today())
                with col_c2:
                    t_period = st.selectbox("Zaman Dilimi", TIME_PERIODS, index=0)

                t_val = st.number_input("Ölçülen Sıcaklık (°C) *", value=float(target_range['min'] + 2.0), step=0.5, format="%.1f")
                t_recorder = st.text_input("Ölçümü Yapan Personel *", value=current_user["full_name"])
                t_action = st.text_input("Aksiyon Notu (Varsa)", placeholder="Örn: Derece yüksek çıktı, termostat 1 kademe düşürüldü.")

                submit_temp = st.form_submit_button("🌡️ Sıcaklık Ölçümünü Kaydet", type="primary", use_container_width=True)

                if submit_temp:
                    t_ok, t_msg, is_safe_flag = add_temperature_log(
                        device_name=dev_name,
                        check_date=t_date,
                        check_time_period=t_period,
                        temperature=t_val,
                        recorded_by=t_recorder,
                        action_taken=t_action
                    )
                    if t_ok:
                        if is_safe_flag:
                            st.success(t_msg)
                        else:
                            st.error(t_msg)
                        st.rerun()
                    else:
                        st.error(t_msg)

        with c_tform2:
            st.markdown("#### 📊 Son Ölçümler ve Uyarılar")
            df_recent_temps = get_temperature_logs_df(days=7)
            if df_recent_temps.empty:
                st.info("Son 7 güne ait henüz sıcaklık kaydı girilmemiş.")
            else:
                unsafe_count = len(df_recent_temps[df_recent_temps['is_safe'] == 0])
                if unsafe_count > 0:
                    st.error(f"🚨 Son 7 gün içinde **{unsafe_count} adet uygunsuz sıcaklık** kaydı tespit edildi!")
                else:
                    st.success("✅ Son 7 gün içindeki tüm sıcaklık ölçümleri yasal sınırlar içinde.")

                # Küçük hızlı özet
                st.dataframe(
                    df_recent_temps[['check_date', 'check_time_period', 'device_name', 'temperature', 'is_safe']].head(6).rename(columns={
                        'check_date': 'Tarih',
                        'check_time_period': 'Öğün',
                        'device_name': 'Depo / Dolap',
                        'temperature': 'Derece (°C)',
                        'is_safe': 'Uygunluk (1=Tamam)'
                    }),
                    use_container_width=True,
                    hide_index=True
                )

        st.markdown("---")
        st.markdown("#### 📜 Resmi Isı Takip Çizelgesi (Denetim Dökümü)")
        
        c_filter1, c_filter2 = st.columns([2, 1])
        with c_filter1:
            dev_filter = st.selectbox("Cihaza Göre Filtrele:", ["Tümü"] + list(TEMPERATURE_TARGETS.keys()))
        
        df_logs = get_temperature_logs_df(device_filter=dev_filter, days=30)
        
        with c_filter2:
            st.write("")
            st.write("")
            if not df_logs.empty:
                excel_temp_bytes = export_dataframe_to_excel(df_logs)
                st.download_button(
                    label="📥 Aylık Isı Çizelgesi İndir (Excel)",
                    data=excel_temp_bytes,
                    file_name=f"Florya_MEV_Sicaklik_Cizelgesi_{datetime.date.today().isoformat()}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )

        if df_logs.empty:
            st.info("Kayıt bulunamadı.")
        else:
            st.dataframe(
                df_logs[['id', 'check_date', 'check_time_period', 'device_name', 'temperature', 'target_min', 'target_max', 'is_safe', 'action_taken', 'recorded_by']].rename(columns={
                    'id': 'No',
                    'check_date': 'Tarih',
                    'check_time_period': 'Zaman',
                    'device_name': 'Cihaz / Depo',
                    'temperature': 'Ölçülen (°C)',
                    'target_min': 'Min (°C)',
                    'target_max': 'Max (°C)',
                    'is_safe': 'Güvenli mi?',
                    'action_taken': 'Alınan Aksiyon',
                    'recorded_by': 'Kaydeden'
                }),
                use_container_width=True,
                hide_index=True
            )

# ----------------------------------------------------------
# SAYFA: 💰 KANTİN KASA & Z RAPORU MUTABAKATI
# ----------------------------------------------------------
elif selected_menu == "💰 Kantin Kasa & Z Raporu":
    render_mev_header("KANTİN GÜNLÜK KASA & Z RAPORU MUTABAKATI", "Gün sonu hasılat, POS mutabakatı ve nakit mutabakat takibi")

    canteen_stats = get_canteen_summary_stats()

    # KPI Kartları
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        render_kpi_card("Bugünkü Toplam Ciro", f"{canteen_stats['today_total']:,.2f} ₺", "Nakit + Kredi Kartı (POS)", "💰", "#10b981")
    with k2:
        render_kpi_card("Bugünkü Nakit", f"{canteen_stats['today_cash']:,.2f} ₺", "Kasaya giren nakit para", "💵", "#3b82f6")
    with k3:
        render_kpi_card("Bugünkü POS (Kart)", f"{canteen_stats['today_pos']:,.2f} ₺", "Z Raporu kredi kartı toplamı", "💳", "#8b5cf6")
    with k4:
        render_kpi_card("Kasadaki Net Nakit", f"{canteen_stats['current_cash_balance']:,.2f} ₺", "Devir ve harcamalar sonrası güncel kasa", "🏦", "#f59e0b")

    tab_kasa1, tab_kasa_pos, tab_kasa2, tab_kasa3, tab_kasa4 = st.tabs([
        "📖 Eylül 2026 Kasa Defteri (Nakit)",
        "💳 POS Cihazları Takibi (Seri No Bazlı)",
        "📝 Gün Sonu Kasa & Z Raporu Girişi",
        "📑 Günlük Kasa Çizelgesi",
        "📊 Finansal Analiz & Özet"
    ])

    # ------------------------------------------------------
    # SEKME 1: EYLÜL 2026 KASA DEFTERİ (GELİR & GİDER TEK TEK)
    # ------------------------------------------------------
    with tab_kasa1:
        st.markdown("### 📖 Basınköy MEV Eylül 2026 Kasa Defteri")
        st.caption("Masaüstünüzdeki 'BASINKÖY MEV KASA' tablosunun birebir canlı, hesaplamalı ve interaktif hali.")

        ledger_sum = get_kasa_ledger_summary("2026-09")

        # 3 Büyük Özet Kartı
        sum1, sum2, sum3 = st.columns(3)
        with sum1:
            st.markdown(f"""
            <div style="background: #ecfdf5; border: 2px solid #10b981; border-radius: 10px; padding: 15px; text-align: center;">
                <div style="font-size: 13px; color: #047857; font-weight: 700; text-transform: uppercase;">🟢 Toplam Gelir Yekûn</div>
                <div style="font-size: 26px; font-weight: 800; color: #065f46; margin: 4px 0;">{ledger_sum['total_gelir']:,.2f} ₺</div>
                <div style="font-size: 11px; color: #059669;">{ledger_sum['count_gelir'] - 1} Günlük Hasılat + Ağustos Devri</div>
            </div>
            """, unsafe_allow_html=True)
        with sum2:
            st.markdown(f"""
            <div style="background: #fef2f2; border: 2px solid #ef4444; border-radius: 10px; padding: 15px; text-align: center;">
                <div style="font-size: 13px; color: #b91c1c; font-weight: 700; text-transform: uppercase;">🔴 Toplam Gider Yekûn</div>
                <div style="font-size: 26px; font-weight: 800; color: #991b1b; margin: 4px 0;">{ledger_sum['total_gider']:,.2f} ₺</div>
                <div style="font-size: 11px; color: #dc2626;">Merkeze Teslim + Tatlıcı + Harcamalar</div>
            </div>
            """, unsafe_allow_html=True)
        with sum3:
            st.markdown(f"""
            <div style="background: #eff6ff; border: 2px solid #3b82f6; border-radius: 10px; padding: 15px; text-align: center;">
                <div style="font-size: 13px; color: #1d4ed8; font-weight: 700; text-transform: uppercase;">💰 Kasa Net Bakiye</div>
                <div style="font-size: 26px; font-weight: 800; color: #1e40af; margin: 4px 0;">{ledger_sum['net_bakiye']:,.2f} ₺</div>
                <div style="font-size: 11px; color: #2563eb;">Kasadaki Güncel Net Nakit Fazlası</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # İki Sütunlu Defter Görünümü (Sol Gider, Sağ Gelir)
        col_gider, col_gelir = st.columns([1, 1])

        df_trans = get_kasa_transactions_df("2026-09")
        df_giderler = df_trans[df_trans["trans_type"] == "GİDER"].copy()
        df_gelirler = df_trans[df_trans["trans_type"] == "GELİR"].copy()

        with col_gider:
            st.markdown("#### 🔴 GİDERLER (Çıkışlar)")
            if not df_giderler.empty:
                disp_gider = df_giderler[['order_no', 'trans_date', 'description', 'amount']].copy()
                disp_gider.rename(columns={
                    'order_no': 'Sıra',
                    'trans_date': 'Tarih',
                    'description': 'Açıklama',
                    'amount': 'Tutar (₺)'
                }, inplace=True)
                disp_gider['Tutar (₺)'] = disp_gider['Tutar (₺)'].apply(lambda x: f"{x:,.2f} ₺")
                st.dataframe(disp_gider, use_container_width=True, hide_index=True)
                st.markdown(f"**Gider Toplamı:** `{ledger_sum['total_gider']:,.2f} ₺`")

        with col_gelir:
            st.markdown("#### 🟢 GELİRLER (Girişler)")
            if not df_gelirler.empty:
                disp_gelir = df_gelirler[['order_no', 'trans_date', 'description', 'amount']].copy()
                disp_gelir.rename(columns={
                    'order_no': 'Sıra',
                    'trans_date': 'Tarih',
                    'description': 'Açıklama',
                    'amount': 'Tutar (₺)'
                }, inplace=True)
                disp_gelir['Tutar (₺)'] = disp_gelir['Tutar (₺)'].apply(lambda x: f"{x:,.2f} ₺")
                st.dataframe(disp_gelir, use_container_width=True, hide_index=True)
                st.markdown(f"**Gelir Toplamı:** `{ledger_sum['total_gelir']:,.2f} ₺`")

        # Excel İndir ve Yeni Kayıt Ekle Butonları
        st.markdown("---")
        c_btn_d1, c_btn_d2 = st.columns([1, 2])
        with c_btn_d1:
            if not df_trans.empty:
                excel_ledger_bytes = export_dataframe_to_excel(
                    df_trans.drop(columns=["id", "created_at"]),
                    sheet_name="Eylul_Kasa",
                    report_title="Basınköy MEV Koleji - Eylül 2026 Kasa Defteri"
                )
                st.download_button(
                    label="📥 Eylül Kasa Defterini Excel İndir",
                    data=excel_ledger_bytes,
                    file_name="Basinkoy_MEV_Kasa_Eylul_2026.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True,
                    type="primary"
                )

        # Yeni Tekil Gelir/Gider Ekleme Formu
        with st.expander("➕ Deftere Yeni Gelir veya Gider Satırı Ekle", expanded=False):
            with st.form("add_single_transaction_form"):
                col_t1, col_t2, col_t3 = st.columns([1, 1, 1])
                with col_t1:
                    t_kind = st.selectbox("İşlem Türü *", ["GELİR", "GİDER"])
                with col_t2:
                    t_date_val = st.date_input("İşlem Tarihi *", value=datetime.date.today())
                with col_t3:
                    t_amount_val = st.number_input("Tutar (TL) *", min_value=1.0, step=50.0, format="%.2f")

                col_t4, col_t5 = st.columns([2, 1])
                with col_t4:
                    t_desc_val = st.text_input("Açıklama *", placeholder="Örn: TÜM KASALAR veya TATLICIYA VERİLDİ")
                with col_t5:
                    t_cat_val = st.selectbox("Kategori", ["Günlük Hasılat", "Merkeze Teslim", "Tedarikçi Ödemesi", "Resmi Harcama", "Diğer Gider"])

                submit_t = st.form_submit_button("💾 Deftere Ekle", type="primary")
                if submit_t:
                    if t_amount_val > 0 and t_desc_val:
                        add_kasa_transaction(
                            trans_type=t_kind,
                            trans_date=t_date_val.isoformat(),
                            description=t_desc_val,
                            amount=t_amount_val,
                            category=t_cat_val,
                            recorded_by=current_user["full_name"]
                        )
                        st.success("✅ Yeni kayıt deftere eklendi ve buluta yedeklendi!")
                        st.rerun()

    # ------------------------------------------------------
    # SEKME: 💳 POS CİHAZLARI TAKİBİ (SERİ NO BAZLI)
    # ------------------------------------------------------
    with tab_kasa_pos:
        st.markdown("### 💳 Kantin POS Cihazları Günlük Takip Paneli")
        st.markdown("""
        <div style="background: #f0fdf4; border-left: 4px solid #16a34a; padding: 10px 14px; border-radius: 6px; margin-bottom: 15px; font-size: 13px; color: #166534;">
            🛡️ <strong>Güvenli Ayrım:</strong> Bu alan yalnızca banka POS cihazı (kredi kartı) sliplerini cihaz seri numaralarına göre takip eder. 
            <strong>Fiziksel nakit kasadan tamamen bağımsızdır ve nakitle karıştırılmaz.</strong>
        </div>
        """, unsafe_allow_html=True)

        pos_stats = get_pos_summary_stats("2026-09")

        # 4 Estetik Kart: 3 Cihaz + Toplam
        pc1, pc2, pc3, pc4 = st.columns(4)
        with pc1:
            st.markdown(f"""
            <div style="background: white; border: 1px solid #bfdbfe; border-top: 4px solid #3b82f6; border-radius: 10px; padding: 14px; box-shadow: 0 2px 4px rgba(0,0,0,0.04);">
                <div style="font-size: 11px; color: #64748b; font-weight: 700; text-transform: uppercase;">1. POS (Ana Kasa)</div>
                <div style="font-size: 12px; color: #1d4ed8; font-weight: 700; font-family: monospace; background: #eff6ff; display: inline-block; padding: 2px 6px; border-radius: 4px; margin: 3px 0;">PAV210002127</div>
                <div style="font-size: 22px; font-weight: 800; color: #1e3a8a; margin: 4px 0;">{pos_stats['total_2127']:,.2f} ₺</div>
                <div style="font-size: 11px; color: #3b82f6;">Eylül Ciro Payı: %{(pos_stats['total_2127']/pos_stats['grand_total']*100 if pos_stats['grand_total'] else 0):.1f}</div>
            </div>
            """, unsafe_allow_html=True)

        with pc2:
            st.markdown(f"""
            <div style="background: white; border: 1px solid #bbf7d0; border-top: 4px solid #10b981; border-radius: 10px; padding: 14px; box-shadow: 0 2px 4px rgba(0,0,0,0.04);">
                <div style="font-size: 11px; color: #64748b; font-weight: 700; text-transform: uppercase;">2. POS (Hızlı Kasa)</div>
                <div style="font-size: 12px; color: #047857; font-weight: 700; font-family: monospace; background: #ecfdf5; display: inline-block; padding: 2px 6px; border-radius: 4px; margin: 3px 0;">PAV210002128</div>
                <div style="font-size: 22px; font-weight: 800; color: #065f46; margin: 4px 0;">{pos_stats['total_2128']:,.2f} ₺</div>
                <div style="font-size: 11px; color: #10b981;">Eylül Ciro Payı: %{(pos_stats['total_2128']/pos_stats['grand_total']*100 if pos_stats['grand_total'] else 0):.1f}</div>
            </div>
            """, unsafe_allow_html=True)

        with pc3:
            st.markdown(f"""
            <div style="background: white; border: 1px solid #ddd6fe; border-top: 4px solid #8b5cf6; border-radius: 10px; padding: 14px; box-shadow: 0 2px 4px rgba(0,0,0,0.04);">
                <div style="font-size: 11px; color: #64748b; font-weight: 700; text-transform: uppercase;">3. POS (Mobil / Yedek)</div>
                <div style="font-size: 12px; color: #6d28d9; font-weight: 700; font-family: monospace; background: #f5f3ff; display: inline-block; padding: 2px 6px; border-radius: 4px; margin: 3px 0;">PAV210009188</div>
                <div style="font-size: 22px; font-weight: 800; color: #5b21b6; margin: 4px 0;">{pos_stats['total_9188']:,.2f} ₺</div>
                <div style="font-size: 11px; color: #8b5cf6;">Eylül Ciro Payı: %{(pos_stats['total_9188']/pos_stats['grand_total']*100 if pos_stats['grand_total'] else 0):.1f}</div>
            </div>
            """, unsafe_allow_html=True)

        with pc4:
            st.markdown(f"""
            <div style="background: white; border: 1px solid #fed7aa; border-top: 4px solid #f59e0b; border-radius: 10px; padding: 14px; box-shadow: 0 2px 4px rgba(0,0,0,0.04);">
                <div style="font-size: 11px; color: #64748b; font-weight: 700; text-transform: uppercase;">💳 TOPLAM KART CİROSU</div>
                <div style="font-size: 12px; color: #b45309; font-weight: 700; background: #fffbeb; display: inline-block; padding: 2px 6px; border-radius: 4px; margin: 3px 0;">3 Cihaz Genel Toplam</div>
                <div style="font-size: 22px; font-weight: 800; color: #92400e; margin: 4px 0;">{pos_stats['grand_total']:,.2f} ₺</div>
                <div style="font-size: 11px; color: #f59e0b;">{pos_stats['active_days']} Aktif Satış Günü</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # Cihaz Dağılım İlerleme Çubukları
        st.markdown("#### 📊 Cihazların Ciro Dağılımı")
        g_tot = pos_stats['grand_total']
        if g_tot > 0:
            c_p1, c_p2, c_p3 = st.columns(3)
            with c_p1:
                r1 = pos_stats['total_2127'] / g_tot
                st.write(f"🔵 **1. POS (PAV210002127):** %{r1*100:.1f} ({pos_stats['total_2127']:,.2f} ₺)")
                st.progress(r1)
            with c_p2:
                r2 = pos_stats['total_2128'] / g_tot
                st.write(f"🟢 **2. POS (PAV210002128):** %{r2*100:.1f} ({pos_stats['total_2128']:,.2f} ₺)")
                st.progress(r2)
            with c_p3:
                r3 = pos_stats['total_9188'] / g_tot
                st.write(f"🟣 **3. POS (PAV210009188):** %{r3*100:.1f} ({pos_stats['total_9188']:,.2f} ₺)")
                st.progress(r3)

        st.markdown("---")

        # Günlük Tablo
        st.markdown("#### 📅 Eylül 2026 Gün Gün POS Dağılım Tablosu")
        df_pos = get_pos_records_df("2026-09")
        if not df_pos.empty:
            disp_pos = df_pos[['record_date', 'day_name', 'pos_2127', 'pos_2128', 'pos_9188', 'total_pos', 'notes']].copy()
            disp_pos.rename(columns={
                'record_date': 'Tarih',
                'day_name': 'Gün',
                'pos_2127': '1. POS: PAV210002127 (₺)',
                'pos_2128': '2. POS: PAV210002128 (₺)',
                'pos_9188': '3. POS: PAV210009188 (₺)',
                'total_pos': 'Günlük Toplam POS (₺)',
                'notes': 'Notlar'
            }, inplace=True)

            # Sayısal formatlama
            for col in ['1. POS: PAV210002127 (₺)', '2. POS: PAV210002128 (₺)', '3. POS: PAV210009188 (₺)', 'Günlük Toplam POS (₺)']:
                disp_pos[col] = disp_pos[col].apply(lambda x: f"{x:,.2f} ₺" if x > 0 else "-")

            st.dataframe(disp_pos, use_container_width=True, hide_index=True)

            # Excel İndir Butonu
            c_pos_btn1, c_pos_btn2 = st.columns([1, 2])
            with c_pos_btn1:
                excel_pos_bytes = export_dataframe_to_excel(
                    df_pos.drop(columns=["id", "created_at"]),
                    sheet_name="POS_Takip",
                    report_title="Florya MEV Koleji - Kantin POS Cihazları Günlük Takip Raporu (Seri No Bazlı)"
                )
                st.download_button(
                    label="📥 POS Raporunu Excel İndir (Seri No Bazlı)",
                    data=excel_pos_bytes,
                    file_name="Kantin_POS_Cihazlari_Seri_No_Eylul_2026.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True,
                    type="primary"
                )

        # Yeni Günlük POS Girişi / Güncelleme Formu
        with st.expander("➕ Günlük POS Çekim Tutarlarını Gir / Güncelle", expanded=False):
            col_pd1, col_pd2 = st.columns([1, 2])
            with col_pd1:
                p_date = st.date_input("Kasa Tarihi Seçin *", value=datetime.date.today(), key="pos_date_selector")
            
            p_pos_snap, p_cash_snap = get_day_financial_snapshot(p_date.isoformat())
            
            with col_pd2:
                if p_pos_snap["total_pos"] > 0:
                    st.info(f"ℹ️ **{p_date.strftime('%d.%m.%Y')}** gününe ait kayıtlı POS toplamı: **{p_pos_snap['total_pos']:,.2f} ₺**. Cihaz tutarlarını aşağıdan güncelleyebilirsiniz.")
                elif p_cash_snap["cash_revenue"] > 0:
                    st.info(f"💵 Bu tarihe ait **{p_cash_snap['cash_revenue']:,.2f} ₺** nakit kaydı mevcut. Gireceğiniz POS tutarları Günlük Kasa Çizelgesi'ne otomatik olarak işlenecektir.")

            with st.form("add_pos_daily_form"):
                p_day_names = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
                default_day_idx = p_date.weekday()
                p_day = st.selectbox("Gün", p_day_names, index=default_day_idx, key="pos_day_in")

                st.markdown("##### 💳 Cihaz Bazlı POS Tutarları (TL)")
                col_pdev1, col_pdev2, col_pdev3 = st.columns(3)
                with col_pdev1:
                    v_2127 = st.number_input("1. POS (PAV210002127)", value=p_pos_snap["pos_2127"], min_value=0.0, step=10.0, format="%.2f", key="in_2127")
                with col_pdev2:
                    v_2128 = st.number_input("2. POS (PAV210002128)", value=p_pos_snap["pos_2128"], min_value=0.0, step=10.0, format="%.2f", key="in_2128")
                with col_pdev3:
                    v_9188 = st.number_input("3. POS (PAV210009188)", value=p_pos_snap["pos_9188"], min_value=0.0, step=10.0, format="%.2f", key="in_9188")

                p_note = st.text_input("Açıklama / Notlar", value=p_pos_snap["notes"], placeholder="Örn: 2. POS cihazında rulo bittiği için öğleden sonra 3. cihaza geçildi", key="pos_note_in")

                submit_pos = st.form_submit_button("💾 POS Tutarlarını Kaydet (Tüm Çizelgelere İşle)", type="primary")
                if submit_pos:
                    add_or_update_pos_record(
                        record_date=p_date.isoformat(),
                        day_name=p_day,
                        pos_2127=v_2127,
                        pos_2128=v_2128,
                        pos_9188=v_9188,
                        notes=p_note,
                        recorded_by=current_user["full_name"]
                    )
                    st.success(f"✅ {p_date.strftime('%d.%m.%Y')} tarihli POS çekimleri kaydedildi ve Günlük Kasa Çizelgesi'ne otomatik olarak işlendi!")
                    st.rerun()

    # ------------------------------------------------------
    # SEKME 3: GÜN SONU KASA & Z RAPORU GİRİŞİ
    # ------------------------------------------------------
    with tab_kasa2:
        st.markdown("### 📝 Gün Sonu Kasa ve Hasılat Kaydı")
        st.caption("Kantin görevlisi gün sonunda Z raporunu alıp eldeki nakit ve harcamaları aşağıdaki forma girmelidir. Girdiğiniz her veri diğer tüm sekmelere ve çizelgelere otomatik olarak aktarılır.")

        c_pick1, c_pick2 = st.columns([1, 2])
        with c_pick1:
            k_date = st.date_input("Kasa Tarihi Seçin *", value=datetime.date.today(), key="entry_kasa_date")

        pos_snap, cash_snap = get_day_financial_snapshot(k_date.isoformat())

        with c_pick2:
            if pos_snap["total_pos"] > 0 and cash_snap["cash_revenue"] > 0:
                st.success(f"ℹ️ **{k_date.strftime('%d.%m.%Y')}** gününe ait Nakit ({cash_snap['cash_revenue']:,.2f} ₺) ve POS ({pos_snap['total_pos']:,.2f} ₺) kayıtları yüklendi. Düzenleyip kaydedebilirsiniz.")
            elif pos_snap["total_pos"] > 0:
                st.info(f"💳 **{k_date.strftime('%d.%m.%Y')}** gününe ait POS Cihazları sekmesinden toplam **{pos_snap['total_pos']:,.2f} ₺** kart çekimi bulundu ve otomatik olarak POS alanına aktarıldı.")
            elif cash_snap["cash_revenue"] > 0:
                st.info(f"💵 **{k_date.strftime('%d.%m.%Y')}** gününe ait **{cash_snap['cash_revenue']:,.2f} ₺** nakit hasılat kaydı yüklendi.")

        with st.form("canteen_cash_entry_form"):
            c_f1, c_f2 = st.columns(2)
            with c_f1:
                st.markdown(f"**Seçili Tarih:** `{k_date.strftime('%d.%m.%Y')}`")
            with c_f2:
                k_zno = st.text_input("Z Raporu / Fiş No", value=cash_snap["z_report_no"], placeholder="Örn: Z-0042 veya Fiş-128")

            st.markdown("#### 🟢 1. Günlük Gelirler (Hasılat)")
            c_rev1, c_rev2 = st.columns(2)
            with c_rev1:
                k_cash = st.number_input("Nakit Hasılat (TL) *", value=cash_snap["cash_revenue"], min_value=0.0, step=10.0, format="%.2f", help="Kasada toplanan fiziksel nakit para")
            with c_rev2:
                init_pos = pos_snap["total_pos"] if pos_snap["total_pos"] > 0 else cash_snap["pos_revenue"]
                k_pos = st.number_input("Kredi Kartı / POS Hasılatı (TL) *", value=init_pos, min_value=0.0, step=10.0, format="%.2f", help="POS cihazlarından veya Z Raporundan çıkan kredi kartı toplamı")

            st.markdown("#### 🔴 2. Kasadan Yapılan Çıkışlar ve Harcamalar")
            c_exp1, c_exp2, c_exp3 = st.columns(3)
            with c_exp1:
                k_hq = st.number_input("Merkeze Gönderilen Nakit (TL)", value=cash_snap["transferred_to_hq"], min_value=0.0, step=50.0, format="%.2f", help="Okul yönetimine veya bankaya teslim edilen para")
            with c_exp2:
                k_vendor = st.number_input("Tedarikçi Ödemesi (TL)", value=cash_snap["vendor_payouts"], min_value=0.0, step=10.0, format="%.2f", help="Tatlıcı, ekmekçi vb. elden yapılan nakit ödemeler")
            with c_exp3:
                k_other = st.number_input("Diğer Giderler / Sarf (TL)", value=cash_snap["other_expenses"], min_value=0.0, step=5.0, format="%.2f", help="Kantin için yapılan acil küçük harcamalar")

            st.markdown("#### 📌 3. Açıklama ve Notlar")
            default_notes = cash_snap["notes"] or (pos_snap["notes"] if pos_snap["notes"] else "")
            k_notes = st.text_area("Açıklama (Örn: Tatlıcı Mehmet Usta'ya 3.000 TL verildi, Merkeze 60.000 TL teslim edildi)", value=default_notes, placeholder="Detayları buraya yazabilirsiniz...")
            k_recorder = st.text_input("Kaydı Yapan Personel", value=cash_snap["recorded_by"] or current_user["full_name"])

            submit_kasa = st.form_submit_button("💾 Günlük Kasayı Sisteme Kaydet (Tüm Çizelgelere İşle)", type="primary", use_container_width=True)

            if submit_kasa:
                if k_cash == 0.0 and k_pos == 0.0:
                    st.warning("⚠️ Lütfen en az bir hasılat tutarı (Nakit veya Kart) giriniz.")
                else:
                    success = add_canteen_cash_record(
                        record_date=k_date.isoformat(),
                        cash_revenue=k_cash,
                        pos_revenue=k_pos,
                        transferred_to_hq=k_hq,
                        vendor_payouts=k_vendor,
                        other_expenses=k_other,
                        z_report_no=k_zno,
                        notes=k_notes,
                        recorded_by=k_recorder
                    )
                    if success:
                        st.success(f"✅ {k_date.strftime('%d.%m.%Y')} tarihli kasa ve POS kayıtları tüm sekmelere (Kasa Çizelgesi, POS Takip, Kasa Defteri) başarıyla işlendi ve buluta yedeklendi!")
                        st.rerun()

    # ------------------------------------------------------
    # SEKME 3: GÜNLÜK KASA ÇİZELGESİ & EXCEL
    # ------------------------------------------------------
    with tab_kasa3:
        st.markdown("### 📑 Günlük Kasa Çizelgesi")
        st.caption("Drive'ınızdaki resmi Kasa Defteri mantığıyla tutulan tüm günlük gelir, gider ve net nakit dökümü.")

        c_filt1, c_filt2, c_filt3 = st.columns([2, 2, 2])
        with c_filt1:
            start_d = st.date_input("Başlangıç Tarihi", value=datetime.date.today().replace(day=1))
        with c_filt2:
            end_d = st.date_input("Bitiş Tarihi", value=datetime.date.today())

        df_canteen = get_canteen_records_df(start_date=start_d.isoformat(), end_date=end_d.isoformat())

        with c_filt3:
            st.write("")
            st.write("")
            if not df_canteen.empty:
                excel_kasa_bytes = export_dataframe_to_excel(
                    df_canteen.drop(columns=["id", "created_at"]),
                    sheet_name="Kasa_Defteri",
                    report_title="Florya MEV Koleji - Kantin Günlük Kasa Defteri"
                )
                st.download_button(
                    label="📥 Kasa Defterini İndir (Excel)",
                    data=excel_kasa_bytes,
                    file_name=f"Florya_MEV_Kantin_Kasa_{datetime.date.today().isoformat()}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )

        if df_canteen.empty:
            st.info("ℹ️ Seçilen tarih aralığında henüz kasa kaydı bulunmuyor. 'Gün Sonu Kasa Girişi' sekmesinden ilk kaydınızı oluşturabilirsiniz.")
        else:
            # Dönem Özet Kartları
            c_tot_cash = float(df_canteen["cash_revenue"].sum())
            c_tot_pos = float(df_canteen["pos_revenue"].sum())
            c_tot_rev = float(df_canteen["total_revenue"].sum())
            c_tot_out = float((df_canteen["transferred_to_hq"] + df_canteen["vendor_payouts"] + df_canteen["other_expenses"]).sum())
            c_tot_net = float(df_canteen["net_cash_remaining"].sum())

            sc1, sc2, sc3, sc4, sc5 = st.columns(5)
            with sc1:
                st.metric("💵 Nakit Hasılat", f"{c_tot_cash:,.2f} ₺")
            with sc2:
                st.metric("💳 POS / Kart", f"{c_tot_pos:,.2f} ₺")
            with sc3:
                st.metric("💰 Toplam Ciro", f"{c_tot_rev:,.2f} ₺")
            with sc4:
                st.metric("🔴 Toplam Çıkış", f"{c_tot_out:,.2f} ₺")
            with sc5:
                st.metric("🏦 Kasa Net Bakiyesi", f"{(c_tot_net + 18845.0):,.2f} ₺", help=f"Ağustos'tan devreden 18.845 ₺ dahil kasadaki güncel net nakit (Eylül net nakit farkı: {c_tot_net:,.2f} ₺)")

            st.write("")

            display_df = df_canteen[['id', 'record_date', 'z_report_no', 'cash_revenue', 'pos_revenue', 'total_revenue',
                                     'transferred_to_hq', 'vendor_payouts', 'other_expenses', 'net_cash_remaining', 'notes', 'recorded_by']].copy()
            display_df.rename(columns={
                'id': 'Kayıt No',
                'record_date': 'Tarih',
                'z_report_no': 'Z Raporu No',
                'cash_revenue': 'Nakit Hasılat (₺)',
                'pos_revenue': 'POS / Kart (₺)',
                'total_revenue': 'Toplam Ciro (₺)',
                'transferred_to_hq': 'Merkeze Teslim (₺)',
                'vendor_payouts': 'Tedarikçi Ödemesi (₺)',
                'other_expenses': 'Diğer Giderler (₺)',
                'net_cash_remaining': 'Kalan Net Nakit (₺)',
                'notes': 'Açıklama',
                'recorded_by': 'Kaydeden'
            }, inplace=True)

            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Nakit Hasılat (₺)": st.column_config.NumberColumn(format="%.2f ₺"),
                    "POS / Kart (₺)": st.column_config.NumberColumn(format="%.2f ₺"),
                    "Toplam Ciro (₺)": st.column_config.NumberColumn(format="%.2f ₺"),
                    "Merkeze Teslim (₺)": st.column_config.NumberColumn(format="%.2f ₺"),
                    "Tedarikçi Ödemesi (₺)": st.column_config.NumberColumn(format="%.2f ₺"),
                    "Diğer Giderler (₺)": st.column_config.NumberColumn(format="%.2f ₺"),
                    "Kalan Net Nakit (₺)": st.column_config.NumberColumn(format="%.2f ₺"),
                }
            )

            # Yönetici için Silme / Düzeltme İzni
            if is_admin():
                with st.expander("🗑️ Hatalı Kasa Kaydını Sil (Yönetici İzni)", expanded=False):
                    del_id = st.selectbox("Silinecek Kayıt Numarasını Seçin:", df_canteen["id"].tolist())
                    if st.button("🚨 Seçili Kaydı Kalıcı Olarak Sil", type="secondary"):
                        delete_canteen_record(del_id)
                        st.success(f"Kayıt #{del_id} başarıyla silindi ve yedekler güncellendi.")
                        st.rerun()

    # ------------------------------------------------------
    # SEKME 4: AYLIK FİNANSAL ÖZET
    # ------------------------------------------------------
    with tab_kasa4:
        st.markdown("### 📊 Kantin Aylık Finansal Tablosu")
        st.caption("Ciro dağılımı, tahsilat yöntemleri ve yapılan masrafların karşılaştırmalı analizi.")

        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.markdown(f"""
            <div style="background: white; border: 1px solid #e2e8f0; border-radius: 10px; padding: 18px; margin-bottom: 15px;">
                <h4 style="color: #1e3a8a; margin-top: 0;">📅 Bu Ayın Toplam Finansal Tablosu</h4>
                <table style="width: 100%; border-collapse: collapse; font-size: 14px;">
                    <tr style="border-bottom: 1px solid #f1f5f9; height: 35px;">
                        <td><strong>💰 Toplam Satış Cirosu:</strong></td>
                        <td style="text-align: right; font-weight: 700; color: #10b981;">{canteen_stats['month_total']:,.2f} ₺</td>
                    </tr>
                    <tr style="border-bottom: 1px solid #f1f5f9; height: 35px;">
                        <td>💵 Nakit Hasılat:</td>
                        <td style="text-align: right; color: #3b82f6;">{canteen_stats['month_cash']:,.2f} ₺</td>
                    </tr>
                    <tr style="border-bottom: 1px solid #f1f5f9; height: 35px;">
                        <td>💳 Kredi Kartı / POS:</td>
                        <td style="text-align: right; color: #8b5cf6;">{canteen_stats['month_pos']:,.2f} ₺</td>
                    </tr>
                    <tr style="border-bottom: 1px solid #f1f5f9; height: 35px;">
                        <td>🏢 Merkeze Teslim Edilen:</td>
                        <td style="text-align: right; color: #64748b;">{canteen_stats['month_transferred']:,.2f} ₺</td>
                    </tr>
                    <tr style="border-bottom: 1px solid #f1f5f9; height: 35px;">
                        <td>🧾 Tedarikçi & Gider Ödemeleri:</td>
                        <td style="text-align: right; color: #ef4444;">{canteen_stats['month_expenses']:,.2f} ₺</td>
                    </tr>
                    <tr style="height: 38px; background: #f8fafc; border-top: 2px solid #cbd5e1;">
                        <td><strong>🏦 Kasadaki Güncel Net Bakiye:</strong></td>
                        <td style="text-align: right; font-weight: 800; color: #1e40af; font-size: 15px;">{canteen_stats['current_cash_balance']:,.2f} ₺</td>
                    </tr>
                </table>
            </div>
            """, unsafe_allow_html=True)

        with col_m2:
            st.markdown("#### 💳 Nakit vs POS Oranı")
            month_tot = canteen_stats['month_total']
            if month_tot > 0:
                cash_pct = (canteen_stats['month_cash'] / month_tot) * 100
                pos_pct = (canteen_stats['month_pos'] / month_tot) * 100
                st.write(f"💵 **Nakit Oranı:** %{cash_pct:.1f} ({canteen_stats['month_cash']:,.2f} ₺)")
                st.progress(cash_pct / 100)
                st.write(f"💳 **Kredi Kartı (POS) Oranı:** %{pos_pct:.1f} ({canteen_stats['month_pos']:,.2f} ₺)")
                st.progress(pos_pct / 100)
            else:
                st.info("Bu aya ait henüz satış kaydı girilmediğinde oran grafiği burada görüntülenecektir.")

# ----------------------------------------------------------
# SAYFA 4: 📥 EXCEL İLE TOPLU YÜKLEME
# ----------------------------------------------------------
elif selected_menu == "📥 Excel ile Toplu Yükleme":
    render_mev_header("EXCEL İLE TOPLU STOK İŞLEMLERİ", "Excel dosyası ile toplu ürün ve stok aktarımı")

    st.markdown("""
    Bu panel üzerinden yüzlerce ürünü ve stok bilgisini tek bir Excel dosyası yükleyerek sisteme aktarabilirsiniz.
    """)

    col_t1, col_t2 = st.columns([1, 1])

    with col_t1:
        st.markdown("### 1. Adım: Örnek Şablonu İndirin")
        st.write("Sütun başlıklarının ve veri türlerinin doğru olması için hazırladığımız formatlı örnek Excel şablonunu kullanınız.")
        template_bytes = generate_import_template()
        st.download_button(
            label="📄 Örnek Excel Şablonunu İndir (.xlsx)",
            data=template_bytes,
            file_name="Florya_MEV_Stok_Sablonu.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            type="primary",
            use_container_width=True
        )

    with col_t2:
        st.markdown("### 2. Adım: Yükleme Seçenekleri")
        import_mode = st.radio(
            "Mevcut Ürün Eşleştiğinde Yapılacak İşlem:",
            [
                ("update", "🔄 Varsa Stoğu Artır / Bilgileri Güncelle (Tavsiye Edilen)"),
                ("new_only", "➕ Sadece Yeni Ürünleri Ekle (Var olanları atla)")
            ],
            format_func=lambda x: x[1]
        )[0]

    st.markdown("---")
    st.markdown("### 3. Adım: Excel Dosyanızı Yükleyin")
    uploaded_file = st.file_uploader("Doldurduğunuz Excel dosyasını buraya sürükleyin (.xlsx veya .xls)", type=["xlsx", "xls"])

    if uploaded_file is not None:
        try:
            preview_df = pd.read_excel(uploaded_file)
            st.success(f"Dosya başarıyla yüklendi! Toplam **{len(preview_df)}** satır tespit edildi.")
            
            with st.expander("👀 Yüklenen Dosyanın Önizlemesi (İlk 10 Satır)", expanded=True):
                st.dataframe(preview_df.head(10), use_container_width=True)

            # Aktarımı Başlat Butonu
            if st.button("🚀 Veritabanına Aktarımı Başlat", type="primary", use_container_width=True):
                with st.spinner("Veriler işleniyor ve veritabanına aktarılıyor..."):
                    uploaded_file.seek(0)
                    result = parse_and_import_excel(
                        file_bytes=uploaded_file.read(),
                        update_mode=import_mode,
                        user_name=current_user["full_name"]
                    )

                if result["success"]:
                    st.success(f"""
                    ✅ **İşlem Tamamlandı!**
                    * Yeni Eklenen Ürün Kartı: **{result['added']}**
                    * Güncellenen / Stok Artırılan: **{result['updated']}**
                    """)
                    if result["errors"]:
                        with st.expander("⚠️ Uyarılar ve Atlanan Satırlar"):
                            for err in result["errors"]:
                                st.write(f"- {err}")
                else:
                    st.error(f"Aktarım başarısız: {result['errors']}")
        except Exception as e:
            st.error(f"Dosya okunurken bir hata meydana geldi: {str(e)}")

# ----------------------------------------------------------
# SAYFA 5: 🔄 HAREKET GEÇMİŞİ (AUDIT LOGS)
# ----------------------------------------------------------
elif selected_menu == "🔄 Hareket Geçmişi (Loglar)":
    render_mev_header("STOK HAREKET GEÇMİŞİ", "Tüm giriş, çıkış, sayım ve fire denetim kayıtları")

    col_h1, col_h2 = st.columns([2, 2])
    with col_h1:
        mov_filter = st.selectbox("Hareket Türü Filtresi", ["Tümü", "GİRİŞ", "ÇIKIŞ", "SAYIM DÜZELTME", "FİRE / İMHA"])
    with col_h2:
        row_limit = st.select_slider("Kayıt Limiti", options=[50, 100, 200, 500, 1000], value=200)

    movements_df = get_stock_movements_df(limit=row_limit, movement_type=mov_filter)

    col_d1, col_d2 = st.columns([4, 2])
    with col_d1:
        st.caption(f"Son {len(movements_df)} hareket kaydı listeleniyor.")
    with col_d2:
        if not movements_df.empty:
            mov_excel = export_dataframe_to_excel(
                movements_df.drop(columns=["id"]),
                sheet_name="Hareket_Loglari",
                report_title="Stok Hareket ve Denetim İzi Raporu"
            )
            st.download_button(
                label="📥 Hareket Raporunu Excel Olarak İndir",
                data=mov_excel,
                file_name=f"Florya_MEV_Hareket_Raporu_{datetime.date.today().isoformat()}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
                type="primary"
            )

    if movements_df.empty:
        st.info("Kayıtlı hareket bulunamadı.")
    else:
        st.dataframe(
            movements_df.drop(columns=["id"]),
            use_container_width=True,
            hide_index=True
        )

# ----------------------------------------------------------
# SAYFA 6: 👥 KULLANICI YÖNETİMİ (ADMIN ONLY)
# ----------------------------------------------------------
elif selected_menu == "👥 Kullanıcı Yönetimi":
    render_mev_header("KULLANICI VE YETKİ YÖNETİMİ", "Sisteme giriş yapabilecek personel ve yöneticiler")

    if not is_admin():
        st.error("⛔ Bu sayfaya yalnızca yöneticiler erişebilir.")
        st.stop()

    users_list = get_all_users()
    users_df = pd.DataFrame(users_list)
    
    st.markdown("### Kayıtlı Kullanıcılar")
    if not users_df.empty:
        st.dataframe(
            users_df[["id", "username", "full_name", "role", "created_at"]].rename(columns={
                "id": "ID",
                "username": "Kullanıcı Adı",
                "full_name": "Ad Soyad",
                "role": "Rol",
                "created_at": "Kayıt Tarihi"
            }),
            use_container_width=True,
            hide_index=True
        )

    st.markdown("---")
    col_u1, col_u2 = st.columns(2)

    with col_u1:
        st.markdown("#### ➕ Yeni Kullanıcı Hesabı Ekle")
        with st.form("add_user_form", clear_on_submit=True):
            nu_username = st.text_input("Kullanıcı Adı *", placeholder="örn: ahmet")
            nu_fullname = st.text_input("Ad Soyad ve Görev *", placeholder="örn: Ahmet Yılmaz (Aşçıbaşı)")
            nu_password = st.text_input("Şifre *", type="password", placeholder="••••••••")
            nu_role = st.selectbox("Rol *", [("personel", "Personel (Giriş/Çıkış yapabilir)"), ("admin", "Yönetici (Tam Yetkili)")], format_func=lambda x: x[1])[0]

            nu_submit = st.form_submit_button("Kullanıcıyı Kaydet 💾", type="primary")
            if nu_submit:
                succ, u_msg = create_user(nu_username, nu_password, nu_fullname, nu_role)
                if succ:
                    st.success(u_msg)
                    st.rerun()
                else:
                    st.error(u_msg)

    with col_u2:
        st.markdown("#### 🗑️ Kullanıcı Hesabı Sil")
        del_candidates = [u for u in users_list if u['id'] != current_user['id']]
        if not del_candidates:
            st.info("Silinebilecek başka bir kullanıcı hesabı bulunmamaktadır.")
        else:
            del_map = {f"{u['full_name']} (@{u['username']})": u['id'] for u in del_candidates}
            selected_del = st.selectbox("Silinecek Kullanıcı:", list(del_map.keys()))
            
            if st.button("Kullanıcıyı Kalıcı Olarak Sil", type="secondary"):
                succ, d_msg = delete_user(del_map[selected_del])
                if succ:
                    st.warning(d_msg)
                    st.rerun()
                else:
                    st.error(d_msg)

# ----------------------------------------------------------
# SAYFA 7: ⚙️ VERİTABANI & AYARLAR (ADMIN ONLY)
# ----------------------------------------------------------
elif selected_menu == "⚙️ Veritabanı & Ayarlar":
    render_mev_header("SİSTEM VE VERİTABANI YAPILANDIRMASI", "SQLite ve Supabase Cloud bağlantı yönetimi")

    if not is_admin():
        st.error("⛔ Bu sayfaya yalnızca yöneticiler erişebilir.")
        st.stop()

    c_sb1, c_sb2 = st.columns(2)

    with c_sb1:
        st.markdown("### 🗄️ Aktif Veritabanı Durumu")
        if is_supabase_active():
            st.success("🟢 **Aktif Veritabanı:** Supabase Cloud (PostgreSQL)")
        else:
            st.info("🔵 **Aktif Veritabanı:** Yerel SQLite (`depo_stok.db`)")
        st.write(f"Dosya Konumu: `{DB_PATH}`")
        st.caption("Veriler yerel dosyanızda güvenle saklanmaktadır. Herhangi bir sunucu kurulumu gerektirmez.")

        st.markdown("#### 💾 Tek Tıkla Veritabanı Yedeği Al")
        if DB_PATH.exists():
            with open(DB_PATH, "rb") as f_db:
                db_bytes = f_db.read()
            
            st.download_button(
                label="📥 depo_stok.db Dosyasını İndir (Tam Sistem Yedeği)",
                data=db_bytes,
                file_name=f"Florya_MEV_Yedek_{datetime.date.today().isoformat()}.db",
                mime="application/x-sqlite3",
                type="primary",
                use_container_width=True
            )
            st.caption("Bu `.db` dosyasını flash belleğe veya Google Drive / OneDrive'a atarak verilerinizi %100 güvenceye alabilirsiniz.")

    with c_sb2:
        st.markdown("### ☁️ Supabase Cloud Entegrasyonu")
        st.markdown("""
        Uygulamayı bulut ortamında (Supabase) çalıştırmak için:
        1. Proje ana dizinindeki `.env` dosyasını açın (veya `.env.example` dosyasını `.env` olarak kopyalayın).
        2. Supabase projenizden aldığınız `SUPABASE_URL` ve `SUPABASE_KEY` değerlerini girin.
        3. `DB_TYPE=supabase` yapın.
        4. Supabase SQL Editor sekmesinde projede bulunan `supabase_schema.sql` dosyasını çalıştırın.
        """)

    with st.expander("📜 Supabase SQL Şeması (Kopyalamak İçin)"):
        with open("supabase_schema.sql", "r", encoding="utf-8") as f:
            st.code(f.read(), language="sql")
