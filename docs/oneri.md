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
| **MGM / AFAD Meteorolojik Uyarılar** | `https://www.mgm.gov.tr/tahmin/uyari-goster.aspx` | İl bazlı fırtına, sel ve aşırı yağış risk kodları (Sarı/Turuncu/Kırmızı) | **Evet (Tarayıcı Gerekli)**: İnteraktif harita ve uyarı panellerinin okunması için tarayıcı gereklidir. | Kamuya açık resmi uyarı sistemidir. Ticari olmayan eğitim/araştırma kapsamında taranacaktır. |

> **Web Verisi İlke Uyumu:** Hiçbir kaynak giriş (login), parola veya captcha gerektirmez. Yalnızca kamuya açık coğrafi/afet verileri toplanacak, hiçbir kullanıcı veya kişisel veri çekilmeyecektir.

---

## 3. Sentetik Veri ve Simülasyon Genişletme Planı

Şirketin mevcut `data/talepler-odemeler.csv` veri modeli ve `src/veri-uret.py` sentetik veri motoru aşağıdaki şekilde genişletilecektir:
* **Bölge Alanları:** Poliçelere 81 il ve ilçe kodları eklenecektir. Böylece AFAD/Kandilli'den gelen il/ilçe verileriyle `left_join` yapılabilecektir.
* **Dış Parametre Desteği:** `veri-uret.py` betiği komut satırından `--iller` veya `--risk-araligi` argümanlarını kabul edecek şekilde güncellenecektir (Örn: `python src/veri-uret.py --iller "Kocaeli,Kahramanmaraş,İzmir"`).
* **Veri Sözlüğü:** Güncellenen alanlar (bina yaşı, poliçe bedeli, deprem teminatı vb.) `docs/veri-sozlugu.md` dosyasına işlenecektir.

---

## 4. Rol Dağılımı ve Abonelikler

Duyuru 10 kapsamında önerilen rol dağılımı ve üyelerin yapay zekâ abonelikleri:

| Ad Soyad | Görevdeki Rolü | GitHub Kullanıcı Adı | Sahip Olunan AI Aboneliği |
|---|---|---|---|
| **Eylül ÜSTÜNKAYA** | **Çekirdek ve Arayüz (Core & UI)** | [@ustunkayaeylul72](https://github.com/ustunkayaeylul72) | Vibe / Claude Code *(Ekip lideri koordinasyonu)* |
| **Mehmet Emin EMEK** | **Ajan 1 (Web Veri Toplayıcı)** | [@emin-emek](https://github.com/emin-emek) | ChatGPT Plus / Vibe *(Veri hattı ve tarayıcı kazıma)* |
| **Gülbahar VAROL** | **Ajan 2 (Veri İşleme ve Eşleme)** | [@gulbaharvarol03-lang](https://github.com/gulbaharvarol03-lang) | **Google Gemini (Advanced / Pro)** |
| **Ayşe AYDIN** | **Ajan 3 (Denetim ve Nihai Rapor)** | [@ays4ydn](https://github.com/ays4ydn) | Vibe / Claude *(Kalite kontrol ve geri besleme)* |
| **Ebru GÖNÜL** | **Junior Destek (Arayüz & Test)** | [@ebruug-nl](https://github.com/ebruug-nl) | ChatGPT / Açık Modeller |
| **Fatma Nisa ARSLAN** | **Junior Destek (Arayüz & Test)** | [@nisaar-ln](https://github.com/nisaar-ln) | ChatGPT / Açık Modeller |

---

## 5. Kontrol Listesi Özeti

- [x] Senaryo ve üç ajanın birer cümlelik tanımı yazıldı.
- [x] Web kaynakları listelendi; en az biri tarayıcı (headless browser) gerektiriyor; robots.txt ve kullanım şartları kontrol edildi.
- [x] Sentetik veri simülasyonunun web kaynaklarıyla eşleşme planı hazırlandı.
- [x] Rol listesi ve abonelikler belirlendi (Gülbahar Varol: Ajan 2, Gemini Advanced).
