# Çok Ajanlı Şirket Programı — Öneri ve Roller (Grup D: EMİN SİGORTA)

**Ders:** VBA II (Veri Bilimi ve Analitik) / Güncel Bilişim Teknolojileri II  
**Şirket:** EMİN SİGORTA (Grup D)  
**Tarih:** 2026-11-21  
**İlgili Duyuru:** Duyuru 10 — Yeni Görev, Çok Ajanlı Şirket Programı  

---

## 1. Senaryo Tanımı

**İş Konusu:** Açık Verilerle Bölgesel Deprem/Afet Risk Analizi ve Dinamik Prim Değerlendirmesi  

EMİN SİGORTA portföyündeki konut, kasko ve iş yeri poliçelerinin bölgesel risk primi, Türkiye genelindeki canlı açık afet ve deprem verileriyle dinamik olarak yeniden değerlendirilecektir. Sistem, kullanıcıdan gelen talep doğrultusunda üç ajanı sırayla çalıştırarak güncel bir risk ve prim analiz raporu üretecektir.

### Üç Ajanın Görev Tanımları:
1. **Ajan 1 (Web Veri Toplayıcı):** AFAD ve Kandilli Rasathanesi'nin açık web kaynaklarından son deprem verilerini ve bölgesel sismik hareketlilik parametrelerini tarayıcı (headless browser) otomasyonuyla toplayarak standart JSON biçimine getirir.
2. **Ajan 2 (Veri İşleme ve Eşleme):** Ajan 1'den gelen bölgesel sismik verileri Emin Sigorta'nın il/ilçe bazlı mevcut poliçe veri kümesiyle eşleştirir; her bölge ve poliçe türü için ağırlıklı risk skorunu ve yeni prim katsayısını Python/Pandas ile hesaplar.
3. **Ajan 3 (Denetim ve Nihai Rapor):** Hesaplanan prim ve risk skorlarının mantıksal sınırlarını, veri tutarlılığını ve tarih güncelliğini denetler; eksik veya çelişkili bulgularda işi gerekçesiyle önceki ajana geri yönlendirir, onaylanan verilerden yönetici özet raporunu üretir.

---

## 2. Web Kaynakları Listesi

Duyuru 10 kurallarına uygun olarak seçilen açık kaynaklar ve denetim sonuçları aşağıdadır:

| Kaynak Adı | Adres (URL) | Verilen Veri | Tarayıcı Gerekli mi? | robots.txt & Kullanım Şartları Durumu |
|---|---|---|---|---|
| **AFAD Son Depremler Portalı** | `https://deprem.afad.gov.tr/last-earthquakes.html` | Tarih, saat, koordinat (enlem/boylam), derinlik, büyüklük (ML/Mw), il/ilçe lokasyonu | **Evet (Tarayıcı Gerekli)**: Sayfa verileri dinamik JavaScript ve asenkron tablolarla render edildiği için Headless Chrome / Playwright ile taranacaktır. | Kamuya açık afet izleme verisidir. Otomasyon için `robots.txt` kısıtlaması bulunmamaktadır. İstekler arasına 2 saniyelik bekleme konularak sunucu yükü önlenecektir. |
| **Kandilli Rasathanesi Sismik Arşiv** | `http://www.koeri.boun.edu.tr/scripts/lst9.asp` | Türkiye ve yakın çevresi gerçek zamanlı deprem kayıtları | Hayır (HTTP GET ile metin ayrıştırma) | Açık bilimsel bülten verisidir. Kişisel veri içermez. Saygı sınırları çerçevesinde periyodik çekim yapılacaktır. |
| **MGM MeteoUYARI** | `https://www.mgm.gov.tr/tahmin/meteouyari.aspx` | İl bazlı fırtına, sel ve aşırı yağış risk kodları (Sarı/Turuncu/Kırmızı) | **Evet (Tarayıcı Gerekli)**: Basit HTTP sayfa isteğiyle (requests) test edildi; sayfa interaktif SVG harita ve asenkron JavaScript ile çalıştığı için il uyarı kodları doğrudan ayrıştırılamıyor, tarayıcı (headless browser/Playwright) gereklidir. | Kamuya açık resmi uyarı sistemidir. robots.txt kontrolü yapıldı (`User-agent: * Allow: /`), genel botlar için erişim engeli bulunmamaktadır. |

> **Web Verisi İlke Uyumu:** Hiçbir kaynak giriş (login), parola veya captcha gerektirmez. Yalnızca kamuya açık coğrafi/afet verileri toplanacak, hiçbir kullanıcı veya kişisel veri çekilmeyecektir.

---

## 3. Sentetik Veri ve Simülasyon Genişletme Planı

Şirketin mevcut `data/talepler-odemeler.csv` veri modeli ve `src/veri-uret.py` sentetik veri motoru aşağıdaki şekilde genişletilecektir:
* **Bölge Alanları:** Poliçelere 81 il ve ilçe kodları eklenecektir. Böylece AFAD/Kandilli'den gelen il/ilçe verileriyle `left_join` yapılabilecektir.
* **Dış Parametre Desteği:** `veri-uret.py` betiği komut satırından `--iller` veya `--risk-araligi` argümanlarını kabul edecek şekilde güncellenecektir (Örn: `python src/veri-uret.py --iller "Kocaeli,Kahramanmaraş,İzmir"`).
* **Veri Sözlüğü:** Güncellenen alanlar (bina yaşı, poliçe bedeli, deprem teminatı vb.) `docs/veri-sozlugu.md` dosyasına işlenecektir.

---

## 4. Rol Dağılımı ve Abonelikler

Duyuru 10 kapsamında ekip üyelerinin rol dağılımı ve abonelik durumu:

| Ad Soyad | Görevdeki Rolü | GitHub Kullanıcı Adı | Sahip Olunan AI Aboneliği | Durum |
|---|---|---|---|---|
| **Gülbahar VAROL** | Ajan 2 (Veri İşleme ve Eşleme)| [@gulbaharvarol03-lang](https://github.com/gulbaharvarol03-lang) | **Google Gemini (Advanced / Pro)** | **Kesinleşti** |
| **Eylül ÜSTÜNKAYA** | Ajan 3 (Denetim ve Nihai Rapor)| [@ustunkayaeylul72](https://github.com/ustunkayaeylul72) | **Claude Code** | **Kesinleşti** |
| **Mehmet Emin EMEK** | Ajan 1 (Web Veri Toplayıcı)| [@emin-emek](https://github.com/emin-emek)  | **Google Gemini (Advanced / Pro)** | **Kesinleşti** |
| **Ayşe AYDIN** |  Çekirdek ve Arayüz | [@ays4ydn](https://github.com/ays4ydn) | **Claude Code** | **Kesinleşti** |
| **Ebru GÖNÜL** | Junior Destek ( web kaynakları araştırması ve robots.txt/şartlar konrtolü) | [@ebruug-nl](https://github.com/ebruug-nl)  | **Google Gemini** | **Kesinleşti** |
| **Fatma Nisa ARSLAN** | Junior Destek (Veri sözlüğü) | [@nisaar-ln](https://github.com/nisaar-ln)  | **Google Gemini** | **Kesinleşti** |

---

## 5. Kontrol Listesi Özeti

- [x] Senaryo ve üç ajanın birer cümlelik tanımı yazıldı.
- [x] Web kaynakları listelendi; en az biri tarayıcı (headless browser) gerektiriyor; robots.txt ve kullanım şartları kontrol edildi.
- [x] Sentetik veri simülasyonunun web kaynaklarıyla eşleşme planı hazırlandı.
- [x] Gülbahar Varol için Ajan 2 ve Gemini Advanced aboneliği bildirildi; diğer roller ekip görüşmesine bırakıldı.
