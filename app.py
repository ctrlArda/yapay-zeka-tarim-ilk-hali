from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Örnek ürün listesi
products = ["Buğday", "Mısır", "Pamuk", "Ayçiçeği"]

# Yapay zekâ öneri fonksiyonu
def get_recommendations(selected_product):
    recommendations = {
        "Buğday": "Toprağı önceden sürün ve organik gübre kullanın.",
        "Mısır": "Damlama sulama sistemi önerilir.",
        "Pamuk": "Erken ekim yapın ve sıcaklık takibini önemseyin.",
        "Ayçiçeği": "Azotlu gübre miktarını artırabilirsiniz."
    }
    return recommendations.get(selected_product, "Bu ürün için öneri bulunamadı.")

@app.route("/")
def index():
    return render_template("index.html", products=products)

@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.json
    selected_product = data.get("product")
    if selected_product:
        recommendation = get_recommendations(selected_product)
        return jsonify({"recommendation": recommendation})
    return jsonify({"error": "Ürün seçimi yapılmadı."}), 400

if __name__ == "__main__":
    app.run(debug=True)