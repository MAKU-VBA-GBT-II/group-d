# Dönem Raporu 1 — Grup D

**Tarih:** 6 Kasım 2026  
**Hazırlayan (PM):** Eylül Üstünkaya  
**Ekip Üyeleri:** Eylül Üstünkaya (PM), Mehmet Emin Emek (BE), Gülbahar Varol (FE), Ayşe Aydın (DQ), Fatma Nisa Arslan (Junior), Ebru Gönül (Junior)  
**Proje Deposu:** [MAKU-VBA-GBT-II/group-d](https://github.com/MAKU-VBA-GBT-II/group-d)  

---

## 1. Yönetici Özeti
Grup D olarak Görev 1 ve Görev 2 süreçlerindeki tüm temel teslimatları başarıyla tamamladık. Ekip içinde rol dağılımı (PM, BE, FE, DQ ve Junior destek) net bir şekilde işletilmiş; sentetik veri üretimi pipeline'ı, veri kalitesi testleri, CI otomasyonları ve görselleştirme çıktılarımız eksiksiz şekilde repoya aktarılmıştır. Görev 2 itibarıyla repo üzerindeki tüm açık Issue'lar kanıt yorumlarıyla kapatılmış, süreç takibi GitHub standartlarına uygun yürütülmüştür. Takımımız Görev 3 kapsamındaki partner entegrasyonu aşamasına tamamen hazırdır.

---

## 2. Teslim Edilenler
Görev 1 kapanışından bugüne kadar tamamlanan ana işler ve kanıt bağlantıları:

- **Veri Pipeline ve Güncellemeleri (BE):** Sentetik veri üretimi, veri sözlüğü alan güncellemeleri ve link düzeltmeleri tamamlandı.
  - Kanıt: [`data/talepler-odemeler.csv`](https://github.com/MAKU-VBA-GBT-II/group-d/blob/main/data/talepler-odemeler.csv), `e4cf64c` (#23), `cea93ee` (#27), `ca87195` (#25), `8eed463` (#12)
- **Görselleştirme Çıktıları (FE):** Çeyreklik trend etiketlerine TL birimi eklendi ve Yan Görev 1 Git keşfi raporu yüklendi.
  - Kanıt: `visuals/ceyreklik-trend.png`, `97adcea` (#24), `2fd0891`
- **Kalite Doğrulama ve Test Otomasyonu (DQ):** TC-06 testleri, CI iş akışı, DAMA-DMBOK kalite karnesi ve analiz dokümanları güncellendi.
  - Kanıt: `docs/analiz-g1.md`, `a4b58cf` (#31), `e9298fd` (#23, #27), `ef4a4c4` (#19), `74edeed`, `c28e0a1`, `5024b22`
- **Sprint ve Süreç Takibi (PM):** Hafta 4 ve Hafta 5 sprint raporları düzenlendi, Issue düzeltmeleri ve release takibi sağlandı.
  - Kanıt: `reports/report-w04.md` (`9e40b8a`), `reports/report-w05.md`, `4729eeb` (#17)
- **Junior Katkıları:** İnceleme raporları ve warm-up egzersizleri teslim edildi.
  - Kanıt: `reports/junior/` (`ae30aef`), `prova_ebru.py` (`cececbe`)

---

## 3. Sayılarla Dönem (Süreç KPI'ları)

| KPI Metriği | Değer |
| :--- | :--- |
| **Açılan / Kapatılan Issue Sayısı** | 31 / 31 |
| **Merge Edilmiş PR Sayısı** | 0 (Doğrudan main branch commit modeli) |
| **PR Başına Ortalama İlk İnceleme Süresi** | N/A (Doğrudan commit akışı) |
| **Son Tarihi Geçen (Geciken) İş Sayısı** | 0 |

### Üye Bazlı Katkı Tablosu

| Üye | Rol | Commit Sayısı | Kapatılan Issue Sayısı |
| :--- | :--- | :--- | :--- |
| Eylül Üstünkaya (`ustunkayaeylul72`) | PM | 15 | 6 |
| Ayşe Aydın (`ays4ydn`) | DQ | 18 | 4 |
| Mehmet Emin Emek (`emin-emek`) | BE | 10 | 6 |
| Gülbahar Varol (`gulbaharvarol03-lang`) | FE | 9 | 4 |
| Ebru Gönül (`ebruug-nl`) | Junior | 7 | 4 |
| Fatma Nisa Arslan (`nisaar-ln`) | Junior | 6 | 4 |

---

## 4. Tıkananlar

1. **Eksik Kanıt Yorumu ve Tag/Release Takibi:** Kapatılan bazı Issue'larda commit bağlantılarının ve dosya yollarının eksik olması otomasyon uyarı riski doğurdu.
   - *Çözüm:* İlgili kayıtların altına (`#17`, `#21` vb.) doğrulanmış commit ID'leri (`4729eeb`, `ae30aef`) ve dosya yolları eklenerek kanıtlar eksiksiz hale getirildi; tag/release süreçleri tamamlandı.

2. **Milestone (Yol Haritası) Yapılandırması:** Repoda varsayılan olarak Görev 2 Milestone'unun kapalı konumda bulunmaması değerlendirme kriteri uyuşmazlığı oluşturdu.
   - *Çözüm:* `GÖREV 2` Milestone'u repoda oluşturularak ilgili tüm 31 kapalı Issue bu Milestone'a bağlandı ve Milestone %100 tamamlanarak kapatıldı.

3. **Göreli Yol (Path) Uyumsuzlukları:** Dokümanlardaki dosya yollarının üst dizin çözünürlüklerinde hatalar fark edildi.
   - *Çözüm:* `ca87195` ve ilgili düzeltme commit'leriyle tüm yol tanımları bağıl konuma çekilerek güncellendi.

---

## 5. Kim Ne Yaptı

| Üye | Ne Teslim Etti? (Kanıtlı) | Neye Takıldı ve Nasıl Aştı? | Gelecek Dönem Hedefi / Önerisi |
| :--- | :--- | :--- | :--- |
| **Eylül Üstünkaya (PM)** | Sprint raporları (`report-w04.md` - `9e40b8a`, `report-w05.md`), `GÖREV 2` Milestone yapılandırması, release/tag güncellemeleri ve `#17` kapatılması (`4729eeb`). | Çapraz grup incelemelerinde kanıt yorumlarının formatına takıldı; Issue kayıtlarına commit ID ve yol detaylarını ekleyerek aştı. | Görev 3'te partner takımla (Grup C) veri entegrasyonunu sıfır hatayla yürütmek ve ekip koordinasyonunu otomatize etmek. |
| **Mehmet Emin Emek (BE)** | `src/veri-uret.py`, `data/talepler-odemeler.csv`, `docs/veri-sozlugu-g1.md`, `skills/be-veri/SKILL.md` ve keşif/prova raporları.<br>**Kanıt:** `030e5dc`, `c67da13`, `8eed463` (#12), `ca87195` (#25), `cea93ee` (#27), `e4cf64c` (#23) | Betik dizin standartlarında (`scripts/` -> `src/`) ve 2026'ya taşan ödeme tarihlerinin sözlük belirsizliğinde takıldı; yapıyı taşıyıp sözlüğe kural notu ekleyerek aştı. | Görev 3'te veri setini 500+ satıra çıkarmayı, yeni alanlar (yaş grubu, poliçe süresi) eklemeyi, Faker entegrasyonunu ve CLI arayüzü sunmayı hedefliyor. |
| **Gülbahar Varol (FE)** | `src/gorsellestir.py`, `visuals/ceyreklik-trend.png`, `visuals/talep-turu-kirilimi.png`, el çizimi mockup'lar (`#20`), Yan Görev 1 ve Yan Görev 3 raporları.<br>**Kanıt:** `75a9cb7` (#6), `c720c44`, `6f73451` (#20), `7f77fc5` (#14), `97adcea` (#24), `2fd0891`, `ccf1e04` (#32) | Grafiklerin bağımsız el çizimi eskiz şartına (`#20`) ve etiketlerdeki 'TL' birim eksikliğine (`#24`) takıldı; el çizimlerini yükleyip `f"{val:.2f}M TL"` kod güncellemesiyle aştı. | Görev 2 ile devreye giren PR kuralına uyup görselleri PR üzerinden DQ onayına sunmak; filtreleme imkanı veren interaktif analiz arayüzleri kurgulamak. |
| **Ayşe Aydın (DQ)** | `docs/analiz-g1.md`, `src/analiz.py`, `tests/test-cases.md`, `tests/test-log.md` (DAMA-DMBOK), `tests/test_veri_kalitesi.py`, CI pipeline (`data-quality-ci.yml`) ve `skills/dq-*`.<br>**Kanıt:** `58d1caf` (#13, #15), `ef4a4c4` (#19), `5024b22`, `c28e0a1`, `e9298fd` (#23, #27), `74edeed`, `a4b58cf` (#31), `b94a853` | TC-06'da 2026'ya taşan vade uyarısına ve sözlükteki "İnceleniyor" belirsizliğine takıldı; BE ile koordine olup sözlük kuralına bağlı assertion ve açıklama güncellemeleriyle aştı. | CI test hattını her PR'da otomatik çalışan kalite kapısı haline getirmek; Görev 3'te Grup C'den gelecek veriler için otomatik şema ve eksik veri doğrulama hattı kurmak. |
| **Fatma Nisa Arslan (Junior)** | Junior analiz ve inceleme raporu (`reports/junior/fatma-nisa-analiz-notlari.md`) ve test senaryosu çalıştırma doğrulama logları.<br>**Kanıt:** `ae30aef`, `338be0a`, `9c6203e`, `b6cf8a3` | Git workflow ve remote branch kullanımında local değişiklikleri push ederken çakışma (conflict) ve yetkilendirme sorunlarına takıldı; ekip desteğiyle `git fetch/rebase` pratikleri yaparak aştı. | Gelecek dönemde Backend veya Frontend görevlerinde daha aktif rol alarak temel kod tabanına doğrudan fonksiyonel katkı sağlamayı ve test kapsama oranını artırmayı hedefliyor. |
| **Ebru Gönül (Junior)** | Junior inceleme ve egzersiz raporu (`reports/junior/inceleme-ebru.md`), `prova_ebru.py` ve veri hattı doğrulama katkıları.<br>**Kanıt:** `cececbe`, `676283f`, `0312db8` | Markdown uzantılı dosya oluştururken sistemin varsayılan `.txt` saklama eğilimine ve GitHub yükleme adımlarına takıldı; dosya uzantı görünürlüğünü açarak ve rehber desteğiyle aştı. | Görev 3'te ekip çalışmalarını daha yakından takip ederek analiz raporlarını ve teknik katkılarını daha erken aşamada repoya entegre etmeyi hedefliyor. |
---

## 6. Dersler (Retrospektif)
1. **Anlık Kanıt Ekleme:** Kapatılan Issue'lara kapatıldığı anda commit koda ve dosya yolu yazmanın otomasyon uyarısı almamak açısından kritik olduğunu öğrendik.
2. **Rol Bağlantıları:** BE veriyi ve sözlüğü güncellemeden FE ve DQ tarafının ilerleyememesi nedeniyle devir-teslim yorumlarının zamanında yapılmasının süreci hızlandırdığını deneyimledik.

---

## 7. Görev 3 Hazırlığı
Partner grubumuz (Grup C) ile veri değişimi yapılması için gerekli veri sözlüğü ve CSV formatlarımız standartlaştırılmıştır. Görev 3 başladığı anda partner verisini alıp kendi analiz ve test pipeline'ımıza entegre etmeye hazırız.

---

### Prompt / Araç Özeti
*Bu rapor, PM tarafından toplanan süreç verileri, GitHub kayıtları ve `skills/pm-rapor/SKILL.md` yönergeleri doğrultusunda Gemini AI asistanı yardımıyla taslak haline getirilmiş ve son kontroller yapılarak imzalanmıştır.*
