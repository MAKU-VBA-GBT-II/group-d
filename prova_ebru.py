import random
import csv
import os

# Klasörün var olduğundan emin oluyoruz
os.makedirs('data', exist_ok=True)

# 1-100 arası 10 rastgele sayı üretimi
sayilar = [random.randint(1, 100) for _ in range(10)]

# Senin adınla özelleştirilmiş dosya yolu
dosya_adi = 'data/prova-ebru.csv'

# CSV dosyasına yazma işlemi (Başlık: deger)
with open(dosya_adi, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['deger']) # Başlık satırı
    for sayi in sayilar:
        writer.writerow([sayi])

print(f"Başarıyla oluşturuldu: {dosya_adi}")
