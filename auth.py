"""
Florya MEV Koleji - Depo ve Stok Takip Sistemi
Kimlik Doğrulama ve Kullanıcı Yönetimi (Auth)
"""

import streamlit as st
import sqlite3
from typing import Optional, Dict, List
from database import get_sqlite_connection, get_hash, is_supabase_active, get_supabase_client

def authenticate(username: str, password: str) -> Optional[Dict]:
    """Kullanıcı adı ve şifreyi doğrular. Başarılı ise kullanıcı bilgilerini döndürür."""
    password_hash = get_hash(password)

    if is_supabase_active():
        try:
            supabase = get_supabase_client()
            res = supabase.table("users").select("*").eq("username", username).eq("password_hash", password_hash).execute()
            if res.data and len(res.data) > 0:
                user = res.data[0]
                return {
                    "id": user["id"],
                    "username": user["username"],
                    "full_name": user["full_name"],
                    "role": user["role"]
                }
        except Exception as e:
            st.error(f"Supabase giriş hatası: {e}")
            return None

    # SQLite doğrulama
    conn = get_sqlite_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, username, full_name, role 
        FROM users 
        WHERE username = ? AND password_hash = ?
    """, (username, password_hash))
    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            "id": row["id"],
            "username": row["username"],
            "full_name": row["full_name"],
            "role": row["role"]
        }
    return None

def login_user(user: Dict):
    """Kullanıcıyı oturuma alır."""
    st.session_state["authenticated"] = True
    st.session_state["user"] = user

def logout_user():
    """Kullanıcı oturumunu sonlandırır."""
    st.session_state["authenticated"] = False
    st.session_state["user"] = None
    st.rerun()

def get_current_user() -> Optional[Dict]:
    """Aktif giriş yapan kullanıcıyı döndürür."""
    return st.session_state.get("user")

def is_authenticated() -> bool:
    """Kullanıcının giriş yapıp yapmadığını kontrol eder."""
    return st.session_state.get("authenticated", False) and st.session_state.get("user") is not None

def is_admin() -> bool:
    """Giriş yapan kullanıcının yönetici olup olmadığını kontrol eder."""
    user = get_current_user()
    return user is not None and user.get("role") == "admin"

def get_all_users() -> List[Dict]:
    """Tüm kayıtlı kullanıcıları listeler."""
    conn = get_sqlite_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, full_name, role, created_at FROM users ORDER BY id ASC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def create_user(username: str, password: str, full_name: str, role: str) -> tuple[bool, str]:
    """Yeni bir kullanıcı hesabı açar."""
    if not username or not password or not full_name:
        return False, "Lütfen tüm zorunlu alanları doldurun."
    
    password_hash = get_hash(password)
    conn = get_sqlite_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO users (username, password_hash, full_name, role)
            VALUES (?, ?, ?, ?)
        """, (username.strip(), password_hash, full_name.strip(), role))
        conn.commit()
        return True, "Kullanıcı başarıyla oluşturuldu."
    except sqlite3.IntegrityError:
        return False, f"'{username}' kullanıcı adı zaten mevcut!"
    except Exception as e:
        return False, f"Hata: {str(e)}"
    finally:
        conn.close()

def delete_user(user_id: int) -> tuple[bool, str]:
    """Kullanıcı hesabını siler."""
    current_user = get_current_user()
    if current_user and current_user.get("id") == user_id:
        return False, "Kendi oturum açtığınız hesabı silemezsiniz!"

    conn = get_sqlite_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        return True, "Kullanıcı başarıyla silindi."
    except Exception as e:
        return False, f"Hata: {str(e)}"
    finally:
        conn.close()

def render_login_page():
    """Giriş formu arayüzünü çizer."""
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 25px 0 10px 0;">
            <div style="font-size: 42px;">📦 🏫</div>
            <h2 style="color: #1e3a8a; margin-bottom: 4px; font-weight: 800;">FLORYA MEV KOLEJİ</h2>
            <h4 style="color: #475569; margin-top: 0; font-weight: 500;">Depo ve Stok Yönetim Portalı</h4>
            <p style="font-size: 13px; color: #64748b;">Lütfen devam etmek için yetkili kullanıcı bilgilerinizle giriş yapın.</p>
        </div>
        """, unsafe_allow_html=True)

        with st.form("login_form", clear_on_submit=False):
            username_input = st.text_input("Kullanıcı Adı", placeholder="Örn: admin veya depo")
            password_input = st.text_input("Şifre", type="password", placeholder="••••••••")
            submit_btn = st.form_submit_button("Giriş Yap 🚀", use_container_width=True, type="primary")

            if submit_btn:
                if not username_input or not password_input:
                    st.warning("Lütfen kullanıcı adı ve şifrenizi girin.")
                else:
                    user = authenticate(username_input.strip(), password_input)
                    if user:
                        login_user(user)
                        st.success(f"Hoş geldiniz, {user['full_name']}!")
                        st.rerun()
                    else:
                        st.error("Hatalı kullanıcı adı veya şifre! Lütfen kontrol edin.")

        # Test giriş bilgileri hatırlatıcısı
        with st.expander("🔑 Varsayılan Giriş Bilgileri (Demo)"):
            st.markdown("""
            * **Yönetici (Admin):**  
              Kullanıcı Adı: `admin` | Şifre: `admin123`
            * **Depo Sorumlusu (Personel):**  
              Kullanıcı Adı: `depo` | Şifre: `depo123`
            * **Kantin Sorumlusu (Personel):**  
              Kullanıcı Adı: `kantin` | Şifre: `kantin123`
            """)
