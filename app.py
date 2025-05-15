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
    data = request.get_json() or {}
    symbol = data.get("symbol")
    tf = data.get("tf")
    if not symbol or not tf:
        return jsonify({"analysis": "Error: Eksik parametre."}), 400

    # Screenshot al
    image_path = capture_chart(symbol, tf)
    # Analiz et
    analysis = analyze_image(image_path, f"{symbol} {tf} chart analysis")
    return jsonify({"analysis": analysis})

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 5000))
    app.run(host=host, port=port)
