import csv
import os
import random

os.makedirs("data", exist_ok=True)
sayilar = [random.randint(1, 100) for _ in range(10)]

with open("data/prova-gulbahar.csv", mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["deger"])
    for sayi in sayilar:
        writer.writerow([sayi])

print("CSV dosyası oluşturuldu!")