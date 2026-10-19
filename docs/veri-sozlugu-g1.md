# Veri Sözlüğü — G1: Sigorta Talepleri ve Ödemeleri

> **Dosya:** `data/talepler-odemeler.csv`
> **Kodlama:** UTF-8 (BOM)
> **Ayırıcı:** Virgül (`,`)
> **Satır sayısı:** 200 (başlık hariç)
> **Üretici betik:** `src/veri-uret.py` (tohum: `42`)

---

## Alan Tanımları

| # | Alan Adı | Veri Tipi | Açıklama | Örnek Değer | Boş Olabilir? |
|---|----------|-----------|----------|-------------|----------------|
| 1 | `talep_id` | `string` | Benzersiz talep kimliği. `TLP-XXXXX` formatında. | `TLP-00001` | Hayır |
| 2 | `talep_tarihi` | `date (YYYY-MM-DD)` | Talebin oluşturulduğu tarih. 2023-01-01 — 2025-12-31 aralığı. | `2023-02-21` | Hayır |
| 3 | `talep_turu` | `string (categorical)` | Sigorta branşı / talep türü. | `Kasko` | Hayır |
| 4 | `sehir` | `string (categorical)` | Talebin açıldığı il. | `İstanbul` | Hayır |
| 5 | `talep_tutari` | `float` | Talep edilen hasar/tazminat tutarı (TL). | `373359.74` | Hayır |
| 6 | `durum` | `string (categorical)` | Talebin güncel durumu. | `Onaylandı` | Hayır |
| 7 | `odeme_tutari` | `float` | Sigorta şirketince ödenen tutar (TL). Reddedilen/bekleyen talepler için `0.0`. | `260588.95` | Hayır |
| 8 | `odeme_tarihi` | `date (YYYY-MM-DD)` | Ödemenin gerçekleştiği tarih. | `2023-03-15` | Evet* |
| 9 | `odeme_yontemi` | `string (categorical)` | Ödeme kanalı. | `Havale/EFT` | Evet* |

> **\*** `odeme_tarihi` ve `odeme_yontemi` yalnızca `durum = "Onaylandı"` olan kayıtlarda doldurulur; diğer durumlarda boş bırakılır.

---

## Kategorik Değerler

### `talep_turu` (6 değer)

| Değer | Açıklama |
|-------|----------|
| `Kasko` | Araç kasko sigortası |
| `Trafik` | Zorunlu trafik sigortası |
| `Sağlık` | Sağlık/tamamlayıcı sağlık sigortası |
| `Konut` | Konut sigortası |
| `DASK` | Doğal Afet Sigortaları Kurumu (deprem) |
| `Hayat` | Hayat sigortası |

### `durum` (4 değer)

| Değer | Açıklama |
|-------|----------|
| `Onaylandı` | Talep değerlendirildi ve ödeme yapıldı |
| `Reddedildi` | Talep reddedildi, ödeme yok |
| `Beklemede` | Talep henüz değerlendirilmedi |
| `İnceleniyor` | Talep inceleme sürecinde |

### `odeme_yontemi` (4 değer)

| Değer | Açıklama |
|-------|----------|
| `Havale/EFT` | Banka havalesi veya elektronik fon transferi |
| `Kredi Kartı` | Kredi kartına iade |
| `Çek` | Çek ile ödeme |
| `Nakit` | Nakit ödeme |

### `sehir` (15 değer)

İstanbul, Ankara, İzmir, Bursa, Antalya, Adana, Konya, Gaziantep, Mersin, Kayseri, Trabzon, Eskişehir, Diyarbakır, Samsun, Denizli

---

## Tutar Aralıkları (TL)

| Talep Türü | Min | Maks |
|------------|-----|------|
| Kasko | 1.000 | 150.000 |
| Trafik | 500 | 80.000 |
| Sağlık | 200 | 50.000 |
| Konut | 1.000 | 200.000 |
| DASK | 5.000 | 300.000 |
| Hayat | 10.000 | 500.000 |

> Onaylanan taleplerde ödeme tutarı, talep tutarının **%60–100**'ü arasında rastgele belirlenir.

---

## Notlar

- Veriler tamamen sentetiktir; gerçek kişi veya kurum bilgisi içermez.
- Sabit tohum (`SEED=42`) sayesinde betik tekrar çalıştırıldığında aynı dosya üretilir.
- Tarih aralığı: **2023-01-01** – **2025-12-31**.
- Ödeme tarihi, talep tarihinden **5–90 gün** sonrasıdır (yalnızca onaylananlarda).
