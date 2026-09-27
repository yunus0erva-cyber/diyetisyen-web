"""
Florya MEV Koleji - Eylul & Ekim 2026 Aylik / Haftalik Yemekhane Menusu (menu_data.py)
Resmi 9 Haftalik (Eylul + Ekim) Yemek Menusu ve Kalori Cetveli (500 Kisilik Mutfak)
"""

import datetime
from typing import Dict, List, Any
import haccp_manager

MENU_WEEKS = {
    # --- EYLÜL 2026 DÖNEMİ ---
    "Eylül 1. Hafta (31 Ağustos - 4 Eylül 2026)": ["2026-08-31", "2026-09-01", "2026-09-02", "2026-09-03", "2026-09-04"],
    "Eylül 2. Hafta (7 - 11 Eylül 2026)": ["2026-09-07", "2026-09-08", "2026-09-09", "2026-09-10", "2026-09-11"],
    "Eylül 3. Hafta (14 - 18 Eylül 2026)": ["2026-09-14", "2026-09-15", "2026-09-16", "2026-09-17", "2026-09-18"],
    "Eylül 4. Hafta (21 - 25 Eylül 2026)": ["2026-09-21", "2026-09-22", "2026-09-23", "2026-09-24", "2026-09-25"],
    "Eylül 5. Hafta (28 Eylül - 2 Ekim 2026)": ["2026-09-28", "2026-09-29", "2026-09-30", "2026-10-01", "2026-10-02"],

    # --- EKİM 2026 DÖNEMİ ---
    "Ekim 1. Hafta (5 - 9 Ekim 2026)": ["2026-10-05", "2026-10-06", "2026-10-07", "2026-10-08", "2026-10-09"],
    "Ekim 2. Hafta (12 - 16 Ekim 2026)": ["2026-10-12", "2026-10-13", "2026-10-14", "2026-10-15", "2026-10-16"],
    "Ekim 3. Hafta (19 - 23 Ekim 2026)": ["2026-10-19", "2026-10-20", "2026-10-21", "2026-10-22", "2026-10-23"],
    "Ekim 4. Hafta (26 - 30 Ekim 2026)": ["2026-10-26", "2026-10-27", "2026-10-28", "2026-10-29", "2026-10-30"],
}

WEEKLY_MENU = {
    # =========================================================================
    # EYLÜL 1. HAFTA: 31 AGUSTOS - 4 EYLUL 2026
    # =========================================================================
    "2026-08-31": {
        "day_name": "PAZARTESİ",
        "date_str": "31 Ağustos 2026",
        "meals": {
            "KAHVALTI": [],
            "ÖĞLE YEMEĞİ": [
                {"name": "Yayla Çorba", "kcal": 130},
                {"name": "Nohut Yemeği", "kcal": 295},
                {"name": "Pirinç Pilavı", "kcal": 210},
                {"name": "Cevizli Şöbiyet", "kcal": 350}
            ],
            "SALATA BÜFESİ": [
                {"name": "Mevsim Yeşilliği", "kcal": 122},
                {"name": "Çoban Salata", "kcal": 114},
                {"name": "Pembe Sultan", "kcal": 63},
                {"name": "Cacık", "kcal": 113},
                {"name": "Kırmızı Lahana", "kcal": 54}
            ],
            "İKİNDİ": []
        }
    },
    "2026-09-01": {
        "day_name": "SALI",
        "date_str": "1 Eylül 2026",
        "meals": {
            "KAHVALTI": [],
            "ÖĞLE YEMEĞİ": [
                {"name": "Mercimek Çorba", "kcal": 120},
                {"name": "Fırın Köfte", "kcal": 210},
                {"name": "Soslu Makarna", "kcal": 210},
                {"name": "Ayran", "kcal": 63}
            ],
            "SALATA BÜFESİ": [
                {"name": "Mevsim Salata", "kcal": 122},
                {"name": "Karpuz", "kcal": 55},
                {"name": "Acılı Ezme", "kcal": 68},
                {"name": "Z.Y. Kabak", "kcal": 69},
                {"name": "Havuç Rende", "kcal": 68}
            ],
            "İKİNDİ": []
        }
    },
    "2026-09-02": {
        "day_name": "ÇARŞAMBA",
        "date_str": "2 Eylül 2026",
        "meals": {
            "KAHVALTI": [],
            "ÖĞLE YEMEĞİ": [
                {"name": "Ayran Aşı Çorba", "kcal": 100},
                {"name": "Sebzeli Kebap", "kcal": 200},
                {"name": "Pirinç Pilavı", "kcal": 210},
                {"name": "Meyve", "kcal": 55}
            ],
            "SALATA BÜFESİ": [
                {"name": "Mevsim Yeşilliği", "kcal": 122},
                {"name": "Roka Salatası", "kcal": 65},
                {"name": "Karışık Turşu", "kcal": 27},
                {"name": "Havuç Tarator", "kcal": 158},
                {"name": "Mısır Salata", "kcal": 110}
            ],
            "İKİNDİ": []
        }
    },
    "2026-09-03": {
        "day_name": "PERŞEMBE",
        "date_str": "3 Eylül 2026",
        "meals": {
            "KAHVALTI": [],
            "ÖĞLE YEMEĞİ": [
                {"name": "Sebze Çorba", "kcal": 140},
                {"name": "Biber Dolma", "kcal": 262},
                {"name": "Su Böreği", "kcal": 150},
                {"name": "Tulumba Tatlısı", "kcal": 250}
            ],
            "SALATA BÜFESİ": [
                {"name": "Mevsim Salata", "kcal": 122},
                {"name": "Yoğurt", "kcal": 63},
                {"name": "Z.Y. Enginar", "kcal": 147},
                {"name": "Havuç Rende", "kcal": 68},
                {"name": "Akdeniz Salata", "kcal": 90}
            ],
            "İKİNDİ": []
        }
    },
    "2026-09-04": {
        "day_name": "CUMA",
        "date_str": "4 Eylül 2026",
        "meals": {
            "KAHVALTI": [],
            "ÖĞLE YEMEĞİ": [
                {"name": "Domates Çorba", "kcal": 122},
                {"name": "Fırın Tavuk", "kcal": 250},
                {"name": "Bulgur Pilavı", "kcal": 120},
                {"name": "Meyve", "kcal": 55}
            ],
            "SALATA BÜFESİ": [
                {"name": "Mevsim Yeşilliği", "kcal": 122},
                {"name": "Çoban Salata", "kcal": 114},
                {"name": "Kırmızı Lahana", "kcal": 54},
                {"name": "Acılı Ezme", "kcal": 68},
                {"name": "Semizotu Salata", "kcal": 44}
            ],
            "İKİNDİ": []
        }
    },

    # =========================================================================
    # EYLÜL 2. HAFTA: 7 - 11 EYLUL 2026
    # =========================================================================
    "2026-09-07": {
        "day_name": "PAZARTESİ",
        "date_str": "7 Eylül 2026",
        "meals": {
            "KAHVALTI": [],
            "ÖĞLE YEMEĞİ": [
                {"name": "Mantar Çorba", "kcal": 100},
                {"name": "Sulu Köfte", "kcal": 270},
                {"name": "Bulgur Pilavı", "kcal": 120},
                {"name": "Meyve", "kcal": 55}
            ],
            "SALATA BÜFESİ": [
                {"name": "Mevsim Salata", "kcal": 122},
                {"name": "Yoğurt", "kcal": 63},
                {"name": "Çoban Salata", "kcal": 114},
                {"name": "Kırmızı Lahana", "kcal": 54},
                {"name": "Karışık Turşu", "kcal": 110}
            ],
            "İKİNDİ": []
        }
    },
    "2026-09-08": {
        "day_name": "SALI",
        "date_str": "8 Eylül 2026",
        "meals": {
            "KAHVALTI": [],
            "ÖĞLE YEMEĞİ": [
                {"name": "Sebze Çorba", "kcal": 140},
                {"name": "Izgara Tavuk", "kcal": 250},
                {"name": "Soslu Makarna", "kcal": 210},
                {"name": "Ayran", "kcal": 63}
            ],
            "SALATA BÜFESİ": [
                {"name": "Mevsim Yeşilliği", "kcal": 122},
                {"name": "Gavurdağı Salata", "kcal": 114},
                {"name": "Köz Patlıcan Salata", "kcal": 65},
                {"name": "Z.Y. Kabak", "kcal": 122},
                {"name": "Nohut Salata", "kcal": 95}
            ],
            "İKİNDİ": []
        }
    },
    "2026-09-09": {
        "day_name": "ÇARŞAMBA",
        "date_str": "9 Eylül 2026",
        "meals": {
            "KAHVALTI": [],
            "ÖĞLE YEMEĞİ": [
                {"name": "Ayran Aşı Çorba", "kcal": 100},
                {"name": "Kuru Fasulye", "kcal": 200},
                {"name": "Pirinç Pilavı", "kcal": 210},
                {"name": "Meyve", "kcal": 55}
            ],
            "SALATA BÜFESİ": [
                {"name": "Mevsim Salata", "kcal": 122},
                {"name": "Roka Salatası", "kcal": 65},
                {"name": "Karışık Turşu", "kcal": 27},
                {"name": "Kırmızı Lahana", "kcal": 54},
                {"name": "Semizotu Salatası", "kcal": 66}
            ],
            "İKİNDİ": []
        }
    },
    "2026-09-10": {
        "day_name": "PERŞEMBE",
        "date_str": "10 Eylül 2026",
        "meals": {
            "KAHVALTI": [],
            "ÖĞLE YEMEĞİ": [
                {"name": "Mercimek Çorba", "kcal": 120},
                {"name": "Karnıyarık", "kcal": 200},
                {"name": "Şehriyeli Pirinç Pilavı", "kcal": 210},
                {"name": "Cevizli Baklava", "kcal": 400}
            ],
            "SALATA BÜFESİ": [
                {"name": "Mevsim Yeşilliği", "kcal": 122},
                {"name": "Z.Y. Kereviz", "kcal": 200},
                {"name": "Cacık", "kcal": 113},
                {"name": "Közlenmiş Biber", "kcal": 34},
                {"name": "Çoban Salata", "kcal": 114}
            ],
            "İKİNDİ": []
        }
    },
    "2026-09-11": {
        "day_name": "CUMA",
        "date_str": "11 Eylül 2026",
        "meals": {
            "KAHVALTI": [],
            "ÖĞLE YEMEĞİ": [
                {"name": "Domates Çorba", "kcal": 122},
                {"name": "Bohça Kebabı", "kcal": 300},
                {"name": "Bulgur Pilavı", "kcal": 120},
                {"name": "Ayran", "kcal": 63}
            ],
            "SALATA BÜFESİ": [
                {"name": "Mevsim Salata", "kcal": 122},
                {"name": "Söğüş Salata", "kcal": 34},
                {"name": "Salatalık Turşusu", "kcal": 15},
                {"name": "Havuç Tarator", "kcal": 158},
                {"name": "Roka-Tere Salata", "kcal": 65}
            ],
            "İKİNDİ": []
        }
    },

    # =========================================================================
    # EYLÜL 3. HAFTA: 14 - 18 EYLUL 2026
    # =========================================================================
    "2026-09-14": {
        "day_name": "PAZARTESİ",
        "date_str": "14 Eylül 2026",
        "meals": {
            "KAHVALTI": [
                {"name": "Haşlanmış Yumurta", "kcal": 79},
                {"name": "Kaşar Peynir", "kcal": 56},
                {"name": "Karışık Zeytin", "kcal": 27},
                {"name": "Havuç Çubukları", "kcal": 34},
                {"name": "Meyve Çayı", "kcal": 14}
            ],
            "ÖĞLE YEMEĞİ": [
                {"name": "Ezogelin Çorba", "kcal": 100},
                {"name": "Hamburger", "kcal": 390},
                {"name": "Patates Tava", "kcal": 100},
                {"name": "Ayran", "kcal": 63}
            ],
            "SALATA BÜFESİ": [
                {"name": "Mevsim Yeşilliği", "kcal": 122},
                {"name": "Çoban Salata", "kcal": 114},
                {"name": "Salatalık Turşusu", "kcal": 15},
                {"name": "Söğüş Salata", "kcal": 34},
                {"name": "Kırmızı Lahana", "kcal": 54}
            ],
            "İKİNDİ": [
                {"name": "Kırmızı Elma", "kcal": 55},
                {"name": "Kuru Kayısı / Ceviz", "kcal": 70}
            ]
        }
    },
    "2026-09-15": {
        "day_name": "SALI",
        "date_str": "15 Eylül 2026",
        "meals": {
            "KAHVALTI": [
                {"name": "Menemen", "kcal": 127},
                {"name": "Beyaz Peynir", "kcal": 93},
                {"name": "Piknik Reçel", "kcal": 60},
                {"name": "Domates-Salatalık", "kcal": 34},
                {"name": "Süt", "kcal": 88}
            ],
            "ÖĞLE YEMEĞİ": [
                {"name": "Mantar Çorba", "kcal": 100},
                {"name": "Pideli Köfte", "kcal": 340},
                {"name": "Bulgur Pilavı", "kcal": 120},
                {"name": "Ayran", "kcal": 63}
            ],
            "SALATA BÜFESİ": [
                {"name": "Mevsim Yeşilliği", "kcal": 122},
                {"name": "Roka Salatası", "kcal": 65},
                {"name": "Acılı Ezme", "kcal": 68},
                {"name": "Havuç Tarator", "kcal": 158},
                {"name": "Közlenmiş Biber", "kcal": 34}
            ],
            "İKİNDİ": [
                {"name": "Mozaik Pasta", "kcal": 370},
                {"name": "Limonata", "kcal": 73}
            ]
        }
    },
    "2026-09-16": {
        "day_name": "ÇARŞAMBA",
        "date_str": "16 Eylül 2026",
        "meals": {
            "KAHVALTI": [
                {"name": "Pişi", "kcal": 122},
                {"name": "Fındık Kreması", "kcal": 63},
                {"name": "Havuç Çubukları", "kcal": 34},
                {"name": "Labne Peynir", "kcal": 39},
                {"name": "Karışık Meyve Çayı", "kcal": 14}
            ],
            "ÖĞLE YEMEĞİ": [
                {"name": "Yayla Çorba", "kcal": 130},
                {"name": "Taze Fasulye", "kcal": 295},
                {"name": "Makarna", "kcal": 210},
                {"name": "Tulumba Tatlısı", "kcal": 400}
            ],
            "SALATA BÜFESİ": [
                {"name": "Mevsim Salata", "kcal": 122},
                {"name": "Cacık", "kcal": 113},
                {"name": "Z.Y. Enginar", "kcal": 147},
                {"name": "Gavurdağı Salata", "kcal": 115},
                {"name": "Karışık Turşu", "kcal": 27}
            ],
            "İKİNDİ": [
                {"name": "Armut", "kcal": 55},
                {"name": "Patlamış Mısır", "kcal": 140}
            ]
        }
    },
    "2026-09-17": {
        "day_name": "PERŞEMBE",
        "date_str": "17 Eylül 2026",
        "meals": {
            "KAHVALTI": [
                {"name": "Kaşarlı Omlet", "kcal": 200},
                {"name": "Beyaz Peynir", "kcal": 93},
                {"name": "Domates-Salatalık", "kcal": 34},
                {"name": "Tahin Pekmez", "kcal": 55},
                {"name": "Süt", "kcal": 88}
            ],
            "ÖĞLE YEMEĞİ": [
                {"name": "Ayran Aşı Çorba", "kcal": 100},
                {"name": "Nohut Yemeği", "kcal": 295},
                {"name": "Pirinç Pilavı", "kcal": 210},
                {"name": "Supangle", "kcal": 180}
            ],
            "SALATA BÜFESİ": [
                {"name": "Mevsim Salata", "kcal": 122},
                {"name": "Karışık Turşu", "kcal": 27},
                {"name": "Kırmızı Lahana", "kcal": 54},
                {"name": "Z.Y. Kabak", "kcal": 69},
                {"name": "Cacık", "kcal": 113}
            ],
            "İKİNDİ": [
                {"name": "Elmalı Kurabiye", "kcal": 300},
                {"name": "Meyve Çayı", "kcal": 14}
            ]
        }
    },
    "2026-09-18": {
        "day_name": "CUMA",
        "date_str": "18 Eylül 2026",
        "meals": {
            "KAHVALTI": [
                {"name": "Haşlanmış Yumurta", "kcal": 79},
                {"name": "Kaşar Peynir", "kcal": 56},
                {"name": "Havuç Çubukları", "kcal": 34},
                {"name": "Karışık Zeytin", "kcal": 27},
                {"name": "Süt", "kcal": 88}
            ],
            "ÖĞLE YEMEĞİ": [
                {"name": "Tarhana Çorba", "kcal": 172},
                {"name": "Piliç Baget / Patates", "kcal": 250},
                {"name": "Soslu Makarna", "kcal": 210},
                {"name": "Meyve", "kcal": 55}
            ],
            "SALATA BÜFESİ": [
                {"name": "Mevsim Yeşilliği", "kcal": 122},
                {"name": "Roka Salatası", "kcal": 65},
                {"name": "Pembe Sultan", "kcal": 70},
                {"name": "Gavurdağı Salata", "kcal": 115},
                {"name": "Akdeniz Salata", "kcal": 90}
            ],
            "İKİNDİ": [
                {"name": "Mini Simit", "kcal": 75},
                {"name": "Ayran", "kcal": 63}
            ]
        }
    },

    # =========================================================================
    # EYLÜL 4. HAFTA: 21 - 25 EYLUL 2026
    # =========================================================================
    "2026-09-21": {
        "day_name": "PAZARTESİ",
        "date_str": "21 Eylül 2026",
        "meals": {
            "KAHVALTI": [
                {"name": "Haşlanmış Yumurta", "kcal": 79},
                {"name": "Beyaz Peynir", "kcal": 93},
                {"name": "Piknik Reçel", "kcal": 60},
                {"name": "Karışık Zeytin", "kcal": 27},
                {"name": "Meyve Çayı", "kcal": 14}
            ],
            "ÖĞLE YEMEĞİ": [
                {"name": "Yayla Çorba", "kcal": 130},
                {"name": "Tavuk Sote", "kcal": 300},
                {"name": "Erişte", "kcal": 200},
                {"name": "Ayran", "kcal": 63}
            ],
            "SALATA BÜFESİ": [
                {"name": "Mevsim Salata", "kcal": 122},
                {"name": "Çoban Salata", "kcal": 114},
                {"name": "Yoğurt", "kcal": 63},
                {"name": "Kırmızı Lahana", "kcal": 54},
                {"name": "Havuç Rende", "kcal": 68}
            ],
            "İKİNDİ": [
                {"name": "Armut", "kcal": 55},
                {"name": "Kuru Kayısı / Ceviz", "kcal": 70}
            ]
        }
    },
    "2026-09-22": {
        "day_name": "SALI",
        "date_str": "22 Eylül 2026",
        "meals": {
            "KAHVALTI": [
                {"name": "Peynirli Omlet", "kcal": 200},
                {"name": "Kaşar Peynir", "kcal": 56},
                {"name": "Domates-Salatalık", "kcal": 34},
                {"name": "Tahin Pekmez", "kcal": 55},
                {"name": "Süt", "kcal": 88}
            ],
            "ÖĞLE YEMEĞİ": [
                {"name": "Sebze Çorba", "kcal": 140},
                {"name": "Kuru Fasulye", "kcal": 200},
                {"name": "Pirinç Pilavı", "kcal": 210},
                {"name": "Meyve", "kcal": 55}
            ],
            "SALATA BÜFESİ": [
                {"name": "Mevsim Yeşilliği", "kcal": 122},
                {"name": "Z.Y. Kereviz", "kcal": 200},
                {"name": "Cacık", "kcal": 113},
                {"name": "Gavurdağı Salata", "kcal": 115},
                {"name": "Karışık Turşu", "kcal": 27}
            ],
            "İKİNDİ": [
                {"name": "Mini Pizza", "kcal": 120},
                {"name": "Limonata", "kcal": 73}
            ]
        }
    },
    "2026-09-23": {
        "day_name": "ÇARŞAMBA",
        "date_str": "23 Eylül 2026",
        "meals": {
            "KAHVALTI": [
                {"name": "Simit", "kcal": 143},
                {"name": "Labne Peynir", "kcal": 39},
                {"name": "Havuç Çubukları", "kcal": 34},
                {"name": "Fındık Kreması", "kcal": 63},
                {"name": "Ihlamur Çayı", "kcal": 14}
            ],
            "ÖĞLE YEMEĞİ": [
                {"name": "Mercimek Çorba", "kcal": 120},
                {"name": "Orman Kebabı", "kcal": 260},
                {"name": "Bulgur Pilavı", "kcal": 120},
                {"name": "Ayran", "kcal": 63}
            ],
            "SALATA BÜFESİ": [
                {"name": "Mevsim Salata", "kcal": 122},
                {"name": "Roka Salata", "kcal": 65},
                {"name": "Havuç Tarator", "kcal": 158},
                {"name": "Kırmızı Lahana", "kcal": 54},
                {"name": "Akdeniz Salata", "kcal": 90}
            ],
            "İKİNDİ": [
                {"name": "Yeşil Elma", "kcal": 55},
                {"name": "Patlamış Mısır", "kcal": 140}
            ]
        }
    },
    "2026-09-24": {
        "day_name": "PERŞEMBE",
        "date_str": "24 Eylül 2026",
        "meals": {
            "KAHVALTI": [
                {"name": "Menemen", "kcal": 127},
                {"name": "Kaşar Peynir", "kcal": 56},
                {"name": "Karışık Zeytin", "kcal": 27},
                {"name": "Domates-Salatalık", "kcal": 34},
                {"name": "Süt", "kcal": 88}
            ],
            "ÖĞLE YEMEĞİ": [
                {"name": "Şehriye Çorba", "kcal": 250},
                {"name": "Bezelye Yemeği", "kcal": 220},
                {"name": "Pirinç Pilavı", "kcal": 210},
                {"name": "Kalburabastı", "kcal": 300}
            ],
            "SALATA BÜFESİ": [
                {"name": "Mevsim Yeşilliği", "kcal": 122},
                {"name": "Z.Y. Kabak", "kcal": 69},
                {"name": "Çoban Salata", "kcal": 114},
                {"name": "Cacık", "kcal": 113},
                {"name": "Karışık Turşu", "kcal": 27}
            ],
            "İKİNDİ": [
                {"name": "Tuzlu Kurabiye", "kcal": 250},
                {"name": "Portakal Suyu", "kcal": 75}
            ]
        }
    },
    "2026-09-25": {
        "day_name": "CUMA",
        "date_str": "25 Eylül 2026",
        "meals": {
            "KAHVALTI": [
                {"name": "Haşlanmış Yumurta", "kcal": 79},
                {"name": "Havuç Çubukları", "kcal": 34},
                {"name": "Piknik Tereyağ", "kcal": 70},
                {"name": "Piknik Bal", "kcal": 37},
                {"name": "Kırmızı Meyve Çayı", "kcal": 14}
            ],
            "ÖĞLE YEMEĞİ": [
                {"name": "Domates Çorba", "kcal": 122},
                {"name": "Pizza", "kcal": 250},
                {"name": "Patates", "kcal": 100},
                {"name": "Ayran", "kcal": 63}
            ],
            "SALATA BÜFESİ": [
                {"name": "Mevsim Yeşilliği", "kcal": 122},
                {"name": "Roka Salata", "kcal": 65},
                {"name": "Salatalık Turşusu", "kcal": 15},
                {"name": "Acılı Ezme", "kcal": 68},
                {"name": "Gavurdağı Salata", "kcal": 115}
            ],
            "İKİNDİ": [
                {"name": "Ekler", "kcal": 150},
                {"name": "Süt", "kcal": 88}
            ]
        }
    },

    # =========================================================================
    # EYLÜL 5. HAFTA: 28 EYLUL - 2 EKIM 2026
    # =========================================================================
    "2026-09-28": {
        "day_name": "PAZARTESİ",
        "date_str": "28 Eylül 2026",
        "meals": {
            "KAHVALTI": [
                {"name": "Haşlanmış Yumurta", "kcal": 79},
                {"name": "Domates-Salatalık", "kcal": 34},
                {"name": "Beyaz Peynir", "kcal": 93},
                {"name": "Piknik Reçel", "kcal": 60},
                {"name": "Meyve Çayı", "kcal": 14}
            ],
            "ÖĞLE YEMEĞİ": [
                {"name": "Mercimek Çorba", "kcal": 120},
                {"name": "Sebzeli Çıtır Tavuk", "kcal": 300},
                {"name": "Pirinç Pilavı", "kcal": 210},
                {"name": "Meyve", "kcal": 55}
            ],
            "SALATA BÜFESİ": [
                {"name": "Mevsim Salata", "kcal": 122},
                {"name": "Çoban Salata", "kcal": 114},
                {"name": "Havuç Rende", "kcal": 68},
                {"name": "Pembe Sultan", "kcal": 70},
                {"name": "Roka Salata", "kcal": 65}
            ],
            "İKİNDİ": [
                {"name": "Mini Simit", "kcal": 75},
                {"name": "Ayran", "kcal": 63}
            ]
        }
    },
    "2026-09-29": {
        "day_name": "SALI",
        "date_str": "29 Eylül 2026",
        "meals": {
            "KAHVALTI": [
                {"name": "Menemen", "kcal": 127},
                {"name": "Havuç Çubukları", "kcal": 34},
                {"name": "Kaşar Peynir", "kcal": 56},
                {"name": "Karışık Zeytin", "kcal": 27},
                {"name": "Süt", "kcal": 88}
            ],
            "ÖĞLE YEMEĞİ": [
                {"name": "Ezogelin Çorba", "kcal": 100},
                {"name": "Biber Dolma", "kcal": 262},
                {"name": "Su Böreği", "kcal": 150},
                {"name": "Tulumba Tatlısı", "kcal": 400}
            ],
            "SALATA BÜFESİ": [
                {"name": "Mevsim Salata", "kcal": 122},
                {"name": "Gavurdağı Salata", "kcal": 115},
                {"name": "Yoğurt", "kcal": 70},
                {"name": "Z.Y. Brokoli", "kcal": 78},
                {"name": "Havuç Tarator", "kcal": 158}
            ],
            "İKİNDİ": [
                {"name": "Armut", "kcal": 55},
                {"name": "Patlamış Mısır", "kcal": 140}
            ]
        }
    },
    "2026-09-30": {
        "day_name": "ÇARŞAMBA",
        "date_str": "30 Eylül 2026",
        "meals": {
            "KAHVALTI": [
                {"name": "Poğaça", "kcal": 210},
                {"name": "Labne Peynir", "kcal": 39},
                {"name": "Fındık Kreması", "kcal": 63},
                {"name": "Domates-Salatalık", "kcal": 34},
                {"name": "Karışık Meyve Çayı", "kcal": 14}
            ],
            "ÖĞLE YEMEĞİ": [
                {"name": "Domates Çorba", "kcal": 122},
                {"name": "Etli Nohut Yemeği", "kcal": 320},
                {"name": "Pirinç Pilavı", "kcal": 210},
                {"name": "Meyve", "kcal": 55}
            ],
            "SALATA BÜFESİ": [
                {"name": "Mevsim Yeşilliği", "kcal": 122},
                {"name": "Karışık Turşu", "kcal": 27},
                {"name": "Kısır", "kcal": 178},
                {"name": "Cacık", "kcal": 113},
                {"name": "Roka Salata", "kcal": 68}
            ],
            "İKİNDİ": [
                {"name": "Mozaik Pasta", "kcal": 370},
                {"name": "Limonata", "kcal": 73}
            ]
        }
    },
    "2026-10-01": {
        "day_name": "PERŞEMBE",
        "date_str": "1 Ekim 2026",
        "meals": {
            "KAHVALTI": [
                {"name": "Kaşarlı Omlet", "kcal": 200},
                {"name": "Beyaz Peynir", "kcal": 93},
                {"name": "Tahin Pekmez", "kcal": 55},
                {"name": "Karışık Zeytin", "kcal": 27},
                {"name": "Süt", "kcal": 88}
            ],
            "ÖĞLE YEMEĞİ": [
                {"name": "Kremalı Tavuk Suyu Çorba", "kcal": 150},
                {"name": "Ispanak Yemeği", "kcal": 262},
                {"name": "Fırın Makarna", "kcal": 300},
                {"name": "Şekerpare", "kcal": 210}
            ],
            "SALATA BÜFESİ": [
                {"name": "Mevsim Yeşilliği", "kcal": 122},
                {"name": "Z.Y. Kereviz", "kcal": 200},
                {"name": "Gavurdağı Salata", "kcal": 115},
                {"name": "Roka Salata", "kcal": 65},
                {"name": "Yoğurt", "kcal": 63}
            ],
            "İKİNDİ": [
                {"name": "Kırmızı Elma", "kcal": 55},
                {"name": "Kuru Kayısı / Ceviz", "kcal": 70}
            ]
        }
    },
    "2026-10-02": {
        "day_name": "CUMA",
        "date_str": "2 Ekim 2026",
        "meals": {
            "KAHVALTI": [
                {"name": "Haşlanmış Yumurta", "kcal": 79},
                {"name": "Havuç Çubukları", "kcal": 34},
                {"name": "Kaşar Peynir", "kcal": 56},
                {"name": "Piknik Bal", "kcal": 37},
                {"name": "Ihlamur Çayı", "kcal": 15}
            ],
            "ÖĞLE YEMEĞİ": [
                {"name": "Tarhana Çorba", "kcal": 172},
                {"name": "İzmir Köfte / Patates", "kcal": 250},
                {"name": "Bulgur Pilavı", "kcal": 120},
                {"name": "Ayran", "kcal": 63}
            ],
            "SALATA BÜFESİ": [
                {"name": "Mevsim Salata", "kcal": 122},
                {"name": "Roka Salata", "kcal": 65},
                {"name": "Salatalık Turşusu", "kcal": 15},
                {"name": "Kırmızı Lahana", "kcal": 54},
                {"name": "Acılı Ezme", "kcal": 68}
            ],
            "İKİNDİ": [
                {"name": "Elmalı Kurabiye", "kcal": 300},
                {"name": "Süt", "kcal": 88}
            ]
        }
    },

    # =========================================================================
    # EKİM 1. HAFTA: 5 - 9 EKİM 2026 (Revize - Uyumlu & Çeşitlendirilmiş)
    # =========================================================================
    "2026-10-05": {
        "day_name": "PAZARTESİ",
        "date_str": "5 Ekim 2026",
        "meals": {
            "KAHVALTI": [
                {"name": "Haşlanmış Yumurta", "kcal": 79},
                {"name": "Beyaz Peynir", "kcal": 93},
                {"name": "Siyah-Yeşil Zeytin", "kcal": 27},
                {"name": "Salatalık Söğüş", "kcal": 20},
                {"name": "Adaçayı", "kcal": 14}
            ],
            "ÖĞLE YEMEĞİ": [
                {"name": "Süzme Mercimek Çorba", "kcal": 120},
                {"name": "Fırında İzmir Köfte", "kcal": 280},
                {"name": "Şehriyeli Bulgur Pilavı", "kcal": 130},
                {"name": "Ayran", "kcal": 63}
            ],
            "SALATA BÜFESİ": [
                {"name": "Mevsim Yeşilliği", "kcal": 122},
                {"name": "Gavurdağı Salata", "kcal": 115},
                {"name": "Közlenmiş Kırmızı Biber", "kcal": 34},
                {"name": "Mor Lahana Salatası", "kcal": 54},
                {"name": "Zeytinyağlı Havuç-Turp Rendesi", "kcal": 68}
            ],
            "İKİNDİ": [
                {"name": "Kırmızı Elma", "kcal": 55},
                {"name": "Ceviz İçi & Kuru Üzüm", "kcal": 75}
            ]
        }
    },
    "2026-10-06": {
        "day_name": "SALI",
        "date_str": "6 Ekim 2026",
        "meals": {
            "KAHVALTI": [
                {"name": "Kaşarlı Omlet", "kcal": 200},
                {"name": "Domates-Salatalık", "kcal": 34},
                {"name": "Çilek Reçeli", "kcal": 60},
                {"name": "Kaşar Peynir", "kcal": 56},
                {"name": "Süt", "kcal": 88}
            ],
            "ÖĞLE YEMEĞİ": [
                {"name": "Şehriyeli Tavuk Çorba", "kcal": 135},
                {"name": "Kıymalı Taze Fasulye", "kcal": 190},
                {"name": "Tereyağlı Pirinç Pilavı", "kcal": 210},
                {"name": "Mevsim Meyvesi (Mandalina)", "kcal": 50}
            ],
            "SALATA BÜFESİ": [
                {"name": "Mevsim Salata", "kcal": 122},
                {"name": "Naneli Cacık", "kcal": 113},
                {"name": "Z.Y. Taze Barbunya", "kcal": 160},
                {"name": "Çoban Salata", "kcal": 114},
                {"name": "Karışık Turşu", "kcal": 27}
            ],
            "İKİNDİ": [
                {"name": "Havuçlu Cevizli Anne Keki", "kcal": 220},
                {"name": "Ihlamur Çayı", "kcal": 14}
            ]
        }
    },
    "2026-10-07": {
        "day_name": "ÇARŞAMBA",
        "date_str": "7 Ekim 2026",
        "meals": {
            "KAHVALTI": [
                {"name": "Çıtır Simit", "kcal": 143},
                {"name": "Labne Peynir", "kcal": 39},
                {"name": "Domates-Salatalık", "kcal": 34},
                {"name": "Tahin Pekmez", "kcal": 55},
                {"name": "Kuşburnu Çayı", "kcal": 14}
            ],
            "ÖĞLE YEMEĞİ": [
                {"name": "Kremalı Domates Çorba", "kcal": 125},
                {"name": "Fırın Tavuk But & Garnitür", "kcal": 260},
                {"name": "Domates Soslu Fiyonk Makarna", "kcal": 210},
                {"name": "Ayran", "kcal": 63}
            ],
            "SALATA BÜFESİ": [
                {"name": "Mevsim Yeşilliği", "kcal": 122},
                {"name": "Roka-Kiraz Domates Salata", "kcal": 65},
                {"name": "Zeytinyağlı Köz Patlıcan", "kcal": 65},
                {"name": "Renkli Lahana Salatası", "kcal": 54},
                {"name": "Tatlı Mısır Salatası", "kcal": 110}
            ],
            "İKİNDİ": [
                {"name": "Armut", "kcal": 55},
                {"name": "Patlamış Mısır", "kcal": 140}
            ]
        }
    },
    "2026-10-08": {
        "day_name": "PERŞEMBE",
        "date_str": "8 Ekim 2026",
        "meals": {
            "KAHVALTI": [
                {"name": "Menemen", "kcal": 127},
                {"name": "Beyaz Peynir", "kcal": 93},
                {"name": "Zeytin", "kcal": 27},
                {"name": "Havuç Çubukları", "kcal": 34},
                {"name": "Süt", "kcal": 88}
            ],
            "ÖĞLE YEMEĞİ": [
                {"name": "Ezogelin Çorba", "kcal": 100},
                {"name": "Geleneksel Kuru Fasulye", "kcal": 210},
                {"name": "Arpa Şehriyeli Pirinç Pilavı", "kcal": 210},
                {"name": "Fırın Sütlaç", "kcal": 220}
            ],
            "SALATA BÜFESİ": [
                {"name": "Mevsim Salata", "kcal": 122},
                {"name": "Karışık Lahana & Salatalık Turşusu", "kcal": 27},
                {"name": "Çoban Salata", "kcal": 114},
                {"name": "Süzme Yoğurt / Kuru Cacık", "kcal": 85},
                {"name": "Sumaklı Maydanozlu Soğan Söğüş", "kcal": 45}
            ],
            "İKİNDİ": [
                {"name": "Peynirli Mini Poğaça", "kcal": 150},
                {"name": "Ayran", "kcal": 63}
            ]
        }
    },
    "2026-10-09": {
        "day_name": "CUMA",
        "date_str": "9 Ekim 2026",
        "meals": {
            "KAHVALTI": [
                {"name": "Haşlanmış Yumurta", "kcal": 79},
                {"name": "Kaşar Peynir", "kcal": 56},
                {"name": "Piknik Bal & Tereyağ", "kcal": 105},
                {"name": "Salatalık Dilimleri", "kcal": 20},
                {"name": "Kırmızı Meyve Çayı", "kcal": 14}
            ],
            "ÖĞLE YEMEĞİ": [
                {"name": "Tarhana Çorba", "kcal": 172},
                {"name": "Çıtır Piliç Şnitzel", "kcal": 280},
                {"name": "Fırın Elma Dilim Patates", "kcal": 140},
                {"name": "Ayran", "kcal": 63}
            ],
            "SALATA BÜFESİ": [
                {"name": "Akdeniz Yeşillikleri Salatası", "kcal": 90},
                {"name": "Tatlı Mısır & Kırmızı Biber Salatası", "kcal": 110},
                {"name": "Çıtır Havuç & Kırmızı Turp", "kcal": 68},
                {"name": "Közlenmiş Biber Salatası", "kcal": 34},
                {"name": "Zeytinyağlı Acılı Ezme", "kcal": 68}
            ],
            "İKİNDİ": [
                {"name": "Mozaik Pasta", "kcal": 370},
                {"name": "Limonata", "kcal": 73}
            ]
        }
    },

    # =========================================================================
    # EKİM 2. HAFTA: 12 - 16 EKİM 2026 (Revize - Uyumlu & Çeşitlendirilmiş)
    # =========================================================================
    "2026-10-12": {
        "day_name": "PAZARTESİ",
        "date_str": "12 Ekim 2026",
        "meals": {
            "KAHVALTI": [
                {"name": "Haşlanmış Yumurta", "kcal": 79},
                {"name": "Beyaz Peynir", "kcal": 93},
                {"name": "Karışık Zeytin", "kcal": 27},
                {"name": "Havuç Çubukları", "kcal": 34},
                {"name": "Meyve Çayı", "kcal": 14}
            ],
            "ÖĞLE YEMEĞİ": [
                {"name": "Yayla Çorba", "kcal": 130},
                {"name": "Hasanpaşa Köfte (Patates Püreli)", "kcal": 290},
                {"name": "Sebzeli Bulgur Pilavı", "kcal": 125},
                {"name": "Mevsim Meyvesi (Amasya Elması)", "kcal": 55}
            ],
            "SALATA BÜFESİ": [
                {"name": "Roka & Kıvırcık Marul Salatası", "kcal": 65},
                {"name": "Nar Ekşili Çoban Salata", "kcal": 114},
                {"name": "Zeytinyağlı Enginar Kalbi", "kcal": 140},
                {"name": "Közlenmiş Kırmızı Biber", "kcal": 34},
                {"name": "Zeytinyağlı Kırmızı Pancar Rendesi", "kcal": 65}
            ],
            "İKİNDİ": [
                {"name": "Kuru İncir & Fındık İçi", "kcal": 85},
                {"name": "Bitki Çayı", "kcal": 14}
            ]
        }
    },
    "2026-10-13": {
        "day_name": "SALI",
        "date_str": "13 Ekim 2026",
        "meals": {
            "KAHVALTI": [
                {"name": "Peynirli Omlet", "kcal": 200},
                {"name": "Kaşar Peynir", "kcal": 56},
                {"name": "Domates-Salatalık", "kcal": 34},
                {"name": "Vişne Reçeli", "kcal": 60},
                {"name": "Süt", "kcal": 88}
            ],
            "ÖĞLE YEMEĞİ": [
                {"name": "Kırmızı Mercimek Çorba", "kcal": 120},
                {"name": "Mantarlı Tavuk Sote", "kcal": 260},
                {"name": "Burgu Makarna (Napoliten Sos)", "kcal": 210},
                {"name": "Ayran", "kcal": 63}
            ],
            "SALATA BÜFESİ": [
                {"name": "Mevsim Yeşilliği", "kcal": 122},
                {"name": "Zeytinyağlı Köz Patlıcan", "kcal": 65},
                {"name": "Z.Y. Havuçlu Pırasa", "kcal": 130},
                {"name": "Gavurdağı Salata", "kcal": 115},
                {"name": "Karışık Turşu", "kcal": 27}
            ],
            "İKİNDİ": [
                {"name": "Kandil Simidi / Tuzlu Kurabiye", "kcal": 240},
                {"name": "Ayran", "kcal": 63}
            ]
        }
    },
    "2026-10-14": {
        "day_name": "ÇARŞAMBA",
        "date_str": "14 Ekim 2026",
        "meals": {
            "KAHVALTI": [
                {"name": "Fırından Sıcak Poğaça", "kcal": 210},
                {"name": "Labne Peynir", "kcal": 39},
                {"name": "Domates Dilimleri", "kcal": 20},
                {"name": "Fındık Kreması", "kcal": 63},
                {"name": "Ihlamur Çayı", "kcal": 14}
            ],
            "ÖĞLE YEMEĞİ": [
                {"name": "Tel Şehriye Çorbası", "kcal": 120},
                {"name": "Kıymalı Biber & Kabak Dolma", "kcal": 250},
                {"name": "Fırın Su Böreği", "kcal": 150},
                {"name": "Mevsim Meyvesi (Mandalina)", "kcal": 55}
            ],
            "SALATA BÜFESİ": [
                {"name": "Mevsim Salata", "kcal": 122},
                {"name": "Naneli Süzme Yoğurt / Cacık", "kcal": 113},
                {"name": "Ekşili Kısır", "kcal": 178},
                {"name": "Kırmızı Lahana", "kcal": 54},
                {"name": "Zeytinyağlı Havuç Rende", "kcal": 68}
            ],
            "İKİNDİ": [
                {"name": "Muz", "kcal": 70},
                {"name": "Süt", "kcal": 88}
            ]
        }
    },
    "2026-10-15": {
        "day_name": "PERŞEMBE",
        "date_str": "15 Ekim 2026",
        "meals": {
            "KAHVALTI": [
                {"name": "Menemen", "kcal": 127},
                {"name": "Kaşar Peynir", "kcal": 56},
                {"name": "Karışık Zeytin", "kcal": 27},
                {"name": "Salatalık", "kcal": 20},
                {"name": "Süt", "kcal": 88}
            ],
            "ÖĞLE YEMEĞİ": [
                {"name": "Tutmaç Çorbası", "kcal": 140},
                {"name": "Etli Nohut Yemeği", "kcal": 310},
                {"name": "Arpa Şehriyeli Pirinç Pilavı", "kcal": 210},
                {"name": "İrmik Helvası", "kcal": 240}
            ],
            "SALATA BÜFESİ": [
                {"name": "Mevsim Yeşilliği", "kcal": 122},
                {"name": "Z.Y. Portakallı Kereviz", "kcal": 180},
                {"name": "Çoban Salata", "kcal": 114},
                {"name": "Naneli Cacık", "kcal": 113},
                {"name": "Salatalık & Biber Turşusu", "kcal": 27}
            ],
            "İKİNDİ": [
                {"name": "Mini Simit", "kcal": 75},
                {"name": "Üçgen Peynir", "kcal": 45}
            ]
        }
    },
    "2026-10-16": {
        "day_name": "CUMA",
        "date_str": "16 Ekim 2026",
        "meals": {
            "KAHVALTI": [
                {"name": "Haşlanmış Yumurta", "kcal": 79},
                {"name": "Beyaz Peynir", "kcal": 93},
                {"name": "Tahin Pekmez", "kcal": 55},
                {"name": "Havuç Çubukları", "kcal": 34},
                {"name": "Kuşburnu Çayı", "kcal": 14}
            ],
            "ÖĞLE YEMEĞİ": [
                {"name": "Domates Çorba (Kaşar Rendeli)", "kcal": 130},
                {"name": "Fırından Karışık Dilim Pizza", "kcal": 320},
                {"name": "Fırın Baharatlı Patates", "kcal": 110},
                {"name": "Ayran", "kcal": 63}
            ],
            "SALATA BÜFESİ": [
                {"name": "Roka & Akdeniz Salata", "kcal": 85},
                {"name": "Çıtır Havuç & Mor Lahana", "kcal": 65},
                {"name": "Kornişon Turşu", "kcal": 15},
                {"name": "Zeytinyağlı Acılı Ezme", "kcal": 68},
                {"name": "Tatlı Mısır Salatası", "kcal": 110}
            ],
            "İKİNDİ": [
                {"name": "Islak Kek (Brownie)", "kcal": 260},
                {"name": "Süt", "kcal": 88}
            ]
        }
    },

    # =========================================================================
    # EKİM 3. HAFTA: 19 - 23 EKİM 2026 (Revize - Uyumlu & Çeşitlendirilmiş)
    # =========================================================================
    "2026-10-19": {
        "day_name": "PAZARTESİ",
        "date_str": "19 Ekim 2026",
        "meals": {
            "KAHVALTI": [
                {"name": "Haşlanmış Yumurta", "kcal": 79},
                {"name": "Kaşar Peynir", "kcal": 56},
                {"name": "Karışık Zeytin", "kcal": 27},
                {"name": "Domates-Salatalık", "kcal": 34},
                {"name": "Meyve Çayı", "kcal": 14}
            ],
            "ÖĞLE YEMEĞİ": [
                {"name": "Ezogelin Çorba", "kcal": 100},
                {"name": "Fırında Kadınbudu Köfte", "kcal": 290},
                {"name": "Fırın Makarna (Kaşar Gratenli)", "kcal": 280},
                {"name": "Ayran", "kcal": 63}
            ],
            "SALATA BÜFESİ": [
                {"name": "Göbek & İnce Havuç Salatası", "kcal": 105},
                {"name": "Çoban Salata", "kcal": 114},
                {"name": "Zeytinyağlı Taze Fasulye", "kcal": 110},
                {"name": "Közlenmiş Kırmızı Biber", "kcal": 34},
                {"name": "Sumaklı Maydanozlu Soğan Piyazı", "kcal": 48}
            ],
            "İKİNDİ": [
                {"name": "Kırmızı Elma", "kcal": 55},
                {"name": "Kuru Kayısı & Fındık", "kcal": 75}
            ]
        }
    },
    "2026-10-20": {
        "day_name": "SALI",
        "date_str": "20 Ekim 2026",
        "meals": {
            "KAHVALTI": [
                {"name": "Menemen", "kcal": 127},
                {"name": "Beyaz Peynir", "kcal": 93},
                {"name": "Piknik Reçel", "kcal": 60},
                {"name": "Havuç Çubukları", "kcal": 34},
                {"name": "Süt", "kcal": 88}
            ],
            "ÖĞLE YEMEĞİ": [
                {"name": "Kremalı Mantar Çorba", "kcal": 110},
                {"name": "Fırında Sebzeli Tavuk But", "kcal": 270},
                {"name": "Şehriyeli Bulgur Pilavı", "kcal": 130},
                {"name": "Mevsim Meyvesi (Mandalina)", "kcal": 50}
            ],
            "SALATA BÜFESİ": [
                {"name": "Mevsim Salata", "kcal": 122},
                {"name": "Salatalıklı Cacık", "kcal": 113},
                {"name": "Z.Y. Barbunya Pilaki", "kcal": 150},
                {"name": "Gavurdağı Salata", "kcal": 115},
                {"name": "Karışık Turşu", "kcal": 27}
            ],
            "İKİNDİ": [
                {"name": "Elmalı Tarçınlı Kurabiye", "kcal": 250},
                {"name": "Bitki Çayı", "kcal": 14}
            ]
        }
    },
    "2026-10-21": {
        "day_name": "ÇARŞAMBA",
        "date_str": "21 Ekim 2026",
        "meals": {
            "KAHVALTI": [
                {"name": "Çıtır Pişi", "kcal": 135},
                {"name": "Labne Peynir", "kcal": 39},
                {"name": "Domates-Salatalık", "kcal": 34},
                {"name": "Fındık Kreması", "kcal": 63},
                {"name": "Ihlamur Çayı", "kcal": 14}
            ],
            "ÖĞLE YEMEĞİ": [
                {"name": "Süzme Mercimek Çorba", "kcal": 120},
                {"name": "Geleneksel Tas Kebabı (Patatesli)", "kcal": 280},
                {"name": "Tel Şehriyeli Pirinç Pilavı", "kcal": 210},
                {"name": "Ayran", "kcal": 63}
            ],
            "SALATA BÜFESİ": [
                {"name": "Mevsim Yeşilliği", "kcal": 122},
                {"name": "Roka-Ceviz Salata", "kcal": 75},
                {"name": "Zeytinyağlı Köz Patlıcan", "kcal": 65},
                {"name": "Limonlu Havuç Rende", "kcal": 68},
                {"name": "Çoban Salata", "kcal": 114}
            ],
            "İKİNDİ": [
                {"name": "Armut", "kcal": 55},
                {"name": "Patlamış Mısır", "kcal": 140}
            ]
        }
    },
    "2026-10-22": {
        "day_name": "PERŞEMBE",
        "date_str": "22 Ekim 2026",
        "meals": {
            "KAHVALTI": [
                {"name": "Kaşarlı Omlet", "kcal": 200},
                {"name": "Kaşar Peynir", "kcal": 56},
                {"name": "Tahin Pekmez", "kcal": 55},
                {"name": "Salatalık", "kcal": 20},
                {"name": "Süt", "kcal": 88}
            ],
            "ÖĞLE YEMEĞİ": [
                {"name": "Kremalı Sebze Çorba", "kcal": 130},
                {"name": "Kıymalı Karnabahar Graten", "kcal": 220},
                {"name": "Cevizli Erişte", "kcal": 210},
                {"name": "Şekerpare", "kcal": 240}
            ],
            "SALATA BÜFESİ": [
                {"name": "Akdeniz Salata", "kcal": 90},
                {"name": "Sarımsaklı Süzme Yoğurt / Haydari", "kcal": 75},
                {"name": "Domates-Salatalık Söğüş", "kcal": 34},
                {"name": "Kırmızı Lahana Salatası", "kcal": 54},
                {"name": "Çıtır Turşu Tabağı", "kcal": 27}
            ],
            "İKİNDİ": [
                {"name": "Mini Pizza", "kcal": 120},
                {"name": "Limonata", "kcal": 73}
            ]
        }
    },
    "2026-10-23": {
        "day_name": "CUMA",
        "date_str": "23 Ekim 2026",
        "meals": {
            "KAHVALTI": [
                {"name": "Haşlanmış Yumurta", "kcal": 79},
                {"name": "Beyaz Peynir", "kcal": 93},
                {"name": "Bal & Tereyağ", "kcal": 105},
                {"name": "Zeytin", "kcal": 27},
                {"name": "Süt", "kcal": 88}
            ],
            "ÖĞLE YEMEĞİ": [
                {"name": "Tarhana Çorba", "kcal": 172},
                {"name": "Okul Tipi Ev Köfteli Hamburger", "kcal": 340},
                {"name": "Fırında Baharatlı Patates Tava", "kcal": 120},
                {"name": "Ayran", "kcal": 63}
            ],
            "SALATA BÜFESİ": [
                {"name": "Mevsim Salata", "kcal": 122},
                {"name": "Çıtır Göbek Marul & Mısır Salata", "kcal": 110},
                {"name": "Salatalık Turşusu", "kcal": 15},
                {"name": "Közlenmiş Biber Salatası", "kcal": 34},
                {"name": "Zeytinyağlı Acılı Ezme", "kcal": 68}
            ],
            "İKİNDİ": [
                {"name": "Mini Ekler", "kcal": 150},
                {"name": "Süt", "kcal": 88}
            ]
        }
    },

    # =========================================================================
    # EKİM 4. HAFTA: 26 - 30 EKİM 2026 (CUMHURİYET BAYRAMI HAFTASI)
    # =========================================================================
    "2026-10-26": {
        "day_name": "PAZARTESİ",
        "date_str": "26 Ekim 2026",
        "meals": {
            "KAHVALTI": [
                {"name": "Haşlanmış Yumurta", "kcal": 79},
                {"name": "Beyaz Peynir", "kcal": 93},
                {"name": "Karışık Zeytin", "kcal": 27},
                {"name": "Havuç Çubukları", "kcal": 34},
                {"name": "Meyve Çayı", "kcal": 14}
            ],
            "ÖĞLE YEMEĞİ": [
                {"name": "Yayla Çorbası", "kcal": 130},
                {"name": "Çiftlik Kebabı (Etli, Havuçlu, Bezelyeli)", "kcal": 270},
                {"name": "Şehriyeli Bulgur Pilavı", "kcal": 130},
                {"name": "Mevsim Meyvesi (Mandalina)", "kcal": 50}
            ],
            "SALATA BÜFESİ": [
                {"name": "Akdeniz Yeşillikleri & Havuç Salata", "kcal": 95},
                {"name": "Gavurdağı Salata", "kcal": 115},
                {"name": "Z.Y. Portakallı Kereviz Mezesi", "kcal": 160},
                {"name": "Kırmızı Turp & Mor Lahana", "kcal": 54},
                {"name": "Zeytinyağlı Köz Kırmızı Biber", "kcal": 34}
            ],
            "İKİNDİ": [
                {"name": "Kırmızı Elma", "kcal": 55},
                {"name": "Ceviz & Kuru Üzüm", "kcal": 75}
            ]
        }
    },
    "2026-10-27": {
        "day_name": "SALI",
        "date_str": "27 Ekim 2026",
        "meals": {
            "KAHVALTI": [
                {"name": "Menemen", "kcal": 127},
                {"name": "Kaşar Peynir", "kcal": 56},
                {"name": "Piknik Reçel", "kcal": 60},
                {"name": "Domates-Salatalık", "kcal": 34},
                {"name": "Süt", "kcal": 88}
            ],
            "ÖĞLE YEMEĞİ": [
                {"name": "Tel Şehriye Çorbası", "kcal": 120},
                {"name": "Fırında Soslu Piliç Baget", "kcal": 260},
                {"name": "Kremalı Sebzeli Makarna", "kcal": 210},
                {"name": "Ayran", "kcal": 63}
            ],
            "SALATA BÜFESİ": [
                {"name": "Mevsim Yeşilliği", "kcal": 122},
                {"name": "Zeytinyağlı Köz Patlıcan", "kcal": 65},
                {"name": "Z.Y. Brokoli (Zeytinyağı-Limon Soslu)", "kcal": 78},
                {"name": "Çoban Salata", "kcal": 114},
                {"name": "Karışık Turşu", "kcal": 27}
            ],
            "İKİNDİ": [
                {"name": "Mozaik Pasta", "kcal": 370},
                {"name": "Limonata", "kcal": 73}
            ]
        }
    },
    "2026-10-28": {
        "day_name": "ÇARŞAMBA",
        "date_str": "28 Ekim 2026",
        "meals": {
            "KAHVALTI": [
                {"name": "Simit", "kcal": 143},
                {"name": "Kaşar Peynir", "kcal": 56},
                {"name": "Zeytin", "kcal": 27},
                {"name": "Domates-Salatalık", "kcal": 34},
                {"name": "Ihlamur Çayı", "kcal": 14}
            ],
            "ÖĞLE YEMEĞİ": [
                {"name": "Süzme Mercimek Çorbası", "kcal": 120},
                {"name": "Geleneksel Orman Kebabı", "kcal": 260},
                {"name": "Tereyağlı Pirinç Pilavı", "kcal": 210},
                {"name": "Cevizli Baklava / Bayram Tatlısı", "kcal": 350}
            ],
            "SALATA BÜFESİ": [
                {"name": "Mevsim Salata", "kcal": 122},
                {"name": "Naneli Cacık / Çırpılmış Yoğurt", "kcal": 113},
                {"name": "Gavurdağı Salata", "kcal": 115},
                {"name": "Kırmızı Lahana Salatası", "kcal": 54},
                {"name": "Zeytinyağlı Semizotu Salatası", "kcal": 50}
            ],
            "İKİNDİ": [
                {"name": "Bayrak Temalı Kırmızı-Beyaz Kurabiye", "kcal": 180},
                {"name": "Meyve Suyu", "kcal": 75}
            ]
        }
    },
    "2026-10-29": {
        "day_name": "PERŞEMBE",
        "date_str": "29 Ekim 2026",
        "meals": {
            "KAHVALTI": [],
            "ÖĞLE YEMEĞİ": [
                {"name": "🇹🇷 29 EKİM CUMHURİYET BAYRAMI (RESMİ TATİL)", "kcal": 0}
            ],
            "SALATA BÜFESİ": [],
            "İKİNDİ": []
        }
    },
    "2026-10-30": {
        "day_name": "CUMA",
        "date_str": "30 Ekim 2026",
        "meals": {
            "KAHVALTI": [
                {"name": "Peynirli Omlet", "kcal": 200},
                {"name": "Beyaz Peynir", "kcal": 93},
                {"name": "Bal & Tereyağ", "kcal": 105},
                {"name": "Havuç Çubukları", "kcal": 34},
                {"name": "Süt", "kcal": 88}
            ],
            "ÖĞLE YEMEĞİ": [
                {"name": "Domates Çorbası", "kcal": 122},
                {"name": "Fırın Dalyan Köfte", "kcal": 280},
                {"name": "Kadife Patates Püresi", "kcal": 140},
                {"name": "Ayran", "kcal": 63}
            ],
            "SALATA BÜFESİ": [
                {"name": "Mevsim Yeşilliği", "kcal": 122},
                {"name": "Roka-Tere-Domates Salatası", "kcal": 65},
                {"name": "Ekşili Kısır", "kcal": 178},
                {"name": "Salatalık Turşusu", "kcal": 15},
                {"name": "Limonlu Havuç Rende", "kcal": 68}
            ],
            "İKİNDİ": [
                {"name": "Mini Simit", "kcal": 75},
                {"name": "Ayran", "kcal": 63}
            ]
        }
    }
}


def auto_register_day_samples(date_key: str, taken_by: str) -> List[str]:
    """Secilen gunun menusundeki yemekleri tek tikla sahit numune olarak kaydeder."""
    if date_key not in WEEKLY_MENU:
        return ["Hata: Gecersiz tarih"]

    day_data = WEEKLY_MENU[date_key]
    day_date = datetime.date.fromisoformat(date_key)
    results = []

    # Eger tatil gunuyse kayit yapma
    lunch_list = day_data["meals"].get("ÖĞLE YEMEĞİ", [])
    if lunch_list and "TATİL" in lunch_list[0]["name"]:
        return ["Bilgi: Resmi tatil gününde şahit numune alınmaz."]

    # 1. Kahvalti Numunesi (varsa)
    breakfast_list = day_data["meals"].get("KAHVALTI", [])
    if breakfast_list:
        breakfast_items = ", ".join([item["name"] for item in breakfast_list[:3]])
        b_ok, b_msg = haccp_manager.add_haccp_sample(
            meal_name=f"{breakfast_items} (Kahvaltı)",
            meal_type="Sabah Kahvaltısı",
            sample_date=day_date,
            sample_time="08:30",
            sample_taken_by=taken_by,
            notes=f"{day_data['date_str']} kahvaltı şahit numunesi"
        )
        results.append(b_msg)

    # 2. Ogle Yemegi Ana Numuneleri (Tek tek corba, ana yemek, garnitur)
    for m in lunch_list:
        if m["kcal"] > 0:
            m_ok, m_msg = haccp_manager.add_haccp_sample(
                meal_name=f"{m['name']} ({m['kcal']} kcal)",
                meal_type="Öğle Yemeği",
                sample_date=day_date,
                sample_time="12:00",
                sample_taken_by=taken_by,
                notes=f"{day_data['date_str']} öğle menüsü şahit numunesi"
            )
            results.append(m_msg)

    # 3. Salata Bufesi Numunesi (varsa)
    salad_list = day_data["meals"].get("SALATA BÜFESİ", [])
    if salad_list:
        salad_items = ", ".join([item["name"] for item in salad_list[:2]])
        s_ok, s_msg = haccp_manager.add_haccp_sample(
            meal_name=f"{salad_items} (Salata Büfesi)",
            meal_type="Öğle Yemeği",
            sample_date=day_date,
            sample_time="12:00",
            sample_taken_by=taken_by,
            notes=f"{day_data['date_str']} salata büfesi numunesi"
        )
        results.append(s_msg)

    # 4. Ikindi Numunesi (varsa)
    ikindi_list = day_data["meals"].get("İKİNDİ", [])
    if ikindi_list:
        ikindi_items = " + ".join([item["name"] for item in ikindi_list])
        i_ok, i_msg = haccp_manager.add_haccp_sample(
            meal_name=f"{ikindi_items} (İkindi)",
            meal_type="İkindi / Ara Öğün",
            sample_date=day_date,
            sample_time="15:30",
            sample_taken_by=taken_by,
            notes=f"{day_data['date_str']} ikindi ara öğün şahit numunesi"
        )
        results.append(i_msg)

    return results
