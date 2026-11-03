# 📋 Dönem Raporu 1 (DR1) — Ayşe AYDIN (DQ)

**Şirket:** EMİN SİGORTA — Grup D  
**Rol:** Data Quality & Analyst (DQ) — Veri Analizi ve Kalite Mühendisliği  
**GitHub:** [@ays4ydn](https://github.com/ays4ydn)  
**Repo:** [MAKU-VBA-GBT-II/group-d](https://github.com/MAKU-VBA-GBT-II/group-d)

---

## 1. Ne Teslim Ettim? (Kapatılan Issue, PR, commit ve dosya linkleri)

### 📌 Ana Teslimatlar

| Teslimat | Dosya | GitHub Linki |
|----------|-------|--------------|
| Veri Analiz Raporu (5 metrik, 36 ay + 12 çeyrek) | `docs/analiz-g1.md` | [docs/analiz-g1.md](https://github.com/MAKU-VBA-GBT-II/group-d/blob/main/docs/analiz-g1.md) |
| Deterministik Veri Analiz Betiği | `src/analiz.py` | [src/analiz.py](https://github.com/MAKU-VBA-GBT-II/group-d/blob/main/src/analiz.py) |
| Veri Kalitesi Test Senaryoları Matrisi (7/7) | `tests/test-cases.md` | [tests/test-cases.md](https://github.com/MAKU-VBA-GBT-II/group-d/blob/main/tests/test-cases.md) |
| Veri Kalitesi Test Günlüğü ve Kalite Karnesi | `tests/test-log.md` | [tests/test-log.md](https://github.com/MAKU-VBA-GBT-II/group-d/blob/main/tests/test-log.md) |
| Otomatik Test Paketi (Unittest) | `tests/test_veri_kalitesi.py` | [tests/test_veri_kalitesi.py](https://github.com/MAKU-VBA-GBT-II/group-d/blob/main/tests/test_veri_kalitesi.py) |
| Bulut Sürekli Entegrasyon (CI) Pipeline | `.github/workflows/data-quality-ci.yml` | [.github/workflows/data-quality-ci.yml](https://github.com/MAKU-VBA-GBT-II/group-d/blob/main/.github/workflows/data-quality-ci.yml) |
| DQ Analiz Skill Paketi | `skills/dq-analiz/SKILL.md` | [skills/dq-analiz/SKILL.md](https://github.com/MAKU-VBA-GBT-II/group-d/blob/main/skills/dq-analiz/SKILL.md) |
| DQ Test Skill Paketi | `skills/dq-test/SKILL.md` | [skills/dq-test/SKILL.md](https://github.com/MAKU-VBA-GBT-II/group-d/blob/main/skills/dq-test/SKILL.md) |
| Yan Görev 1 Keşif Raporu | `reports/yan-gorev-1/kesif-ayşe.md` | [reports/yan-gorev-1/kesif-ayşe.md](https://github.com/MAKU-VBA-GBT-II/group-d/blob/main/reports/yan-gorev-1/kesif-ay%C5%9Fe.md) |
| H2 Isınma Prova Betiği | `src/prova_ayşe.py` | [src/prova_ayşe.py](https://github.com/MAKU-VBA-GBT-II/group-d/blob/main/src/prova_ay%C5%9Fe.py) |
| Yan Görev 3 Çapraz İnceleme (Grup C) | Grup C Issue #21 | [Grup C Issue #21](https://github.com/MAKU-VBA-GBT-II/group-c/issues/21) |

### 📜 Commit Geçmişi (17 commit)

| Tarih | Commit Hash | Mesaj |
|-------|-------------|-------|
| 2026-10-05 | `169cf85` | Update README.md (Takım üyeleri ve roller) |
| 2026-10-11 | `9852d6e` | H2 ısınma - prova-ayşe.csv eklendi (10 satır) |
| 2026-10-11 | `61c2135` | Yan görev raporu: kesif-ayşe.md eklendi |
| 2026-10-20 | `58d1caf` | **G1: DQ analiz raporu, test senaryolari ve skill envanteri eklendi (#13 #15)** |
| 2026-10-20 | `9471f85` | docs: analiz metrikleri Issue #13 kabul kriterleriyle birebir eslestirildi |
| 2026-10-20 | `cd291cf` | docs: ceyreklik trend tablosu eklendi, test senaryolari guncellendi (#13 #15) |
| 2026-10-25 | `ef4a4c4` | docs: ceyreklik trend agregasyon gerekcesi eklendi (Fixes #19) |
| 2026-10-25 | `96ecf1a` | tests: Hafta 4 veri kalitesi test kosumu tamamlandi ve test-log eklendi |
| 2026-10-25 | `b4296d3` | docs: test-log dosyasina acilan Issue #23 ve #24 referanslari eklendi |
| 2026-10-25 | `5024b22` | test: otomatik veri kalitesi test paketi eklendi ve dq-test skill guncellendi |
| 2026-10-25 | `c28e0a1` | ci: GitHub Actions otomatik CI is akisi ve DAMA-DMBOK kalite karnesi eklendi |
| 2026-10-27 | `e9298fd` | docs: aylik trend tablosu eklendi ve TC-06 basari durumu guncellendi (#23 #27) |
| 2026-10-27 | `8d1f930` | docs: test-log ve analiz-g1 notlari guncellendi, junior bolumu eklendi |
| 2026-10-27 | `74edeed` | test: TC-06 2026-03-31 sinir dogrulamasi ve test-log tarih guncellemesi |
| 2026-10-27 | `a4b58cf` | docs: dq-test skill senaryo tanim ifadesi netlestirildi (#31) |
| 2026-10-27 | `b94a853` | docs: README calistirma talimatlari ve test-log junior bolumu guncellendi |
| 2026-10-27 | `26395b7` | docs: report-w04 tablosuna junior katkilari ve commit detaylari eklendi |

### 🎯 Kapatılan / Katkıda Bulunulan Issue'lar

| Issue # | Başlık | Durum / Rol |
|---------|--------|-------------|
| #13 | G1-analiz — Metrikleri hesapla ve bulguları yaz | ✅ Kapatıldı — Kanıt yorumu ve onay ile tamamlandı |
| #15 | G1-test — Veri kalitesi testleri | ✅ Kapatıldı — Kanıt yorumu ve CI linkiyle tamamlandı |
| #19 | G1-analiz: trend ve süreç yorumları | ✅ Kapatıldı — ef4a4c4 açıklamasıyla tamamlandı |
| #23 | bug: 2025 sonu onaylı taleplerde ödeme tarihi 2026'ya taşıyor | ✅ Açıldı & Doğrulandı — BE tarafından çözüldü |
| #24 | enhancement: Çeyreklik trend grafiğine TL birimi eklenmesi | ✅ Açıldı & Doğrulandı — FE tarafından çözüldü |
| #27 | Sözlük alan 7: "bekleyen" ifadesi İnceleniyor durumunu kapsamıyor | ✅ Açıldı & Doğrulandı — BE tarafından çözüldü |
| #31 | Skill incelemesi: dq-test (Gürol Pekmezci, Grup C) | ✅ Yanıtlandı & Kapatıldı — Commit `a4b58cf` ile giderildi |
| Grup C #21 | Skill incelemesi: dq-analiz (Ayşe Aydın, Grup D) | ✅ Grup C reposunda Yan Görev 3 incelemesi açıldı |

---

## 2. Neye Takıldım, Nasıl Aştım?

### 🚧 Engel 1: TC-06 Testinde 2026 Yılına Taşan Ödeme Tarihleri (Issue #23)
- **Problem:** Gerçek veri koşumunda, 2025 yılının son aylarında onaylanan taleplerin ödemeleri 5–90 günlük vade kuralı gereği 2026 yılına taşmaktaydı (`TLP-00074` ve `TLP-00123`). Başlangıçta bu durum sözlükteki genel simülasyon aralığı (`2023-01-01 – 2025-12-31`) ile çelişiyor gibi görünmekteydi.
- **Çözüm:** Issue #23 açılarak BE (Mehmet Emin) ile koordine olundu. Sözlük Notlar bölümüne *"Ödeme tarihi onay tarihinden 5–90 gün sonradır; bu nedenle 2025 sonu onaylı taleplerin ödemesi en geç 2026-03-31 tarihine kadar taşabilir, aralık dışı sayılmaz"* kuralı eklendi. Test suite ve `tests/test-log.md` güncellenerek TC-06 başarısı 200/200 geçerlilikle sağlandı.

### 🚧 Engel 2: Zaman Serisi Kırılım Türü Sapması (Issue #19)
- **Problem:** Dönem planı Kırılım 2'de günlük veya haftalık trend beklerken, 200 satırlık verinin 3 yıla yayılması nedeniyle haftalık bazda seyrek dağılım oluşmuş ve FE görseli için çeyreklik trend tercih edilmişti.
- **Çözüm:** Hem FE'nin mevcut çeyreklik grafik ihtiyacını koruduk hem de hocanın ve planın beklentisini karşılamak üzere `src/analiz.py` ve `docs/analiz-g1.md` içerisine 36 aylık tam aylık zaman serisi tablosu ile çeyreklik seçim gerekçesi eklendi.

### 🚧 Engel 3: Veri Sözlüğü Alan 7 Belirsizliği (Issue #27)
- **Problem:** Sözlükte onaylanmayan talepler için "Reddedilen/bekleyen talepler için 0.0" denilmişti; ancak verideki "İnceleniyor" durumunun bu kapsama girip girmediği açık değildi.
- **Çözüm:** Issue #27 açılarak BE'ye iletildi. Sözlük tanımı "Onaylanmayan üç durum (Reddedildi, Beklemede, İnceleniyor) için 0.0" şeklinde netleştirildi ve TC-05 testinde tam uyum sağlandı.

### 🚧 Engel 4: B2B Çapraz İnceleme Geri Bildirimi (Issue #31)
- **Problem:** Grup C'den Gürol Pekmezci, `skills/dq-test/SKILL.md` içindeki "7 temel kalite boyutu" ifadesinin test senaryolarıyla kavram kargaşası yaratabileceğini belirtti.
- **Çözüm:** Geri bildirim anında incelendi; `skills/dq-test/SKILL.md` güncellenerek *"Veri sözlüğündeki kurallara göre yedi test senaryosu tanımla"* biçimine dönüştürüldü (commit `a4b58cf`), nezaket yanıtı verilip Issue kapatıldı.

---

## 3. Gelecek Dönem (Görev 2–3) İçin Hedefim / Önerim

> **Görev 2'de** rol rotasyonu gereğince **Backend Developer (BE)** rolünü devralıyorum. DQ sürecinde veri şeması, kalite boyutları ve sınır değerleri üzerinde edindiğim derin tecrübeyi, yeni rolümde **en az 2 parametreli dinamik simülasyon mimarisine** (`src/simulasyon.py`) aktaracağım.  
> **Görev 3 (B2B Veri Değişimi)** sürecinde, partner grubumuz Grup C (Bankacılık) ile yapılacak veri takasında şema uyumu, eksik veri filtreleme ve PR bazlı kod inceleme süreçlerini en yüksek profesyonellikle sürdürmeyi hedefliyorum.

---

## 📊 Özet İstatistikler

| Metrik | Değer |
|--------|-------|
| Toplam commit sayısı | 17 |
| Kapatılan / çözülen issue sayısı | 8 (#13, #15, #19, #23, #24, #27, #31, Grup C #21) |
| Üretilen / güncellenen dosya sayısı | 10 |
| Doğrulanan veri kalitesi test senaryosu | 7/7 (%100 Başarılı) |
| Veri Kalitesi İndeksi (DQI) | %100.0 (A+ Kusursuz) |
| Otomatik CI Test Süresi | ~0.02 saniye |
| Aktif çalışma dönemi | 2026-10-05 — 2026-10-27 (~3.5 hafta) |
