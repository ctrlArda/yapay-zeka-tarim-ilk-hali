from fpdf import FPDF

# PDF fonksiyonu
def save_recommendations_to_pdf(recommendations, filename="report.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Akıllı Tarım Yapay Zeka Önerileri", ln=True, align='C')
    pdf.ln(10)

    for crop, score, reasons in recommendations:
        pdf.set_font("Arial", size=12, style='B')
        pdf.cell(200, 10, txt=f"Ürün: {crop} (Skor: {score:.2f})", ln=True)
        pdf.set_font("Arial", size=10)
        for key, reason in reasons.items():
            pdf.cell(200, 10, txt=f"  - {key.capitalize()}: {reason}", ln=True)
        pdf.ln(5)

    pdf.output(filename)
    print(f"PDF raporu başarıyla kaydedildi: {filename}")

# Tahmin kodu
if __name__ == "__main__":
    # Örnek ürün ve çevresel veriler
    crop_data = [
        CropData("Buğday", 24, 55, 180, 6.0, 7),
        CropData("Mısır", 28, 60, 200, 6.5, 6),
        CropData("Pirinç", 30, 80, 250, 6.0, 5)
    ]
    environmental_data = EnvironmentalData(25, 60, 200, 6.5, 35, 3)

    # Tahmin işlemi
    model = CropPredictionModel(crop_data)
    recommendations = model.predict_best_crops(environmental_data)

    # Önerileri yazdırma
    print("\n=== Akıllı Tarım Yapay Zeka Önerileri ===\n")
    for crop, score, reasons in recommendations:
        print(f"Ürün: {crop} (Skor: {score:.2f})")
        print("Nedenler:")
        for key, reason in reasons.items():
            print(f"  - {key.capitalize()}: {reason}")
        print()

    # PDF kaydetme
    save_recommendations_to_pdf(recommendations)
