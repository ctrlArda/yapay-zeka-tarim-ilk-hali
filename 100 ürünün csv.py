import csv
import random

# Rastgele ürün bilgileri oluşturmak için veriler
crop_names = [f"urun_{i}" for i in range(1, 101)]  # Ürün isimleri (Ürün_1, Ürün_2, ..., Ürün_100)

# CSV için ürün bilgileri oluşturma
crop_data = []
for name in crop_names:
    crop_data.append({
        "name": name,
        "optimal_temp": random.uniform(15, 35),  # Optimal sıcaklık (15-35°C arasında)
        "optimal_humidity": random.uniform(40, 90),  # Optimal nem (%40-%90 arasında)
        "water_needs": random.uniform(100, 300),  # Su ihtiyacı (100-300 mm arasında)
        "optimal_ph": random.uniform(5.5, 7.5),  # Optimal pH (5.5-7.5 arasında)
        "pest_resistance": random.uniform(1, 10)  # Zararlı direnci (1-10 arasında)
    })

# CSV dosyasını yazma
csv_file_path = "crops.csv"  # Çalıştırdığınız dizinde "crops.csv" olarak kaydedilecek
with open(csv_file_path, mode="w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=["name", "optimal_temp", "optimal_humidity", "water_needs", "optimal_ph", "pest_resistance"])
    writer.writeheader()
    writer.writerows(crop_data)

print(f"{csv_file_path} dosyası başarıyla oluşturuldu.")
