import time
import board
import busio
import adafruit_bme280.basic as adafruit_bme280
import adafruit_ssd1306

from PIL import Image, ImageDraw, ImageFont

# ------------------------
# Set up I2C
# ------------------------
i2c = busio.I2C(board.SCL, board.SDA)

# BME280 sensor
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=0x76)

# OLED display (128x64)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)

# Clear display
oled.fill(0)
oled.show()

width = oled.width
height = oled.height

image = Image.new("1", (width, height))
draw = ImageDraw.Draw(image)

font = ImageFont.load_default()

while True:

    # Clear image
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    # Read sensor
    temp = bme280.temperature
    humidity = bme280.relative_humidity
    pressure = bme280.pressure

    # Draw text
    draw.text((0, 0), "Weather Station", font=font, fill=255)
    draw.text((0, 18), f"Temp: {temp:.1f} C", font=font, fill=255)
    draw.text((0, 34), f"Hum : {humidity:.1f} %", font=font, fill=255)
    draw.text((0, 50), f"Pres: {pressure:.1f}", font=font, fill=255)

    oled.image(image)
    oled.show()

    time.sleep(2)
