"""
Generates detailed recommendations based on predictions.
"""
from typing import Dict, List
from data_loader import EnvironmentalData
from prediction_model import CropPredictionModel

class RecommendationEngine:
    def __init__(self, model: CropPredictionModel):
        self.model = model

    def generate_recommendations(self, env: EnvironmentalData) -> Dict:
        best_crops = self.model.predict_best_crops(env)
        
        recommendations = {
            'crop_recommendations': best_crops,
            'irrigation_schedule': self._get_irrigation_schedule(env),
            'pest_control': self._get_pest_control_recommendations(env),
            'risk_assessment': self._assess_risks(env)
        }
        
        return recommendations

    def _get_irrigation_schedule(self, env: EnvironmentalData) -> Dict:
        if env.soil_moisture < 0.3:
            return {'frequency': 'high', 'amount': 'moderate'}
        elif env.soil_moisture < 0.6:
            return {'frequency': 'moderate', 'amount': 'moderate'}
        else:
            return {'frequency': 'low', 'amount': 'low'}

    def _get_pest_control_recommendations(self, env: EnvironmentalData) -> List[str]:
        recommendations = []
        if env.pest_risk > 7:
            recommendations.append("Immediate pest control measures required")
        elif env.pest_risk > 4:
            recommendations.append("Monitor pest situation closely")
        return recommendations

    def _assess_risks(self, env: EnvironmentalData) -> List[str]:
        risks = []
        if env.temperature > 35:
            risks.append("High temperature risk")
        if env.humidity > 80:
            risks.append("Disease risk due to high humidity")
        if env.soil_moisture < 0.2:
            risks.append("Drought risk")
        return risks