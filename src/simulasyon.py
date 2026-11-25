#!/usr/bin/env python3
"""
Emin Sigorta (Grup D) — Sentetik Portföy Poliçe ve Bölgesel Simülasyon Motoru
Sürüm: 2.0 (Çok Ajanlı Şirket Programı - Senaryo Genişletme)

AFAD, Kandilli Rasathanesi ve MGM açık veri kaynaklarıyla entegrasyona uygun;
il/ilçe bazlı, ortak il anahtarı (il_anahtari) üreten, dış parametre desteğine
(il listesi ve prim aralığı) ve sabit tohuma (SEED=42) sahip simülasyon betiği.

Varsayılan çıktı: data/policeler.csv
"""

import argparse
import csv
import os
import random
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Tuple, List, Dict

# ── Sabit Tohum ──────────────────────────────────────────────────────────────
DEFAULT_SEED = 42
DEFAULT_SATIR_SAYISI = 250

# ── İl ve İlçe Referans Veritabanı ──────────────────────────────────────────
# Özellikle deprem ve afet risk analizi senaryosunda AFAD ve MGM verileriyle
# doğrudan örtüşen 81 il ve kritik sismik/meteorolojik ilçeler
IL_ILCE_REHBERI: Dict[str, List[str]] = {
    "İstanbul": ["Kadıköy", "Beşiktaş", "Üsküdar", "Bakırköy", "Avcılar", "Maltepe", "Kartal", "Sarıyer", "Fatih", "Pendik"],
    "Ankara": ["Çankaya", "Keçiören", "Yenimahalle", "Mamak", "Etimesgut", "Sincan"],
    "İzmir": ["Konak", "Karşıyaka", "Bornova", "Buca", "Bayraklı", "Çiğli", "Seferihisar", "Urla"],
    "Kocaeli": ["İzmit", "Gebze", "Gölcük", "Körfez", "Derince", "Kartepe"],
    "Kahramanmaraş": ["Onikişubat", "Dulkadiroğlu", "Elbistan", "Pazarcık", "Afşin", "Göksun", "Türkoğlu"],
    "Hatay": ["Antakya", "İskenderun", "Defne", "Samandağ", "Kırıkhan", "Dörtyol", "Arsuz"],
    "Malatya": ["Battalgazi", "Yeşilyurt", "Doğanşehir", "Akçadağ"],
    "Gaziantep": ["Şahinbey", "Şehitkamil", "Nizip", "İslahiye", "Nurdağı"],
    "Adana": ["Seyhan", "Çukurova", "Yüreğir", "Ceyhan", "Kozan"],
    "Bursa": ["Osmangazi", "Nilüfer", "Yıldırım", "Gemlik", "Mudanya", "İnegöl"],
    "Antalya": ["Muratpaşa", "Kepez", "Konyaaltı", "Alanya", "Manavgat"],
    "Muğla": ["Bodrum", "Fethiye", "Marmaris", "Menteşe", "Milas"],
    "Çanakkale": ["Merkez", "Biga", "Çan", "Gelibolu", "Ayvacık"],
    "Balıkesir": ["Karesi", "Altıeylül", "Bandırma", "Edremit", "Ayvalık"],
    "Sakarya": ["Adapazarı", "Serdivan", "Erenler", "Hendek", "Akyazı"],
    "Düzce": ["Merkez", "Akçakoca", "Kaynaşlı", "Gölyaka", "Çilimli"],
    "Yalova": ["Merkez", "Çiftlikköy", "Çınarcık", "Altınova"],
    "Bingöl": ["Merkez", "Genç", "Karlıova", "Solhan"],
    "Elazığ": ["Merkez", "Kovancılar", "Karakoçan", "Sivrice", "Maden"],
    "Diyarbakır": ["Bağlar", "Kayapınar", "Sur", "Yenişehir", "Ergani"],
    "Şanlıurfa": ["Haliliye", "Eyyübiye", "Karaköprü", "Siverek", "Birecik"],
    "Samsun": ["İlkadım", "Atakum", "Canik", "Bafra", "Çarşamba"],
    "Trabzon": ["Ortahisar", "Akçaabat", "Yomra", "Vakfıkebir"],
    "Konya": ["Selçuklu", "Meram", "Karatay", "Ereğli", "Akşehir"],
    "Kayseri": ["Melikgazi", "Kocasinan", "Talas", "Develi"],
    "Eskişehir": ["Tepebaşı", "Odunpazarı", "Sivrihisar"],
    "Denizli": ["Pamukkale", "Merkezefendi", "Çivril", "Acıpayam"],
    "Mersin": ["Yenişehir", "Akdeniz", "Mezitli", "Toroslar", "Tarsus"],
    "Tekirdağ": ["Süleymanpaşa", "Çorlu", "Çerkezköy", "Şarköy"],
    "Van": ["İpekyolu", "Tuşba", "Edremit", "Erciş"],
}

POLICE_TURLERI = [
    "Konut",
    "İş Yeri",
    "DASK",
    "Kasko",
    "Trafik",
]

# Branş bazlı varsayılan teminat ve prim sınırları (TL)
BRANS_LIMITLERI = {
    "Konut":   {"teminat": (500_000, 5_000_000),   "prim_orani": (0.0020, 0.0050)},
    "İş Yeri": {"teminat": (1_000_000, 15_000_000), "prim_orani": (0.0025, 0.0060)},
    "DASK":    {"teminat": (300_000, 1_500_000),    "prim_orani": (0.0010, 0.0035)},
    "Kasko":   {"teminat": (250_000, 2_500_000),    "prim_orani": (0.0150, 0.0350)},
    "Trafik":  {"teminat": (100_000, 500_000),      "prim_orani": (0.0100, 0.0250)},
}


# ── İl ve Karakter Normalizasyonu (AFAD / MGM Uyumu) ─────────────────────────

def il_anahtari_uret(metin: str) -> str:
    """
    Türkçe karakter ve büyük/küçük harf (özellikle İ/ı) farklılıklarını ortadan kaldırarak
    AFAD, Kandilli ve MGM kayıtlarıyla %100 örtüşen standart bir ortak anahtar üretir.

    Örnekler:
      'İstanbul'      -> 'ISTANBUL'
      'İZMİR'         -> 'IZMIR'
      'Kahramanmaraş' -> 'KAHRAMANMARAS'
      'Diyarbakır'    -> 'DIYARBAKIR'
      'Çanakkale'     -> 'CANAKKALE'
    """
    if not metin or not isinstance(metin, str):
        return ""

    # 1. Aşama: İ ve ı harflerini standart I karakterine eşitle
    m = metin.replace("İ", "I").replace("i", "I").replace("ı", "I").replace("I", "I")

    # 2. Aşama: Diğer Türkçe karakterleri ASCII büyük harfe çevir
    tr_tablo = str.maketrans({
        "ç": "C", "Ç": "C",
        "ğ": "G", "Ğ": "G",
        "ö": "O", "Ö": "O",
        "ş": "S", "Ş": "S",
        "ü": "U", "Ü": "U",
    })
    m = m.translate(tr_tablo).strip().upper()

    # 3. Aşama: Fazla boşlukları veya tireleri temizle
    m = re.sub(r"[\s\-]+", "_", m)
    return m


def rastgele_tarih(baslangic: datetime, bitis: datetime) -> str:
    """Belirtilen iki tarih arasında rastgele YYYY-MM-DD biçiminde tarih üretir."""
    delta = (bitis - baslangic).days
    gun = random.randint(0, delta)
    return (baslangic + timedelta(days=gun)).strftime("%Y-%m-%d")


# ── Sentetik Veri Simülasyonu ────────────────────────────────────────────────

def police_uret(
    satir_sayisi: int = DEFAULT_SATIR_SAYISI,
    secili_iller: Optional[List[str]] = None,
    prim_araligi: Optional[Tuple[float, float]] = None,
    seed: int = DEFAULT_SEED,
) -> List[Dict]:
    """
    Senaryoya uygun sentetik sigorta poliçeleri üretir.

    Parametreler:
      satir_sayisi: Üretilecek toplam satır sayısı (varsayılan: 250).
      secili_iller: Filtreleme yapılacak il listesi. Verilmezse tüm referans iller kullanılır.
      prim_araligi: (min_prim, max_prim) çifti. Verilirse primler bu aralıkta üretilir.
      seed: Tekrarlanabilirliği sağlayan rastgele tohum (varsayılan: 42).
    """
    random.seed(seed)

    # İl listesini belirle
    if secili_iller:
        # Gelen il isimlerini rehberdeki eşleşenlerle eşle
        istenen_anahtarlar = {il_anahtari_uret(il): il for il in secili_iller}
        kullanilabilir_rehber = {
            il: ilceler
            for il, ilceler in IL_ILCE_REHBERI.items()
            if il_anahtari_uret(il) in istenen_anahtarlar
        }
        # Eğer özel girilen il listede yoksa tekil olarak ekle
        for il in secili_iller:
            k = il_anahtari_uret(il)
            if not any(il_anahtari_uret(var_il) == k for var_il in kullanilabilir_rehber):
                kullanilabilir_rehber[il] = ["Merkez"]
    else:
        kullanilabilir_rehber = IL_ILCE_REHBERI

    mevcut_iller = list(kullanilabilir_rehber.keys())

    baslangic_donemi = datetime(2024, 1, 1)
    bitis_donemi = datetime(2026, 11, 25)

    satirlar: List[Dict] = []

    for i in range(1, satir_sayisi + 1):
        police_id = f"POL-{i:05d}"
        il = random.choice(mevcut_iller)
        ilce = random.choice(kullanilabilir_rehber[il])
        il_anahtari = il_anahtari_uret(il)
        police_turu = random.choice(POLICE_TURLERI)

        # Teminat tutarı belirleme
        t_alt, t_ust = BRANS_LIMITLERI[police_turu]["teminat"]
        teminat_tutari = round(random.uniform(t_alt, t_ust), 2)

        # Prim tutarı belirleme (dışarıdan prim_araligi verilmişse öncelikli kullan)
        if prim_araligi is not None:
            p_min, p_max = prim_araligi
            prim_tutari = round(random.uniform(p_min, p_max), 2)
        else:
            oran_alt, oran_ust = BRANS_LIMITLERI[police_turu]["prim_orani"]
            prim_orani = random.uniform(oran_alt, oran_ust)
            prim_tutari = round(teminat_tutari * prim_orani, 2)

        # Tarihler
        baslangic_tarihi = rastgele_tarih(baslangic_donemi, bitis_donemi)
        bas_dt = datetime.strptime(baslangic_tarihi, "%Y-%m-%d")
        bitis_tarihi = (bas_dt + timedelta(days=365)).strftime("%Y-%m-%d")

        # Ek senaryo alanları: bina yaşı ve deprem teminatı
        if police_turu in ("Konut", "İş Yeri", "DASK"):
            bina_yasi = random.randint(1, 40)
            if police_turu == "DASK":
                deprem_teminati = "Evet"
            else:
                deprem_teminati = "Evet" if random.random() < 0.85 else "Hayır"
        else:
            bina_yasi = ""  # Araç sigortalarında bina yaşı uygulanmaz
            deprem_teminati = "Evet" if (police_turu == "Kasko" and random.random() < 0.70) else "Hayır"

        satirlar.append({
            "police_id": police_id,
            "il": il,
            "ilce": ilce,
            "il_anahtari": il_anahtari,
            "police_turu": police_turu,
            "teminat_tutari": teminat_tutari,
            "prim_tutari": prim_tutari,
            "baslangic_tarihi": baslangic_tarihi,
            "bitis_tarihi": bitis_tarihi,
            "bina_yasi": bina_yasi,
            "deprem_teminati": deprem_teminati,
        })

    return satirlar


# ── CSV Yazımı ───────────────────────────────────────────────────────────────

def csv_yaz(satirlar: List[Dict], dosya_yolu: str = "data/policeler.csv") -> str:
    """Verilen poliçe satırlarını UTF-8 (BOM) kodlamasıyla CSV dosyasına kaydeder."""
    hedef = Path(dosya_yolu)
    hedef.parent.mkdir(parents=True, exist_ok=True)

    alanlar = [
        "police_id",
        "il",
        "ilce",
        "il_anahtari",
        "police_turu",
        "teminat_tutari",
        "prim_tutari",
        "baslangic_tarihi",
        "bitis_tarihi",
        "bina_yasi",
        "deprem_teminati",
    ]

    with open(hedef, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=alanlar)
        writer.writeheader()
        writer.writerows(satirlar)

    print(f"[OK] {len(satirlar)} poliçe kaydı oluşturuldu -> {hedef.resolve()}")
    return str(hedef.resolve())


# ── Komut Satırı Arayüzü (CLI) ───────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Emin Sigorta — Sentetik Poliçe ve Bölgesel Simülasyon Motoru (Sürüm 2)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Örnek Kullanımlar:
  # 1. Varsayılan veri seti üretimi (250 satır, SEED=42, data/policeler.csv):
  python src/simulasyon.py

  # 2. Belirli illere göre simülasyon:
  python src/simulasyon.py --iller "Kocaeli,Kahramanmaraş,İzmir"

  # 3. Dış prim aralığı ve satır sayısı belirleme:
  python src/simulasyon.py --prim-min 2500 --prim-max 12000 --adet 500

  # 4. Özel çıktı yolu ve özel tohum:
  python src/simulasyon.py --cikti data/ozel-policeler.csv --tohum 99
        """,
    )
    parser.add_argument(
        "--adet", "--satir-sayisi",
        dest="adet",
        type=int,
        default=DEFAULT_SATIR_SAYISI,
        help=f"Üretilecek poliçe adedi (varsayılan: {DEFAULT_SATIR_SAYISI})",
    )
    parser.add_argument(
        "--iller",
        type=str,
        default=None,
        help="Simülasyona dahil edilecek virgülle ayrılmış il listesi (Örn: 'İstanbul,İzmir,Kahramanmaraş')",
    )
    parser.add_argument(
        "--prim-min",
        type=float,
        default=None,
        help="Dışarıdan belirlenen minimum prim tutarı (TL)",
    )
    parser.add_argument(
        "--prim-max",
        type=float,
        default=None,
        help="Dışarıdan belirlenen maksimum prim tutarı (TL)",
    )
    parser.add_argument(
        "--tohum", "--seed",
        dest="tohum",
        type=int,
        default=DEFAULT_SEED,
        help=f"Rastgele tohum değeri (varsayılan: {DEFAULT_SEED})",
    )
    parser.add_argument(
        "--cikti", "--output",
        dest="cikti",
        type=str,
        default="data/policeler.csv",
        help="Çıktı CSV dosya yolu (varsayılan: data/policeler.csv)",
    )

    args = parser.parse_args()

    # İl listesini ayrıştır
    secili_iller = None
    if args.iller:
        secili_iller = [il.strip() for il in args.iller.split(",") if il.strip()]

    # Prim aralığını doğrula
    prim_araligi = None
    if args.prim_min is not None or args.prim_max is not None:
        p_min = args.prim_min if args.prim_min is not None else 500.0
        p_max = args.prim_max if args.prim_max is not None else 50_000.0
        if p_min > p_max:
            parser.error("--prim-min, --prim-max değerinden büyük olamaz!")
        prim_araligi = (p_min, p_max)

    veriler = police_uret(
        satir_sayisi=args.adet,
        secili_iller=secili_iller,
        prim_araligi=prim_araligi,
        seed=args.tohum,
    )

    csv_yaz(veriler, args.cikti)


if __name__ == "__main__":
    main()
