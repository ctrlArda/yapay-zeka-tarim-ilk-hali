import csv
from typing import List, Tuple, Dict
import pandas as pd
import numpy as np
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime

# Veri yapıları ve mevcut sınıflar aynı kalıyor
class EnvironmentalData:
    def __init__(self, temperature, humidity, rainfall, soil_ph, soil_moisture, pest_risk):
        self.temperature = temperature
        self.humidity = humidity
        self.rainfall = rainfall
        self.soil_ph = soil_ph
        self.soil_moisture = soil_moisture
        self.pest_risk = pest_risk

class CropData:
    def __init__(self, name, optimal_temp, optimal_humidity, water_needs, optimal_ph, pest_resistance):
        self.name = name
        self.optimal_temp = optimal_temp
        self.optimal_humidity = optimal_humidity
        self.water_needs = water_needs
        self.optimal_ph = optimal_ph
        self.pest_resistance = pest_resistance

class CropPredictionModel:
    def __init__(self, crop_data: List[CropData]):
        self.crop_data = crop_data
        self.weights = {
            'temperature': 0.25,
            'humidity': 0.2,
            'water': 0.2,
            'ph': 0.2,
            'pest': 0.15
        }

    def calculate_crop_score(self, env: EnvironmentalData, crop: CropData) -> Tuple[float, Dict[str, str]]:
        reasons = {}
        
        temp_diff = abs(env.temperature - crop.optimal_temp)
        temp_score = 1 - temp_diff / 50
        reasons['Sicaklik'] = f"Sicaklik farki {temp_diff}°C ve {'uygun' if temp_score > 0.7 else 'uygun değil'}."

        humidity_diff = abs(env.humidity - crop.optimal_humidity)
        humidity_score = 1 - humidity_diff / 100
        reasons['Nem'] = f"Nem farki {humidity_diff}% ve {'uygun' if humidity_score > 0.7 else 'uygun değil'}."

        water_diff = abs(env.rainfall - crop.water_needs)
        water_score = 1 - water_diff / 1000
        reasons['Su'] = f"Su ihtiyaci farki {water_diff}mm ve {'yeterli' if water_score > 0.7 else 'yetersiz'}."

        ph_diff = abs(env.soil_ph - crop.optimal_ph)
        ph_score = 1 - ph_diff / 14
        reasons['Ph'] = f"Toprak pH farki {ph_diff} ve {'optimal' if ph_score > 0.7 else 'düzeltilmesi gerekiyor'}."

        pest_score = (crop.pest_resistance / 10) * (1 - env.pest_risk / 10)
        reasons['Zararli'] = f"Zararli direnci mevcut risk göz önüne alindiginda.{'yüksek' if pest_score > 0.5 else 'düsük'} "

        total_score = (
            self.weights['temperature'] * temp_score +
            self.weights['humidity'] * humidity_score +
            self.weights['water'] * water_score +
            self.weights['ph'] * ph_score +
            self.weights['pest'] * pest_score
        )
        
        return total_score, reasons

    def predict_best_crops(self, env: EnvironmentalData, top_n: int = 5) -> List[Tuple[str, float, Dict[str, str]]]:
        scores = []
        for crop in self.crop_data:
            score, reasons = self.calculate_crop_score(env, crop)
            scores.append((crop.name, score, reasons))
        return sorted(scores, key=lambda x: x[1], reverse=True)[:top_n]

def generate_pdf_report(recommendations, sensor_data, alerts, sensor_recommendations):
    doc = SimpleDocTemplate("tarim_raporu.pdf", pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Başlık
    elements.append(Paragraph("Akilli Tarim Raporu", styles['Heading1']))
    elements.append(Paragraph(f"Olusturulma Tarihi: {datetime.now().strftime('%d/%m/%Y %H:%M')}", styles['Normal']))
    elements.append(Spacer(1, 12))

    # Ürün Önerileri
    elements.append(Paragraph("Ürün Önerileri", styles['Heading2']))
    for crop, score, reasons in recommendations:
        elements.append(Paragraph(f"Ürün: {crop} (Skor: {score:.2f})", styles['Normal']))
        for key, reason in reasons.items():
            elements.append(Paragraph(f"  - {key.capitalize()}: {reason}", styles['Normal']))
        elements.append(Spacer(1, 6))

    # Sensör Verileri
    elements.append(Paragraph("Sensör Verileri", styles['Heading2']))
    sensor_data_list = [[key, f"{value:.1f}"] for key, value in sensor_data.items()]
    sensor_table = Table([["Parametre", "Deger"]] + sensor_data_list)
    sensor_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(sensor_table)
    elements.append(Spacer(1, 12))

    # Uyarılar ve Öneriler
    if alerts:
        elements.append(Paragraph("Uyarilar", styles['Heading2']))
        for alert in alerts:
            elements.append(Paragraph(f"• {alert}", styles['Normal']))
        elements.append(Spacer(1, 12))

    if sensor_recommendations:
        elements.append(Paragraph("Öneriler", styles['Heading2']))
        for recommendation in sensor_recommendations:
            elements.append(Paragraph(f"• {recommendation}", styles['Normal']))

    doc.build(elements)
    return "tarim_raporu.pdf"

# Mevcut yardımcı fonksiyonlar
def get_sensor_data():
    return {
        'Temperature': np.random.uniform(15, 35),
        'Humidity': np.random.uniform(40, 100),
        'Soil_pH': np.random.uniform(4, 9),
        'Light': np.random.uniform(200, 2000)
    }

def analyze_sensor_data(sensor_data, crop_conditions, selected_crop):
    crop_data = crop_conditions[crop_conditions['Crop'] == selected_crop].iloc[0]
    
    alerts = []
    recommendations = []

    for param in ['Temperature', 'Humidity', 'Soil_pH', 'Light']:
        current_value = sensor_data.get(param)
        ideal_min = crop_data[f'{param}_Min']
        ideal_max = crop_data[f'{param}_Max']

        if current_value < ideal_min or current_value > ideal_max:
            alerts.append(f"{param} su anda {current_value}. Ideal aralik: {ideal_min}-{ideal_max}.")
            recommendations.append(f"{param} seviyesini düzeltmek için gerekli önlemleri alin.")

    return alerts, recommendations

# Ana akış
import random

if __name__ == "__main__":
    # Çevresel veri
    environmental_data = EnvironmentalData(
        temperature=random.uniform(15, 35),  # 15 ile 35 derece arasında rastgele sıcaklık
        humidity=random.uniform(30, 90),     # %30 ile %90 arasında rastgele nem
        rainfall=random.uniform(100, 300),   # 100 ile 300 mm arasında rastgele yağış
        soil_ph=random.uniform(5.5, 7.5),    # 5.5 ile 7.5 arasında rastgele toprak pH'ı
        soil_moisture=random.uniform(20, 50),# %20 ile %50 arasında rastgele toprak nemi
        pest_risk=random.randint(1, 5)       # 1 ile 5 arasında rastgele zararlı riski
    )

    # CSV'den ürün verilerini yükleme
    crop_data = []  # Örnek veri yapısı
    with open("crops.csv", mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            crop_data.append(CropData(
                name=row['name'],
                optimal_temp=float(row['optimal_temp']),
                optimal_humidity=float(row['optimal_humidity']),
                water_needs=float(row['water_needs']),
                optimal_ph=float(row['optimal_ph']),
                pest_resistance=float(row['pest_resistance'])
            ))

    # Modeli başlatma ve tahmin
    model = CropPredictionModel(crop_data)
    recommendations = model.predict_best_crops(environmental_data)

    # Ek sensör analizi
    crop_conditions = pd.read_csv('crop_conditions.csv')
    sensor_data = get_sensor_data()
    selected_crop = 'Domates'
    alerts, sensor_recommendations = analyze_sensor_data(sensor_data, crop_conditions, selected_crop)

    # Sonuçları yazdırma
    print("\n=== Akilli Tarim Yapay Zeka Önerileri ===\n")
    for crop, score, reasons in recommendations:
        print(f"Ürün: {crop} (Skor: {score:.2f})")
        print("Nedenler:")
        for key, reason in reasons.items():
            print(f"  - {key.capitalize()}: {reason}")
        print()

    print("\n=== Sensör Analizi Sonuçlari ===\n")
    print("Uyarılar:")
    for alert in alerts:
        print(alert)

    print("\nTavsiyeler:")
    for recommendation in sensor_recommendations:
        print(recommendation)

    # PDF raporu oluşturma
    pdf_filename = generate_pdf_report(recommendations, sensor_data, alerts, sensor_recommendations)
    print(f"\nPDF raporu oluşturuldu: {pdf_filename}")