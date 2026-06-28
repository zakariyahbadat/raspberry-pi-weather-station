from flask import Flask, jsonify, render_template_string
import random
import threading
import time

app = Flask(__name__)

# Simulates sensor data for cloud deployment
latest = {"temp": 22.0, "humidity": 55.0, "pressure": 1013.0}

def simulate_sensor():
    while True:
        latest["temp"] = round(22 + random.uniform(-0.5, 0.5), 1)
        latest["humidity"] = round(55 + random.uniform(-1, 1), 1)
        latest["pressure"] = round(1013 + random.uniform(-0.5, 0.5), 1)
        time.sleep(5)

threading.Thread(target=simulate_sensor, daemon=True).start()

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Zak's Weather Station</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: sans-serif; background: #111; color: white; text-align: center; padding: 40px; }
        h1 { font-size: 2em; margin-bottom: 10px; }
        p { color: #aaa; margin-bottom: 40px; }
        .grid { display: flex; justify-content: center; gap: 30px; flex-wrap: wrap; }
        .card { background: #222; border-radius: 16px; padding: 30px 40px; min-width: 150px; }
        .value { font-size: 3em; font-weight: bold; }
        .label { font-size: 1em; color: #aaa; margin-top: 8px; }
        .temp .value { color: #ff6b6b; }
        .humidity .value { color: #4ecdc4; }
        .pressure .value { color: #95e77e; }
    </style>
    <script>
        async function update() {
            const res = await fetch('/data');
            const d = await res.json();
            document.getElementById('temp').innerText = d.temp + '°C';
            document.getElementById('humidity').innerText = d.humidity + '%';
            document.getElementById('pressure').innerText = d.pressure + ' hPa';
        }
        setInterval(update, 5000);
        update();
    </script>
</head>
<body>
    <h1>🌤 Zak's Weather Station</h1>
    <p>Raspberry Pi 3B — London</p>
    <div class="grid">
        <div class="card temp">
            <div class="value" id="temp">--</div>
            <div class="label">Temperature</div>
        </div>
        <div class="card humidity">
            <div class="value" id="humidity">--</div>
            <div class="label">Humidity</div>
        </div>
        <div class="card pressure">
            <div class="value" id="pressure">--</div>
            <div class="label">Pressure</div>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/data')
def data():
    return jsonify(latest)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
# Deployed to Railway: raspberry-pi-projects-production.up.railway.app