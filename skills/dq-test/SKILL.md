---
name: dq-test
description: Veri kalitesi gereksinimlerine göre test senaryolarını (tests/test-cases.md) tasarlar ve doğrular.
---

# dq-test: Veri Kalitesi Test Senaryoları Tasarımı ve Doğrulama

Bu skill, üretilen veri setinin (`data/talepler-odemeler.csv`) veri sözlüğüne (`docs/veri-sozlugu-g1.md`) ve veri kalitesi (Data Quality) kurallarına uygunluğunu denetlemek için test senaryolarını yapılandırır.

## Amaç

- Veri setinde eksik, hatalı, sınır dışı veya şemaya uymayan kayıtları tespit etmek.
- Hafta 3'te test senaryolarını, ID'lerini, adımlarını ve beklenen sonuçlarını belirlemek (`tests/test-cases.md`).
- Hafta 4'te testleri çalıştırıp gerçekleşen sonuçları raporlamak.

## Adımlar

1. `docs/veri-sozlugu-g1.md` dosyasındaki alan tipleri, tutar aralıkları, kategori listeleri ve boş değer kurallarını incele.
2. Veri sözlüğündeki kurallara göre yedi test senaryosu tanımla:
   - **TC-01:** Dosya varlığı ve kodlama (UTF-8 BOM).
   - **TC-02:** Boyut ve sütun yapısı (200 satır + başlık, 9 alan).
   - **TC-03:** `talep_id` benzersizliği ve `TLP-XXXXX` formatı.
   - **TC-04:** Kategorik değer kümeleri (branş, durum, şehir, ödeme yöntemi).
   - **TC-05:** Onaylanmayan taleplerde tutarın 0.0 olması ve tarih/yöntem alanlarının boşluğu.
   - **TC-06:** Onaylanan taleplerde %60–100 ödeme oranı ve 5–90 gün ödeme vadesi.
   - **TC-07:** Branş bazlı min–maks tutar sınırları.
3. Senaryoları, beklenen sonuçları ve test adımlarını `tests/test-cases.md` tablosuna işle.
4. Hafta 4'te testleri yürütüp "Gerçekleşen Sonuç" ve "Geçti / Kaldı" sütunlarını güncelle.

## Kullandığı Dosyalar

- `docs/veri-sozlugu-g1.md` (kural ve şema referansı)
- `data/talepler-odemeler.csv` (test edilen veri)
- `tests/test-cases.md` (test senaryoları ve sonuç matrisi)
- `tests/test_veri_kalitesi.py` (otomatik test paketi)
- `tests/test-log.md` (test yürütme günlüğü)

## Nasıl Çalıştırılır

```bash
# Otomatik veri kalitesi test paketini çalıştır
python tests/test_veri_kalitesi.py
```

Ajan ortamında: *"dq-test skill'ini kullanarak tests/test_veri_kalitesi.py test paketini çalıştır ve tests/test-log.md dosyasında sonuçları raporla"* komutu verilir.
