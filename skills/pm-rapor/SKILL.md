---
name: pm-rapor
description: Haftalık sprint raporunu (report-wXX.md) GitHub Issue ve commit izlerinden hazırlar.
---

# pm-rapor

Bu skill, deponun Issue ve commit geçmişine bakarak `reports/report-wXX.md` sprint raporunu yazar.

## Adımlar
1. Açık ve kapalı Issue'ları listele (G1-veri, G1-analiz, G1-gorsel, G1-test).
2. Her Issue için kanıt yorumundaki commit hash'ini ve devir teslim yorumlarını bul.
3. Planlanan / yapılan / tıkanan / kim-ne-yaptı bölümlerini Issue ve commit numaralarıyla doldur.
4. Gelecek hafta planını yaz.

## Kullandığı dosyalar
- `reports/report-wXX.md` (çıktı)
- Depodaki Issue'lar ve commit geçmişi (girdi)

## Nasıl çalıştırılır
Ajana (Claude Code, Codex vb.) "pm-rapor skill'ini kullanarak Hafta 3 raporunu yaz" de; çıktıyı kontrol edip commit'le.
