"""
Florya MEV Koleji - Depo ve Stok Takip Sistemi
Görsel Bileşenler, Özel Stiller (CSS) ve Kartlar
"""

import streamlit as st

def inject_custom_css():
    """Uygulamaya özel modern ve kurumsal CSS stilini enjekte eder."""
    st.markdown("""
    <style>
        /* Ana font ve sayfa ayarları */
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        /* Başlıklar */
        h1, h2, h3 {
            color: #0f172a;
            font-weight: 700;
        }

        /* KPI Metrik Kartları */
        .kpi-card {
            background-color: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 16px 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.04);
            margin-bottom: 12px;
            transition: transform 0.15s ease, box-shadow 0.15s ease;
        }
        .kpi-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.08);
        }
        .kpi-title {
            font-size: 13px;
            font-weight: 600;
            color: #64748b;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 6px;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .kpi-value {
            font-size: 26px;
            font-weight: 800;
            color: #0f172a;
            line-height: 1.2;
        }
        .kpi-subtext {
            font-size: 12px;
            color: #94a3b8;
            margin-top: 4px;
        }

        /* Kritik Rozetler */
        .badge-danger {
            background-color: #fef2f2;
            color: #b91c1c;
            border: 1px solid #fecaca;
            padding: 3px 8px;
            border-radius: 6px;
            font-weight: 700;
            font-size: 12px;
            display: inline-block;
        }
        .badge-warning {
            background-color: #fffbeb;
            color: #b45309;
            border: 1px solid #fde68a;
            padding: 3px 8px;
            border-radius: 6px;
            font-weight: 700;
            font-size: 12px;
            display: inline-block;
        }
        .badge-success {
            background-color: #f0fdf4;
            color: #15803d;
            border: 1px solid #bbf7d0;
            padding: 3px 8px;
            border-radius: 6px;
            font-weight: 700;
            font-size: 12px;
            display: inline-block;
        }

        /* Üst Kurumsal Header */
        .mev-header {
            background: linear-gradient(135deg, #1e3a8a 0%, #172554 100%);
            color: white;
            padding: 16px 24px;
            border-radius: 12px;
            margin-bottom: 24px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            box-shadow: 0 4px 10px rgba(30, 58, 138, 0.15);
        }
        .mev-header-title {
            font-size: 20px;
            font-weight: 800;
            letter-spacing: 0.5px;
            margin: 0;
            color: #ffffff;
        }
        .mev-header-sub {
            font-size: 13px;
            color: #cbd5e1;
            margin-top: 4px;
        }

        /* Tablo Stilleri */
        .stDataFrame {
            border-radius: 8px;
            overflow: hidden;
        }
    </style>
    """, unsafe_allow_html=True)

def render_mev_header(title: str = "DEPO VE STOK YÖNETİM PORTALI", subtitle: str = "Florya MEV Koleji Operasyon Yönetimi"):
    """Sayfa üstünde şık bir kurumsal başlık gösterir."""
    st.markdown(f"""
    <div class="mev-header">
        <div>
            <div class="mev-header-title">🏫 FLORYA MEV KOLEJİ • {title}</div>
            <div class="mev-header-sub">{subtitle}</div>
        </div>
        <div style="text-align: right; font-size: 12px; color: #93c5fd;">
            <b>Gıda Güvenliği & HACCP</b><br>FEFO Takip Sistemi
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_kpi_card(title: str, value: str, subtext: str = "", icon: str = "📊", border_color: str = "#e2e8f0"):
    """Özel tasarımlı KPI kartı çizer."""
    st.markdown(f"""
    <div class="kpi-card" style="border-left: 4px solid {border_color};">
        <div class="kpi-title">{icon} {title}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-subtext">{subtext}</div>
    </div>
    """, unsafe_allow_html=True)
