# Sprint Raporu — Hafta 03
**Şirket:** EMİN SİGORTA · **PM:** Eylül ÜSTÜNKAYA · **Tarih:** 2026-10-20

## Planlanan
- G1-veri, G1-analiz, G1-gorsel, G1-test Issue'larının açılması ve Hafta 3 işlerinin tamamlanması
- Her üyenin kendi adımı için bir skill yazıp işi o skill'le yapması
- PM tarafında: pano takibi, kök `AGENTS.md` (skill envanteri), sprint raporu

## Yapılan
- **G1-veri (#12, BE):** `data/talepler-odemeler.csv` (200 satır, 9 alan, 6 talep türü), `docs/veri-sozlugu-g1.md`, sabit tohumlu `src/veri-uret.py` (tohum 42), `skills/be-veri/SKILL.md`. Commit `030e5dc`. DQ şema onayı: yapıldı. Devir teslim yorumları `G1-analiz` ve `G1-gorsel` Issue'larına yazıldı.
- **G1-analiz (#13, DQ):** `docs/analiz-g1.md` (toplam, ortalama, talep türü kırılımı, yıllık trend, en sık 3 talep türü, ek kırılımlar, 3 gözlem, 1 eylem önerisi), `src/analiz.py`, `skills/dq-analiz/SKILL.md`. Commit `9471f85`. FE'ye devir teslim yorumu: yazıldı.
- **G1-gorsel (#14, FE):** 2 PNG `/visuals` içinde, taslaklar Issue'da, kod `/src` içinde, skill `skills/fe-gorsel/SKILL.md`. Commit `c720c44` , tamamlandı.
- **G1-test ( #15, DQ):** `tests/test-cases.md` (≥5 senaryo), `skills/dq-test/SKILL.md`. Commit `cd291cf` , tamamlandı.
- **PM:** 4 Görev 1 Issue'su açıldı ve panoya eklendi, `AGENTS.md` ve `skills/pm-rapor/SKILL.md` eklendi, bu rapor yazıldı.


## Kim Ne Yaptı
| Üye | Rol | Bu haftaki katkı |
|---|---|---|
| Eylül ÜSTÜNKAYA | PM | 4 G1 Issue'su, pano takibi, `AGENTS.md`, `pm-rapor` skill'i, sprint raporu |
| Mehmet Emin EMEK | BE | Veri seti (200 satır), şema (`veri-sozlugu-g1.md`), `src/veri-uret.py`, `be-veri` skill'i, devir teslim yorumları |
| Ayşe AYDIN | DQ | Analiz (`analiz-g1.md`, `src/analiz.py`), `dq-analiz` skill'i, <test senaryoları ve `dq-test` skill'i> |
| Gülbahar VAROL | FE | <grafik taslakları, 2 PNG, `fe-gorsel` skill'i> |
| Ebru GÖNÜL | Junior | G1-junior: Veri Hattı Destek Çalışması ve Yan Görev 2 Hazırlığı |
| Fatma Nisa ARSLAN | Junior | G1-junior: Veri Hattı Destek Çalışması ve Yan Görev 2 Hazırlığı |

## Gelecek Hafta Planı
- DQ testleri çalıştırıp `tests/test-log.md`'ye işleyecek, en az 2 `bug` Issue'su açacak
- BE ve FE hataları `Fixes #n` ile kapatacak
- DQ, `G1-analiz` Issue'suna nihai veri üzerinde doğrulama yorumu yazacak
- Ebru GÖNÜL'ün #16 görevi destekle tamamlanacak
- 22 Ekim derste sözlü repo sunumu (yan görev 2)
- `report-w04.md` yazılacak ve `gorev1-final` release'i oluşturulacak
