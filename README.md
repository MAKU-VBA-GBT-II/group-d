# EMİN SİGORTA — Grup D

VBA II (Veri Bilimi ve Analitik) dersi kapsamındaki **veri şirketi simülasyonu** çalışma deposu.

## Şirket

| Alan | Değer |
|---|---|
| Şirket adı | EMİN SİGORTA |
| Sektör | Sigorta |
| Teknoloji kararı | Dil: Python · Kütüphaneler: pandas, numpy, matplotlib, seaborn, Faker · Görselleştirme: PNG |

> Teknoloji serbesttir; karar Hafta 1'de şirketçe verilip buraya yazılır.

## Üyeler

Kendi satırınızı başlangıç rolünüzle ekleyin. Lider `PM`'dir; diğer üç üye PM'nin işe alımıyla başlangıç rollerine yerleştirilir. Roller Görev 1–3 boyunca dönem planı §1.3'e göre döner:

- Eylül ÜSTÜNKAYA — PM (lider) [@ustunkayaeylul72](https://github.com/ustunkayaeylul72)
- Mehmet Emin EMEK — BE (başlangıç rolü) [@emin-emek](https://github.com/emin-emek)
- Gülbahar VAROL — FE (başlangıç rolü) [@gulbaharvarol03-lang](https://github.com/gulbaharvarol03-lang)
- Ayşe AYDIN — DQ (başlangıç rolü, veri analisti ve kalite) [@ays4ydn](https://github.com/ays4ydn)
- Ebru GÖNÜL — Junior Veri Analisti [@ebruug-nl](https://github.com/ebruug-nl)
- Fatma Nisa ARSLAN — Junior Veri Analisti [@nisaar-ln](https://github.com/nisaar-ln)

## Klasör Yapısı

| Yol | Amaç |
|---|---|
| `src/` | Kod: simülasyon, analiz ve görselleştirme betikleri |
| `data/` | Üretilen veri dosyaları (`.csv`, `.json`) |
| `visuals/` | Dışa aktarılmış grafikler (`.png`) |
| `docs/` | `veri-sozlugu-g1.md`, `analiz-g1.md`, `requirements.md` |
| `tests/` | `test-cases.md`, `test-log.md`, `test_veri_kalitesi.py` |
| `reports/` | Haftalık sprint raporları (`report-wXX.md`) |
| `skills/` | Ajan becerileri ve talimat paketleri (`SKILL.md`) |
| `exchange/` | Görev 3 veri değişimi (`output.csv`) |

## Hızlı Başlangıç & Çalıştırma Talimatları

### 1. Sentetik Veri Üretimi (BE)
```bash
python src/veri-uret.py
```
*`docs/veri-sozlugu-g1.md` şemasına uygun 200 satırlık sigorta talep ve ödeme veri kümesini (`data/talepler-odemeler.csv`) üretir.*

### 2. Veri Analizi ve Metrik Hesaplama (DQ)
```bash
python src/analiz.py
```
*Tüm temel metrikleri, 36 aylık ve 12 çeyreklik zaman serisi trendini ve branş kırılımlarını hesaplar; bulguları konsola ve rapora döker.*

### 3. Veri Görselleştirme ve Grafik Üretimi (FE)
```bash
python src/gorsellestir.py
```
*Zaman serisi (`visuals/ceyreklik-trend.png`) ve branş kırılımı (`visuals/talep-turu-kirilimi.png`) grafiklerini 300 DPI yüksek çözünürlükte üretir.*

### 4. Otomatik Veri Kalitesi Testlerini Koşma (DQ)
```bash
python tests/test_veri_kalitesi.py
```
*`tests/test-cases.md` dosyasında tanımlanan 7 veri kalitesi senaryosunu programatik olarak sınar ve CI uyumunu doğrular.*
