from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from datetime import date

app = Flask(__name__)
CORS(app)

# ---------------------------
# 天気取得 API
# ---------------------------
@app.route("/weather")
def weather():
    area = request.args.get("area")

    if not area:
        return jsonify({"error": "area is required"}), 400

    url = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{area}.json"

    try:
        res = requests.get(url, timeout=5)
        res.raise_for_status()
        data = res.json()

        ts = data[0]["timeSeries"][0]
        weather_text = ts["areas"][0]["weathers"][0]
        area_name = ts["areas"][0]["area"]["name"]

        return jsonify({
            "area": area_name,
            "date": date.today().isoformat(),
            "weather": weather_text,
            "source": "気象庁"
        })

    except Exception as e:
        print("ERROR in /weather:", e)
        return jsonify({"error": "weather fetch failed"}), 500


# ---------------------------
# 地域一覧 API（forecast 対応コード自動抽出）
# ---------------------------
@app.route("/areas")
def areas():
    """
    気象庁 area.json を取得し、
    forecast API で実際に 200 OK が返る地域コードのみ返す
    """
    try:
        area_url = "https://www.jma.go.jp/bosai/common/const/area.json"
        area_data = requests.get(area_url, timeout=5).json()

        offices = area_data["offices"]
        valid_areas = []

        for code, info in offices.items():
            forecast_url = (
                f"https://www.jma.go.jp/bosai/forecast/data/forecast/{code}.json"
            )
            res = requests.get(forecast_url, timeout=5)

            if res.status_code == 200:
                valid_areas.append({
                    "code": code,
                    "name": info["name"]
                })

        return jsonify(valid_areas)

    except Exception as e:
        print("ERROR in /areas:", e)
        return jsonify({"error": "areas fetch failed"}), 500


if __name__ == "__main__":
    app.run(debug=True)
