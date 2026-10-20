# Veri Analiz Raporu — G1: Sigorta Talepleri ve Ödemeleri

> **Hazırlayan:** Ayşe AYDIN (DQ — Veri Analisti ve Kalite Mühendisi)  
> **Tarih:** 2026-10-20  
> **Kaynak Veri:** `data/talepler-odemeler.csv` (200 satır, 9 alan, Commit: `c67da13`)  
> **Analiz Betiği:** `src/analiz.py`  
> **İlgili Skill:** `skills/dq-analiz/SKILL.md`  

---

## 1. Yönetici Özeti

Bu analiz raporu, **Emin Sigorta** portföyüne ait sentetik sigorta talep ve tazminat ödeme verileri (`data/talepler-odemeler.csv`) üzerinden hazırlanmıştır. Veri seti, 2023–2025 yılları arasındaki 200 adet hasar talebini ve bunlara ilişkin ödeme süreçlerini kapsamaktadır.

Analizin temel amacı; şirketin branş bazındaki hasar yoğunluğunu, talep sonuçlanma oranlarını, finansal risk dağılımını belirlemek ve **FE (Frontend / Görselleştirici)** adımında üretilecek grafikler için referans metrikleri sağlamaktır.

---

## 2. Temel Metrikler (En Az 5 Metrik)

Aşağıdaki metrikler `src/analiz.py` çalıştırılarak veri setinden doğrudan ve tekrarlanabilir biçimde hesaplanmıştır.

### Metrik 1: Toplam Talep ve Ödeme Tutarı (1 Toplam Metrik)
* **Toplam Talep Sayısı:** 200 adet
* **Toplam Talep Edilen Tutar:** **20.275.728,27 TL**
* **Toplam Ödenen Tazminat Tutarı:** **4.016.662,66 TL**
* *Yorum:* Şirkete 2023–2025 döneminde iletilen toplam hasar talebi yaklaşık 20,28 Milyon TL olup, bu taleplerin 4,02 Milyon TL'lik kısmı onaylanarak hak sahiplerine ödenmiştir.

### Metrik 2: Ortalama Talep ve Onaylanan Ödeme Tutarı (1 Ortalama Metrik)
* **Ortalama Talep Tutarı:** **101.378,64 TL**
* **Onaylanan Talepler İçin Ortalama Ödeme Tutarı:** **80.333,25 TL**
* *Yorum:* Talep başına ortalama hasar maliyeti 101 Bin TL seviyesindedir. Onaylanan dosyalarda talep edilen tutarların ortalama %79,65'i tazmin edilmiş ve dosya başına ortalama 80.333 TL ödeme yapılmıştır.

### Metrik 3: Talep Türüne (Branşa) Göre Finansal Dağılım (Kırılım 1)
Sigorta branşlarına göre dağılım incelendiğinde adet ve maliyet arasında belirgin bir ayrışma görülmektedir:

| Talep Türü | Talep Adedi | Toplam Talep Tutarı (TL) | Ortalama Talep (TL) | Toplam Ödeme (TL) | Tutar Payı (%) |
|:---|:---:|:---:|:---:|:---:|:---:|
| **Hayat** | 27 | 7.081.027,93 | 262.260,29 | 1.223.671,15 | %34,92 |
| **DASK** | 37 | 4.992.318,33 | 134.927,52 | 622.405,90 | %24,62 |
| **Konut** | 34 | 3.289.847,64 | 96.760,22 | 1.050.753,57 | %16,23 |
| **Kasko** | 33 | 2.727.522,83 | 82.652,21 | 777.078,31 | %13,45 |
| **Sağlık** | 43 | 1.172.554,90 | 27.268,72 | 233.335,53 | %5,78 |
| **Trafik** | 26 | 1.012.456,64 | 38.940,64 | 109.418,20 | %4,99 |
| **TOPLAM** | **200** | **20.275.728,27** | **101.378,64** | **4.016.662,66** | **%100,00** |

* *Yorum:* Sağlık sigortası 43 talep (%21,5 adet payı) ile işlem hacminde ilk sırada olmasına karşın, Hayat branşı sadece 27 talep ile toplam portföy tutarının %34,92'sini tek başına oluşturmaktadır. Hayat ve DASK birlikte toplam talebin yaklaşık %60'ını oluşturmaktadır.

### Metrik 4: Dosya Durumuna Göre Dağılım (Kırılım 2)
Taleplerin operasyonel durumlarına göre dağılımı aşağıdaki gibidir:

| Durum | Talep Adedi | Pay (%) | Toplam Talep Tutarı (TL) | Toplam Ödenen Tutar (TL) |
|:---|:---:|:---:|:---:|:---:|
| **Beklemede** | 51 | %25,5 | 6.034.474,81 | 0,00 |
| **Onaylandı** | 50 | %25,0 | 5.042.993,01 | 4.016.662,66 |
| **Reddedildi** | 50 | %25,0 | 4.656.877,93 | 0,00 |
| **İnceleniyor** | 49 | %24,5 | 4.541.382,52 | 0,00 |
| **TOPLAM** | **200** | **%100,0** | **20.275.728,27** | **4.016.662,66** |

* *Yorum:* Taleplerin %25'i onaylanmış, %25'i reddedilmiş ve %50'si (100 adet dosya) henüz sonuçlandırılmamış durumdadır (Beklemede + İnceleniyor). Henüz sonuçlanmamış dosyaların temsil ettiği potansiyel talep yükü 10,58 Milyon TL'dir.

### Metrik 5: Şehirlere Göre En Yüksek Talep Tutarlı Top-3 İl (Top-3 Listesi)
Talebin coğrafi yoğunlaşmasını gösteren ilk 3 il:

| Sıra | Şehir | Talep Adedi | Toplam Talep Tutarı (TL) | Toplamdaki Payı (%) |
|:---:|:---|:---:|:---:|:---:|
| 1 | **Samsun** | 23 | 2.566.340,90 | %12,66 |
| 2 | **Diyarbakır** | 18 | 2.518.595,59 | %12,42 |
| 3 | **İzmir** | 17 | 2.127.152,61 | %10,49 |
| - | **Top-3 Toplamı** | **58** | **7.212.089,10** | **%35,57** |

* *Yorum:* 15 farklı şehir arasında Samsun, Diyarbakır ve İzmir illeri, toplam talep tutarının %35,57'sini (7,21 Milyon TL) oluşturarak risk ve talep tutarının üçte birinden fazlasını çekmektedir. Samsun hem talep sayısı (23 adet) hem de talep tutarı (2,57 Milyon TL) bakımından birinci sıradadır.

---

## 3. Somut Gözlemler (3 Adet)

1. **Gözlem 1 — Portföy Risk Yoğunlaşması (Hayat ve DASK Baskısı):**  
   Adet bazında en çok talep açılan branş Sağlık (43 dosya, ortalama 27.268 TL) iken; şirketin mali riskinin %59,54'ü Hayat (7,08 Milyon TL) ve DASK (4,99 Milyon TL) branşlarında toplanmıştır. Özellikle Hayat branşında dosya başına ortalama talep 262.260 TL olup şirket ortalamasının 2,5 katıdır.

2. **Gözlem 2 — Süreçte Bekleyen Yüksek Mali Yük (Likidite Riski):**  
   İnceleniyor (49 dosya) ve Beklemede (51 dosya) statüsündeki 100 dosya, toplam 10.575.857,33 TL tutar büyüklüğüne sahiptir. Mevcut %25 onaylanma ve %79,65 ödeme/talep karşılama oranı korunduğu takdirde, bu bekleyen dosyalardan yaklaşık 2,1 Milyon TL ödeme çıkması öngörülmektedir.

3. **Gözlem 3 — Bölgesel Yoğunlaşma ve Hasar Odağı:**  
   Metropol şehirlerden ziyade Samsun (2,57 Milyon TL) ve Diyarbakır (2,52 Milyon TL) gibi illerde talep tutarı büyüklüğü dikkat çekmektedir. En yüksek talep tutarına sahip ilk 3 şehir toplam taleplerin üçte birinden fazlasını (%35,57) oluşturmaktadır.

---

## 4. Eylem Önerisi (1 Adet)

* **Eylem Önerisi — Yüksek Tutarlı Dosyalar İçin Hızlı Ekspertiz ve Likidite Karşılığı:**  
  "Beklemede" ve "İnceleniyor" durumundaki 100 dosyanın (%52,16 tutar büyüklüğü) tasfiyesi için öncelikle tutarı 200.000 TL üzeri olan Hayat ve DASK dosyalarına öncelik veren bir **"Hızlı İnceleme Kurulu"** oluşturulmalıdır. Ayrıca onay bekleyen talepler için Finans departmanı tarafından en az **2,2 Milyon TL nakit karşılık (muallak tazminat karşılığı)** ayrılmalı ve ödeme kanallarında Havale/EFT ağırlıklı süreç yönetilmelidir.

---

## 5. Frontend (FE) Görselleştirme İçin Girdiler

FE rolünün (`skills/fe-gorsel/SKILL.md`) üreteceği 2 görsel için önerilen veri eşleşmeleri:
1. **Zaman Serisi Grafiği (Aylık/Yıllık Talep Trendi):** 2023–2025 yılları boyunca aylık talep ve ödeme tutarları değişimi.
2. **Kırılım Grafiği (Branş veya Durum Kırılımı):** 6 talep türünün toplam talep tutarı içindeki payları (Bar veya Pasta Grafik).
