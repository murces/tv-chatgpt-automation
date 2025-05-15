import os
from flask import Flask, request, jsonify, render_template
from screenshot import capture_chart
from analysis import analyze_images
from concurrent.futures import ThreadPoolExecutor

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
    tasks = []
    # ThreadPool ile eş zamanlı
    with ThreadPoolExecutor(max_workers=6) as executor:
        for sym in symbols:
            for tf in timeframes:
                tasks.append(executor.submit(capture_chart, sym, tf))
        # Hepsi bitene kadar bekle
        images_payload = []
        for future in tasks:
            path = future.result()
            # path stringi "charts/SYMTF.png" → sym, tf çıkartmak için:
            fname = os.path.basename(path).rsplit(".", 1)[0]  # e.g. "BTCUSDT_1h"
            sym, tf = fname.split("_")
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
