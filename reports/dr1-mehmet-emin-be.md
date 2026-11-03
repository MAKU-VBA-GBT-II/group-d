# 📋 Dönem Raporu 1 (DR1) — Mehmet Emin EMEK (BE)

**Şirket:** EMİN SİGORTA — Grup D  
**Rol:** Backend (BE) — Sentetik Veri Üretimi  
**GitHub:** [@emin-emek](https://github.com/emin-emek)  
**Repo:** [MAKU-VBA-GBT-II/group-d](https://github.com/MAKU-VBA-GBT-II/group-d)

---

## 1. Ne Teslim Ettim? (Kapatılan Issue, PR, commit ve dosya linkleri)

### 🗂️ Ana Teslimatlar

| Teslimat | Dosya | GitHub Linki |
|----------|-------|--------------|
| Sentetik veri üretici betiği | `src/veri-uret.py` | [src/veri-uret.py](https://github.com/MAKU-VBA-GBT-II/group-d/blob/main/src/veri-uret.py) |
| Üretilen veri seti (200 satır, 9 alan) | `data/talepler-odemeler.csv` | [data/talepler-odemeler.csv](https://github.com/MAKU-VBA-GBT-II/group-d/blob/main/data/talepler-odemeler.csv) |
| Veri sözlüğü / şema dokümantasyonu | `docs/veri-sozlugu-g1.md` | [docs/veri-sozlugu-g1.md](https://github.com/MAKU-VBA-GBT-II/group-d/blob/main/docs/veri-sozlugu-g1.md) |
| BE skill talimat dosyası | `skills/be-veri/SKILL.md` | [skills/be-veri/SKILL.md](https://github.com/MAKU-VBA-GBT-II/group-d/blob/main/skills/be-veri/SKILL.md) |
| Yan Görev 1 keşif raporu | `reports/yan-gorev-1/kesif-emin.md` | [reports/yan-gorev-1/kesif-emin.md](https://github.com/MAKU-VBA-GBT-II/group-d/blob/main/reports/yan-gorev-1/kesif-emin.md) |
| Isınma prova dosyası | `src/prova_emin.py` | [src/prova_emin.py](https://github.com/MAKU-VBA-GBT-II/group-d/blob/main/src/prova_emin.py) |

### 📌 Commit Geçmişi (9 commit)

| Tarih | Commit Hash | Mesaj |
|-------|-------------|-------|
| 2026-10-04 | `7ee79ff` | Update team member details in README.md |
| 2026-10-11 | `bcbdc2e` | H2 ısınma — prova-emin.csv eklendi (10 satır) |
| 2026-10-11 | `7dfbd93` | Yan görev raporu: kesif-emin.md eklendi |
| 2026-10-19 | `030e5dc` | **G1: Sentetik sigorta talep/odeme verisi (200 satır, 9 alan, tohum=42)** |
| 2026-10-19 | `c67da13` | refactor: veri-uret.py betiği scripts/ → src/ altına taşındı |
| 2026-10-26 | `8eed463` | fix: AGENTS.md be-veri nasıl-kullanılır satırını doldur — Fixes #12 |
| 2026-10-26 | `ca87195` | fix: SKILL.md veri-sozlugu link yolu düzeltildi (#25) |
| 2026-10-27 | `cea93ee` | Sözlük alan 7 netleştirildi — Fixes #27 |
| 2026-10-27 | `e4cf64c` | Sözlük: ödeme tarihi 2026'ya taşabilir notu — Fixes #23 |

### 🎯 Kapatılan / Katkıda Bulunulan Issue'lar

| Issue # | Başlık | Durum |
|---------|--------|-------|
| #12 | G1-veri (BE ana görevi) | ✅ Kapatıldı — Kanıt yorumu ve düzeltme commit'leriyle |
| #23 | Ödeme tarihi 2026'ya taşıyor | ✅ Fixes #23 ile kapatıldı (`e4cf64c`) |
| #25 | SKILL.md link yolu hatalı | ✅ Fix commit'i (`ca87195`) |
| #27 | Sözlük alan 7 netleştirilmesi | ✅ Fixes #27 ile kapatıldı (`cea93ee`) |

---

## 2. Neye Takıldım, Nasıl Aştım?

### 🔴 Engel 1: Betik Dizin Yapısı Karmaşası
- **Problem:** İlk commit'te `veri-uret.py` betiği `scripts/` dizini altına konulmuştu. Proje standartları `src/` dizinini gerektiriyordu.
- **Çözüm:** `c67da13` commit'iyle dosya `scripts/` → `src/` altına taşındı. SKILL.md'deki referans yolları da `ca87195` ile güncellendi.

### 🔴 Engel 2: Ödeme Tarihi 2026'ya Taşma Sorunu (Issue #23)
- **Problem:** Veri üretici, talep tarihinden 5–90 gün sonrası ödeme tarihi üretiyordu. Aralık 2025'te açılan onaylanmış talepler için `odeme_tarihi` 2026'ya taşıyordu. DQ testlerinde bu "tarih aralık dışı" olarak yakalandı.
- **Çözüm:** Bu bir bug değil, kuralın doğal sonucu olduğu belirlendi. `docs/veri-sozlugu-g1.md` dosyasına "Ödeme tarihi talep tarihinden 5–90 gün sonradır; bu yüzden Aralık 2025'te açılan onaylanmış talepler için `odeme_tarihi` 2026 başına (en geç 2026-03-31) taşabilir. Bu bir hata değil, kuralın sonucudur." notu eklendi (commit `e4cf64c`).

### 🔴 Engel 3: Veri Sözlüğü Alan 7 Belirsizliği (Issue #27)
- **Problem:** `odeme_tutari` alanının (alan 7) sıfır mı yoksa boş mu olacağı konusunda netlik yoktu. "Reddedildi / Beklemede / İnceleniyor" durumlarında `0.0` yazılıyordu ama sözlükte "Boş olabilir mi?" sütunu kafa karıştırıyordu.
- **Çözüm:** Sözlükte ilgili açıklama netleştirildi: "Onaylanmayan talepler (Reddedildi, Beklemede, İnceleniyor) için `0.0`" ifadesi eklendi (commit `cea93ee`).

### 🔴 Engel 4: Issue Kanıt Yorumu Atlama
- **Problem:** G1-veri issue'su (#12) kanıt yorumu yazılmadan kapandı ve kart otomatik olarak "Done"'a geçti.
- **Çözüm:** Kanıt yorumu sonradan eklenerek süreç tamamlandı. Bu deneyim, ilerideki issue'larda "önce kanıt yorumu, sonra kapatma" prensibini pekiştirdi.

---

## 3. Gelecek Dönem (Görev 2–3) İçin Hedefim / Önerim

> **Görev 2'de** rol rotasyonu gereği yeni role geçeceğim. Geçiş öncesi BE teslimatlarımın tüm dokümantasyonunu güncel ve devir-teslime hazır tutacağım.  
> **Görev 3 (veri seti geliştirme)** kapsamında mevcut 200 satırlık veri setini en az 500 satıra çıkarmayı, yeni kategorik alanlar (ör. yaş grubu, poliçe süresi) eklemeyi ve Faker kütüphanesi ile daha gerçekçi müşteri profilleri üretmeyi hedefliyorum. Ayrıca veri üretim sürecini parametrik hale getirip komut satırından satır sayısı ve tarih aralığı belirlenebilir bir CLI arayüzü eklemeyi planlıyorum.

---

## 📊 Özet İstatistikler

| Metrik | Değer |
|--------|-------|
| Toplam commit sayısı | 9 |
| Kapatılan issue sayısı | 4 (#12, #23, #25, #27) |
| Üretilen dosya sayısı | 6 |
| Veri seti satır sayısı | 200 |
| Veri seti alan sayısı | 9 |
| Aktif çalışma dönemi | 2026-10-04 → 2026-10-27 (≈ 3.5 hafta) |
