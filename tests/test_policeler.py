"""
Emin Sigorta (Grup D) — Sentetik Portföy Poliçeleri ve Simülasyon Test Paketi
Sürüm 2 (Görev 3: Çok Ajanlı Şirket Programı)

Bu test paketi, data/policeler.csv veri setinin ve src/simulasyon.py betiğinin:
- Sözlük şemasına ve alan tiplerine uygunluğunu,
- AFAD/MGM kayıtları için üretilen il_anahtari değerlerinin Türkçe karakter (İ/ı) doğruluğunu,
- Dış parametre desteğini (il filtreleme ve prim aralığı) ve tohum tekrarlanabilirliğini (idempotentlik)
otomatik olarak doğrular.
"""

import os
import re
import sys
import unittest
import pandas as pd

# src dizinini import yoluna ekle
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(BASE_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from simulasyon import police_uret, il_anahtari_uret, IL_ILCE_REHBERI, POLICE_TURLERI


class TestPolicelerVeSimulasyon(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base_dir = BASE_DIR
        cls.data_path = os.path.join(cls.base_dir, "data", "policeler.csv")
        cls.sozluk_path = os.path.join(cls.base_dir, "docs", "veri-sozlugu.md")
        cls.beklenen_sutunlar = [
            "police_id", "il", "ilce", "il_anahtari", "police_turu",
            "teminat_tutari", "prim_tutari", "baslangic_tarihi",
            "bitis_tarihi", "bina_yasi", "deprem_teminati"
        ]

    def test_tp01_dosya_varligi_ve_kodlama(self):
        """TP-01: data/policeler.csv dosyasının varlığı ve UTF-8 (BOM) kodlaması."""
        self.assertTrue(os.path.exists(self.data_path), "data/policeler.csv dosyası bulunamadı!")
        self.assertGreater(os.path.getsize(self.data_path), 0, "Dosya boş (0 bayt) olamaz!")
        
        try:
            with open(self.data_path, "r", encoding="utf-8-sig") as f:
                baslik = f.readline().strip().split(",")
                self.assertEqual(baslik, self.beklenen_sutunlar, "Başlık sütunları sözlükle uyuşmuyor!")
        except UnicodeDecodeError as e:
            self.fail(f"Dosya UTF-8-sig ile okunamadı: {e}")

    def test_tp02_boyut_ve_satir_sayisi(self):
        """TP-02: Satır sayısı (varsayılan: 250) ve sütun yapısı kontrolü."""
        df = pd.read_csv(self.data_path, encoding="utf-8-sig")
        self.assertEqual(len(df), 250, f"Varsayılan simülasyon satır sayısı 250 olmalıdır; {len(df)} bulundu.")
        self.assertEqual(list(df.columns), self.beklenen_sutunlar, "Sütun adları veya sıralaması hatalı!")

    def test_tp03_police_id_formati_ve_tekillik(self):
        """TP-03: police_id sütununda benzersizlik ve ^POL-\\d{5}$ formatı."""
        df = pd.read_csv(self.data_path, encoding="utf-8-sig")
        self.assertEqual(df["police_id"].nunique(), len(df), "Mükerrer police_id kayıtları mevcut!")
        regex = re.compile(r"^POL-\d{5}$")
        for pid in df["police_id"]:
            self.assertTrue(bool(regex.match(str(pid))), f"Geçersiz police_id: {pid}")

    def test_tp04_il_anahtari_ve_turkce_karakter_uyumu(self):
        """TP-04: AFAD/MGM eşleşmesi için il_anahtari doğruluğu ve İ/ı karakter testleri."""
        df = pd.read_csv(self.data_path, encoding="utf-8-sig")
        for _, row in df.iterrows():
            beklenen_anahtar = il_anahtari_uret(row["il"])
            self.assertEqual(row["il_anahtari"], beklenen_anahtar, f"il_anahtari hatalı: {row['il']} -> {row['il_anahtari']}")

        # Özel karakter normalizasyon fonksiyonel testi
        test_senaryolari = {
            "İstanbul": "ISTANBUL",
            "İzmir": "IZMIR",
            "Kahramanmaraş": "KAHRAMANMARAS",
            "Diyarbakır": "DIYARBAKIR",
            "Çanakkale": "CANAKKALE",
            "Şanlıurfa": "SANLIURFA",
            "Tekirdağ": "TEKIRDAG",
            "Gaziantep": "GAZIANTEP",
        }
        for girdi, beklenen in test_senaryolari.items():
            self.assertEqual(il_anahtari_uret(girdi), beklenen, f"Karakter dönüşüm hatası: {girdi}")

    def test_tp05_brans_ve_teminat_kurallari(self):
        """TP-05: Poliçe branşları ve tutarların geçerlilik sınırları."""
        df = pd.read_csv(self.data_path, encoding="utf-8-sig")
        fark_brans = set(df["police_turu"].unique()) - set(POLICE_TURLERI)
        self.assertEqual(len(fark_brans), 0, f"Tanımsız poliçe türleri: {fark_brans}")

        self.assertTrue((df["teminat_tutari"] > 0).all(), "Teminat tutarı pozitif olmalıdır!")
        self.assertTrue((df["prim_tutari"] > 0).all(), "Prim tutarı pozitif olmalıdır!")
        self.assertTrue(set(df["deprem_teminati"].unique()).issubset({"Evet", "Hayır"}), "Deprem teminatı Evet veya Hayır olmalıdır!")

    def test_tp06_parametrik_simulasyon_destegi(self):
        """TP-06: Fonksiyonun dışarıdan il listesi ve prim aralığı alabilmesi."""
        secili_iller = ["Kahramanmaraş", "Kocaeli", "İzmir"]
        p_min, p_max = 4000.0, 7500.0

        ozel_veriler = police_uret(
            satir_sayisi=60,
            secili_iller=secili_iller,
            prim_araligi=(p_min, p_max),
            seed=123,
        )
        self.assertEqual(len(ozel_veriler), 60)
        for kayit in ozel_veriler:
            self.assertIn(kayit["il"], secili_iller, f"Filtre dışı il üretildi: {kayit['il']}")
            self.assertGreaterEqual(kayit["prim_tutari"], p_min, f"Prim minimum sınırın altında: {kayit['prim_tutari']}")
            self.assertLessEqual(kayit["prim_tutari"], p_max, f"Prim maksimum sınırın üstünde: {kayit['prim_tutari']}")

    def test_tp07_idempotentlik(self):
        """TP-07: Sabit tohum (SEED=42) ile tekrarlanabilirlik garantisi."""
        uret_1 = police_uret(satir_sayisi=50, seed=42)
        uret_2 = police_uret(satir_sayisi=50, seed=42)
        self.assertEqual(uret_1, uret_2, "Aynı tohum ile üretilen veriler birebir aynı olmalıdır!")


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestPolicelerVeSimulasyon)
    runner = unittest.TextTestRunner(verbosity=2)
    res = runner.run(suite)
    if res.wasSuccessful():
        print("\n>>> TEBRİKLER: TÜM POLİÇE VE SİMÜLASYON TESTLERİ (%100) BAŞARIYLA GEÇTİ! <<<")
    else:
        sys.exit(1)
