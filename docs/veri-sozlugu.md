# Veri Sözlüğü — Sürüm 2: Portföy Poliçeleri ve Bölgesel Afet Simülasyonu

> **Dosya:** `data/policeler.csv`  
> **Kodlama:** UTF-8 (BOM)  
> **Ayırıcı:** Virgül (`,`)  
> **Satır sayısı:** 250 (başlık hariç, varsayılan simülasyon)  
> **Üretici betik:** `src/simulasyon.py` (tohum: `42`)  
> **Hazırlayanlar:** Mehmet Emin EMEK (BE) & Ayşe AYDIN (DQ)  
> **İlgili Görev / Senaryo:** Görev 3 — Çok Ajanlı Şirket Programı (Açık Verilerle Bölgesel Deprem Risk Analizi ve Dinamik Prim Değerlendirmesi)

---

## 1. Alan Tanımları

| # | Alan Adı | Veri Tipi | Açıklama | Örnek Değer | Boş Olabilir? |
|---|----------|-----------|----------|-------------|----------------|
| 1 | `police_id` | `string` | Benzersiz poliçe kimliği. `POL-XXXXX` formatında. | `POL-00001` | Hayır |
| 2 | `il` | `string (categorical)` | Poliçenin ait olduğu il adı (Resmi Türkçe yazım). | `Kahramanmaraş` | Hayır |
| 3 | `ilce` | `string (categorical)` | Poliçenin ait olduğu ilçe adı. | `Onikişubat` | Hayır |
| 4 | `il_anahtari` | `string (categorical)` | AFAD ve MGM verileriyle güvenli eşleme için standartlaştırılmış ortak il anahtarı. | `KAHRAMANMARAS` | Hayır |
| 5 | `police_turu` | `string (categorical)` | Sigorta branşı / poliçe tipi. | `Konut` | Hayır |
| 6 | `teminat_tutari` | `float` | Poliçe azami teminat / teminat bedeli (TL). | `3836977.25` | Hayır |
| 7 | `prim_tutari` | `float` | Sigortalı tarafından ödenen yıllık poliçe prim tutarı (TL). | `10492.89` | Hayır |
| 8 | `baslangic_tarihi` | `date (YYYY-MM-DD)` | Poliçe yürürlük başlangıç tarihi (2024-01-01 — 2026-11-25). | `2024-10-12` | Hayır |
| 9 | `bitis_tarihi` | `date (YYYY-MM-DD)` | Poliçe yürürlük bitiş tarihi (Başlangıçtan tam 1 yıl / 365 gün sonra). | `2025-10-12` | Hayır |
| 10 | `bina_yasi` | `integer` | Gayrimenkulün yaşı (1–40 yıl). Yalnızca Konut, İş Yeri ve DASK poliçelerinde doldurulur. | `7` | Evet* |
| 11 | `deprem_teminati` | `string (categorical)` | Poliçenin deprem riskini kapsayıp kapsamadığı (`Evet` veya `Hayır`). | `Evet` | Hayır |

> **\*** `bina_yasi` alanı yalnızca gayrimenkul branşlarında (`Konut`, `İş Yeri`, `DASK`) doldurulur; motorlu araç branşlarında (`Kasko`, `Trafik`) boş bırakılır.

---

## 2. AFAD ve MGM Kayıtlarıyla Eşleşme Standardı (`il_anahtari`)

AFAD (Afet ve Acil Durum Yönetimi Başkanlığı), Kandilli Rasathanesi ve MGM (Meteoroloji Genel Müdürlüğü) veri kaynaklarında il adları farklı büyük/küçük harf biçimlerinde veya Türkçe karakter sorunlarıyla (`İ` vs `I`, `ı` vs `i`, `Diyarbakır` vs `DIYARBAKIR`) gelebilmektedir.

Ajan 2'nin (Veri İşleme ve Eşleme) veri tablolarını `left_join` ile hatasız bağlayabilmesi için aşağıdaki normalizasyon kuralı uygulanmıştır:

1. **`İ` ve `ı` Harf Eşitlemesi:** `İ`, `i`, `ı`, `I` varyasyonları ASCII `I` karakterine dönüştürülür.
2. **Karakter Sadeleştirme:** `ç/Ç -> C`, `ğ/Ğ -> G`, `ö/Ö -> O`, `ş/Ş -> S`, `ü/Ü -> U`.
3. **Büyük Harfe Çevirme ve Boşluk Temizleme:** Tüm karakterler büyük harfe çekilir; boşluklar ve tireler alt çizgiye (`_`) çevrilir.

### Örnek Eşleşme Tablosu

| Kaynak Yazımı (AFAD / MGM / Kullanıcı) | Ortak `il_anahtari` Değeri |
|---|---|
| `İstanbul` / `İSTANBUL` / `istanbul` / `ISTANBUL` | `ISTANBUL` |
| `İzmir` / `İZMİR` / `izmir` / `IZMIR` | `IZMIR` |
| `Kahramanmaraş` / `KAHRAMANMARAŞ` / `kahramanmaras` | `KAHRAMANMARAS` |
| `Diyarbakır` / `DİYARBAKIR` / `diyarbakir` | `DIYARBAKIR` |
| `Çanakkale` / `ÇANAKKALE` | `CANAKKALE` |
| `Tekirdağ` / `TEKİRDAĞ` | `TEKIRDAG` |
| `Şanlıurfa` / `ŞANLIURFA` | `SANLIURFA` |

---

## 3. Kategorik Değerler ve Limitler

### 3.1. `police_turu` (5 Değer)

| Poliçe Türü | Kapsam | Teminat Aralığı (TL) | Varsayılan Prim Oranı | Deprem Teminatı Dağılımı |
|---|---|---|---|---|
| `Konut` | Bina ve ev eşyası teminatı | 500.000 — 5.000.000 | %0.20 — %0.50 | %85 Evet / %15 Hayır |
| `İş Yeri` | Ticari bina ve demirbaş teminatı | 1.000.000 — 15.000.000 | %0.25 — %0.60 | %85 Evet / %15 Hayır |
| `DASK` | Zorunlu deprem sigortası | 300.000 — 1.500.000 | %0.10 — %0.35 | %100 Evet |
| `Kasko` | Motorlu araç genişletilmiş kasko | 250.000 — 2.500.000 | %1.50 — %3.50 | %70 Evet / %30 Hayır |
| `Trafik` | Karayolları zorunlu mali sorumluluk | 100.000 — 500.000 | %1.00 — %2.50 | %100 Hayır |

### 3.2. `deprem_teminati` (2 Değer)
- `Evet`: Deprem sarsıntı ve yangın/infilak klozu dahil.
- `Hayır`: Deprem teminatı kapsam dışı.

---

## 4. Parametrik Simülasyon Kullanımı (`src/simulasyon.py`)

Simülasyon motoru hem komut satırından (CLI) hem de Python modülü olarak dışarıdan parametre alabilir:

### 4.1. Komut Satırından Çalıştırma

```bash
# 1. Varsayılan üretim (250 satır, SEED=42 -> data/policeler.csv):
python src/simulasyon.py

# 2. Belirli riskli iller için veri üretme:
python src/simulasyon.py --iller "Kahramanmaraş,Hatay,Kocaeli,İzmir"

# 3. Dışarıdan prim aralığı ve satır sayısı belirleme:
python src/simulasyon.py --prim-min 3000 --prim-max 15000 --adet 500

# 4. Özel çıktı yolu ve özel tohum:
python src/simulasyon.py --cikti data/ozel-policeler.csv --tohum 123
```

### 4.2. Python İçinden Çağırma

```python
from src.simulasyon import police_uret, csv_yaz, il_anahtari_uret

# Belirli iller ve prim aralığı ile veri üret
veriler = police_uret(
    satir_sayisi=100,
    secili_iller=["İstanbul", "İzmir", "Kahramanmaraş"],
    prim_araligi=(2500.0, 10000.0),
    seed=42
)

# Dosyaya kaydet
csv_yaz(veriler, "data/policeler.csv")
```

---

## 5. İdempotentlik ve Doğrulama Notları

- **Sabit Tohum:** Varsayılan tohum (`SEED=42`) kullanıldığında her çalıştırma birebir aynı `data/policeler.csv` dosyasını üretir.
- **Sürüm Bağımsızlığı:** Bu doküman ve üretilen veriler Sürüm 2 (Görev 3) kapsamındadır. Görev 1'e ait `docs/veri-sozlugu-g1.md` ve `data/talepler-odemeler.csv` dosyalarına dokunulmamıştır.
