# Görev 1: Mini Veri Hattı Dokümantasyon ve Analiz İnceleme Raporu

> **Hazırlayan:** Ebru GÖNÜL (Junior Ekip Üyesi — BE/DQ Destek)  
> **Tarih:** 2026-10-20  
> **İncelenen Dokümanlar:** `docs/veri-sozlugu-g1.md` ve `docs/analiz-g1.md`  
> **İlgili Görev:** Issue #16 (G1-junior Destek Çalışması)  

---

## 1. Çalışmanın Amacı
Bu çalışma, Emin Sigorta mini veri hattı projesinde kıdemli ekip üyelerimiz BE (Mehmet Emin EMEK) ve DQ (Ayşe AYDIN) tarafından hazırlanan veri sözlüğü ve analiz raporuna junior dokümantasyon desteği sağlamak amacıyla hazırlanmıştır.

## 2. Yapılan İncelemeler ve Kontroller
- **Veri Sözlüğü (`docs/veri-sozlugu-g1.md`):** 9 alanın tamamı (`talep_id`, `talep_tarihi`, `talep_turu`, `sehir`, `talep_tutari`, `durum`, `odeme_tutari`, `odeme_tarihi`, `odeme_yontemi`) incelenmiş; tipler, branş kategorileri ve sadece onaylanan 50 kayıtta ödeme bilgilerinin dolu olması kuralı doğrulanmıştır.
- **Analiz Raporu (`docs/analiz-g1.md`):** Toplam talep tutarı (20.275.728,27 TL), ortalama talep tutarı (101.378,64 TL), 6 branş kırılımı ve FE için hazırlanan 12 çeyreklik zaman serisi trend tablosu doğrulanmıştır.

## 3. Junior Bulguları ve Geri Bildirimler
- Adet bazında en çok talep Sağlık branşında (43 adet) iken, maliyet olarak en büyük portföy riskinin Hayat sigortasında (%34,92) olması raporda çok net ve yerinde tespit edilmiştir.
- Süreçte bekleyen 100 dosya için hesaplanan 2,2 Milyon TL'lik nakit karşılık formülünün raporda açıkça belirtilmesi finansal şeffaflığı ve güvenilirliği artırmıştır.

## 4. Sonuç
incelenen kısımlarda kritik bir uyumsuzluk görülmemiştir. Test ve görselleştirme adımlarının onayı DQ ve PM'e aittir.
