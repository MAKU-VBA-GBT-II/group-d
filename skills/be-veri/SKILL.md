---
name: be-veri
description: >
  Sigorta talepleri, ödemeleri ve portföy poliçeleri için sentetik veri üretme ve bölgesel simülasyon becerisi.
  Sabit tohumlu (deterministic) CSV veri seti oluşturur.
---

# BE-Veri: Sentetik Sigorta Verisi ve Poliçe Simülasyonu

Bu beceri, sigorta talepleri ve ödeme kayıtları ile AFAD/MGM açık veri entegrasyonuna uygun bölgesel portföy poliçe veri setlerini sentetik olarak üretir.

## Amaç

- Analiz, afet risk modellemesi ve çok ajanlı entegrasyon çalışmaları için **gerçekçi ama yapay** sigorta verisi sağlamak.
- Sabit tohum (`SEED=42`) ile **tekrarlanabilir** (idempotent) veri üretimini garanti etmek.
- AFAD ve MGM ile uyumlu ortak il anahtarı (`il_anahtari`) ve dış parametre desteği sunmak.

## Kullanım

### 1. Portföy Poliçe Simülasyonu (Sürüm 2 — Çok Ajanlı Şirket Programı)
```bash
# Varsayılan üretim (250 satır, data/policeler.csv)
python src/simulasyon.py

# Dış parametrelerle üretim (belirli iller ve prim aralığı)
python src/simulasyon.py --iller "Kahramanmaraş,Hatay,Kocaeli,İzmir" --prim-min 3000 --prim-max 15000 --adet 500
```
Çıktı: `data/policeler.csv` (Şema: [`docs/veri-sozlugu.md`](../../docs/veri-sozlugu.md))

### 2. Talep ve Ödeme Verisi (Sürüm 1)
```bash
python src/veri-uret.py
```
Çıktı: `data/talepler-odemeler.csv` (Şema: [`docs/veri-sozlugu-g1.md`](../../docs/veri-sozlugu-g1.md))

## Dosya Yapısı

```
├── data/
│   ├── policeler.csv            # Portföy poliçeleri ve bölgesel veriler (Sürüm 2)
│   └── talepler-odemeler.csv    # Hasar talep ve ödeme veri seti (Sürüm 1)
├── docs/
│   ├── veri-sozlugu.md          # Sürüm 2 veri sözlüğü
│   └── veri-sozlugu-g1.md       # Sürüm 1 veri sözlüğü
├── src/
│   ├── simulasyon.py            # Parametrik simülasyon motoru (Sürüm 2)
│   └── veri-uret.py             # Hasar veri üreticisi (Sürüm 1)
└── skills/
    └── be-veri/
        └── SKILL.md             # Bu dosya
```

## İdempotentlik

Her iki betik de varsayılan tohum (`42`) ile çalıştırıldığında her seferinde birebir aynı CSV dosyasını üretir.

## Bağımlılıklar

- Python 3.10+
- Yalnızca standart kütüphane (`csv`, `random`, `datetime`, `argparse`, `re`).
