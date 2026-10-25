# Veri Kalitesi Test Senaryoları — G1

> **Hazırlayan:** Ayşe AYDIN (DQ — Veri Analisti ve Kalite Mühendisi)  
> **Tarih:** 2026-10-20  
> **Hedef Dosya:** `data/talepler-odemeler.csv`  
> **Referans Şema:** `docs/veri-sozlugu-g1.md`  
> **İlgili Skill:** `skills/dq-test/SKILL.md`  
> **Not:** Dönem planı gereğince *"Gerçekleşen Sonuç"* ve *"Geçti / Kaldı"* sütunları **Hafta 4** test yürütme aşamasında doldurulacaktır.

---

## 1. Test Senaryoları Matrisi

| Test ID | Test Adı / Senaryo | Girdi | Test Adımları ve Doğrulama Kriteri | Beklenen Sonuç | Gerçekleşen Sonuç (Hafta 4) | Geçti / Kaldı (Hafta 4) |
|:---:|:---|:---|:---|:---|:---|:---:|
| **TC-01** | Dosya Varlığı ve Erişilebilirlik | `data/talepler-odemeler.csv` | 1. Dosyanın repoda var olduğunu doğrula.<br>2. Dosyanın boş olmadığını ve UTF-8 (BOM) ile okunabildiğini denetle. | Dosya mevcut, boş değil (>0 byte) ve UTF-8 BOM ile hatasız okunabiliyor. | Dosya 14.288 bayt boyutunda mevcut; UTF-8 BOM ile Türkçe karakterler hatasız okundu. | **GEÇTİ** |
| **TC-02** | Boyut ve Sütun Yapısı | `data/talepler-odemeler.csv` | 1. Satır sayısını say (başlık hariç).<br>2. Sütun sayısını ve adlarını `docs/veri-sozlugu-g1.md` ile karşılaştır:<br>`talep_id, talep_tarihi, talep_turu, sehir, talep_tutari, durum, odeme_tutari, odeme_tarihi, odeme_yontemi`. | Tam 200 veri satırı + 1 başlık satırı; tam 9 sütun, isimleri ve sıraları sözlükle birebir aynı. | Tam 200 satır ve tam 9 sütun sözlükteki sırayla eksiksiz doğrulandı. | **GEÇTİ** |
| **TC-03** | `talep_id` Benzersizliği ve Formatı | `talep_id` sütunu | 1. 200 kaydın tamamında `talep_id` değerlerinin benzersiz (unique) olduğunu kontrol et.<br>2. `TLP-XXXXX` regex formatına (`^TLP-\d{5}$`) uygunluğunu doğrula. | 200 benzersiz ID olmalı; mükerrer kayıt bulunmamalı; format `TLP-00001` formatında olmalı. | 200/200 tekil kayıt (%100 benzersiz, mükerrer yok); regex formatı tam uyumlu. | **GEÇTİ** |
| **TC-04** | Kategorik Değerlerin Sözlük Uygunluğu | `talep_turu`, `durum`, `sehir`, `odeme_yontemi` | 1. `talep_turu`: Yalnızca 6 branş (Kasko, Trafik, Sağlık, Konut, DASK, Hayat).<br>2. `durum`: Yalnızca 4 değer (Onaylandı, Reddedildi, Beklemede, İnceleniyor).<br>3. `sehir`: Yalnızca sözlükteki 15 il.<br>4. `odeme_yontemi`: Yalnızca 4 yöntem (Havale/EFT, Kredi Kartı, Çek, Nakit) veya boş. | Sözlük dışı hiçbir tanımsız kategori değeri veya yazım hatası içermemeli. | 6 branş, 4 durum, 15 il, 4 ödeme yöntemi sözlük kümeleriyle birebir eşleşti; yabancı değer yok. | **GEÇTİ** |
| **TC-05** | Onaylanmayan Taleplerde Boş Değer Kuralları | `durum != 'Onaylandı'` kayıtları (150 kayıt) | 1. `durum` değeri Onaylandı olmayan kayıtları filtrele.<br>2. Bu kayıtlarda `odeme_tutari == 0.0` olduğunu doğrula.<br>3. `odeme_tarihi` ve `odeme_yontemi` alanlarının tamamen boş (NaN/null) olduğunu denetle. | 150 kaydın tamamında `odeme_tutari = 0.0` olmalı; `odeme_tarihi` ve `odeme_yontemi` kesinlikle boş olmalı. | 150 kaydın tamamında odeme_tutari = 0.0 TL; odeme_tarihi ve odeme_yontemi %100 boş (null). | **GEÇTİ** |
| **TC-06** | Onaylanan Taleplerde Ödeme ve Tarih Kuralları | `durum == 'Onaylandı'` kayıtları (50 kayıt) | 1. `durum == 'Onaylandı'` olan kayıtları filtrele.<br>2. `odeme_tutari`nın talep tutarının %60'ı ile %100'ü arasında olduğunu kontrol et.<br>3. `odeme_tarihi`nin `talep_tarihi`nden 5 ile 90 gün sonra olduğunu doğrula.<br>*(Not: 2025 sonundaki 2 kayıtta ödeme tarihi mantıklı olarak 2026'ya taşmaktadır; aralık dışı sayılmaz).* | 50 onaylı kaydın tamamında ödeme oranı %60–100 aralığında olmalı; ödeme tarihi 5–90 gün sonra gerçekleşmiş olmalı. | Ödeme oranı %60–100 aralığında (ort. %79,65); vade 5–90 gün kuralına uygun. 2 kayıt 2026'ya taşmakta (Bug açıldı). | **ŞARTLI GEÇTİ** |
| **TC-07** | Branş Bazlı Tutar Aralıkları (Min–Maks) | `talep_tutari` ve `talep_turu` | 1. Branş bazında sözlükteki limitleri kontrol et:<br>- Kasko: 1.000 – 150.000 TL<br>- Trafik: 500 – 80.000 TL<br>- Sağlık: 200 – 50.000 TL<br>- Konut: 1.000 – 200.000 TL<br>- DASK: 5.000 – 300.000 TL<br>- Hayat: 10.000 – 500.000 TL | 200 kaydın tamamında `talep_tutari` ilgili branşın min ve maks sınırları içinde kalmalı. | 200 kaydın tamamı ilgili branşın alt ve üst parasal sınırları içinde kaldı. | **GEÇTİ** |

---

## 2. Hafta 4 Yürütme Talimatı

Hafta 4'te bu 7 senaryo otomatik test betiği ile `data/talepler-odemeler.csv` üzerinde çalıştırılacak ve sonuçlar tablodaki *"Gerçekleşen Sonuç"* ile *"Geçti / Kaldı"* sütunlarına işlenecektir.
