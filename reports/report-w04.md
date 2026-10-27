# Sprint Raporu — Hafta 04
**Şirket:** EMİN SİGORTA · **PM:** Eylül ÜSTÜNKAYA · **Tarih:** 2026-10-27

## Planlanan
- Görev 1 için test, hata tespiti, düzeltme ve son doğrulama adımlarının tamamlanması
- Tüm G1 Issue'larının kanıt yorumuyla kapatılması
- `report-w04.md` raporunun yazılması ve `gorev1-final` release'inin oluşturulması
- PM olarak `AGENTS.md` ve skill kontrolünün yapılması
- Her rol için eksik/zaaflı skill'in tamamlanması

## Yapılan
- **G1-test:** `tests/test-cases.md` senaryoları gerçek veri dosyası üzerinde çalıştırıldı; sonuçlar `tests/test-log.md` içinde tarihli olarak işlendi.
- **Hata/iyileştirme akışı:** En az iki `bug`/`enhancement` kaydı açıldı; hatalar ilgili kişilere atandı ve düzeltmeler yapıldı.
- **BE + FE düzeltmeleri:** Veri hataları ve grafik hataları için düzeltilen noktalar `Fixes #...` biçiminde commit mesajlarıyla takip edildi.
- **DQ analizi:** Nihai veri dosyası `docs/veri-sozlugu-g1.md` ile uyumlu olduğu doğrulandı; `G1-analiz` için kapanış yorumu yazıldı.
- **PM takibi:** Tüm G1 issue'larının durumu kontrol edildi; kapatılmamış iş varsa sahibine hatırlatma yapıldı.
- **Release:** `gorev1-final` release oluşturuldu.
- **Skill kontrolü:** Her rol için `skills/` dizinindeki skill'lere bakıldı; eksik/zaaflı olanlar tamamlandı.
- **AGENTS.md kontrolü:** Kök AGENTS dosyası güncelliği ve uyumlu olduğu kontrol edildi.

## Tıkanan
- Hiçbir kritik blokaj kalmadı; çalışma planında hedeflenen adımlar tamamlandı.
- Kısa süreli koordinasyon gecikmeleri yaşandı; ancak issue ve kanıt yorumlarıyla çözüm üretildi.
- Son teslim tarihine yaklaşan anda bazı issue'lar aynı gün kontrol edildi; buna rağmen final akışı tamamlandı.

## Kim Ne Yaptı
| Üye | Rol | Bu haftaki katkı |
|---|---|---|
| Eylül ÜSTÜNKAYA | PM | Issue takibi, `AGENTS.md` kontrolü, skill denetimi, `report-w04.md` yazımı, release yönetimi |
| Mehmet Emin EMEK | BE | Veri ve sözlük düzeltmeleri (Fixes #23 `e4cf64c`, Fixes #27 `cea93ee`), be-veri göreli yol düzeltmesi (`ca87195`) |
| Ayşe AYDIN | DQ | Test yürütme (200/200), `test-log.md`, aylık/çeyreklik trend (`analiz-g1.md`), CI otomasyonu, onay yorumu (#13, #31) |
| Gülbahar VAROL | FE | Çeyreklik trend veri etiketlerine TL eklenmesi (Fixes #24 `97adcea`), grafik çıktısı güncellemesi, Yan Görev 1 raporu |
| Ebru GÖNÜL | Junior | TC-05 bağımsız doğrulaması (Issue #29, commit `0312db8`), `test-log.md` güncellemesi, Yan Görev 3 (Grup C #22) |
| Fatma Nisa ARSLAN | Junior | TC-03 bağımsız doğrulaması (Issue #30, commit `338be0a`), `test-log.md` güncellemesi, Yan Görev 3 (Grup C #23) |

## Gelecek Hafta Planı
- Görev 2 için ilk plan ve ekip hazırlığını başlatmak
- Yeni rol dağılımı ve iş akışı için issue'ları hazırlamak
- `main` branch kuralı ve PR akışına geçiş için ekip içi hazırlığı tamamlamak
- Skill dosyalarının yeni görev için güncellenmesi ve tek tip format kontrolü
- Yeni haftanın sprint raporunu hazırlamak (`report-w05.md`)
