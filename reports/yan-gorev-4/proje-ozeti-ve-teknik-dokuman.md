# Yan Görev 4 — Proje Başvurusu ve Teknik Çalışma Raporu

**Öğrenci:** Eylül Üstünkaya (`ustunkayaeylul72`)  
**Grup:** Grup D (`MAKU-VBA-GBT-II/group-d`)  
**Tarih:** 25 Kasım 2026  

---

## 1. Resmi Proje Başvurusu (`AI-TECH-513`)

* **Program Adı:** 100. Yıla 100 Yapay Zekâ Proje Fikri
* **Başvuru Numarası:** `AI-TECH-513`
* **Başvuru Tarihi:** 24.11.2026
* **Durum:** Açık / Başvuru Tamamlandı
* **Başvuru Ekran Görüntüsü:** Eklendi
---

## 2. Proje Başvuru İçeriği ve Özeti

**Proje Başlığı:** Döngüsel Ekonomi Yaklaşımıyla Biyogaz Tesisi Yer Seçimi ve Atık Lojistiği Optimizasyonu: Burdur İli Örneği

### Amaç ve Kapsam
Burdur ilinde hayvancılıktan kaynaklanan yüksek miktardaki büyükbaş hayvan atığının Burdur Gölü Havzası'nda oluşturduğu nitrat kirliliği ve sera gazı emisyonu sorununa çözüm üretmek amacıyla, hayvansal atıkların tesise toplanması ile üretilen fermente organik gübrenin tarım arazilerine dağıtımını çift yönlü optimize eden Python tabanlı bir mekansal karar destek modeli geliştirilmektedir.

### Temel Hipotezler ve Metodoloji (6 Aşamalı İş Akışı)
1. **Veri Toplama ve Ön İşleme:** TÜİK ilçe bazlı hayvan varlığı istatistikleri, OpenStreetMap (OSM) karayolu ağı/yerleşim sınırları, Copernicus CORINE arazi örtüsü ve NASA SRTM yükseklik (DEM) verileri Pandas ve GeoPandas ile birleştirilerek teorik enerji ve gübre potansiyeli hesaplanır.
2. **Mekansal Kısıt Analizi (Eleme):** Rasterio ve Shapely kullanılarak mutlak koruma alanları (Ramsar vb.), göl kıyısına 2 km tampon bölge, yerleşim yerlerine 1 km tampon bölge ve %10 üzeri eğimli araziler elenerek uygun aday alanlar haritalanır.
3. **Kümeleme ve Ağ Analizi:** Uygun alanlar üzerinde Scikit-learn ile Ağırlıklı K-Means kümeleme uygulanır; OSMnx ve NetworkX (Dijkstra) kütüphaneleri ile gerçek karayolu mesafeleri ve ton-km taşıma maliyetleri hesaplanır.
4. **Çok Kriterli Karar Verme (AHP-TOPSIS):** Aday sahalar enerji potansiyeli, toplama/dağıtım maliyeti, elektrik iletim hattına ve tarım arazilerine yakınlık kriterlerine göre puanlanır.
5. **Karşılaştırmalı Performans Değerlendirmesi:** İlçe ağırlıklı geometrik merkez (baseline) senaryosuna kıyasla atık toplama maliyetinde (ton-km) en az %20, fermente gübre dağıtım mesafesinde (km) en az %15 iyileşme test edilir.
6. **Gerçek Saha Doğrulaması (Model Validasyonu):** Burdur ilinde halihazırda faaliyette olan 1,5 MW kurulu güce sahip mevcut biyogaz tesisinin coğrafi konumu doğrulama noktası (ground-truth) olarak kullanılarak modelin sahadaki geçerliliği test edilir.

---

## 3. Hazırlanan Teknik Çalışma Dosyaları ve Veri Pipeline'ı

Proje hazırlık sürecinde, Burdur ili özelinde gerçek coğrafi katmanların elde edilmesi ve ön işlenmesi için açık kaynaklı veri setleri indirilmiş ve Python veri toplama betiği geliştirilmiştir:

* **Kaynak Python Betiği:** [`01_osm_ve_veri_cekme.py`](./01_osm_ve_veri_cekme.py)
* **Temin Edilen Veri Katmanları ve İşlemler:**
  * **OpenStreetMap / Geofabrik & OSMnx:** Türkiye resmi veri tabanından çekilen gerçek karayolu ağı, yerleşim yerleri, su kütleleri ve koruma alanları `geopandas` (`gpd.clip(gdf, burdur_il)`) kullanılarak Burdur il sınırına göre kırpılmıştır.
  * **Copernicus CORINE & OpenTopography (SRTM):** Arazi örtüsü ve topografik eğim kısıt analizleri için indirilen harici uydu ve yükseklik veri setleri.
