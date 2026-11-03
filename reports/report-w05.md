# PM Sprint Raporu — Hafta 05 (Görev 2 Kapanış)

**Tarih:** 5 Kasım 2026  
**Hazırlayan:** Eylül Üstünkaya (PM)  
**Kapsam:** Görev 2 Final ve Açık Issue Kapanışları  

---

## 1. Planlanan İşler
- Repodaki tüm açık Issue'ların kanıt yorumlarıyla kapatılması veya dürüstçe neticelendirilmesi
- Uyarı ve geri bildirim kayıtlarının (eksik kanıt, hatalı path vb.) düzeltilmesi
- Yan Görev 3 (Grup C skill incelemesi) incelemesinin tamamlanması
- Görev 2 Milestone'unun tamamlanıp kapatılması
- Hafta 5 sprint raporunun (`report-w05.md`) repoya eklenmesi

---

## 2. Yapılan İşler ve Devir Teslimler
- **BE (Mehmet Emin Emek):** Sözlük güncellemeleri, link yolu düzeltmeleri ve AGENTS.md doldurma işlemleri tamamlandı. İlgili Issue'lara fix commit'leri bağlandı.
    - Kanıt Commit'leri: e4cf64c (#23), cea93ee (#27), ca87195 (#25), 8eed463 (#12)   
- **FE (Gülbahar Varol):**Çeyreklik trend görsellerinde veri etiketlerine TL birimi eklendi.Yan Görev 1 kapsamında Git keşfi raporu repoya yüklendi ve ilgili Issue kapatıldı.
    - Kanıt Commit'leri: 97adcea (#24), 2fd0891
- **DQ (Ayşe Aydın):** Veri kalitesi test senaryoları (TC-06), otomatik CI iş akışları, DAMA-DMBOK kalite karnesi, test-log, analiz-g1 ve dq-test skill senaryoları güncellendi.
    - Kanıt Commit'leri: a4b58cf (#31), e9298fd (#23, #27), ef4a4c4 (#19), 74edeed, 8d1f930, c28e0a1, 5024b22, b4296d3, 26395b7, b94a853
- **PM (Eylül Üstünkaya):** Hafta 4 haftalık sprint raporu (report-w04.md) eklendi, Hafta 3 raporundaki düzeltmeler yapıldı ve ilişkili Issue #17 kapatıldı. Ayrıca release ve tag takibi sağlandı.
-   - Kanıt Commit'leri: 9e40b8a, 4729eeb (#17)

---

## 3. Tıkanıklıklar (Blockers)
- Uyarı Issue'larında (Issue #17, #21 vb.) düz "Yaptım" yorumlarının otomasyon uyarısı alma riski tespit edildi. 
  - *Çözüm:* İlgili yorumların altına commit ID (`4729eeb`, `ae30aef`) ve dosya yolları eklenerek düzeltildi.

---

## 4. Kim Ne Yaptı?

| Üye | Rol | Kapatılan Issue / Yapılan İş | Kanıt (Commit / PR) |
| :--- | :--- | :--- | :--- |
| Eylül Üstünkaya | PM | Sprint Raporu w04 eklendi (9e40b8a), report-w03 düzeltmeleri yapıldı ve ilişkili Issue #17 kapatıldı (4729eeb). Release ve tag takibi sağlandı. | `9e40b8a`,`4729eeb` |
| Mehmet Emin Emek | BE | Sözlük güncellemeleri (#23, #27), link yolu düzeltmeleri (#25) ve AGENTS.md doldurma adımları tamamlandı. | `e4cf64c`, `cea93ee`, `ca87195`, `8eed463` |
| Gülbahar Varol | FE | Çeyreklik trend veri etiketlerine TL birimi eklendi (#24) ve Yan Görev 1 Git keşfi raporu repoya yüklendi. | `97adcea`, `2fd0891` |
| Ayşe Aydın | DQ | Veri kalitesi testleri (TC-06), CI iş akışları, DAMA-DMBOK karnesi, dq-test ve analiz doküman güncellemeleri yapıldı. | `a4b58cf`, `e9298fd`, `ef4a4c4`, `74edeed`, `8d1f930`, `c28e0a1`, `5024b22`, `b4296d3`, `26395b7`, `b94a853` |
| Fatma Nisa Arslan | Junior | Junior inceleme raporu teslim edildi ve doğrulama log güncellemeleri tamamlandı. | `ae30aef`, `338be0a`, `9c6203e`, `b6cf8a3` |
| Ebru Gönlül | Junior | Warm-up egzersizi tamamlandı, script isimlendirmesi (prova_ebru.py) düzeltildi ve doğrulama güncellemeleri yapıldı. | `cececbe`, `676283f`, `0312db8` |

---

## 5. Gelecek Hafta Planı (Görev 3)
- Dönem Raporu 1 (`reports/donem-raporu-1.md`) teslimatının tamamlanması ve teslim Issue'sunun açılması (8 Kasım).
- Partner grup olan Grup C ile veri değişimi sürecinin başlatılması.
- Alınan partner verisinin kendi pipeline ve test ortamımıza entegre edilmesi.
