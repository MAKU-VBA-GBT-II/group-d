Merhaba@ays4ydn,

G1-junior destek çalışması kapsamında tests/test-cases.mdve data/talepler-odemeler.csvdosyaları üzerindeki incelemeyi tamamladım. İnceleme raporum aşağıdadır:

Görev 1: Mini Veri Hattı Test Senaryoları İnceleme Raporu
Hazırlayan: Fatma Nisa ARSLAN (Küçük Ekip Üyesi — DQ Destek)
Tarih: 2026-10-20
İncelenen Döküman: tests/test-cases.md ve data/talepler-odemeler.csv
İlgili Görev: Sayı #16 (G1-junior Destek Çalışması)

1. Çalışmanın Amacı
Bu çalışma, Emin Sigorta mini veri hattı projesinde son DQ üyemiz (Ayşe AYDIN) tarafından geliştirilmiş veri kaliteleri test senaryolarını ( tests/test-cases.md) değerlendirmeleri, kriterlerin veri birimlerine uygunluğunu kesintiye uğratmak ve Junior test performansını sunmak amacıyla hazırlanmıştır.

2. Test Senaryolarının İncelenmesi ve Değerlendirilmesi
TC-01 — TC-03 (Temel Yapı): data/talepler-odemeler.csv bunların mevcudiyeti, UTF-8 BOM tasması, 200 veri satır ve TLP-XXXXXformatki tekil kimlik kuralları doğrulanmıştır.
TC-04 — TC-05 (Kategorik ve Boş Değer Kuralları): 6 branş, 4 durum, 15 şehir limitleri ile onaylanmayan 150 kayıtta ödeme ayırmanın 0.0 olup ödeme tarihi ve yönteminin boş olması kuralı kontrol edilmiştir.
TC-06 — TC-07 (Finansal ve Tarih Sınırları): Onaylanan 50 kayıtta %60–100 ödeme oranı, 5–90 gün vade kuralı ve branşa dayalı min/maks tutarlılık kuralları.
3. Junior Geri Bildirimleri ve Katkı
Senaryolarda ID, Adımlar, Girdi ve Beklenen Sonuçlar alanları eksiksiz ve sistematik biçimde biçimlendirilmektedir.
Dönem planına uygun olarak "Gerçekleşen Sonuç" ve "Geçti/Kaldı" sütunlarının Hafta 4 test yürütülmesine izin verilmesi kuralına tam uyum sağlar.
4. Sonuç
Test matrisi veri tam anlamıyla garanti kapsamında alacak derinliğidir. Hafta 4 test aşaması için onaylanmıştır.
