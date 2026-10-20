---
name: dq-test
description: Veri kalitesi gereksinimlerine göre test senaryolarını (tests/test-cases.md) tasarlar ve doğrular.
---

# dq-test: Veri Kalitesi Test Senaryoları Tasarımı ve Doğrulama

Bu skill, üretilen veri setinin (`data/talepler-odemeler.csv`) veri sözlüğüne (`docs/veri-sozlugu-g1.md`) ve veri kalitesi (Data Quality) kurallarına uygunluğunu denetlemek için test senaryolarını yapılandırır.

## Amaç

- Veri setinde eksik, hatalı, sınır dışı veya şemaya uymayan kayıtları tespit etmek.
- Hafta 3'te test senaryolarını ve kabul kriterlerini belirlemek (`tests/test-cases.md`).
- Hafta 4'te testleri çalıştırıp gerçekleşen sonuçları raporlamak.

## Adımlar

1. `docs/veri-sozlugu-g1.md` dosyasındaki alan tipleri, tutar aralıkları, kategori listeleri ve boş değer kurallarını incele.
2. En az 5 temel kalite boyutunu kapsayan senaryolar tanımla:
   - Dosya varlığı ve kodlama (UTF-8 BOM)
   - Satır sayısı doğrulaması (200 satır)
   - Sütun isimleri ve sayısı (9 alan)
   - Tipler ve branş bazlı min/maks tutar aralıkları
   - Kategorik değer kümeleri ve koşullu boş değer kuralları
3. Senaryoları, beklenen sonuçları ve test adımlarını `tests/test-cases.md` tablosuna işle.
4. Hafta 4'te testleri yürütüp "Gerçekleşen Sonuç" ve "Durum" sütunlarını güncelle.

## Kullandığı Dosyalar

- `docs/veri-sozlugu-g1.md` (kural ve şema referansı)
- `data/talepler-odemeler.csv` (test edilen veri)
- `tests/test-cases.md` (test senaryoları ve sonuç matrisi)

## Nasıl Çalıştırılır

Ajan ortamında: *"dq-test skill'ini kullanarak tests/test-cases.md dosyasında veri kalitesi senaryolarını oluştur"* komutu verilir.
