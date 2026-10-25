# Veri Kalitesi Test Günlüğü (Test Log) — G1 / Hafta 4

> **Test Eden:** Ayşe AYDIN (DQ — Veri Analisti ve Kalite Mühendisi)  
> **Tarih:** 2026-10-25  
> **Test Edilen Dosya:** `data/talepler-odemeler.csv` (Commit: `c67da13`)  
> **Referans Şema:** `docs/veri-sozlugu-g1.md`  
> **Test Senaryoları Matrisi:** `tests/test-cases.md`  
> **İlgili Skill:** `skills/dq-test/SKILL.md`  

---

## 1. Test Yürütme Özeti

Dönem planı (§GÖREV 1 → Hafta 4) gereğince, `tests/test-cases.md` dosyasında tanımlanan **7 veri kalitesi senaryosu**, şirketin gerçek sektör veri seti (`data/talepler-odemeler.csv`) üzerinde tek tek çalıştırılmış ve sonuçlar doğrulanmıştır.

| Toplam Senaryo | Başarılı (GEÇTİ) | Bulgulu / İyileştirme (Şartlı GEÇTİ) | Başarısız (KALDI) |
|:---:|:---:|:---:|:---:|
| **7** | **6** | **1** *(TC-06: 2026'ya taşma - Bug #23 açıldı)* | **0** |

---

## 2. Senaryo Bazlı Test Sonuçları (Ayrıntılı Günlük)

### 🔹 TC-01: Dosya Varlığı ve Erişilebilirlik
* **Test Adımları:** `data/talepler-odemeler.csv` dosyasının dosya sistemindeki varlığı, boyutu ve UTF-8 (BOM) formatı kontrol edildi.
* **Beklenen Sonuç:** Dosya mevcut, boş değil (>0 byte) ve UTF-8 BOM ile hatasız okunabilir olmalı.
* **Gerçekleşen Sonuç:** Dosya `data/talepler-odemeler.csv` konumunda mevcut (14.288 bayt). UTF-8 BOM kodlamasıyla Türkçe karakterler (`ş, ğ, ı, ö, ü, ç`) bozulmadan başarıyla okundu.
* **Durum:** **GEÇTİ**

---

### 🔹 TC-02: Boyut ve Sütun Yapısı
* **Test Adımları:** Toplam satır sayısı ve sütun başlıkları sayıldı.
* **Beklenen Sonuç:** Tam 200 veri satırı + 1 başlık satırı; 9 alan tam sıralamayla mevcut olmalı.
* **Gerçekleşen Sonuç:** Başlık hariç tam 200 veri satırı tespit edildi. Sütun adları (`talep_id, talep_tarihi, talep_turu, sehir, talep_tutari, durum, odeme_tutari, odeme_tarihi, odeme_yontemi`) sözlükle %100 eşleşti.
* **Durum:** **GEÇTİ**

---

### 🔹 TC-03: `talep_id` Benzersizliği ve Format Doğrulaması
* **Test Adımları:** `talep_id` alanındaki tekillik ve `^TLP-\d{5}$` regex formatı denetlendi.
* **Beklenen Sonuç:** 200 benzersiz ID; `TLP-00001` formatında düzenli sıra.
* **Gerçekleşen Sonuç:** Tekil ID sayısı: 200/200 (%100 benzersiz, mükerrer kayıt yok). Format regex kontrolünü 200 kaydın tamamı geçti.
* **Durum:** **GEÇTİ**

---

### 🔹 TC-04: Kategorik Değerlerin Sözlük Uygunluğu
* **Test Adımları:** `talep_turu`, `durum`, `sehir` ve `odeme_yontemi` alanlarındaki benzersiz değerler sözlük kümeleriyle karşılaştırıldı.
* **Beklenen Sonuç:** Yalnızca sözlükte tanımlı değerler bulunmalı, yabancı/yazım hatalı değer olmamalı.
* **Gerçekleşen Sonuç:**
  * `talep_turu`: 6 geçerli branş (Kasko, Trafik, Sağlık, Konut, DASK, Hayat).
  * `durum`: 4 geçerli durum (Onaylandı, Reddedildi, Beklemede, İnceleniyor).
  * `sehir`: 15 geçerli il (İstanbul, Ankara, İzmir, Bursa, Antalya, Adana, Konya, Gaziantep, Mersin, Kayseri, Trabzon, Eskişehir, Diyarbakır, Samsun, Denizli).
  * `odeme_yontemi`: 4 geçerli yöntem (Havale/EFT, Kredi Kartı, Çek, Nakit). Tanım dışı değer bulunmadı.
* **Durum:** **GEÇTİ**

---

### 🔹 TC-05: Onaylanmayan Taleplerde Boş Değer (Nullability) Kuralları
* **Test Adımları:** `durum != 'Onaylandı'` olan 150 dosya filtrelendi; `odeme_tutari`, `odeme_tarihi` ve `odeme_yontemi` alanları denetlendi.
* **Beklenen Sonuç:** Onaylanmayanlarda `odeme_tutari == 0.0` olmalı; ödeme tarihi ve yöntemi kesinlikle boş (null/NaN) olmalı.
* **Gerçekleşen Sonuç:** 150 kaydın tamamında `odeme_tutari = 0.0` TL olarak doğrulandı. Hiçbirinde ödeme tarihi ve yöntemi girilmediği (%100 null) teyit edildi.
* **Durum:** **GEÇTİ**

---

### 🔹 TC-06: Onaylanan Taleplerde Ödeme Oranı ve Vade Uygunluğu
* **Test Adımları:** `durum == 'Onaylandı'` olan 50 dosya filtrelendi; ödeme oranı (`odeme_tutari / talep_tutari`) ve gün farkı (`odeme_tarihi - talep_tarihi`) incelendi.
* **Beklenen Sonuç:** Ödeme tutarı, talebin %60–100'ü aralığında olmalı; vade 5–90 gün arasında kalmalı.
* **Gerçekleşen Sonuç:** 50 kaydın tamamında ödeme oranı %60 ile %100 arasında (ortalama %79,65); vade 5–90 gün kuralına uygundur.
  * **Bulgu (Hata Kaydı):** 2025 yılı sonundaki 2 kayıtta (`TLP-00074` ve `TLP-00123`) 90 günlük vade nedeniyle ödeme tarihi 2026 yılına (`2026-02-28` ve `2026-01-20`) sarkmaktadır. Veri sözlüğü Madde 85'te tarih sınırı 2023–2025 olarak tanımlandığından BE için `bug` Issue'su açılmıştır.
* **Durum:** **ŞARTLI GEÇTİ (Bulgu Bildirildi)**

---

### 🔹 TC-07: Branş Bazlı Min–Maks Parasal Limitler
* **Test Adımları:** Her branş için `talep_tutari` minimum ve maksimum sözlük sınırlarıyla kıyaslandı.
* **Beklenen Sonuç:** Tüm talepler ilgili branşın tanımlı parasal sınırları içinde kalmalı.
* **Gerçekleşen Sonuç:** 200 kaydın tamamı ilgili branşın limitlerine tam uygundur (Kasko: 1K–150K, Trafik: 500–80K, Sağlık: 200–50K, Konut: 1K–200K, DASK: 5K–300K, Hayat: 10K–500K TL).
* **Durum:** **GEÇTİ**

---

## 3. Açılan Hata ve İyileştirme Kayıtları

Dönem planı gereğince test sonuçlarına istinaden depoda 2 adet Issue açılmıştır:
1. **BE için (Hata - `bug`):** [#23 - 2025 yılı sonundaki onaylı taleplerde ödeme tarihi 2026 yılına taşıyor](https://github.com/MAKU-VBA-GBT-II/group-d/issues/23) (`TLP-00074`, `TLP-00123`).
2. **FE için (İyileştirme - `enhancement`):** [#24 - Çeyreklik trend grafiğindeki tepe etiketlerine para birimi (TL) eklenmesi](https://github.com/MAKU-VBA-GBT-II/group-d/issues/24).
