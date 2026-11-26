# Çok Ajanlı Şirket Programı — Öneri ve Roller (Grup D: EMİN SİGORTA)

**Ders:** VBA II (Veri Bilimi ve Analitik) / Güncel Bilişim Teknolojileri II  
**Şirket:** EMİN SİGORTA (Grup D)  
**Tarih:** 2026-11-21 (Son Güncelleme: 2026-11-26)  
**İlgili Duyuru:** Duyuru 10 — Yeni Görev, Çok Ajanlı Şirket Programı  

---

## 1. Senaryo Tanımı

**İş Konusu:** Açık Verilerle Bölgesel Deprem/Afet Risk Analizi ve Dinamik Prim Değerlendirmesi  

EMİN SİGORTA portföyündeki konut, kasko, trafik, DASK ve iş yeri poliçelerinin bölgesel risk primi; AFAD ve Kandilli Rasathanesi'nin canlı deprem verileri ile Meteoroloji Genel Müdürlüğü'nün (MGM) meteorolojik afet uyarılarıyla dinamik olarak yeniden değerlendirilecektir. Sistem, kullanıcıdan gelen talep doğrultusunda üç ajanı sırayla çalıştırarak güncel bir afet risk ve prim analiz raporu üretecektir.

### Üç Ajanın Görev Tanımları:
1. **Ajan 1 (Web Veri Toplayıcı):** AFAD ve Kandilli Rasathanesi'nin açık web kaynaklarından son deprem verilerini ve MGM'den (Meteoroloji Genel Müdürlüğü) il bazlı meteorolojik afet ve fırtına uyarılarını tarayıcı (headless browser) otomasyonu ve HTTP bülten ayrıştırmasıyla toplayarak standart JSON biçimine getirir.
2. **Ajan 2 (Veri İşleme ve Eşleme):** Ajan 1'den gelen bölgesel sismik ve meteorolojik risk verilerini Emin Sigorta'nın il/ilçe bazlı mevcut poliçe veri kümesiyle (`data/policeler.csv`) normalize edilmiş `il_anahtari` üzerinden eşleştirir; her bölge ve poliçe türü için ağırlıklı risk skorunu ve yeni prim katsayısını Python/Pandas ile hesaplar.
3. **Ajan 3 (Denetim ve Nihai Rapor):** Hesaplanan prim ve risk skorlarının mantıksal sınırlarını, veri tutarlılığını ve tarih güncelliğini denetler; eksik veya çelişkili bulgularda işi gerekçesiyle önceki ajana geri yönlendirir, onaylanan verilerden yönetici özet raporunu üretir.

---

## 2. Web Kaynakları Listesi

Duyuru 10 kurallarına uygun olarak seçilen açık kaynaklar ve denetim sonuçları aşağıdadır:

| Kaynak Adı | Adres (URL) | Verilen Veri | Tarayıcı Gerekli mi? | robots.txt & Kullanım Şartları Durumu | Kontrol Tarihi |
|---|---|---|---|---|---|
| **AFAD Son Depremler Portalı** | `https://deprem.afad.gov.tr/last-earthquakes.html` | Tarih, saat, koordinat (enlem/boylam), derinlik, büyüklük (ML/Mw), il/ilçe lokasyonu | **Evet (Tarayıcı Gerekli)**: Sayfa verileri dinamik JavaScript ve asenkron tablolarla render edildiği için Headless Chrome / Playwright ile taranacaktır. | `https://deprem.afad.gov.tr/robots.txt` açıldı; bot erişimini kısıtlayan Disallow satırı bulunmamaktadır. Kullanım Şartları: 4982 sayılı Bilgi Edinme Hakkı Kanunu ve AFAD Açık Veri ilkeleri kapsamında kamu bilgilendirme amaçlı afet verisidir; kişisel veri içermez, akademik ve eğitim odaklı kullanım serbesttir. | 25–26 Kasım 2026 |
| **Kandilli Rasathanesi Sismik Arşiv** | `http://www.koeri.boun.edu.tr/scripts/lst0.asp` | Türkiye ve yakın çevresi gerçek zamanlı deprem kayıtları (tarih, saat, koordinat, derinlik, büyüklük, yer) | **Hayır (HTTP GET)**: Sayfa `curl` / `requests` ile doğrudan çekilebilmekte (HTTP 200) ve düz metin tablosu (ASCII/HTML bülten) olarak ayrıştırılabilmektedir. | `http://www.koeri.boun.edu.tr/robots.txt` açıldı; dosya mevcut değildir (HTTP 404). Kullanım Şartları: Boğaziçi Üniversitesi KRDAE Bölgesel Deprem-Tsunami İzleme ve Değerlendirme Merkezi kamuya açık sismik bültenidir; telif/erişim kısıtı ve kişisel veri bulunmamaktadır, sunucu yükü oluşturmayacak aralıklarla sorgulanacaktır. | 25–26 Kasım 2026 |
| **MGM MeteoUYARI** | `https://www.mgm.gov.tr/Meteouyari/turkiye.aspx` (ve `meteouyari.aspx`) | İl bazlı meteorolojik afet, fırtına, sel ve aşırı yağış risk kodları (Yeşil/Sarı/Turuncu/Kırmızı) | **Evet (Tarayıcı Gerekli)**: Gülbahar Varol tarafından `requests` ile test edildi; HTTP 200 durum kodu döndü ancak yanıtta il uyarı kodları yer almayıp SVG harita ve veriler JavaScript ile asenkron yüklendiğinden doğrudan HTTP GET ile çekilememektedir, tarayıcı (headless browser/Playwright) gereklidir [25 Kasım 2026]. | `https://www.mgm.gov.tr/robots.txt` açıldı; `User-agent: * Allow: /` ve `Disallow: /index.aspx/` yazmaktadır; uyarı ve tahmin sayfalarına erişim engeli bulunmamaktadır. Kullanım Şartları: MGM kamu hizmeti standartları kapsamında hava tahmini ve erken uyarı verisidir, giriş/login veya şifre gerektirmez. | 25–26 Kasım 2026 |

> **Web Verisi İlke Uyumu:** Hiçbir kaynak giriş (login), parola veya captcha gerektirmez. Yalnızca kamuya açık coğrafi/afet verileri toplanacak, hiçbir kullanıcı veya kişisel veri çekilmeyecektir.

---

## 3. Sentetik Veri ve Simülasyon Durumu

Şirketin sentetik poliçe ve simülasyon motoru (`src/simulasyon.py`), örnek veri seti (`data/policeler.csv`) ve veri sözlüğü (`docs/veri-sozlugu.md`) repoya eklenmiş olup çalışır durumdadır:
* **Bölge ve Eşleme Alanları:** Poliçelere 81 il (`il`), ilçe (`ilce`) ve AFAD/MGM verileriyle hatasız `left_join` sağlayan standart `il_anahtari` (Örn: `KAHRAMANMARAS`, `ISTANBUL`) eklenmiştir.
* **Dış Parametre Desteği:** `src/simulasyon.py` betiği komut satırından `--iller`, `--prim-min`, `--prim-max`, `--adet` ve `--tohum` argümanlarını kabul etmektedir (Örn: `python src/simulasyon.py --iller "Kocaeli,Kahramanmaraş,İzmir" --prim-min 3000 --prim-max 15000`).
* **Veri Sözlüğü:** Güncellenen 11 temel alan (`police_id`, `il`, `ilce`, `il_anahtari`, `police_turu`, `teminat_tutari`, `prim_tutari`, `baslangic_tarihi`, `bitis_tarihi`, `bina_yasi`, `deprem_teminati`) `docs/veri-sozlugu.md` dosyasına ayrıntılı açıklamaları, tipleri ve normalizasyon kurallarıyla işlenmiştir.

---

## 4. Rol Dağılımı ve Abonelikler

Duyuru 10 kapsamında ekip üyelerinin rol dağılımı ve abonelik durumu:

| Ad Soyad | Görevdeki Rolü | GitHub Kullanıcı Adı | Sahip Olunan AI Aboneliği | Durum |
|---|---|---|---|---|
| **Gülbahar VAROL** | **Ajan 2 (Veri İşleme ve Eşleme)** | [@gulbaharvarol03-lang](https://github.com/gulbaharvarol03-lang) | **Google Gemini (Advanced / Pro)** | **Kesinleşti** |
| **Eylül ÜSTÜNKAYA** | **Ajan 3 (Denetim ve Nihai Rapor)** | [@ustunkayaeylul72](https://github.com/ustunkayaeylul72) | **Claude Code** | **Kesinleşti** |
| **Mehmet Emin EMEK** | **Ajan 1 (Web Veri Toplayıcı)** | [@emin-emek](https://github.com/emin-emek) | **Google Gemini (Advanced / Pro)** | **Kesinleşti** |
| **Ayşe AYDIN** | **Çekirdek ve Arayüz** | [@ays4ydn](https://github.com/ays4ydn) | **Claude Code** | **Kesinleşti** |
| **Ebru GÖNÜL** | Junior Destek (Web kaynakları araştırması ve robots.txt/şartlar kontrolü) | [@ebruug-nl](https://github.com/ebruug-nl) | **Google Gemini** | **Kesinleşti** |
| **Fatma Nisa ARSLAN** | Junior Destek (Veri sözlüğü ve doğrulama) | [@nisaar-ln](https://github.com/nisaar-ln) | **Google Gemini** | **Kesinleşti** |

---

## 5. Kontrol Listesi Özeti

- [x] Senaryo ve üç ajanın birer cümlelik tanımı yazıldı.
- [x] Web kaynakları listelendi; AFAD ve MGM için tarayıcı (headless browser) gerekliliği belgelendi; robots.txt ve kullanım şartları ayrıntılı kontrol edilip kontrol tarihleriyle tabloya işlendi.
- [x] Simülasyon web kaynaklarıyla eşleşen alanlar (`il_anahtari`, `bina_yasi`, `deprem_teminati`) üretiyor, dışarıdan parametre alabiliyor (`--iller`, `--prim-min`, `--prim-max`); çalışan kod (`src/simulasyon.py`), örnek veri (`data/policeler.csv`) ve güncel sözlük (`docs/veri-sozlugu.md`) repoda mevcut.
- [x] Ekip rolleri ve abonelik durumları kesinleştirilerek güncellendi.
