Güncelleme:** 2026-10-26 (hoca geri bildirimine göre düzeltildi)

# Sprint Raporu — Hafta 03
**Şirket:** EMİN SİGORTA · **PM:** Eylül ÜSTÜNKAYA · **Tarih:** 2026-10-20

## Planlanan
- G1-veri, G1-analiz, G1-gorsel, G1-test Issue'larının açılması ve Hafta 3 işlerinin tamamlanması
- Her üyenin kendi adımı için bir skill yazıp işi o skill'le yapması
- PM tarafında: pano takibi, kök `AGENTS.md` (skill envanteri), sprint raporu

## Yapılan
- **G1-veri (#12, BE):** `data/talepler-odemeler.csv` (200 satır, 9 alan, 6 talep türü), `docs/veri-sozlugu-g1.md`, sabit tohumlu `src/veri-uret.py` (tohum 42), `skills/be-veri/SKILL.md`. Commit `c67da13` (ilk commit `030e5dc`). DQ şema onayı: yapıldı. Devir teslim yorumları `G1-analiz` ve `G1-gorsel` Issue'larına yazıldı.
- **G1-analiz (#13, DQ):** `docs/analiz-g1.md` (toplam, ortalama, talep türü kırılımı, 12 çeyreklik trend, en sık 3 talep türü, ek kırılımlar, 3 gözlem, 1 eylem önerisi), `src/analiz.py`, `skills/dq-analiz/SKILL.md`. Commit `9471f85`. FE'ye devir teslim yorumu: yazıldı.
- **G1-gorsel (#14, FE):** 2 PNG `/visuals` içinde, taslaklar Issue'da, kod `/src` içinde, skill `skills/fe-gorsel/SKILL.md`. Taslak ve skill commit'i `c720c44`, nihai grafikler commit `7f77fc5`. Tamamlandı.
- **G1-test (#15, DQ):** `tests/test-cases.md` (en az 5 senaryo), `skills/dq-test/SKILL.md`. Commit `cd291cf`. Tamamlandı.
- **PM:** 4 Görev 1 Issue'su açıldı ve panoya eklendi, `AGENTS.md` ve `skills/pm-rapor/SKILL.md` eklendi, bu rapor yazıldı.

## Tıkanan
- **G1-veri (#12) kanıt yorumu:** Issue kanıt yorumu yazılmadan kapandı ve kart otomatik olarak `Done`'a geçti. BE kanıt yorumunu sonradan ekledi (commit `c67da13`).
- **Trend türü sapması (#13):** Issue'da günlük/haftalık trend bekleniyordu, DQ 12 çeyreklik trend teslim etti. Gerekçe: 200 satırlık veri 3 yıla yayıldığı için haftalık dağılım seyrek kalıyor, çeyreklik trend grafik için daha okunaklı. Sapma PM'in önerisiyle yapıldı, haftalık trendin Hafta 4'te eklenmesi değerlendirilecek.
- **Son tarih hatası (#12–#15):** Issue'larda son tarih 19 Ekim Pazartesi yazılmıştı, doğrusu 20 Ekim Salı 23:59. 26 Ekim'de düzeltildi.
- **Junior katkısı (#16):** İki juniorun katkısı da commit’e dönüştü (Ebru `53b3ee3`, Fatma Nisa `f88e429`).


## Kim Ne Yaptı
| Üye | Rol | Bu haftaki katkı |
|---|---|---|
| Eylül ÜSTÜNKAYA | PM | 4 G1 Issue'su, pano takibi, `AGENTS.md`, `pm-rapor` skill'i, sprint raporu |
| Mehmet Emin EMEK | BE | Veri seti (200 satır), şema (`veri-sozlugu-g1.md`), `src/veri-uret.py`, `be-veri` skill'i, devir teslim yorumları |
| Ayşe AYDIN | DQ | Analiz (`analiz-g1.md`, 12 çeyreklik trend, `src/analiz.py`), `dq-analiz` skill'i, test senaryoları (`tests/test-cases.md`, commit `cd291cf`) ve `dq-test` skill'i |
| Gülbahar VAROL | FE | Grafik taslakları (commit `c720c44`), nihai 2 PNG (commit `7f77fc5`) ve `fe-gorsel` skill'i |
| Ebru GÖNÜL | Junior | G1-junior (#16): dokümantasyon incelemesi `reports/junior/inceleme-ebru.md` (ilk commit `53b3ee3`, son düzeltme `fcaa471`); yan görev 2 için repo seçildi (microsoft/Data-Science-For-Beginners) |
| Fatma Nisa ARSLAN | Junior | G1-junior (#16): test senaryosu incelemesi `reports/junior/inceleme-nisa.md` (commit `f88e429`); yan görev 2 için repo seçildi (pandas-dev/pandas) |


## Gelecek Hafta Planı
- DQ testleri çalıştırıp `tests/test-log.md`'ye işleyecek, en az 2 `bug` Issue'su açacak
- BE ve FE hataları `Fixes #n` ile kapatacak
- DQ, `G1-analiz` Issue'suna nihai veri üzerinde doğrulama yorumu yazacak
- Juniorlara Hafta 4 kartları açılacak (bir test senaryosu çalıştırıp `test-log.md`'ye satır eklemek)
- `report-w04.md` yazılacak ve `gorev1-final` release'i oluşturulacak

