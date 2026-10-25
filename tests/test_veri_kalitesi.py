"""
Emin Sigorta (Grup D) — Veri Kalitesi Otomatik Test Paketi (DQ)
Hafta 4 / Görev 1 Kapanışı

Bu test paketi, tests/test-cases.md dosyasında tanımlanan 7 veri kalitesi
senaryosunu data/talepler-odemeler.csv üzerinde programatik olarak çalıştırır
ve tests/test-log.md ile birebir örtüşen sonuçları raporlar.
"""

import os
import re
import unittest
import pandas as pd

class TestVeriKalitesi(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Dosya yolları
        cls.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        cls.data_path = os.path.join(cls.base_dir, "data", "talepler-odemeler.csv")
        cls.sozluk_path = os.path.join(cls.base_dir, "docs", "veri-sozlugu-g1.md")
        
        # Referans sözlük kümeleri
        cls.gecerli_branslar = {"Kasko", "Trafik", "Sağlık", "Konut", "DASK", "Hayat"}
        cls.gecerli_durumlar = {"Onaylandı", "Reddedildi", "Beklemede", "İnceleniyor"}
        cls.gecerli_sehirler = {
            "İstanbul", "Ankara", "İzmir", "Bursa", "Antalya",
            "Adana", "Konya", "Gaziantep", "Mersin", "Kayseri",
            "Trabzon", "Eskişehir", "Diyarbakır", "Samsun", "Denizli"
        }
        cls.gecerli_yontemler = {"Havale/EFT", "Kredi Kartı", "Çek", "Nakit"}
        cls.beklenen_sutunlar = [
            "talep_id", "talep_tarihi", "talep_turu", "sehir",
            "talep_tutari", "durum", "odeme_tutari", "odeme_tarihi", "odeme_yontemi"
        ]
        cls.brans_limitleri = {
            "Kasko": (1000, 150000),
            "Trafik": (500, 80000),
            "Sağlık": (200, 50000),
            "Konut": (1000, 200000),
            "DASK": (5000, 300000),
            "Hayat": (10000, 500000)
        }

    def test_tc01_dosya_varligi_ve_kodlama(self):
        """TC-01: Dosya varlığı, boyutu (>0) ve UTF-8 kodlama kontrolü."""
        self.assertTrue(os.path.exists(self.data_path), "data/talepler-odemeler.csv dosyası mevcut değil!")
        size = os.path.getsize(self.data_path)
        self.assertGreater(size, 0, "Veri dosyası boş (0 bayt)!")
        
        # UTF-8 BOM veya UTF-8 ile okunabilirlik
        try:
            with open(self.data_path, "r", encoding="utf-8-sig") as f:
                content = f.read()
                self.assertIn("talep_id", content, "Başlık satırı okunamadı!")
        except UnicodeDecodeError as e:
            self.fail(f"Dosya UTF-8 ile okunamadı: {e}")

    def test_tc02_boyut_ve_sutun_yapisi(self):
        """TC-02: Satır sayısı (200) ve sütun adları/sırası."""
        df = pd.read_csv(self.data_path, encoding="utf-8-sig")
        self.assertEqual(len(df), 200, f"Satır sayısı 200 olmalı, fakat {len(df)} bulundu!")
        self.assertEqual(list(df.columns), self.beklenen_sutunlar, "Sütun isimleri veya sıralaması sözlükle uyuşmuyor!")

    def test_tc03_talep_id_benzersizligi_ve_formati(self):
        """TC-03: talep_id tekilliği ve ^TLP-\\d{5}$ regex formatı."""
        df = pd.read_csv(self.data_path, encoding="utf-8-sig")
        self.assertEqual(df["talep_id"].nunique(), 200, "talep_id sütununda mükerrer (duplicate) kayıt var!")
        
        regex = re.compile(r"^TLP-\d{5}$")
        for tid in df["talep_id"]:
            self.assertTrue(bool(regex.match(str(tid))), f"Geçersiz talep_id formatı: {tid}")

    def test_tc04_kategorik_degerlerin_sozluk_uygunlugu(self):
        """TC-04: Branş, durum, şehir ve ödeme yöntemi değerlerinin doğruluğu."""
        df = pd.read_csv(self.data_path, encoding="utf-8-sig")
        
        # Branş kontrolü
        fark_brans = set(df["talep_turu"].unique()) - self.gecerli_branslar
        self.assertEqual(len(fark_brans), 0, f"Tanımsız branşlar: {fark_brans}")
        
        # Durum kontrolü
        fark_durum = set(df["durum"].unique()) - self.gecerli_durumlar
        self.assertEqual(len(fark_durum), 0, f"Tanımsız durumlar: {fark_durum}")
        
        # Şehir kontrolü
        fark_sehir = set(df["sehir"].unique()) - self.gecerli_sehirler
        self.assertEqual(len(fark_sehir), 0, f"Tanımsız şehirler: {fark_sehir}")
        
        # Ödeme yöntemi kontrolü (boş değerler hariç)
        dolu_yontemler = set(df["odeme_yontemi"].dropna().unique())
        fark_yontem = dolu_yontemler - self.gecerli_yontemler
        self.assertEqual(len(fark_yontem), 0, f"Tanımsız ödeme yöntemleri: {fark_yontem}")

    def test_tc05_onaylanmayan_taleplerde_bos_deger_kurallari(self):
        """TC-05: Onaylanmayan 150 kayıtta odeme_tutari=0.0 ve tarih/yöntem alanlarının boşluğu."""
        df = pd.read_csv(self.data_path, encoding="utf-8-sig")
        onaysiz = df[df["durum"] != "Onaylandı"]
        self.assertEqual(len(onaysiz), 150, "Onaylanmayan talep sayısı 150 olmalıdır!")
        
        # Ödeme tutarı 0.0 olmalı
        self.assertTrue((onaysiz["odeme_tutari"] == 0.0).all(), "Onaylanmayan bazı taleplerde ödeme tutarı 0.0 değil!")
        
        # Tarih ve yöntem boş (null/NaN) olmalı
        self.assertTrue(onaysiz["odeme_tarihi"].isna().all(), "Onaylanmayan taleplerde ödeme tarihi dolu kayıt var!")
        self.assertTrue(onaysiz["odeme_yontemi"].isna().all(), "Onaylanmayan taleplerde ödeme yöntemi dolu kayıt var!")

    def test_tc06_onaylanan_taleplerde_odeme_ve_tarih_kurallari(self):
        """TC-06: Onaylanan 50 kayıtta %60-100 ödeme oranı ve 5-90 gün vade."""
        df = pd.read_csv(self.data_path, encoding="utf-8-sig")
        onayli = df[df["durum"] == "Onaylandı"].copy()
        self.assertEqual(len(onayli), 50, "Onaylanan talep sayısı 50 olmalıdır!")
        
        # Ödeme oranı: %60 - %100
        oran = onayli["odeme_tutari"] / onayli["talep_tutari"]
        self.assertTrue((oran >= 0.5999).all() and (oran <= 1.0001).all(), "Ödeme oranı %60-%100 sınırları dışında!")
        
        # Vade kontrolü: 5 ile 90 gün
        t_talep = pd.to_datetime(onayli["talep_tarihi"])
        t_odeme = pd.to_datetime(onayli["odeme_tarihi"])
        fark_gun = (t_odeme - t_talep).dt.days
        self.assertTrue((fark_gun >= 5).all() and (fark_gun <= 90).all(), "Ödeme vadesi 5-90 gün aralığı dışında!")
        
        # 2026 yılına taşma kontrolü (Bulgu / Bug #23 tespiti)
        tasankayitlar = onayli[t_odeme.dt.year > 2025]
        self.assertEqual(len(tasankayitlar), 2, "2026'ya taşan kayıt sayısı tam 2 olmalıdır (TLP-00074 ve TLP-00123)!")

    def test_tc07_brans_bazli_tutar_araliklari(self):
        """TC-07: Her branş için min ve maks tutar sınırlarının kontrolü."""
        df = pd.read_csv(self.data_path, encoding="utf-8-sig")
        for brans, (alt, ust) in self.brans_limitleri.items():
            b_df = df[df["talep_turu"] == brans]
            min_val = b_df["talep_tutari"].min()
            max_val = b_df["talep_tutari"].max()
            self.assertGreaterEqual(min_val, alt, f"{brans} minimum tutar sınırının ({alt} TL) altında: {min_val}")
            self.assertLessEqual(max_val, ust, f"{brans} maksimum tutar sınırının ({ust} TL) üstünde: {max_val}")

if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestVeriKalitesi)
    runner = unittest.TextTestRunner(verbosity=2)
    res = runner.run(suite)
    if res.wasSuccessful():
        print("\n>>> TEBRİKLER: TÜM VERİ KALİTESİ TESTLERİ (%100) BAŞARIYLA GEÇTİ! <<<")
    else:
        print("\n>>> DİKKAT: BAZI TESTLER BAŞARISIZ OLDU! <<<")
