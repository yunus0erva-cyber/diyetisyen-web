# 🏫 Florya MEV Koleji - Depo ve Stok Takip Web Uygulaması

Python ve Streamlit kullanılarak sıfırdan geliştirilmiş; SQLite ve Supabase veritabanı desteğine sahip, güvenli oturum açma (login), Excel ile toplu stok yükleme/güncelleme, kritik stok uyarı paneli ve Excel dışa aktarma (export) özelliklerini barındıran profesyonel depo ve stok takip web uygulamasıdır.

---

## 🌟 Temel Özellikler

1. **🔐 Güvenli Kullanıcı Girişi & Rol Yönetimi**:
   - Sadece izin verilen kayıtlı kullanıcılar sisteme erişebilir.
   - Rol bazlı yetkilendirme:
     - **Yönetici (Admin)**: Ürün ekleme/düzenleme/silme, kullanıcı tanımlama ve silme, sistem yapılandırması.
     - **Personel**: Stok giriş/çıkış hareketleri yapma, kritik stokları ve listeleri görüntüleme, Excel rapor indirme.
   - Varsayılan Giriş Bilgileri:
     - **Yönetici:** `admin` / `admin123` *(Erva Yunus)*
     - **Depo Sorumlusu:** `depo` / `depo123` *(Ahmet Yılmaz)*
     - **Kantin Sorumlusu:** `kantin` / `kantin123` *(Merve Kaya)*

2. **🚨 Kritik Stok & FEFO Uyarı Paneli**:
   - `Mevcut Stok <= Kritik Eşik` olan tüm ürünler renk kodlu acil uyarı kartlarıyla listelenir.
   - Eksik miktar (`Kritik Eşik - Mevcut Stok`) otomatik hesaplanır.
   - **Tek tıkla Satınalma / Sipariş Listesi Excel Export**: Tedarikçiye iletilebilecek biçimlendirilmiş sipariş listesi anında indirilebilir.
   - **FEFO (First Expired First Out) & SKT Takibi**: Son kullanma tarihi 30 günden az kalan ürünleri listeler; 7 gün altındakilere "Çok Acil Tüketim" uyarısı verir.

3. **📋 Detaylı Stok Yönetimi**:
   - Ürün arama (Barkod, Ürün Kodu, Ürün Adı, Lot No).
   - Kategori ve Depo Lokasyonu bazlı filtreleme (*Kuru Depo, Soğuk Depo (+4°C), Donuk Depo (-18°C), Kantin Deposu, Mutfak Hazırlık*).
   - Tekli ürün kartı tanımlama, düzenleme ve silme.

4. **⚡ Hızlı Stok Hareketi (Giriş / Çıkış / Sayım / Fire)**:
   - Seçilen üründen anlık stok düşme veya ekleme.
   - İrsaliye/Fatura belge no ve açıklama kaydı.
   - Tüm işlemler için otomatik denetim izi (Audit Log) oluşturulur.

5. **📥 Excel ile Toplu Stok Yükleme / Güncelleme**:
   - Format hatalarını önleyen, açıklamalı **"Örnek Excel Şablonu"** tek tıkla indirilebilir.
   - İki modda yükleme:
     - *Varsa Stoğu Artır / Bilgileri Güncelle (Tavsiye Edilen)*
     - *Sadece Yeni Ürünleri Ekle (Var olanları atla)*
   - Yüklenen dosyanın canlı önizlemesi ve aktarım onay adımı.

6. **📤 Profesyonel Excel Dışa Aktarma (Export)**:
   - Tüm stok envanteri veya arama sonucu filtrelenmiş liste kurumsal Florya MEV başlıkları ve sütun formatlarıyla Excel (`.xlsx`) olarak indirilebilir.
   - Stok hareket geçmişi ve denetim logları Excel formatında dışa aktarılabilir.

7. **🗄️ Veritabanı Seçimi (SQLite / Supabase)**:
   - **SQLite (Varsayılan):** Kurulum gerektirmeden yerel `depo_stok.db` üzerinde hemen çalışır.
   - **Supabase Cloud (PostgreSQL):** `.env` dosyasına bilgiler girildiğinde ve `supabase_schema.sql` Supabase üzerinde çalıştırıldığında buluta bağlanabilir.

---

## 🚀 Kurulum ve Çalıştırma Adımları

### 1. Bağımlılıkların Kurulumu

Terminal (PowerShell veya Komut Satırı) açarak proje klasöründe şu komutu çalıştırın:

```powershell
pip install -r requirements.txt
```

*(Python ortamınız yüklü değilse `python` veya tam Python yolu ile `python -m pip install -r requirements.txt` çalıştırabilirsiniz.)*

### 2. Uygulamanın Başlatılması

Aşağıdaki komut ile Streamlit sunucusunu başlatın:

```powershell
streamlit run app.py
```

Komut çalıştıktan sonra tarayıcınız otomatik olarak açılacak veya `http://localhost:8501` adresine giderek uygulamaya erişebilirsiniz.

### 3. İlk Giriş

Giriş ekranında aşağıdaki bilgilerden biriyle oturum açabilirsiniz:

* **Kullanıcı Adı:** `admin`
* **Şifre:** `admin123`

---

## ☁️ Supabase Cloud Entegrasyonu (İsteğe Bağlı)

Yerel SQLite yerine Supabase Cloud kullanmak isterseniz:

1. [Supabase](https://supabase.com) üzerinde ücretsiz bir proje oluşturun.
2. Sol menüdeki **SQL Editor** sekmesine girin ve projedeki `supabase_schema.sql` dosyasının içeriğini yapıştırıp **Run** butonuna tıklayın.
3. Proje dizininde bulunan `.env.example` dosyasının adını `.env` olarak değiştirin ve değerleri doldurun:
   ```env
   DB_TYPE=supabase
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_KEY=your-anon-or-service-role-key
   ```
4. Uygulamayı yeniden başlatın (`streamlit run app.py`). Artık veriler Supabase bulutunda saklanacaktır.

---

## 📁 Proje Dosya Ağacı

```
Florya_MEV_Operasyon/
│
├── app.py                     # Ana Streamlit web arayüzü ve sayfa yönlendirmeleri
├── database.py                # SQLite ve Supabase veri tabanı bağlantı ve tohumlama katmanı
├── auth.py                    # Kimlik doğrulama, şifre hashleme ve oturum yönetimi
├── stock_manager.py           # Stok hareketleri, kritik eşik ve FEFO iş mantığı
├── excel_utils.py             # Excel şablon üretimi, toplu okuma ve stilize export
├── components.py              # Şık KPI kartları ve özel CSS teması
├── supabase_schema.sql        # Supabase Cloud için hazır SQL şeması
├── requirements.txt           # Gerekli Python kütüphaneleri
├── .env.example               # Çevre değişkenleri şablonu
└── README.md                  # Bu kılavuz
```
