import random
import csv
import os
os.makedirs('data',exist_ok=True)
sayılar = [random.randint(1, 100) for _ in range(10)]
dosya_adi = 'data/prova-fatmanisa.csv'
with open(dosya_adi, 'w' , newline='', encoding='utf-8') as f:
 writer = csv.writer(f)
 writer.writerow(['deger'])
 for sayi in sayılar:
  writer.writerow([sayi])
print(f"başarıyla oluşturuldu: {dosya_adi}")