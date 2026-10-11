import random
import csv
import os

klasor = "data"
if not os.path.exists(klasor):
    os.makedirs(klasor)

dosya_yolu = os.path.join(klasor, "prova-ayşe.csv")

sayilar = [random.randint(1, 100) for _ in range(10)]

with open(dosya_yolu, mode='w', newline='', encoding='utf-8') as dosya:
    yazici = csv.writer(dosya)
    yazici.writerow(["deger"])
    for sayi in sayilar:
        yazici.writerow([sayi])

print(f"Dosya başarıyla oluşturuldu: {dosya_yolu}")