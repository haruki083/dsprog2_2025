from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import sqlite3
from datetime import date

app = Flask(__name__)
CORS(app)

DB_FILE = "weather.db"

# ---------------------------
# 今日の天気取得＆保存
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
        today = date.today().isoformat()

        # --- DBに保存 ---
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO weather (area_code, area_name, weather)
            VALUES (?, ?, ?)
        """, (area, area_name, weather_text))
        conn.commit()
        conn.close()

        return jsonify({
            "area": area_name,
            "date": today,
            "weather": weather_text,
            "source": "気象庁"
        })

    except Exception as e:
        print("ERROR in /weather:", e)
        return jsonify({"error": "weather fetch failed"}), 500


# ---------------------------
# 過去天気取得
# ---------------------------
@app.route("/history")
def history():
    area = request.args.get("area")
    day = request.args.get("date")
    if not area or not day:
        return jsonify({"error": "area and date are required"}), 400

    try:
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute("""
            SELECT area_name, weather, created_at
            FROM weather
            WHERE area_code = ? AND DATE(created_at) = ?
            ORDER BY created_at DESC
            LIMIT 1
        """, (area, day))
        row = cur.fetchone()
        conn.close()

        if row:
            return jsonify({
                "area": row[0],
                "date": day,
                "weather": row[1]
            })
        else:
            return jsonify({"error": "no data"}), 404

    except Exception as e:
        print("ERROR in /history:", e)
        return jsonify({"error": "history fetch failed"}), 500


# ---------------------------
# 有効な地域コード一覧
# ---------------------------
@app.route("/areas")
def areas():
    try:
        area_url = "https://www.jma.go.jp/bosai/common/const/area.json"
        area_data = requests.get(area_url, timeout=5).json()

        offices = area_data["offices"]
        valid_areas = []

        for code, info in offices.items():
            forecast_url = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{code}.json"
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
