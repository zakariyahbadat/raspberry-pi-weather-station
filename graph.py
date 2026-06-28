import csv
import matplotlib.pyplot as plt
from datetime import datetime

timestamps, temps, humidities, pressures = [], [], [], []

with open("weather_log.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        timestamps.append(datetime.strptime(row["timestamp"], "%Y-%m-%d %H:%M:%S"))
        temps.append(float(row["temp_c"]))
        humidities.append(float(row["humidity_%"]))
        pressures.append(float(row["pressure_hpa"]))

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 8), sharex=True)

ax1.plot(timestamps, temps, color="red")
ax1.set_ylabel("Temperature (°C)")
ax1.grid(True)

ax2.plot(timestamps, humidities, color="blue")
ax2.set_ylabel("Humidity (%)")
ax2.grid(True)

ax3.plot(timestamps, pressures, color="green")
ax3.set_ylabel("Pressure (hPa)")
ax3.grid(True)

plt.xlabel("Time")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("weather_graph.png")
plt.show()
