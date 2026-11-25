import os
import time
import urllib.request
import zipfile
import warnings
import geopandas as gpd
import networkx as nx
from shapely.geometry import Point

warnings.filterwarnings("ignore")

BASE_DIR = r"C:\Users\Eylül\Desktop\TÜBİTAK 2209-A"
RAW_OSM = os.path.join(BASE_DIR, "data", "raw", "osm_geofabrik")
PROC_DIR = os.path.join(BASE_DIR, "data", "processed")
os.makedirs(RAW_OSM, exist_ok=True)
os.makedirs(PROC_DIR, exist_ok=True)

TARGET_CRS = "EPSG:32636"
burdur_il = gpd.read_file(os.path.join(PROC_DIR, "burdur_il_siniri.gpkg")).to_crs(TARGET_CRS)

print("=" * 70)
print("TÜBİTAK 2209-A | GEOFABRIK STATİK SUNUCUDAN BURDUR OSM KATMANLARI")
print("=" * 70)

# 1. TÜRKİYE OSM SHAPEFILE PAKETİNİ İNDİR (Tek seferlik statik dosya indirme)
zip_path = os.path.join(RAW_OSM, "turkey-latest-free.shp.zip")
url = "https://download.geofabrik.de/europe/turkey-latest-free.shp.zip"

if not os.path.exists(zip_path):
    print("\n[1/4] Türkiye OSM paketi indiriliyor (yaklaşık 750 MB, bağlantı hızına göre 1-2 dk)...")
    t0 = time.time()
    urllib.request.urlretrieve(url, zip_path)
    print(f"      -> İndirildi ({time.time()-t0:.1f} sn).")
else:
    print("\n[1/4] turkey-latest-free.shp.zip zaten mevcut, atlandı.")

# 2. İLGİLİ KATMANLARI ZIP İÇİNDEN ÇIKAR VE BURDUR SINIRINA KES
katman_eslesme = {
    "burdur_yol_kenarlar": "gis_osm_roads_free_1.shp",
    "su_yuzeyleri": "gis_osm_water_a_free_1.shp",
    "yerlesimler": "gis_osm_places_a_free_1.shp",
    "koruma_alanlari": "gis_osm_natural_a_free_1.shp",
}

print("\n[2/4] Katmanlar Burdur il sınırına göre kesiliyor...")
with zipfile.ZipFile(zip_path, "r") as zf:
    for cikti_adi, shp_adi in katman_eslesme.items():
        hedef_gpkg = os.path.join(PROC_DIR, f"{cikti_adi}.gpkg")
        if os.path.exists(hedef_gpkg):
            print(f"      - {cikti_adi}.gpkg zaten mevcut, atlandı.")
            continue
        ilgili_dosyalar = [f for f in zf.namelist() if f.startswith(shp_adi.replace(".shp", "."))]
        for f in ilgili_dosyalar:
            zf.extract(f, RAW_OSM)
        shp_full = os.path.join(RAW_OSM, shp_adi)
        gdf = gpd.read_file(shp_full).to_crs(TARGET_CRS)
        gdf_burdur = gpd.clip(gdf, burdur_il)
        if cikti_adi == "burdur_yol_kenarlar":
            lojistik_siniflar = ["motorway", "trunk", "primary", "secondary", "tertiary", "unclassified",
                                 "motorway_link", "trunk_link", "primary_link", "secondary_link", "tertiary_link"]
            gdf_burdur = gdf_burdur[gdf_burdur["fclass"].isin(lojistik_siniflar)].copy()
        gdf_burdur.to_file(hedef_gpkg, driver="GPKG")
        print(f"      + {cikti_adi}.gpkg oluşturuldu ({len(gdf_burdur):,} öğe)")

# 3. KARAYOLU KATMANINDAN NETWORKX GRAFİĞİ (.graphml) OLUŞTUR
yol_graph_dosya = os.path.join(PROC_DIR, "burdur_yol_agi.graphml")
if not os.path.exists(yol_graph_dosya):
    print("\n[3/4] NetworkX karayolu ağ grafiği oluşturuluyor...")
    edges = gpd.read_file(os.path.join(PROC_DIR, "burdur_yol_kenarlar.gpkg"))
    edges = edges.explode(index_parts=False).reset_index(drop=True)
    G = nx.Graph()
    for idx, row in edges.iterrows():
        coords = list(row.geometry.coords)
        u = (round(coords[0][0], 1), round(coords[0][1], 1))
        v = (round(coords[-1][0], 1), round(coords[-1][1], 1))
        uzunluk = row.geometry.length
        G.add_node(u, x=u[0], y=u[1])
        G.add_node(v, x=v[0], y=v[1])
        G.add_edge(u, v, length=uzunluk, fclass=str(row.get("fclass", "")))
    nx.write_graphml(G, yol_graph_dosya)
    print(f"      + burdur_yol_agi.graphml kaydedildi ({G.number_of_nodes():,} düğüm, {G.number_of_edges():,} kenar)")

print("\n" + "=" * 70)
print("TÜM VERİLER HİÇBİR API SINIRINA TAKILMADAN TAMAMLANDI!")
print("=" * 70)