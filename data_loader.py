"""
Handles loading and preprocessing of agricultural data from CSV files.
"""
import csv
from typing import List, Dict
from dataclasses import dataclass

@dataclass
class EnvironmentalData:
    temperature: float
    humidity: float
    rainfall: float
    soil_ph: float
    soil_moisture: float
    pest_risk: float

@dataclass
class CropData:
    name: str
    optimal_temp: float
    optimal_humidity: float
    water_needs: float
    optimal_ph: float
    pest_resistance: float

def load_environmental_data(filepath: str) -> List[EnvironmentalData]:
    data = []
    with open(filepath, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(EnvironmentalData(
                temperature=float(row['sıcaklık']),
                humidity=float(row['nem']),
                rainfall=float(row['yağış']),
                soil_ph=float(row['toprak_ph']),
                soil_moisture=float(row['toprak_nem']),
                pest_risk=float(row['zararlı_risk'])
            ))
    return data

def load_crop_data(filepath: str) -> List[CropData]:
    crops = []
    with open(filepath, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            crops.append(CropData(
                name=row['name'],
                optimal_temp=float(row['en_uygun_sıcaklık']),
                optimal_humidity=float(row['en_uygun_nem']),
                water_needs=float(row['su_ihtiyacı']),
                optimal_ph=float(row['en_uygun_ph']),
                pest_resistance=float(row['zararlı_direnci'])
            ))
    return crops