import csv
import random

random.seed(42)
sayilar = [random.randint(1, 100) for _ in range(10)]

with open("data/prova-eylul.csv", "w", newline="", encoding="utf-8") as f:
    yazici = csv.writer(f)
    yazici.writerow(["deger"])
    for s in sayilar:
        yazici.writerow([s])
