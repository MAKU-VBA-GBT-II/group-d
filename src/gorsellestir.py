#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FE: Sigorta Talepleri ve Ödemeleri Veri Görselleştirme Betiği
Bu betik, data/talepler-odemeler.csv veri dosyasını ve docs/analiz-g1.md
içindeki metrikleri referans alarak:
1. visuals/ceyreklik-trend.png (12 Çeyreklik Zaman Serisi Trendi)
2. visuals/talep-turu-kirilimi.png (Sigorta Branşı Finansal Kırılımı)
grafiklerini üretir ve yüksek çözünürlüklü (300 DPI) PNG olarak kaydeder.
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def gorsellestir():
    # Çalışma dizinini dinamik olarak ayarla (repo kökü veya src/)
    dosya_yolu = Path(__file__).resolve()
    repo_koku = dosya_yolu.parent.parent if dosya_yolu.parent.name == "src" else dosya_yolu.parent

    veri_yolu = repo_koku / "data" / "talepler-odemeler.csv"
    visuals_dizini = repo_koku / "visuals"
    visuals_dizini.mkdir(parents=True, exist_ok=True)

    if not veri_yolu.exists():
        raise FileNotFoundError(f"Veri dosyası bulunamadı: {veri_yolu}")

    print(f"Veri okunuyor: {veri_yolu}")
    df = pd.read_csv(veri_yolu, encoding="utf-8-sig")
    df["talep_tarihi_dt"] = pd.to_datetime(df["talep_tarihi"])

    # Matplotlib stil ayarları
    plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Segoe UI", "sans-serif"]
    plt.rcParams["axes.unicode_minus"] = False

    # =========================================================================
    # GRAFİK 1: 12 ÇEYREKLİK ZAMAN SERİSİ TRENDİ (MİLYON TL)
    # =========================================================================
    df["ceyrek"] = df["talep_tarihi_dt"].dt.to_period("Q").astype(str)
    trend_df = df.groupby("ceyrek").agg(
        toplam_talep=("talep_tutari", "sum"),
        toplam_odeme=("odeme_tutari", "sum")
    ).reset_index().sort_values(by="ceyrek")

    # Tutarları Milyon TL'ye çevir
    trend_df["talep_milyon"] = trend_df["toplam_talep"] / 1_000_000.0
    trend_df["odeme_milyon"] = trend_df["toplam_odeme"] / 1_000_000.0

    fig, ax = plt.subplots(figsize=(12, 6), dpi=300)

    x_indeks = np.arange(len(trend_df))
    ceyreklikler = trend_df["ceyrek"].tolist()

    # Çizgi ve dolgu
    ax.plot(x_indeks, trend_df["talep_milyon"], marker="o", color="#1f77b4",
            linewidth=2.5, markersize=7, label="Toplam Talep Tutarı (Milyon TL)")
    ax.plot(x_indeks, trend_df["odeme_milyon"], marker="s", color="#2ca02c",
            linewidth=2.5, markersize=7, label="Toplam Ödenen Tazminat (Milyon TL)")

    ax.fill_between(x_indeks, trend_df["talep_milyon"], alpha=0.08, color="#1f77b4")
    ax.fill_between(x_indeks, trend_df["odeme_milyon"], alpha=0.08, color="#2ca02c")

    # Veri etiketleri
    for i, val in enumerate(trend_df["talep_milyon"]):
        ax.annotate(f"{val:.2f}M", (i, val), textcoords="offset points",
                    xytext=(0, 8), ha="center", fontsize=8.5, fontweight="bold", color="#144d75")
    for i, val in enumerate(trend_df["odeme_milyon"]):
        ax.annotate(f"{val:.2f}M", (i, val), textcoords="offset points",
                    xytext=(0, -13), ha="center", fontsize=8.5, fontweight="bold", color="#1c661c")

    ax.set_title("2023–2025 Çeyreklik Sigorta Talep ve Ödenen Tazminat Trendi",
                 fontsize=14, fontweight="bold", pad=15, color="#222222")
    ax.set_xlabel("Dönem / Çeyrek (Yıl-Çeyrek)", fontsize=11, fontweight="bold", labelpad=10)
    ax.set_ylabel("Tutar (Milyon TL)", fontsize=11, fontweight="bold", labelpad=10)
    ax.set_xticks(x_indeks)
    ax.set_xticklabels(ceyreklikler, rotation=30, ha="right", fontsize=9.5)
    ax.set_ylim(0, max(trend_df["talep_milyon"]) * 1.22)
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.legend(loc="upper right", frameon=True, facecolor="#ffffff", framealpha=0.9, fontsize=10)

    plt.tight_layout()
    cikis_trend = visuals_dizini / "ceyreklik-trend.png"
    fig.savefig(cikis_trend)
    plt.close(fig)
    print(f"Grafik 1 oluşturuldu: {cikis_trend}")

    # =========================================================================
    # GRAFİK 2: TALEP TÜRÜNE GÖRE KATEGORİK KIRILIM (MİLYON TL)
    # =========================================================================
    brans_df = df.groupby("talep_turu").agg(
        toplam_talep=("talep_tutari", "sum"),
        toplam_odeme=("odeme_tutari", "sum")
    ).reset_index().sort_values(by="toplam_talep", ascending=False)

    brans_df["talep_milyon"] = brans_df["toplam_talep"] / 1_000_000.0
    brans_df["odeme_milyon"] = brans_df["toplam_odeme"] / 1_000_000.0

    fig2, ax2 = plt.subplots(figsize=(11, 6), dpi=300)

    x2 = np.arange(len(brans_df))
    genislik = 0.36

    bar1 = ax2.bar(x2 - genislik / 2, brans_df["talep_milyon"], genislik,
                   label="Toplam Talep Tutarı (Milyon TL)", color="#2b5c8f", edgecolor="#1a3959", linewidth=0.8)
    bar2 = ax2.bar(x2 + genislik / 2, brans_df["odeme_milyon"], genislik,
                   label="Toplam Ödenen Tazminat (Milyon TL)", color="#d95f02", edgecolor="#8c3d01", linewidth=0.8)

    # Çubuk üzeri değer etiketleri
    for bar in bar1:
        yukseklik = bar.get_height()
        ax2.annotate(f"{yukseklik:.2f}M TL",
                     xy=(bar.get_x() + bar.get_width() / 2, yukseklik),
                     xytext=(0, 4), textcoords="offset points",
                     ha="center", va="bottom", fontsize=9, fontweight="bold", color="#1a3959")

    for bar in bar2:
        yukseklik = bar.get_height()
        ax2.annotate(f"{yukseklik:.2f}M TL",
                     xy=(bar.get_x() + bar.get_width() / 2, yukseklik),
                     xytext=(0, 4), textcoords="offset points",
                     ha="center", va="bottom", fontsize=9, fontweight="bold", color="#8c3d01")

    ax2.set_title("Sigorta Branşlarına Göre Toplam Talep ve Ödenen Tazminat Tutarları",
                  fontsize=14, fontweight="bold", pad=15, color="#222222")
    ax2.set_xlabel("Sigorta Branşı / Talep Türü", fontsize=11, fontweight="bold", labelpad=10)
    ax2.set_ylabel("Tutar (Milyon TL)", fontsize=11, fontweight="bold", labelpad=10)
    ax2.set_xticks(x2)
    ax2.set_xticklabels(brans_df["talep_turu"], fontsize=10.5, fontweight="bold")
    ax2.set_ylim(0, max(brans_df["talep_milyon"]) * 1.18)
    ax2.grid(True, axis="y", linestyle="--", alpha=0.5)
    ax2.legend(loc="upper right", frameon=True, facecolor="#ffffff", framealpha=0.9, fontsize=10)

    plt.tight_layout()
    cikis_brans = visuals_dizini / "talep-turu-kirilimi.png"
    fig2.savefig(cikis_brans)
    plt.close(fig2)
    print(f"Grafik 2 oluşturuldu: {cikis_brans}")

    print("Tüm grafikler başarıyla oluşturuldu!")

if __name__ == "__main__":
    gorsellestir()
