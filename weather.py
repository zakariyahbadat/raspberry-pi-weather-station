import board
import adafruit_bme280.basic as adafruit_bme280
import time
import csv
from datetime import datetime

i2c = board.I2C()
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=0x76)

with open("weather_log.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["timestamp", "temp_c", "humidity_%", "pressure_hpa"])

while True:
    temp = bme280.temperature
    humidity = bme280.relative_humidity
    pressure = bme280.pressure
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"{timestamp} | Temp: {temp:.1f}°C | Humidity: {humidity:.1f}% | Pressure: {pressure:.1f}hPa")

    with open("weather_log.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, f"{temp:.1f}", f"{humidity:.1f}", f"{pressure:.1f}"])

    time.sleep(30)

