#!/usr/bin/env python3
"""
Sigorta talepleri ve ödemeleri için sentetik veri üreteci.

Sabit tohum (SEED=42) kullanılarak her çalıştırmada aynı CSV dosyası üretilir.
Çıktı: data/talepler-odemeler.csv
"""

import csv
import os
import random
from datetime import datetime, timedelta
from pathlib import Path

# ── Sabit Tohum ──────────────────────────────────────────────────────────────
SEED = 42
random.seed(SEED)

# ── Parametreler ─────────────────────────────────────────────────────────────
SATIR_SAYISI = 200  # en az 100 satır (200 üretiyoruz)

TALEP_TURLERI = [
    "Kasko",
    "Trafik",
    "Sağlık",
    "Konut",
    "DASK",
    "Hayat",
]

DURUM_DEGERLERI = [
    "Onaylandı",
    "Reddedildi",
    "Beklemede",
    "İnceleniyor",
]

SEHIRLER = [
    "İstanbul", "Ankara", "İzmir", "Bursa", "Antalya",
    "Adana", "Konya", "Gaziantep", "Mersin", "Kayseri",
    "Trabzon", "Eskişehir", "Diyarbakır", "Samsun", "Denizli",
]

ODEME_YONTEMLERI = [
    "Havale/EFT",
    "Kredi Kartı",
    "Çek",
    "Nakit",
]

# ── Yardımcı Fonksiyonlar ───────────────────────────────────────────────────

def rastgele_tarih(baslangic: datetime, bitis: datetime) -> str:
    """baslangic ile bitis arasında rastgele bir tarih üretir (YYYY-MM-DD)."""
    delta = (bitis - baslangic).days
    rastgele_gun = random.randint(0, delta)
    return (baslangic + timedelta(days=rastgele_gun)).strftime("%Y-%m-%d")


def talep_tutari(talep_turu: str) -> float:
    """Talep türüne göre makul bir tutar aralığı belirler."""
    araliklar = {
        "Kasko":   (1_000, 150_000),
        "Trafik":  (500, 80_000),
        "Sağlık":  (200, 50_000),
        "Konut":   (1_000, 200_000),
        "DASK":    (5_000, 300_000),
        "Hayat":   (10_000, 500_000),
    }
    alt, ust = araliklar[talep_turu]
    return round(random.uniform(alt, ust), 2)


def odeme_tutari(talep_tutar: float, durum: str) -> float:
    """Duruma göre ödeme tutarı hesaplar."""
    if durum == "Reddedildi":
        return 0.0
    if durum in ("Beklemede", "İnceleniyor"):
        return 0.0
    # Onaylandı → %60-100 arası ödeme
    oran = random.uniform(0.60, 1.00)
    return round(talep_tutar * oran, 2)


# ── Veri Üretimi ─────────────────────────────────────────────────────────────

def veri_uret(satir_sayisi: int = SATIR_SAYISI) -> list[dict]:
    """Sentetik sigorta talep ve ödeme verileri üretir."""
    random.seed(SEED)  # Her çağrıda aynı sonucu garanti et

    baslangic = datetime(2023, 1, 1)
    bitis = datetime(2025, 12, 31)

    satirlar = []
    for i in range(1, satir_sayisi + 1):
        talep_turu = random.choice(TALEP_TURLERI)
        durum = random.choice(DURUM_DEGERLERI)
        talep_tarihi = rastgele_tarih(baslangic, bitis)
        talep_tutar = talep_tutari(talep_turu)
        odeme_tutar = odeme_tutari(talep_tutar, durum)

        # Ödeme tarihi: talep tarihinden 5-90 gün sonra (sadece onaylananlar)
        if durum == "Onaylandı":
            talep_dt = datetime.strptime(talep_tarihi, "%Y-%m-%d")
            odeme_tarihi = (talep_dt + timedelta(days=random.randint(5, 90))).strftime("%Y-%m-%d")
        else:
            odeme_tarihi = ""

        odeme_yontemi = random.choice(ODEME_YONTEMLERI) if durum == "Onaylandı" else ""
        sehir = random.choice(SEHIRLER)

        satirlar.append({
            "talep_id": f"TLP-{i:05d}",
            "talep_tarihi": talep_tarihi,
            "talep_turu": talep_turu,
            "sehir": sehir,
            "talep_tutari": talep_tutar,
            "durum": durum,
            "odeme_tutari": odeme_tutar,
            "odeme_tarihi": odeme_tarihi,
            "odeme_yontemi": odeme_yontemi,
        })

    return satirlar


# ── CSV Yazımı ───────────────────────────────────────────────────────────────

def csv_yaz(satirlar: list[dict], dosya_yolu: str = "data/talepler-odemeler.csv"):
    """Verileri CSV dosyasına yazar."""
    hedef = Path(dosya_yolu)
    hedef.parent.mkdir(parents=True, exist_ok=True)

    alan_adlari = [
        "talep_id", "talep_tarihi", "talep_turu", "sehir",
        "talep_tutari", "durum", "odeme_tutari", "odeme_tarihi",
        "odeme_yontemi",
    ]

    with open(hedef, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=alan_adlari)
        writer.writeheader()
        writer.writerows(satirlar)

    print(f"[OK] {len(satirlar)} satir -> {hedef.resolve()}")
    return str(hedef.resolve())


# ── Ana Giriş ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    veriler = veri_uret()
    csv_yaz(veriler)
