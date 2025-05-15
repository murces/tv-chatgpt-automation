import os
from flask import Flask, request, jsonify, render_template
from screenshot import capture_chart
from analysis import analyze_image

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/trigger-analysis", methods=["POST"])
def trigger():
    print("🟢 [DEBUG] trigger-analysis başladı")
    data = request.get_json(silent=True) or {}
    symbol = data.get("symbol")
    tf = data.get("tf")

    print(f"🟢 [DEBUG] symbol={symbol}, tf={tf}")
    # 1) Ekran görüntüsünü al
    image_path = capture_chart(symbol, tf)
    print(f"🟢 [DEBUG] screenshot başarıyla alındı: {image_path}")

    # 2) OpenAI analizine gönder
    analysis = analyze_image(image_path, f"{symbol} {tf} chart analysis")
    print("🟢 [DEBUG] OpenAI analizi tamamlandı")

    return jsonify({"analysis": analysis})

    # 1) Grafiği yakala
    image_path = capture_chart(symbol, tf)
    # 2) OpenAI API ile analiz et
    analysis_text = analyze_image(image_path, f"{symbol} {tf} chart analysis")

    return jsonify({"analysis": analysis_text})

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 5000))
    app.run(host=host, port=port)
