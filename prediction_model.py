"""
Core prediction model for crop recommendations.
"""
from typing import List, Tuple
from data_loader import EnvironmentalData, CropData

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

    def calculate_crop_score(self, env: EnvironmentalData, crop: CropData) -> float:
        """Calculate compatibility score between environment and crop."""
        temp_score = 1 - abs(env.temperature - crop.optimal_temp) / 50
        humidity_score = 1 - abs(env.humidity - crop.optimal_humidity) / 100
        water_score = 1 - abs(env.rainfall - crop.water_needs) / 1000
        ph_score = 1 - abs(env.soil_ph - crop.optimal_ph) / 14
        pest_score = (crop.pest_resistance / 10) * (1 - env.pest_risk / 10)

        return (
            self.weights['temperature'] * temp_score +
            self.weights['humidity'] * humidity_score +
            self.weights['water'] * water_score +
            self.weights['ph'] * ph_score +
            self.weights['pest'] * pest_score
        )

    def predict_best_crops(self, env: EnvironmentalData, top_n: int = 3) -> List[Tuple[str, float]]:
        """Predict the best crops for given environmental conditions."""
        scores = []
        for crop in self.crop_data:
            score = self.calculate_crop_score(env, crop)
            scores.append((crop.name, score))
        
        return sorted(scores, key=lambda x: x[1], reverse=True)[:top_n]
def assess_risks(self, env: EnvironmentalData) -> List[str]:
    """Assess potential risks based on environmental conditions."""
    risks = []
    if env.rainfall < 100:
        risks.append("Drought risk detected: Rainfall is too low.")
    if env.pest_risk > 7:
        risks.append("High pest risk detected.")
    if env.soil_ph < 5.5 or env.soil_ph > 7.5:
        risks.append("Soil pH is outside optimal range for most crops.")
    return risks
def pest_control_suggestions(self, env: EnvironmentalData) -> List[str]:
    """Provide suggestions for pest control based on pest risk."""
    suggestions = []
    if env.pest_risk > 5:
        suggestions.append("Consider using pest-resistant crops.")
        suggestions.append("Apply pest control measures (e.g., biological control or pesticides).")
    elif env.pest_risk > 7:
        suggestions.append("Immediate pest control is required.")
    return suggestions
    