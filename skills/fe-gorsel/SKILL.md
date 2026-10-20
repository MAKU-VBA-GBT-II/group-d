---
name: fe-gorsel
description: Sigorta talep ve ödeme verilerini (data/talepler-odemeler.csv) ve DQ analiz metriklerini (docs/analiz-g1.md) kullanarak zaman serisi ve branş kırılımı grafiklerini (visuals/) üretir.
---

# fe-gorsel: Veri Görselleştirme ve Grafik Üretimi

Bu skill, BE tarafından üretilen sentetik sigorta verisi (`data/talepler-odemeler.csv`) ve DQ tarafından hazırlanan analiz metrikleri (`docs/analiz-g1.md`) doğrultusunda, zaman serisi trendi ve branş kırılımı grafiklerini oluşturarak `visuals/` klasörüne yüksek çözünürlüklü PNG formatında kaydeder.

## Amaç

- Sektörel sigorta talep ve tazminat ödeme eğilimlerini anlaşılır, profesyonel grafiklerle görselleştirmek.
- Ders gereksinimleri doğrultusunda; başlık, X/Y eksen etiketleri, ölçü birimleri ve açıklayıcı göstergeleri (legend) eksiksiz içeren standartlara uygun görseller sunmak.

## Adımlar

1. `G1-gorsel` Issue'su üzerindeki BE ve DQ devir teslim yorumlarını doğrula.
2. İki grafik için taslak (mockup) hazırla ve `G1-gorsel` Issue'suna yükle.
3. `data/talepler-odemeler.csv` dosyasını oku ve tarih alanını 12 çeyreklik dönemlere (`YYYY-QX`) ayrıştır.
4. `src/gorsellestir.py` betiğini çalıştırarak 2 temel grafiği üret:
   - **Grafik 1 (Zaman Serisi):** 12 çeyreklik (2023-Q1 — 2025-Q4) talep ve ödenen tazminat tutarı trend çizgisi (`visuals/ceyreklik-trend.png`).
   - **Grafik 2 (Kategorik Kırılım):** 6 sigorta branşında (Hayat, DASK, Konut, Kasko, Sağlık, Trafik) toplam talep ve ödenen tazminat tutarlarını karşılaştıran çubuk grafiği (`visuals/talep-turu-kirilimi.png`).
5. Her iki grafiğin de şu standartları sağladığını denetle:
   - Açıklayıcı Türkçe başlık
   - X ve Y eksen etiketleri
   - Ölçü birimi (Milyon TL / TL)
   - Renk ve lejant ayrımı
   - Yüksek çözünürlük (300 DPI, PNG)
6. Üretilen görselleri `visuals/` klasörüne kaydet.
7. `G1-gorsel` Issue'suna commit hash'i ve çıktı yollarını içeren kanıt yorumu yazarak devir teslimi tamamla.

## Kullandığı Dosyalar

- `data/talepler-odemeler.csv` (girdi veri seti)
- `docs/analiz-g1.md` (metrik ve bulgular referansı)
- `docs/veri-sozlugu-g1.md` (şema ve tip sınırları referansı)
- `src/gorsellestir.py` (görselleştirme betiği)
- `visuals/ceyreklik-trend.png` (çıktı zaman serisi grafiği)
- `visuals/talep-turu-kirilimi.png` (çıktı kategorik kırılım grafiği)

## Nasıl Çalıştırılır

```bash
# Görselleştirme betiğini çalıştır
python src/gorsellestir.py
```

Ajan ortamında: *"fe-gorsel skill'ini kullanarak data/talepler-odemeler.csv verisinden zaman serisi ve kategori kırılım grafiklerini üretip visuals/ dizinine kaydet"* talimatı verilir.
