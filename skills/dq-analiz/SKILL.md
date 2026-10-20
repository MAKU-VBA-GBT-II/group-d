---
name: dq-analiz
description: Sigorta talepleri ve ödemeleri verisinden metrik hesaplar, kırılımları inceler ve analiz raporu (docs/analiz-g1.md) üretir.
---

# dq-analiz: Veri Analizi ve Metrik Raporlama

Bu skill, üretilen sentetik sigorta talep ve ödeme veri setini (`data/talepler-odemeler.csv`) analiz ederek temel metrikleri, branş ve durum kırılımlarını hesaplar, somut iş gözlemleri ve eylem önerisi üretir.

## Amaç

- Ham veri setinden özet istatistikler ve yönetsel metrikler çıkarmak.
- FE (Frontend / Görselleştirici) rolüne grafik üretimi için referans veri ve göstergeler sağlamak.
- Veri kalitesi ve operasyonel darboğazları tespit edip raporlamak.

## Adımlar

1. `data/talepler-odemeler.csv` veri dosyasını UTF-8 (BOM) kodlaması ile oku.
2. `src/analiz.py` betiğini çalıştırarak temel metrikleri hesapla:
   - Toplam talep ve ödeme tutarları
   - Ortalama talep ve onaylanan ödeme tutarları
   - Talep türüne (branşa) göre adet, toplam tutar ve ortalama kırılımı
   - Dosya durumuna (Onaylandı, Beklemede vb.) göre dağılım kırılımı
   - En yüksek talep tutarına sahip Top-3 il ve bireysel dosya sıralamaları
3. Hesaplanan her metriğe 1–2 cümlelik iş analizi yorumu ekle.
4. Portföy riski, likidite ihtiyacı ve bölgesel dağılım ekseninde en az 3 somut gözlem çıkar.
5. Şirket yönetimi için uygulanabilir 1 stratejik eylem önerisi formüle et.
6. Tüm çıktıları `docs/analiz-g1.md` dosyasında dokümante et.
7. FE rolü için `G1-gorsel` Issue'sına devir teslim yorumu hazırla.

## Kullandığı Dosyalar

- `data/talepler-odemeler.csv` (girdi veri seti)
- `docs/veri-sozlugu-g1.md` (veri şeması ve sınır referansı)
- `src/analiz.py` (tekrarlanabilir analiz betiği)
- `docs/analiz-g1.md` (çıktı analiz raporu)

## Nasıl Çalıştırılır

```bash
# Analiz betiğini çalıştır
python src/analiz.py
```

Ajan ortamında: *"dq-analiz skill'ini kullanarak veri setini analiz et ve docs/analiz-g1.md raporunu hazırla"* talimatı verilir.
