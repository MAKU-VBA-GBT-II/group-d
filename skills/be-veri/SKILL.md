---
name: be-veri
description: >
  Sigorta talepleri ve ödemeleri için sentetik veri üretme becerisi.
  Sabit tohumlu (deterministic) CSV veri seti oluşturur.
---

# BE-Veri: Sentetik Sigorta Verisi Üretimi

Bu beceri, sigorta talepleri ve ödeme kayıtlarını içeren sentetik (yapay) veri seti üretir.

## Amaç

- Analiz, görselleştirme ve raporlama çalışmaları için **gerçekçi ama yapay** sigorta verisi sağlamak.
- Sabit tohum (`SEED=42`) ile **tekrarlanabilir** (idempotent) veri üretimini garanti etmek.

## Kullanım

```bash
# Veriyi üret (veya yeniden üret)
python src/veri-uret.py
```

Çıktı: `data/talepler-odemeler.csv`

## Çıktı Dosyası

| Özellik | Değer |
|---------|-------|
| Dosya yolu | `data/talepler-odemeler.csv` |
| Kodlama | UTF-8 (BOM) |
| Satır sayısı | 200 |
| Alan sayısı | 9 |
| Talep türü çeşitliliği | 6 (Kasko, Trafik, Sağlık, Konut, DASK, Hayat) |
| Durum çeşitliliği | 4 (Onaylandı, Reddedildi, Beklemede, İnceleniyor) |
| Tarih aralığı | 2023-01-01 – 2025-12-31 |
| Tohum | 42 |

## Şema

Detaylı alan tanımları ve kategorik değerler için bkz. [`docs/veri-sozlugu-g1.md`](../docs/veri-sozlugu-g1.md).

## Dosya Yapısı

```
├── data/
│   └── talepler-odemeler.csv    # Üretilen veri seti
├── docs/
│   └── veri-sozlugu-g1.md       # Veri sözlüğü / şema
├── src/
│   └── veri-uret.py             # Üretici betik
└── skills/
    └── be-veri/
        └── SKILL.md             # Bu dosya
```

## İdempotentlik

Betik aynı tohum (`42`) ile çalıştırıldığında **her seferinde aynı CSV** dosyasını üretir.
Bu sayede:
- CI/CD pipeline'larında tutarlı veri kullanılabilir.
- Analiz sonuçları tekrarlanabilir.
- Hash karşılaştırmasıyla veri bütünlüğü doğrulanabilir.

## Bağımlılıklar

- Python 3.10+
- Ek paket gerekmez (yalnızca standart kütüphane: `csv`, `random`, `datetime`).
