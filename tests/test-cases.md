# Veri Kalitesi Test Senaryoları — G1

> **Hazırlayan:** Ayşe AYDIN (DQ — Veri Analisti ve Kalite Mühendisi)  
> **Tarih:** 2026-10-20  
> **Hedef Dosya:** `data/talepler-odemeler.csv`  
> **Referans Şema:** `docs/veri-sozlugu-g1.md`  
> **İlgili Skill:** `skills/dq-test/SKILL.md`  
> **Not:** Dönem planı gereğince *"Gerçekleşen Sonuç"* ve *"Durum"* sütunları **Hafta 4** test yürütme aşamasında doldurulacaktır.

---

## 1. Test Senaryoları Tablosu

| Test ID | Test Kategorisi | Test Adı / Senaryo | Test Adımları ve Doğrulama Kriteri | Beklenen Sonuç | Gerçekleşen Sonuç (Hafta 4) | Durum (Hafta 4) |
|:---:|:---|:---|:---|:---|:---:|:---:|
| **TC-01** | Dosya Varlığı | Veri Dosyasının Varlığı ve Kodlama Uygunluğu | 1. `data/talepler-odemeler.csv` dosyasının repoda var olduğunu doğrula.<br>2. Dosyanın UTF-8 (BOM) kodlamasıyla okunabildiğini doğrula. | Dosya mevcut, erişilebilir ve UTF-8 BOM ile hatasız okunabilir olmalı. | *(Hafta 4'te doldurulacak)* | Beklemede |
| **TC-02** | Boyut / Hacim | Satır Sayısı Doğrulaması | 1. CSV dosyasındaki toplam satır sayısını say.<br>2. Başlık satırı hariç veri satır sayısını kontrol et. | Başlık hariç tam olarak 200 satır veri bulunmalı. | *(Hafta 4'te doldurulacak)* | Beklemede |
| **TC-03** | Şema / Yapı | Sütun Sayısı ve İsim Doğrulaması | 1. Başlık satırındaki sütun isimlerini ve sırasını oku.<br>2. `docs/veri-sozlugu-g1.md` ile birebir eşleştir: `talep_id`, `talep_tarihi`, `talep_turu`, `sehir`, `talep_tutari`, `durum`, `odeme_tutari`, `odeme_tarihi`, `odeme_yontemi`. | Tam 9 sütun bulunmalı; sütun adları ve sıraları veri sözlüğü ile eksiksiz eşleşmeli. | *(Hafta 4'te doldurulacak)* | Beklemede |
| **TC-04** | Tipler ve Aralıklar | Tutar Değerleri ve Aralık Kuralları | 1. `talep_tutari` ve `odeme_tutari` pozitif float olmalı.<br>2. `talep_tutari` branş sınırlarında olmalı:<br>   - Kasko: 1.000 - 150.000 TL<br>   - Trafik: 500 - 80.000 TL<br>   - Sağlık: 200 - 50.000 TL<br>   - Konut: 1.000 - 200.000 TL<br>   - DASK: 5.000 - 300.000 TL<br>   - Hayat: 10.000 - 500.000 TL<br>3. `durum = 'Onaylandı'` ise `odeme_tutari`, talep tutarının %60 - %100'ü aralığında olmalı.<br>4. Onaylanmayanlarda `odeme_tutari == 0.0` olmalı. | Tüm sayısal değerler tiplere uygun olmalı ve tanımlanan min/maks limitleri aşmamalı. | *(Hafta 4'te doldurulacak)* | Beklemede |
| **TC-05** | Kategorik Değerler | Kategori Kümeleri ve İzin Verilen Değerler | 1. `talep_turu` yalnızca 6 değerden biri olmalı (Kasko, Trafik, Sağlık, Konut, DASK, Hayat).<br>2. `durum` yalnızca 4 değerden biri olmalı (Onaylandı, Reddedildi, Beklemede, İnceleniyor).<br>3. `sehir` tanımlı 15 ilden biri olmalı.<br>4. `odeme_yontemi` yalnızca 4 değerden biri veya boş olmalı (Havale/EFT, Kredi Kartı, Çek, Nakit). | Tanımlı liste dışı hiçbir geçersiz kategorik değer veya yazım hatası içermemeli. | *(Hafta 4'te doldurulacak)* | Beklemede |
| **TC-06** | Boş Değer Kuralları | Koşullu Boş Değer (Nullability) Uygunluğu | 1. `durum == 'Onaylandı'` olan kayıtlarda `odeme_tarihi` ve `odeme_yontemi` dolu olmalı.<br>2. `durum != 'Onaylandı'` olan kayıtlarda `odeme_tarihi` ve `odeme_yontemi` kesinlikle boş (null) olmalı.<br>3. Diğer 7 zorunlu alanda hiçbir boş değer bulunmamalı. | Yalnızca onaylı kayıtlarda (50 kayıt) ödeme bilgileri dolu; diğer 150 kayıtta boş olmalı. Zorunlu alanlarda 0 boş değer olmalı. | *(Hafta 4'te doldurulacak)* | Beklemede |
| **TC-07** | Mantıksal Bütünlük | Tarih Formatı ve Kronolojik Tutarlılık | 1. `talep_tarihi` ve `odeme_tarihi` `YYYY-MM-DD` formatında ve 2023-01-01 ile 2025-12-31 arasında olmalı.<br>2. Onaylı kayıtlarda `odeme_tarihi >= talep_tarihi` olmalı ve aradaki fark 5 ile 90 gün arasında bulunmalı. | Tüm tarihler geçerli formatta olmalı, geçmişe dönük ödeme veya mantıksız tarih aralığı olmamalı. | *(Hafta 4'te doldurulacak)* | Beklemede |

---

## 2. Test Yürütme Talimatı

Hafta 4'te bu senaryolar `tests/` veya `src/` altındaki otomatik doğrulama betiği ile çalıştırılacak ve sonuçlar yukarıdaki tablonun *"Gerçekleşen Sonuç"* ve *"Durum"* sütunlarına işlenecektir.
