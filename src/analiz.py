#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DQ: Sigorta Talepleri ve Ödemeleri Veri Analizi Betiği
Bu betik, data/talepler-odemeler.csv dosyasını okuyarak temel metrikleri,
kırılımları ve 12 çeyreklik zaman serisi trendini hesaplar.
"""

import pandas as pd
from pathlib import Path

def analiz_yap(csv_yolu: str = "data/talepler-odemeler.csv"):
    yol = Path(csv_yolu)
    if not yol.exists():
        raise FileNotFoundError(f"Veri dosyası bulunamadı: {csv_yolu}")
    
    df = pd.read_csv(yol, encoding="utf-8-sig")
    df["talep_tarihi_dt"] = pd.to_datetime(df["talep_tarihi"])
    
    # 1. Toplam Metrikler
    toplam_kayit = len(df)
    toplam_talep_tutari = df["talep_tutari"].sum()
    toplam_odeme_tutari = df["odeme_tutari"].sum()
    
    # 2. Ortalama Metrikler
    ortalama_talep_tutari = df["talep_tutari"].mean()
    onaylananlar = df[df["durum"] == "Onaylandı"]
    ortalama_odeme_onaylanan = onaylananlar["odeme_tutari"].mean()
    onay_orani = (len(onaylananlar) / toplam_kayit) * 100
    odeme_karsilama_orani = (onaylananlar["odeme_tutari"].sum() / onaylananlar["talep_tutari"].sum()) * 100

    # 3. Kırılım 1: Talep Türüne Göre Dağılım
    kirilim_talep_turu = df.groupby("talep_turu").agg(
        talep_adedi=("talep_id", "count"),
        toplam_talep=("talep_tutari", "sum"),
        ortalama_talep=("talep_tutari", "mean"),
        toplam_odeme=("odeme_tutari", "sum")
    ).sort_values(by="toplam_talep", ascending=False)
    kirilim_talep_turu["pay_yuzde"] = (kirilim_talep_turu["toplam_talep"] / toplam_talep_tutari) * 100

    # 4. Metrik 4: Zaman Serisi Trend Analizi (Aylık 36 Ay ve Çeyreklik 12 Çeyrek)
    df["yil_ay"] = df["talep_tarihi_dt"].dt.to_period("M").astype(str)
    trend_aylik = df.groupby("yil_ay").agg(
        talep_adedi=("talep_id", "count"),
        toplam_talep=("talep_tutari", "sum"),
        ortalama_talep=("talep_tutari", "mean"),
        toplam_odeme=("odeme_tutari", "sum")
    )

    df["ceyrek"] = df["talep_tarihi_dt"].dt.to_period("Q").astype(str)
    trend_ceyrek = df.groupby("ceyrek").agg(
        talep_adedi=("talep_id", "count"),
        toplam_talep=("talep_tutari", "sum"),
        ortalama_talep=("talep_tutari", "mean"),
        toplam_odeme=("odeme_tutari", "sum")
    )

    # 5. Metrik 5: En Sık Görülen 3 Talep Türü
    en_sik_3_tur = df["talep_turu"].value_counts().head(3).reset_index()
    en_sik_3_tur.columns = ["talep_turu", "talep_adedi"]
    en_sik_3_tur["pay_yuzde"] = (en_sik_3_tur["talep_adedi"] / toplam_kayit) * 100

    # Ek Kırılım: Duruma Göre
    kirilim_durum = df.groupby("durum").agg(
        talep_adedi=("talep_id", "count"),
        toplam_talep=("talep_tutari", "sum"),
        ortalama_talep=("talep_tutari", "mean"),
        toplam_odeme=("odeme_tutari", "sum")
    ).sort_values(by="talep_adedi", ascending=False)
    kirilim_durum["pay_yuzde"] = (kirilim_durum["talep_adedi"] / toplam_kayit) * 100

    # Ek Sıralama: Şehirlere Göre Top-3 İl
    top3_sehir = df.groupby("sehir").agg(
        talep_adedi=("talep_id", "count"),
        toplam_talep=("talep_tutari", "sum")
    ).sort_values(by="toplam_talep", ascending=False).head(3)
    top3_sehir["pay_yuzde"] = (top3_sehir["toplam_talep"] / toplam_talep_tutari) * 100

    print("=" * 60)
    print("EMİN SİGORTA — G1 VERİ ANALİZİ ÇIKTILARI (DQ)")
    print("=" * 60)
    print(f"1. Toplam Talep Sayısı: {toplam_kayit} adet")
    print(f"2. Toplam Talep Tutarı: {toplam_talep_tutari:,.2f} TL")
    print(f"3. Toplam Ödeme Tutarı: {toplam_odeme_tutari:,.2f} TL")
    print(f"4. Ortalama Talep Tutarı: {ortalama_talep_tutari:,.2f} TL")
    print(f"5. Onaylanan Talepler Ortalama Ödeme Tutarı: {ortalama_odeme_onaylanan:,.2f} TL")
    print(f"   - Onaylanma Oranı: %{onay_orani:.1f}")
    print(f"   - Onaylananlarda Ödeme/Talep Karşılama Oranı: %{odeme_karsilama_orani:.2f}")

    print("\n--- METRİK 3: TALEP TÜRÜNE GÖRE KIRILIM ---")
    print(kirilim_talep_turu.to_string())

    print("\n--- METRİK 4A: AYLIK TREND ANALİZİ (36 AY) ---")
    print(trend_aylik.to_string())

    print("\n--- METRİK 4B: ÇEYREKLİK TREND ANALİZİ (12 ÇEYREK) ---")
    print(trend_ceyrek.to_string())

    print("\n--- METRİK 5: EN SIK GÖRÜLEN 3 TALEP TÜRÜ ---")
    print(en_sik_3_tur.to_string(index=False))

    print("\n--- EK KIRILIM: DURUM DAĞILIMI ---")
    print(kirilim_durum.to_string())

    print("\n--- EK SIRALAMA: EN ÇOK TALEP ALAN TOP-3 ŞEHİR ---")
    print(top3_sehir.to_string())
    print("=" * 60)

    return {
        "df": df,
        "toplam_kayit": toplam_kayit,
        "toplam_talep_tutari": toplam_talep_tutari,
        "toplam_odeme_tutari": toplam_odeme_tutari,
        "ortalama_talep_tutari": ortalama_talep_tutari,
        "ortalama_odeme_onaylanan": ortalama_odeme_onaylanan,
        "kirilim_talep_turu": kirilim_talep_turu,
        "trend_aylik": trend_aylik,
        "trend_ceyrek": trend_ceyrek,
        "en_sik_3_tur": en_sik_3_tur,
        "kirilim_durum": kirilim_durum,
        "top3_sehir": top3_sehir
    }

if __name__ == "__main__":
    analiz_yap()
