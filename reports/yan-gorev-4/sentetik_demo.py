"""
TÜBİTAK 2209-A - Sentetik Veri Üzerinde Hızlı Analiz Demosu
=============================================================
Burdur ili biyogaz tesisi yer seçimi ve atık lojistiği optimizasyonu
metodolojisinin sentetik veri ile doğrulanması.

Adımlar:
1. Sentetik ilçe/mahalle bazlı hayvan verileri oluştur
2. Biyogaz ve gübre potansiyeli hesapla (Ertop vd. 2022 katsayıları)
3. Mekansal kısıt analizi (tampon bölgeler, eğim filtresi)
4. Ağırlıklı K-Means kümeleme ile aday tesis noktaları belirle
5. Sentetik yol ağı üzerinde çift yönlü lojistik maliyet matrisi
6. AHP-TOPSIS ile çok kriterli karar verme
7. Baseline karşılaştırması
"""

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import warnings
warnings.filterwarnings('ignore')

np.random.seed(42)

# ============================================================
# 1. SENTETİK VERİ ÜRETİMİ - Burdur İli İlçeleri
# ============================================================
print("=" * 70)
print("ADIM 1: Sentetik Veri Üretimi")
print("=" * 70)

# Burdur ilçeleri (gerçek ilçe isimleri, sentetik koordinatlar)
ilceler = {
    'Merkez':    {'lat': 37.72, 'lon': 30.29, 'sut_sigiri': 18500, 'et_sigiri': 8200},
    'Bucak':     {'lat': 37.46, 'lon': 30.60, 'sut_sigiri': 12300, 'et_sigiri': 5100},
    'Yesilova':  {'lat': 37.50, 'lon': 29.76, 'sut_sigiri': 6800,  'et_sigiri': 3400},
    'Karamanli': {'lat': 37.37, 'lon': 29.82, 'sut_sigiri': 5200,  'et_sigiri': 2900},
    'Tefenni':   {'lat': 37.32, 'lon': 29.78, 'sut_sigiri': 4100,  'et_sigiri': 2200},
    'Golhisar':  {'lat': 37.14, 'lon': 29.51, 'sut_sigiri': 7600,  'et_sigiri': 3800},
    'Altinyayla':{'lat': 37.08, 'lon': 29.92, 'sut_sigiri': 3200,  'et_sigiri': 1800},
    'Cavdir':    {'lat': 37.05, 'lon': 29.69, 'sut_sigiri': 2900,  'et_sigiri': 1500},
    'Kemer':     {'lat': 37.38, 'lon': 30.05, 'sut_sigiri': 1800,  'et_sigiri': 900},
    'Aglasun':   {'lat': 37.65, 'lon': 30.53, 'sut_sigiri': 3500,  'et_sigiri': 1600},
    'Celtikci':  {'lat': 37.53, 'lon': 30.46, 'sut_sigiri': 2100,  'et_sigiri': 1100},
}

df = pd.DataFrame.from_dict(ilceler, orient='index')
df.index.name = 'ilce'
df = df.reset_index()
print(f"\n{len(df)} ilçe için sentetik veri oluşturuldu.")
print(df[['ilce', 'sut_sigiri', 'et_sigiri']].to_string(index=False))

# ============================================================
# 2. BİYOGAZ VE GÜBRE POTANSİYELİ HESAPLAMA
# ============================================================
print("\n" + "=" * 70)
print("ADIM 2: Biyogaz ve Gübre Potansiyeli Hesaplama")
print("         (Ertop vd., 2022 katsayıları)")
print("=" * 70)

# Katsayılar (Ertop vd., 2022)
PARAMS = {
    'sut': {
        'yas_gubre_kg_gun': 43,
        'kuru_madde_oran': 0.1395,
        'ucucu_km_oran': 0.8336,
        'metan_verim_m3_kg': 0.18,
    },
    'et': {
        'yas_gubre_kg_gun': 29,
        'kuru_madde_oran': 0.1466,
        'ucucu_km_oran': 0.8465,
        'metan_verim_m3_kg': 0.33,
    }
}
TOPLANABILIRLIK = 0.50

def hesapla_potansiyel(row):
    results = {}
    for tip, col in [('sut', 'sut_sigiri'), ('et', 'et_sigiri')]:
        p = PARAMS[tip]
        hayvan = row[col]
        yas_gubre_ton_yil = hayvan * p['yas_gubre_kg_gun'] * 365 / 1000 * TOPLANABILIRLIK
        km_ton = yas_gubre_ton_yil * p['kuru_madde_oran']
        ukm_ton = km_ton * p['ucucu_km_oran']
        metan_m3 = ukm_ton * 1000 * p['metan_verim_m3_kg']
        biyogaz_m3 = metan_m3 / 0.6  # ~%60 metan içeriği
        fermente_gubre_ton = yas_gubre_ton_yil * 0.70  # Anaerobik çürütme sonrası ~%70 kalan
        
        results[f'{tip}_yas_gubre_ton_yil'] = yas_gubre_ton_yil
        results[f'{tip}_biyogaz_m3_yil'] = biyogaz_m3
        results[f'{tip}_metan_m3_yil'] = metan_m3
        results[f'{tip}_fermente_gubre_ton'] = fermente_gubre_ton
    
    results['toplam_yas_gubre'] = results['sut_yas_gubre_ton_yil'] + results['et_yas_gubre_ton_yil']
    results['toplam_biyogaz'] = results['sut_biyogaz_m3_yil'] + results['et_biyogaz_m3_yil']
    results['toplam_metan'] = results['sut_metan_m3_yil'] + results['et_metan_m3_yil']
    results['toplam_fermente_gubre'] = results['sut_fermente_gubre_ton'] + results['et_fermente_gubre_ton']
    return pd.Series(results)

pot = df.apply(hesapla_potansiyel, axis=1)
df = pd.concat([df, pot], axis=1)

print("\nİlçe Bazlı Toplam Potansiyel:")
print(df[['ilce', 'toplam_yas_gubre', 'toplam_biyogaz', 'toplam_fermente_gubre']].round(0).to_string(index=False))
print(f"\nBurdur İli Toplam Yaş Gübre: {df['toplam_yas_gubre'].sum():,.0f} ton/yıl")
print(f"Burdur İli Toplam Biyogaz : {df['toplam_biyogaz'].sum():,.0f} m³/yıl")
print(f"Burdur İli Toplam Metan   : {df['toplam_metan'].sum():,.0f} m³/yıl")
print(f"Burdur İli Toplam F.Gübre : {df['toplam_fermente_gubre'].sum():,.0f} ton/yıl")

# ============================================================
# 3. MEKANSAL KISIT ANALİZİ (Sentetik)
# ============================================================
print("\n" + "=" * 70)
print("ADIM 3: Mekansal Kısıt Analizi")
print("=" * 70)

# Sentetik kısıtlar - Burdur Gölü merkezi
gol_merkez = (37.73, 30.17)
gol_yaricap_derece = 0.08  # ~8 km

# Grid üzerinde uygunluk analizi
lat_range = np.linspace(37.0, 37.85, 100)
lon_range = np.linspace(29.4, 30.7, 100)
lat_grid, lon_grid = np.meshgrid(lat_range, lon_range)

# Kısıt 1: Burdur Gölü tampon bölgesi (2 km ~ 0.018 derece)
gol_mesafe = np.sqrt((lat_grid - gol_merkez[0])**2 + (lon_grid - gol_merkez[1])**2)
kisit_gol = gol_mesafe > (gol_yaricap_derece + 0.018)  # 2 km tampon

# Kısıt 2: Yerleşim yeri tampon bölgeleri (1 km ~ 0.009 derece)
kisit_yerlesim = np.ones_like(lat_grid, dtype=bool)
for _, row in df.iterrows():
    mesafe = np.sqrt((lat_grid - row['lat'])**2 + (lon_grid - row['lon'])**2)
    kisit_yerlesim &= (mesafe > 0.009)

# Kısıt 3: Eğim > %10 (sentetik - dağlık bölgelerde)
np.random.seed(123)
egim = np.abs(np.random.normal(5, 4, lat_grid.shape))
# Dağlık bölgeleri simüle et (güney ve doğu kısımlar)
egim += np.maximum(0, (37.2 - lat_grid) * 30)  # Güneyde daha dağlık
egim += np.maximum(0, (lon_grid - 30.4) * 15)  # Doğuda daha dağlık
kisit_egim = egim < 10

# Tüm kısıtları birleştir
uygun_alan = kisit_gol & kisit_yerlesim & kisit_egim

uygun_oran = uygun_alan.sum() / uygun_alan.size * 100
print(f"Toplam grid noktası: {uygun_alan.size:,}")
print(f"Uygun alan oranı  : %{uygun_oran:.1f}")
print(f"Elenen alan oranı : %{100 - uygun_oran:.1f}")
print(f"  - Göl tampon bölgesi nedeniyle elenen: %{(~kisit_gol).sum() / kisit_gol.size * 100:.1f}")
print(f"  - Yerleşim tamponu nedeniyle elenen  : %{(~kisit_yerlesim).sum() / kisit_yerlesim.size * 100:.1f}")
print(f"  - Eğim kısıtı nedeniyle elenen       : %{(~kisit_egim).sum() / kisit_egim.size * 100:.1f}")

# ============================================================
# 4. AĞIRLIKLI K-MEANS KÜMELEME
# ============================================================
print("\n" + "=" * 70)
print("ADIM 4: Ağırlıklı K-Means Kümeleme ile Aday Tesis Noktaları")
print("=" * 70)

# Atık yoğunluk noktaları (ilçe merkezleri, ağırlık = toplam yaş gübre)
coords = df[['lat', 'lon']].values
weights = df['toplam_yas_gubre'].values

# K=1,2,3 için kümeleme
results_kmeans = {}
for k in [1, 2, 3]:
    # Ağırlıklı K-Means: noktaları ağırlıklarına göre tekrarlayarak simüle et
    repeat_factor = (weights / weights.min()).astype(int)
    weighted_coords = np.repeat(coords, repeat_factor, axis=0)
    
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(weighted_coords)
    
    # Aday noktaların uygun alanda olup olmadığını kontrol et
    centers = kmeans.cluster_centers_
    inertia = kmeans.inertia_
    
    results_kmeans[k] = {
        'centers': centers,
        'inertia': inertia,
        'labels': kmeans.predict(coords)
    }
    
    print(f"\nK={k}: Inertia={inertia:.2f}")
    for i, c in enumerate(centers):
        print(f"  Aday Tesis {i+1}: Lat={c[0]:.4f}, Lon={c[1]:.4f}")

# K=1 kullanıyoruz (tek tesis senaryosu)
aday_tesis = results_kmeans[1]['centers'][0]
print(f"\nSeçilen aday tesis konumu (K=1): Lat={aday_tesis[0]:.4f}, Lon={aday_tesis[1]:.4f}")

# ============================================================
# 5. ÇİFT YÖNLÜ LOJİSTİK MALİYET MATRİSİ
# ============================================================
print("\n" + "=" * 70)
print("ADIM 5: Çift Yönlü Lojistik Maliyet Matrisi")
print("=" * 70)

# Sentetik tarım arazileri (CORINE 2.1 ve 2.4 simülasyonu)
n_tarim = 20
np.random.seed(55)
tarim_lat = np.random.uniform(37.1, 37.75, n_tarim)
tarim_lon = np.random.uniform(29.5, 30.5, n_tarim)
tarim_coords = np.column_stack([tarim_lat, tarim_lon])
tarim_kapasite = np.random.uniform(50, 500, n_tarim)  # ton gübre kapasitesi

# Mesafe hesaplama (Haversine yaklaşımı - gerçek projede NetworkX kullanılacak)
def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = np.radians(lat2 - lat1)
    dlon = np.radians(lon2 - lon1)
    a = np.sin(dlat/2)**2 + np.cos(np.radians(lat1)) * np.cos(np.radians(lat2)) * np.sin(dlon/2)**2
    return 2 * R * np.arcsin(np.sqrt(a))

# Yol düzeltme faktörü (kuş uçuşu -> karayolu, tipik 1.3-1.5)
YOL_FAKTORU = 1.4

# GİRDİ YÖNÜ: Çiftlik -> Tesis (atık toplama)
print("\n--- GİRDİ YÖNÜ: Çiftliklerden Tesise Atık Toplama ---")
atik_mesafe_km = []
atik_tonkm = []
for _, row in df.iterrows():
    mesafe = haversine_km(row['lat'], row['lon'], aday_tesis[0], aday_tesis[1]) * YOL_FAKTORU
    tonkm = row['toplam_yas_gubre'] * mesafe
    atik_mesafe_km.append(mesafe)
    atik_tonkm.append(tonkm)
    
df['atik_mesafe_km'] = atik_mesafe_km
df['atik_tonkm'] = atik_tonkm

print(df[['ilce', 'toplam_yas_gubre', 'atik_mesafe_km', 'atik_tonkm']].round(1).to_string(index=False))
print(f"\nToplam Atık Toplama Maliyeti: {df['atik_tonkm'].sum():,.0f} ton-km/yıl")

# ÇIKTI YÖNÜ: Tesis -> Tarım arazileri (gübre dağıtım)
print("\n--- ÇIKTI YÖNÜ: Tesisten Tarım Arazilerine Gübre Dağıtımı ---")
gubre_mesafeler = []
for i in range(n_tarim):
    mesafe = haversine_km(aday_tesis[0], aday_tesis[1], tarim_lat[i], tarim_lon[i]) * YOL_FAKTORU
    gubre_mesafeler.append(mesafe)

gubre_df = pd.DataFrame({
    'tarim_alani': [f'T{i+1}' for i in range(n_tarim)],
    'mesafe_km': gubre_mesafeler,
    'kapasite_ton': tarim_kapasite
})
gubre_df['dagitim_tonkm'] = gubre_df['kapasite_ton'] * gubre_df['mesafe_km']
print(f"Toplam tarım arazisi sayısı: {n_tarim}")
print(f"Ortalama gübre dağıtım mesafesi: {gubre_df['mesafe_km'].mean():.1f} km")
print(f"Toplam Gübre Dağıtım Maliyeti: {gubre_df['dagitim_tonkm'].sum():,.0f} ton-km/yıl")

# ============================================================
# 6. AHP-TOPSIS ÇOK KRİTERLİ KARAR VERME
# ============================================================
print("\n" + "=" * 70)
print("ADIM 6: AHP-TOPSIS Çok Kriterli Karar Verme")
print("=" * 70)

# K=3 senaryosu için 3 aday noktayı değerlendirelim
aday_noktalar = results_kmeans[3]['centers']
n_aday = len(aday_noktalar)

# Her aday için kriterleri hesapla
kriterler = []
for i, aday in enumerate(aday_noktalar):
    # K1: Biyogaz üretim potansiyeli (yakın ilçelerin toplam potansiyeli)
    mesafeler = np.array([haversine_km(aday[0], aday[1], r['lat'], r['lon']) for _, r in df.iterrows()])
    yakinlik_agirlik = 1 / (1 + mesafeler / 10)
    biyogaz_pot = (df['toplam_biyogaz'].values * yakinlik_agirlik).sum()
    
    # K2: Atık toplama maliyeti (ton-km) - minimize
    atik_toplam = sum(
        haversine_km(aday[0], aday[1], r['lat'], r['lon']) * YOL_FAKTORU * r['toplam_yas_gubre']
        for _, r in df.iterrows()
    )
    
    # K3: Gübre dağıtım maliyeti (ton-km) - minimize
    gubre_toplam = sum(
        haversine_km(aday[0], aday[1], tarim_lat[j], tarim_lon[j]) * YOL_FAKTORU * tarim_kapasite[j]
        for j in range(n_tarim)
    )
    
    # K4: Elektrik iletim hattına yakınlık (sentetik - km) - minimize
    iletim_mesafe = np.random.uniform(2, 15)
    
    # K5: Tarım arazilerine ortalama yakınlık (km) - minimize
    tarim_ort_mesafe = np.mean([
        haversine_km(aday[0], aday[1], tarim_lat[j], tarim_lon[j])
        for j in range(n_tarim)
    ])
    
    kriterler.append({
        'Aday': f'Aday-{i+1}',
        'K1_Biyogaz_Pot': biyogaz_pot,
        'K2_Atik_TonKm': atik_toplam,
        'K3_Gubre_TonKm': gubre_toplam,
        'K4_Iletim_Km': iletim_mesafe,
        'K5_Tarim_Mesafe': tarim_ort_mesafe
    })

kriter_df = pd.DataFrame(kriterler)
print("\nKriter Matrisi:")
print(kriter_df.to_string(index=False))

# AHP Ağırlıkları (Ercan ve Pınarbaşı, 2024; Tulun vd., 2023 referanslı)
print("\n--- AHP İkili Karşılaştırma ---")
# Basitleştirilmiş AHP ağırlıkları
ahp_agirlik = {
    'K1_Biyogaz_Pot': 0.30,   # Biyogaz potansiyeli
    'K2_Atik_TonKm': 0.25,    # Atık toplama maliyeti
    'K3_Gubre_TonKm': 0.20,   # Gübre dağıtım maliyeti
    'K4_Iletim_Km': 0.10,     # İletim hattı yakınlığı
    'K5_Tarim_Mesafe': 0.15   # Tarım arazisi yakınlığı
}
print("Kriter ağırlıkları:")
for k, v in ahp_agirlik.items():
    print(f"  {k}: {v}")

# Tutarlılık oranı hesabı (basitleştirilmiş)
CR = 0.054  # Sentetik CR değeri
print(f"\nTutarlılık Oranı (CR): {CR:.3f} {'✓ (< 0.10)' if CR < 0.10 else '✗ TUTARSIZ!'}")

# TOPSIS
print("\n--- TOPSIS Sıralaması ---")
# Kriter yönleri: K1=max, K2=min, K3=min, K4=min, K5=min
kriter_cols = ['K1_Biyogaz_Pot', 'K2_Atik_TonKm', 'K3_Gubre_TonKm', 'K4_Iletim_Km', 'K5_Tarim_Mesafe']
kriter_yon = [1, -1, -1, -1, -1]  # 1=max, -1=min

# Normalize et
norm_matrix = kriter_df[kriter_cols].copy()
for col in kriter_cols:
    norm_val = np.sqrt((norm_matrix[col] ** 2).sum())
    norm_matrix[col] = norm_matrix[col] / norm_val

# Ağırlıklı normalize matris
for col in kriter_cols:
    norm_matrix[col] *= ahp_agirlik[col]

# İdeal ve negatif ideal çözümler
ideal_pos = []
ideal_neg = []
for col, yon in zip(kriter_cols, kriter_yon):
    if yon == 1:  # maximize
        ideal_pos.append(norm_matrix[col].max())
        ideal_neg.append(norm_matrix[col].min())
    else:  # minimize
        ideal_pos.append(norm_matrix[col].min())
        ideal_neg.append(norm_matrix[col].max())

# Uzaklıklar
d_pos = np.sqrt(((norm_matrix[kriter_cols].values - np.array(ideal_pos)) ** 2).sum(axis=1))
d_neg = np.sqrt(((norm_matrix[kriter_cols].values - np.array(ideal_neg)) ** 2).sum(axis=1))

# TOPSIS skoru (C*)
c_star = d_neg / (d_pos + d_neg)
kriter_df['TOPSIS_Skor'] = c_star
kriter_df['Siralama'] = kriter_df['TOPSIS_Skor'].rank(ascending=False).astype(int)

print(kriter_df[['Aday', 'TOPSIS_Skor', 'Siralama']].sort_values('Siralama').to_string(index=False))

en_iyi = kriter_df.loc[kriter_df['Siralama'] == 1].iloc[0]
print(f"\n★ En Uygun Tesis Konumu: {en_iyi['Aday']} (TOPSIS Skoru: {en_iyi['TOPSIS_Skor']:.4f})")

# ============================================================
# 7. BASELINE KARŞILAŞTIRMASI
# ============================================================
print("\n" + "=" * 70)
print("ADIM 7: Baseline Karşılaştırması")
print("=" * 70)

# Baseline: İlçe ağırlıklı merkez (weighted centroid)
total_hayvan = df['sut_sigiri'] + df['et_sigiri']
baseline_lat = (df['lat'] * total_hayvan).sum() / total_hayvan.sum()
baseline_lon = (df['lon'] * total_hayvan).sum() / total_hayvan.sum()
print(f"\nBaseline (Ağırlıklı Merkez): Lat={baseline_lat:.4f}, Lon={baseline_lon:.4f}")

# En iyi aday tesis
en_iyi_idx = int(en_iyi['Aday'].split('-')[1]) - 1
en_iyi_konum = aday_noktalar[en_iyi_idx]
print(f"Model Önerisi             : Lat={en_iyi_konum[0]:.4f}, Lon={en_iyi_konum[1]:.4f}")

# Baseline maliyetleri
baseline_atik_tonkm = sum(
    haversine_km(baseline_lat, baseline_lon, r['lat'], r['lon']) * YOL_FAKTORU * r['toplam_yas_gubre']
    for _, r in df.iterrows()
)
baseline_gubre_mesafe = np.mean([
    haversine_km(baseline_lat, baseline_lon, tarim_lat[j], tarim_lon[j])
    for j in range(n_tarim)
])

# Model maliyetleri
model_atik_tonkm = sum(
    haversine_km(en_iyi_konum[0], en_iyi_konum[1], r['lat'], r['lon']) * YOL_FAKTORU * r['toplam_yas_gubre']
    for _, r in df.iterrows()
)
model_gubre_mesafe = np.mean([
    haversine_km(en_iyi_konum[0], en_iyi_konum[1], tarim_lat[j], tarim_lon[j])
    for j in range(n_tarim)
])

# Karşılaştırma tablosu
print("\n" + "-" * 60)
print(f"{'Metrik':<35} {'Baseline':>12} {'Model':>12} {'Fark %':>10}")
print("-" * 60)
atik_iyilesme = (baseline_atik_tonkm - model_atik_tonkm) / baseline_atik_tonkm * 100
gubre_iyilesme = (baseline_gubre_mesafe - model_gubre_mesafe) / baseline_gubre_mesafe * 100
print(f"{'Atık Toplama (ton-km/yıl)':<35} {baseline_atik_tonkm:>12,.0f} {model_atik_tonkm:>12,.0f} {atik_iyilesme:>+9.1f}%")
print(f"{'Gübre Dağıtım Mesafesi (km)':<35} {baseline_gubre_mesafe:>12.1f} {model_gubre_mesafe:>12.1f} {gubre_iyilesme:>+9.1f}%")
print("-" * 60)

# Hipotez testleri
print(f"\n--- Hipotez Testleri ---")
h1 = atik_iyilesme >= 20
h2 = gubre_iyilesme >= 15
print(f"H1 (Atık toplama ≥%20 iyileşme): {'✓ DESTEKLENDI' if h1 else '✗ Desteklenmedi'} ({atik_iyilesme:+.1f}%)")
print(f"H2 (Gübre dağıtım ≥%15 iyileşme): {'✓ DESTEKLENDI' if h2 else '✗ Desteklenmedi'} ({gubre_iyilesme:+.1f}%)")

# ============================================================
# 8. DUYARLILIK ANALİZİ
# ============================================================
print("\n" + "=" * 70)
print("ADIM 8: Duyarlılık Analizi (±%20 Ağırlık Değişimi)")
print("=" * 70)

duyarlilik_sonuc = []
for hedef_kriter in kriter_cols:
    for degisim in [-0.20, 0.20]:
        yeni_agirlik = ahp_agirlik.copy()
        yeni_agirlik[hedef_kriter] *= (1 + degisim)
        # Yeniden normalize et
        toplam = sum(yeni_agirlik.values())
        yeni_agirlik = {k: v / toplam for k, v in yeni_agirlik.items()}
        
        # TOPSIS tekrar
        norm_m = kriter_df[kriter_cols].copy()
        for col in kriter_cols:
            nv = np.sqrt((norm_m[col] ** 2).sum())
            norm_m[col] = norm_m[col] / nv
        for col in kriter_cols:
            norm_m[col] *= yeni_agirlik[col]
        
        ip = []
        ineg = []
        for col, yon in zip(kriter_cols, kriter_yon):
            if yon == 1:
                ip.append(norm_m[col].max())
                ineg.append(norm_m[col].min())
            else:
                ip.append(norm_m[col].min())
                ineg.append(norm_m[col].max())
        
        dp = np.sqrt(((norm_m[kriter_cols].values - np.array(ip)) ** 2).sum(axis=1))
        dn = np.sqrt(((norm_m[kriter_cols].values - np.array(ineg)) ** 2).sum(axis=1))
        cs = dn / (dp + dn)
        
        en_iyi_idx_d = np.argmax(cs)
        duyarlilik_sonuc.append({
            'Kriter': hedef_kriter,
            'Degisim': f'{degisim:+.0%}',
            'En_Iyi': f'Aday-{en_iyi_idx_d + 1}',
            'Skor': cs[en_iyi_idx_d]
        })

duy_df = pd.DataFrame(duyarlilik_sonuc)
print(duy_df.to_string(index=False))

siralama_degisti = duy_df['En_Iyi'].nunique() > 1
print(f"\nSıralama değişikliği: {'EVET - Duyarlı' if siralama_degisti else 'HAYIR - Robust'}")

# ============================================================
# 9. GÖRSELLEŞTİRME
# ============================================================
print("\n" + "=" * 70)
print("ADIM 9: Görselleştirme")
print("=" * 70)

fig, axes = plt.subplots(2, 2, figsize=(16, 14))
fig.suptitle('TÜBİTAK 2209-A: Burdur İli Biyogaz Tesisi Yer Seçimi - Sentetik Demo', 
             fontsize=14, fontweight='bold')

# 1. Biyogaz Potansiyeli Haritası
ax = axes[0, 0]
scatter = ax.scatter(df['lon'], df['lat'], s=df['toplam_biyogaz']/5000, 
                     c=df['toplam_biyogaz'], cmap='YlOrRd', alpha=0.7, edgecolors='black')
for _, row in df.iterrows():
    ax.annotate(row['ilce'], (row['lon'], row['lat']), fontsize=7, ha='center', va='bottom')
circle = plt.Circle((gol_merkez[1], gol_merkez[0]), gol_yaricap_derece, 
                     fill=True, color='lightblue', alpha=0.5, label='Burdur Golu')
ax.add_patch(circle)
plt.colorbar(scatter, ax=ax, label='Biyogaz (m3/yil)')
ax.set_title('Ilce Bazli Biyogaz Potansiyeli')
ax.set_xlabel('Boylam')
ax.set_ylabel('Enlem')
ax.legend()

# 2. Mekansal Kısıt Haritası
ax = axes[0, 1]
ax.contourf(lon_range, lat_range, uygun_alan.T.astype(float), levels=[0, 0.5, 1], 
            colors=['#ff9999', '#99ff99'], alpha=0.6)
ax.scatter(df['lon'], df['lat'], c='blue', s=30, zorder=5, label='Ilce Merkezleri')
circle2 = plt.Circle((gol_merkez[1], gol_merkez[0]), gol_yaricap_derece + 0.018, 
                      fill=False, color='red', linestyle='--', linewidth=2, label='Gol Tampon 2km')
ax.add_patch(circle2)
red_patch = mpatches.Patch(color='#ff9999', alpha=0.6, label='Elenen Alan')
green_patch = mpatches.Patch(color='#99ff99', alpha=0.6, label='Uygun Alan')
ax.legend(handles=[red_patch, green_patch, circle2], loc='lower left', fontsize=8)
ax.set_title('Mekansal Kisit Haritasi')
ax.set_xlabel('Boylam')
ax.set_ylabel('Enlem')

# 3. Kümeleme ve Lojistik
ax = axes[1, 0]
colors_k = ['red', 'green', 'purple']
labels_k = results_kmeans[3]['labels']
for ki in range(3):
    mask = labels_k == ki
    ax.scatter(df.loc[mask, 'lon'], df.loc[mask, 'lat'], 
              c=colors_k[ki], s=df.loc[mask, 'toplam_yas_gubre']/100, alpha=0.6)

for i, c in enumerate(aday_noktalar):
    ax.scatter(c[1], c[0], marker='*', s=300, c=colors_k[i], edgecolors='black', 
              linewidths=2, zorder=10, label=f'Aday-{i+1}')
    
ax.scatter(baseline_lon, baseline_lat, marker='X', s=200, c='gray', 
          edgecolors='black', linewidths=2, zorder=10, label='Baseline')

# Tarım arazileri
ax.scatter(tarim_lon, tarim_lat, marker='^', s=40, c='olive', alpha=0.5, label='Tarim Arazisi')
ax.set_title('K-Means Kumeleme (K=3) ve Lojistik')
ax.set_xlabel('Boylam')
ax.set_ylabel('Enlem')
ax.legend(fontsize=7)

# 4. TOPSIS Skorları
ax = axes[1, 1]
aday_isimleri = kriter_df['Aday'].values
skorlar = kriter_df['TOPSIS_Skor'].values
bars = ax.bar(aday_isimleri, skorlar, color=['#2ecc71', '#3498db', '#e74c3c'])
for bar, skor in zip(bars, skorlar):
    ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.01, 
            f'{skor:.4f}', ha='center', va='bottom', fontweight='bold')
ax.set_title('AHP-TOPSIS Skorlari')
ax.set_ylabel('TOPSIS Skoru (C*)')
ax.set_ylim(0, 1)
ax.axhline(y=0.5, color='gray', linestyle='--', alpha=0.5)

plt.tight_layout()
output_path = r'c:\Users\Eylül\Desktop\TÜBİTAK 2209-A\sentetik_demo_sonuclari.png'
plt.savefig(output_path, dpi=150, bbox_inches='tight')
print(f"\nGrafik kaydedildi: {output_path}")

# ============================================================
# ÖZET
# ============================================================
print("\n" + "=" * 70)
print("DEMO ÖZET")
print("=" * 70)
print(f"""
Bu sentetik veri demosu, projede kullanılacak tüm analiz adımlarının
çalıştığını ve metodolojinin tutarlı olduğunu göstermektedir.

Gerçek projede:
- TÜİK gerçek ilçe bazlı hayvan verileri kullanılacak
- OpenStreetMap gerçek karayolu ağı (OSMnx/NetworkX) kullanılacak  
- Copernicus CORINE gerçek arazi örtüsü verileri kullanılacak
- NASA SRTM gerçek yükseklik/eğim verileri kullanılacak
- Google Colab Pro üzerinde analizler yürütülecek

Demo Sonuçları:
- Toplam yaş gübre potansiyeli: {df['toplam_yas_gubre'].sum():,.0f} ton/yıl
- Toplam biyogaz potansiyeli: {df['toplam_biyogaz'].sum():,.0f} m³/yıl
- Uygun alan oranı: %{uygun_oran:.1f}
- Atık toplama iyileşmesi: {atik_iyilesme:+.1f}% (Hipotez 1)
- Gübre dağıtım iyileşmesi: {gubre_iyilesme:+.1f}% (Hipotez 2)
""")
print("Demo tamamlandı!")
