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
    print("🟢 [DEBUG] trigger-analysis başladı")        # ← EKLENDİ
    data = request.get_json(silent=True) or {}
    print(f"🟢 [DEBUG] Gelen JSON: {data}")              # ← EKLENDİ
    symbol = data.get("symbol", None)
    tf = data.get("tf", None)
    print(f"🟢 [DEBUG] symbol={symbol}, tf={tf}")        # ← EKLENDİ

    # 1) Grafiği yakala
    image_path = capture_chart(symbol, tf)
    # 2) OpenAI API ile analiz et
    analysis_text = analyze_image(image_path, f"{symbol} {tf} chart analysis")

    return jsonify({"analysis": analysis_text})

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 5000))
    app.run(host=host, port=port)
