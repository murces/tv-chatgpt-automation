import os
from flask import Flask, request, jsonify, render_template
from screenshot import capture_chart
from analysis import analyze_images

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/trigger-analysis", methods=["POST"])
def trigger():
    data = request.get_json() or {}
    symbols = data.get("symbols", [])
    if not symbols:
        return jsonify({"analysis": "Error: Hiç coin seçilmedi."}), 400

    timeframes = ["5m", "1h", "4h"]
    images_payload = []

    for sym in symbols:
        for tf in timeframes:
            path = capture_chart(sym, tf)
            images_payload.append({
                "symbol": sym,
                "tf": tf,
                "path": path
            })

    analysis = analyze_images(images_payload)
    return jsonify({"analysis": analysis})

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 5000))
    app.run(host=host, port=port)
