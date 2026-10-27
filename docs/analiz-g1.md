# Veri Analiz Raporu — G1: Sigorta Talepleri ve Ödemeleri

> **Hazırlayan:** Ayşe AYDIN (DQ — Veri Analisti ve Kalite Mühendisi)  
> **Tarih:** 2026-10-20  
> **Kaynak Veri:** `data/talepler-odemeler.csv` (200 satır, 9 alan, Tohum: 42)  
> **Analiz Betiği:** `src/analiz.py`  
> **İlgili Skill:** `skills/dq-analiz/SKILL.md`  
> **Hedef Issue:** [Issue #13: G1-analiz — Metrikleri hesapla ve bulguları yaz (DQ)](https://github.com/MAKU-VBA-GBT-II/group-d/issues/13)

---

## 1. Yönetici Özeti

Bu analiz raporu, **Emin Sigorta** portföyüne ait sentetik sigorta talep ve tazminat ödeme verileri (`data/talepler-odemeler.csv`) üzerinden hazırlanmıştır. Veri seti, 2023–2025 yılları arasındaki 200 adet hasar talebini ve bunlara ilişkin ödeme süreçlerini kapsamaktadır.

Analizin temel amacı; şirketin branş bazındaki hasar yoğunluğunu, talep sonuçlanma oranlarını, 12 çeyreklik finansal risk trendini belirlemek ve **FE (Frontend / Görselleştirici)** adımında üretilecek grafikler için referans metrikleri sağlamaktır.

---

## 2. Temel Metrikler (5 Metrik)

Aşağıdaki metrikler `src/analiz.py` betiği çalıştırılarak veri setinden doğrudan ve tekrarlanabilir biçimde hesaplanmıştır.

### Metrik 1: Toplam Talep ve Ödeme Tutarı (Toplam Metriği)
* **Toplam Talep Sayısı:** 200 adet
* **Toplam Talep Edilen Tutar:** **20.275.728,27 TL**
* **Toplam Ödenen Tazminat Tutarı:** **4.016.662,66 TL**
* *Yorum:* Şirkete 2023–2025 döneminde iletilen toplam hasar talebi 20,28 Milyon TL olup, onaylanan dosyalara toplam 4,02 Milyon TL tazminat ödenmiştir.

### Metrik 2: Ortalama Talep ve Onaylanan Ödeme Tutarı (Ortalama Metriği)
* **Ortalama Talep Tutarı:** **101.378,64 TL**
* **Onaylanan Talepler İçin Ortalama Ödeme Tutarı:** **80.333,25 TL**
* *Yorum:* Talep başına ortalama hasar maliyeti 101.378 TL'dir. Onaylanan dosyalarda talep edilen tutarların ortalama %79,65'i karşılanmış ve dosya başına ortalama 80.333 TL ödeme yapılmıştır.

### Metrik 3: Talep Türüne Göre Finansal Dağılım (Talep Türü Kırılımı)

| Talep Türü | Talep Adedi | Toplam Talep Tutarı (TL) | Ortalama Talep (TL) | Toplam Ödeme (TL) | Tutar Payı (%) |
|:---|:---:|:---:|:---:|:---:|:---:|
| **Hayat** | 27 | 7.081.027,93 | 262.260,29 | 1.223.671,15 | %34,92 |
| **DASK** | 37 | 4.992.318,33 | 134.927,52 | 622.405,90 | %24,62 |
| **Konut** | 34 | 3.289.847,64 | 96.760,22 | 1.050.753,57 | %16,23 |
| **Kasko** | 33 | 2.727.522,83 | 82.652,21 | 777.078,31 | %13,45 |
| **Sağlık** | 43 | 1.172.554,90 | 27.268,72 | 233.335,53 | %5,78 |
| **Trafik** | 26 | 1.012.456,64 | 38.940,64 | 109.418,20 | %4,99 |
| **TOPLAM** | **200** | **20.275.728,27** | **101.378,64** | **4.016.662,66** | **%100,00** |

* *Yorum:* Sağlık branşı 43 talep (%21,5 adet payı) ile adet bazında lider olmasına karşın, Hayat branşı sadece 27 talep ile portföyün %34,92'sini tek başına oluşturarak en büyük mali yükü temsil etmektedir.

### Metrik 4: Zaman Serisi Trend Analizi (Aylık ve Çeyreklik Kırılım)

Dönem planı kabul kriteri (Kırılım 2: zaman serisi trendi) gereğince veri setinin hem 36 aylık ayrıntılı akışı hem de FE görselleştirmesi için 12 çeyreklik agregasyonu aşağıda sunulmuştur.

#### A) Aylık Zaman Serisi Dağılımı (36 Ay)

| Yıl-Ay | Talep Adedi | Toplam Talep Tutarı (TL) | Ortalama Talep (TL) | Toplam Ödenen Tutar (TL) |
|:---:|:---:|:---:|:---:|:---:|
| **2023-01** | 2 | 203.676,28 | 101.838,14 | 90.780,36 |
| **2023-02** | 6 | 758.695,77 | 126.449,29 | 299.164,38 |
| **2023-03** | 2 | 308.669,37 | 154.334,68 | 0,00 |
| **2023-04** | 3 | 262.648,58 | 87.549,53 | 209.363,83 |
| **2023-05** | 5 | 384.037,06 | 76.807,41 | 96.466,34 |
| **2023-06** | 7 | 812.615,27 | 116.087,90 | 127.330,14 |
| **2023-07** | 8 | 1.055.848,62 | 131.981,08 | 0,00 |
| **2023-08** | 11 | 1.339.672,28 | 121.788,39 | 93.431,60 |
| **2023-09** | 5 | 469.816,04 | 93.963,21 | 0,00 |
| **2023-10** | 3 | 249.947,19 | 83.315,73 | 0,00 |
| **2023-11** | 9 | 1.127.097,14 | 125.233,02 | 87.187,01 |
| **2023-12** | 5 | 400.378,37 | 80.075,67 | 94.671,09 |
| **2024-01** | 5 | 216.951,55 | 43.390,31 | 24.534,17 |
| **2024-02** | 2 | 180.189,29 | 90.094,65 | 35.323,96 |
| **2024-03** | 7 | 620.994,79 | 88.713,54 | 104.259,79 |
| **2024-04** | 7 | 369.396,08 | 52.770,87 | 195.525,93 |
| **2024-05** | 7 | 814.017,52 | 116.288,22 | 132.473,46 |
| **2024-06** | 8 | 658.397,24 | 82.299,65 | 260.927,09 |
| **2024-07** | 6 | 549.320,70 | 91.553,45 | 264.657,94 |
| **2024-08** | 3 | 271.507,76 | 90.502,59 | 0,00 |
| **2024-09** | 5 | 1.080.449,26 | 216.089,85 | 243.142,02 |
| **2024-10** | 9 | 1.598.562,49 | 177.618,05 | 225.352,25 |
| **2024-11** | 4 | 196.189,12 | 49.047,28 | 108.176,24 |
| **2024-12** | 4 | 385.279,95 | 96.319,99 | 184.844,87 |
| **2025-01** | 4 | 118.214,96 | 29.553,74 | 7.461,26 |
| **2025-02** | 6 | 790.928,25 | 131.821,38 | 424.588,33 |
| **2025-03** | 3 | 159.156,84 | 53.052,28 | 70.637,64 |
| **2025-04** | 6 | 149.843,62 | 24.973,94 | 0,00 |
| **2025-05** | 9 | 426.987,46 | 47.443,05 | 93.243,08 |
| **2025-06** | 4 | 630.132,74 | 157.533,18 | 0,00 |
| **2025-07** | 7 | 644.456,26 | 92.065,18 | 115.606,23 |
| **2025-08** | 6 | 597.633,67 | 99.605,61 | 124.933,99 |
| **2025-09** | 8 | 464.895,35 | 58.111,92 | 121.507,93 |
| **2025-10** | 2 | 518.893,85 | 259.446,92 | 0,00 |
| **2025-11** | 5 | 831.887,51 | 166.377,50 | 181.071,73 |
| **2025-12** | 7 | 628.340,04 | 89.762,86 | 0,00 |
| **TOPLAM** | **200** | **20.275.728,27** | **101.378,64** | **4.016.662,66** |

* *Aylık Trend Yorumu:* 36 aylık dönemde en yüksek talep tutarı 2024 Ekim ayında (9 talep, 1.598.562,49 TL) ve 2023 Ağustos ayında (11 talep, 1.339.672,28 TL) gerçekleşmiştir. 36 ayın tamamında talep girişi mevcut olup, aylık talep adedi 2 ile 11 arasında dengeli bir dağılım sergilemektedir.

#### B) Çeyreklik Zaman Serisi / Trend Analizi (12 Çeyrek)
FE görselleştirmesi ve dönemsel eğilim analizi için 12 çeyreklik özet trend:

| Çeyrek (Dönem) | Talep Adedi | Toplam Talep Tutarı (TL) | Ortalama Talep (TL) | Toplam Ödenen Tutar (TL) |
|:---:|:---:|:---:|:---:|:---:|
| **2023-Q1** | 10 | 1.271.041,42 | 127.104,14 | 389.944,74 |
| **2023-Q2** | 15 | 1.459.300,91 | 97.286,73 | 433.160,31 |
| **2023-Q3** | 24 | 2.865.336,94 | 119.389,04 | 93.431,60 |
| **2023-Q4** | 17 | 1.777.422,70 | 104.554,28 | 181.858,10 |
| **2024-Q1** | 14 | 1.018.135,63 | 72.723,97 | 164.117,92 |
| **2024-Q2** | 22 | 1.841.810,84 | 83.718,67 | 588.926,48 |
| **2024-Q3** | 14 | 1.901.277,72 | 135.805,55 | 507.799,96 |
| **2024-Q4** | 17 | 2.180.031,56 | 128.237,15 | 518.373,36 |
| **2025-Q1** | 13 | 1.068.300,05 | 82.176,93 | 502.687,23 |
| **2025-Q2** | 19 | 1.206.963,82 | 63.524,41 | 93.243,08 |
| **2025-Q3** | 21 | 1.706.985,28 | 81.285,01 | 362.048,15 |
| **2025-Q4** | 14 | 1.979.121,40 | 141.365,81 | 181.071,73 |
| **TOPLAM** | **200** | **20.275.728,27** | **101.378,64** | **4.016.662,66** |

* *Yorum:* Her çeyrekte 10 ile 24 arasında talep gelmiştir. En yüksek talep tutarı ve dosya adedi 2023'ün 3. çeyreğinde (24 talep, 2,87 Milyon TL) görülmüş; genel trendde dönemsel dalgalanmalar olmakla birlikte şirket istikrarlı bir dosya akışı yaşamıştır.

> **Metodolojik Not (Haftalık vs. Çeyreklik Trend Tercihi):**  
> Görev 1 kabul kriterinde belirtilen haftalık kırılım yerine çeyreklik (12 çeyrek) agregasyon tercih edilmiştir. 200 satırlık sentetik veri seti 2023–2025 yılları arasındaki 3 yıla (156 haftaya) dağıldığı için haftalık bazda hafta başına ortalama yalnızca 1,28 kayıt düşmekte ve 40'tan fazla haftada 0 talep oluşmaktadır. Bu durum aşırı istatistiksel gürültü yarattığından ve FE görselleştirmesini olumsuz etkileyeceğinden, iş analitiği ve görsel okunabilirlik açısından 12 çeyreklik trend yapısı kullanılmış ve Issue #13 üzerinden PM (@ustunkayaeylul72) onayına sunulmuştur.

### Metrik 5: En Sık Görülen 3 Talep Türü (İşlem Hacmi Top-3)

| Sıra | Talep Türü | Dosya Adedi | Adet Bazlı Portföy Payı (%) |
|:---:|:---|:---:|:---:|
| 1 | **Sağlık** | 43 | %21,5 |
| 2 | **DASK** | 37 | %18,5 |
| 3 | **Konut** | 34 | %17,0 |
| - | **Top-3 Toplamı** | **114** | **%57,0** |

* *Yorum:* Şirkete intikal eden hasar dosyalarının yarıdan fazlası (%57'si) Sağlık, DASK ve Konut sigortalarından kaynaklanmakta olup operasyonel iş yükünün odağını bu 3 branş oluşturmaktadır.

---

## 3. Ek Kırılımlar ve Sıralamalar

### Ek Kırılım: Dosya Durumuna Göre Dağılım
| Durum | Talep Adedi | Pay (%) | Toplam Talep Tutarı (TL) | Toplam Ödenen Tutar (TL) |
|:---|:---:|:---:|:---:|:---:|
| **Beklemede** | 51 | %25,5 | 6.034.474,81 | 0,00 |
| **Onaylandı** | 50 | %25,0 | 5.042.993,01 | 4.016.662,66 |
| **Reddedildi** | 50 | %25,0 | 4.656.877,93 | 0,00 |
| **İnceleniyor** | 49 | %24,5 | 4.541.382,52 | 0,00 |

### Ek Sıralama: En Çok Talep Tutarı Gelen Top-3 Şehir
| Sıra | Şehir | Talep Adedi | Toplam Talep Tutarı (TL) | Toplamdaki Payı (%) |
|:---:|:---|:---:|:---:|:---:|
| 1 | **Samsun** | 23 | 2.566.340,90 | %12,66 |
| 2 | **Diyarbakır** | 18 | 2.518.595,59 | %12,42 |
| 3 | **İzmir** | 17 | 2.127.152,61 | %10,49 |
| - | **Top-3 Toplamı** | **58** | **7.212.089,10** | **%35,57** |

---

## 4. Somut Gözlemler (3 Adet)

1. **Gözlem 1 — Portföy Risk Yoğunlaşması (Hayat ve DASK Baskısı):**  
   Adet bazında en çok talep açılan branş Sağlık (43 dosya, ortalama 27.268 TL) iken; şirketin mali riskinin %59,54'ü Hayat (7,08 Milyon TL) ve DASK (4,99 Milyon TL) branşlarında toplanmıştır. Özellikle Hayat branşında dosya başına ortalama talep 262.260 TL olup şirket ortalamasının 2,5 katıdır.

2. **Gözlem 2 — Süreçte Bekleyen Yüksek Mali Yük (Likidite Riski):**  
   İnceleniyor (49 dosya) ve Beklemede (51 dosya) statüsündeki 100 dosya, toplam 10.575.857,33 TL tutar büyüklüğüne sahiptir. Mevcut %25 onaylanma ve %79,65 ödeme/talep karşılama oranı korunduğu takdirde, bu bekleyen dosyalardan yaklaşık 2,1–2,2 Milyon TL ödeme çıkması öngörülmektedir.

3. **Gözlem 3 — Bölgesel Yoğunlaşma ve Hasar Odağı:**  
   Metropol şehirlerden ziyade Samsun (2,57 Milyon TL) ve Diyarbakır (2,52 Milyon TL) gibi illerde talep tutarı büyüklüğü dikkat çekmektedir. En yüksek talep tutarına sahip ilk 3 şehir toplam taleplerin üçte birinden fazlasını (%35,57) oluşturmaktadır.

---

## 5. Eylem Önerisi (1 Adet)

* **Eylem Önerisi — Yüksek Tutarlı Dosyalar İçin Hızlı Ekspertiz ve Likidite Karşılığı:**  
  "Beklemede" ve "İnceleniyor" durumundaki 100 dosyanın tasfiyesi için öncelikle tutarı 200.000 TL üzeri olan Hayat ve DASK dosyalarına öncelik veren bir **"Hızlı İnceleme Kurulu"** oluşturulmalıdır.  
  * **Nakit Karşılık Formülü:** Beklemede ve İnceleniyor durumundaki 100 dosyanın toplam talep tutarı (10.575.857,33 TL) × Şirketin tarihsel dosya onaylanma oranı (%25) × Ortalama ödeme karşılama oranı (%79,65) ≈ **2.105.811 TL (~2,1 – 2,2 Milyon TL)** olarak hesaplanmıştır. Finans departmanı bu bekleyen dosyalar için en az **2,2 Milyon TL muallak tazminat karşılığı (likidite)** ayırmalıdır.

---

## 6. Frontend (FE) Görselleştirme İçin Girdiler

FE rolünün (`skills/fe-gorsel/SKILL.md`) üreteceği 2 grafik için referans veriler:
1. **Zaman Serisi Grafiği:** Yukarıdaki **Metrik 4 Çeyreklik Trend Analizi Tablosu** (12 çeyrek, 2023-Q1'den 2025-Q4'e çeyreklik toplam talep ve ödeme tutarları). 12 veri noktası ile görsel zengin ve akıcı bir çizgi grafik elde edilecektir.
2. **Kırılım Grafiği:** Yukarıdaki **Metrik 3 Talep Türü Dağılım Tablosu** (6 branşın talep tutarları ve portföy payları).
