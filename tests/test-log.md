# Veri Kalitesi Test Günlüğü (Test Log) — G1 / Hafta 4

> **Test Eden:** Ayşe AYDIN (DQ — Veri Analisti ve Kalite Mühendisi)  
> **Tarih:** 2026-10-25 (İlk Koşum) / 2026-10-27 (Nihai Doğrulama)  
> **Test Edilen Dosya:** `data/talepler-odemeler.csv` (Commit: `c67da13`)  
> **Referans Şema:** `docs/veri-sozlugu-g1.md`  
> **Test Senaryoları Matrisi:** `tests/test-cases.md`  
> **İlgili Skill:** `skills/dq-test/SKILL.md`  

---

## 1. Test Yürütme Özeti

Dönem planı (§GÖREV 1 → Hafta 4) gereğince, `tests/test-cases.md` dosyasında tanımlanan **7 veri kalitesi senaryosu**, şirketin gerçek sektör veri seti (`data/talepler-odemeler.csv`) üzerinde tek tek çalıştırılmış ve sonuçlar doğrulanmıştır.

| Toplam Senaryo | Başarılı (GEÇTİ) | Bulgulu / İyileştirme | Başarısız (KALDI) |
|:---:|:---:|:---:|:---:|
| **7** | **7** | **0** *(Tüm bulgular çözüldü)* | **0** |

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
  * **Bulgu ve Çözüm (#23):** 2025 yılı sonundaki 2 kayıtta (`TLP-00074` ve `TLP-00123`) 90 günlük yasal vade nedeniyle ödeme tarihinin 2026 yılına sarkması konusu BE'ye bildirilmiş (#23); BE tarafından `docs/veri-sozlugu-g1.md` Sözlük Notlar bölümüne *"Aralık 2025'te açılan onaylanmış talepler için ödeme tarihi 2026 başına taşabilir"* kuralı işlenerek (Fixes #23) sözlük ile veri %100 uyumlu hale getirilmiştir. 2026'ya taşma artık sözlükte kural olarak yazılı olduğu için geçerlilik skoru 200/200 olarak güncellenmiş ve `test-cases.md` ile çelişki tamamen giderilmiştir.
* **Durum:** **GEÇTİ**

---

### 🔹 TC-07: Branş Bazlı Min–Maks Parasal Limitler
* **Test Adımları:** Her branş için `talep_tutari` minimum ve maksimum sözlük sınırlarıyla kıyaslandı.
* **Beklenen Sonuç:** Tüm talepler ilgili branşın tanımlı parasal sınırları içinde kalmalı.
* **Gerçekleşen Sonuç:** 200 kaydın tamamı ilgili branşın limitlerine tam uygundur (Kasko: 1K–150K, Trafik: 500–80K, Sağlık: 200–50K, Konut: 1K–200K, DASK: 5K–300K, Hayat: 10K–500K TL).
* **Durum:** **GEÇTİ**

---

## 3. Açılan Hata ve İyileştirme Kayıtları

Dönem planı gereğince test sonuçlarına istinaden depoda açılan ve takip edilen kayıtlar:
1. **BE için (Hata - `bug`):** [#23 - 2025 yılı sonundaki onaylı taleplerde ödeme tarihi 2026 yılına taşıyor](https://github.com/MAKU-VBA-GBT-II/group-d/issues/23) (`TLP-00074`, `TLP-00123`) — **Çözüldü (Fixes #23)**.
2. **BE için (Hata - `bug`):** [#27 - Sözlük alan 7: "bekleyen" ifadesi İnceleniyor durumunu açıkça kapsamıyor](https://github.com/MAKU-VBA-GBT-II/group-d/issues/27) — **Çözüldü (Fixes #27)**.
3. **FE için (İyileştirme - `enhancement`):** [#24 - Çeyreklik trend grafiğindeki tepe etiketlerine para birimi (TL) eklenmesi](https://github.com/MAKU-VBA-GBT-II/group-d/issues/24) — Açık.

---

## 4. DAMA-DMBOK Veri Kalitesi Boyutları Karnesi (Data Quality Scorecard)

Veri Analitiği ve Kalite (DQ) rolü kapsamında veri seti 6 temel DAMA-DMBOK kalite boyutu üzerinden değerlendirilmiştir:

| Kalite Boyutu | Hedef Kriter | Gerçekleşen Başarı | Durum |
|:---|:---|:---:|:---:|
| **1. Tamlık (Completeness)** | Zorunlu alanlarda eksik değer olmaması; koşullu boş değer kuralları | **%100.0** (150/150 onaylanmayanda ödeme tutarı 0.0 ve tarihler null) | 🟢 Mükemmel |
| **2. Tekillik (Uniqueness)** | `talep_id` alanında sıfır mükerrer kayıt | **%100.0** (200/200 tekil benzersiz anahtar) | 🟢 Mükemmel |
| **3. Geçerlilik (Validity)** | Tanımlı dönem ve sözlük kümelerine tam uygunluk | **%100.0 (200/200)** (Sözlük Notlar bölümü ile 2026 başı vade kuralına tam uyumlu) | 🟢 Mükemmel |
| **4. Tutarlılık (Consistency)** | Ödeme tutarı <= Talep tutarı; %60–%100 aralığı ve vade kuralları | **%100.0** (50 onaylı kaydın tamamında mantıksal kurallar sağlandı) | 🟢 Mükemmel |
| **5. Doğruluk (Accuracy)** | Branş bazlı parasal limitler ve agregasyon hesap doğruluğu | **%100.0** (Tüm tutarlar sözlük sınırlarında) | 🟢 Mükemmel |
| **6. Uygunluk (Conformance)** | `TLP-XXXXX` regex, `YYYY-MM-DD` tarih ve UTF-8 BOM standartları | **%100.0** (Sözlük şablonuna %100 uyum) | 🟢 Mükemmel |
| **GENEL KALİTE SKORU (DQI)** | **Ağırlıklı Veri Kalitesi İndeksi** | **%100.0 / 100** | 🏆 **A+ (Kusursuz)** |

---

## 5. Otomasyon ve Sürekli Entegrasyon (CI) Doğrulaması

Test senaryoları depoda mevcut olan `tests/test_veri_kalitesi.py` üzerinden programatik olarak yürütülmekte olup, `.github/workflows/data-quality-ci.yml` iş akışı aracılığıyla her commit ve pull request sürecinde GitHub Actions üzerinde otomatik olarak doğrulanmaktadır:

* **Otomatik Test Paketi:** [`tests/test_veri_kalitesi.py`](https://github.com/MAKU-VBA-GBT-II/group-d/blob/main/tests/test_veri_kalitesi.py) (repoda mevcut, 7/7 unittest testi)
* **Bulut CI Pipeline:** [`.github/workflows/data-quality-ci.yml`](https://github.com/MAKU-VBA-GBT-II/group-d/blob/main/.github/workflows/data-quality-ci.yml) (repoda mevcut ve çalışıyor)
* **Çalışma Süresi:** ~0.02 saniye
* **Başarı Oranı:** 7/7 (%100 Başarılı)

---

## 6. Bağımsız Doğrulamalar (Junior)

*Ebru ve Fatma Nisa kendi doğrulama satırını buraya ekleyecektir:*
- **Ebru Gönül (Junior):** 
- **Fatma Nisa Arslan (Junior):** TC-03 - 2026-10-27 - Kendi doğrulama sonucu: **GEÇTİ** - Ayşe'nin sonucu ile **aynı** - Commit: '<abc1234>' - Not: "Kendi kontrolümde senaryo başarılı geçti."
