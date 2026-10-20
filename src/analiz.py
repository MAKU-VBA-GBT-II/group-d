#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DQ: Sigorta Talepleri ve Ödemeleri Veri Analizi Betiği
Bu betik, data/talepler-odemeler.csv dosyasını okuyarak temel metrikleri,
kırılımları ve sıralamaları hesaplar.
"""

import pandas as pd
from pathlib import Path

def analiz_yap(csv_yolu: str = "data/talepler-odemeler.csv"):
    yol = Path(csv_yolu)
    if not yol.exists():
        raise FileNotFoundError(f"Veri dosyası bulunamadı: {csv_yolu}")
    
    df = pd.read_csv(yol, encoding="utf-8-sig")
    
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

    # 3. Kırılım 1: Talep Türüne Göre
    kirilim_talep_turu = df.groupby("talep_turu").agg(
        talep_adedi=("talep_id", "count"),
        toplam_talep=("talep_tutari", "sum"),
        ortalama_talep=("talep_tutari", "mean"),
        toplam_odeme=("odeme_tutari", "sum")
    ).sort_values(by="toplam_talep", ascending=False)
    kirilim_talep_turu["pay_yuzde"] = (kirilim_talep_turu["toplam_talep"] / toplam_talep_tutari) * 100

    # 4. Kırılım 2: Duruma Göre
    kirilim_durum = df.groupby("durum").agg(
        talep_adedi=("talep_id", "count"),
        toplam_talep=("talep_tutari", "sum"),
        ortalama_talep=("talep_tutari", "mean"),
        toplam_odeme=("odeme_tutari", "sum")
    ).sort_values(by="talep_adedi", ascending=False)
    kirilim_durum["pay_yuzde"] = (kirilim_durum["talep_adedi"] / toplam_kayit) * 100

    # 5. Top-3 Listesi: En Yüksek Toplam Talep Tutarına Sahip 3 Şehir
    top3_sehir = df.groupby("sehir").agg(
        talep_adedi=("talep_id", "count"),
        toplam_talep=("talep_tutari", "sum")
    ).sort_values(by="toplam_talep", ascending=False).head(3)
    top3_sehir["pay_yuzde"] = (top3_sehir["toplam_talep"] / toplam_talep_tutari) * 100

    # Top-3 En Yüksek Tutarli Bireysel Talep
    top3_talepler = df.sort_values(by="talep_tutari", ascending=False)[
        ["talep_id", "talep_turu", "sehir", "talep_tutari", "durum", "odeme_tutari"]
    ].head(3)

    print("=" * 60)
    print("EMİN SİGORTA — G1 VERİ ANALİZİ ÇIKTILARI (DQ)")
    print("=" * 60)
    print(f"1. Toplam Talep Sayısı: {toplam_kayit} adet")
    print(f"2. Toplam Talep Tutarı: {toplam_talep_tutari:,.2f} TL")
    print(f"3. Toplam Ödeme Tutarı: {toplam_odeme_tutari:,.2f} TL")
    print(f"4. Ortalama Talep Tutarı: {ortalama_talep_tutari:,.2f} TL")
    print(f"5. Onaylanan Talepler Ortalama Ödeme Tutarı: {ortalama_odeme_onaylanan:,.2f} TL")
    print(f"   - Onaylanma Oranı: %{onay_orani:.1f} ({len(onaylananlar)}/{toplam_kayit})")
    print(f"   - Onaylananlarda Ödeme/Talep Karşılama Oranı: %{odeme_karsilama_orani:.2f}")
    
    print("\n--- KIRILIM 1: TALEP TÜRÜNE GÖRE ---")
    print(kirilim_talep_turu.to_string())

    print("\n--- KIRILIM 2: DURUM DAĞILIMINA GÖRE ---")
    print(kirilim_durum.to_string())

    print("\n--- TOP-3 ŞEHİR (TALEP TUTARINA GÖRE) ---")
    print(top3_sehir.to_string())

    print("\n--- TOP-3 BİREYSEL TALEP ---")
    print(top3_talepler.to_string(index=False))
    print("=" * 60)

    return {
        "df": df,
        "toplam_kayit": toplam_kayit,
        "toplam_talep_tutari": toplam_talep_tutari,
        "toplam_odeme_tutari": toplam_odeme_tutari,
        "ortalama_talep_tutari": ortalama_talep_tutari,
        "ortalama_odeme_onaylanan": ortalama_odeme_onaylanan,
        "kirilim_talep_turu": kirilim_talep_turu,
        "kirilim_durum": kirilim_durum,
        "top3_sehir": top3_sehir,
        "top3_talepler": top3_talepler
    }

if __name__ == "__main__":
    analiz_yap()
