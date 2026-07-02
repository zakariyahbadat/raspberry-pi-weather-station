import time
import math
from collections import deque
from datetime import datetime

import board
import busio
import adafruit_bme280.basic as adafruit_bme280
import adafruit_ssd1306

from PIL import Image, ImageDraw, ImageFont

# =====================================================
# INITIALISE HARDWARE
# =====================================================

i2c = busio.I2C(board.SCL, board.SDA)

bme280 = adafruit_bme280.Adafruit_BME280_I2C(
    i2c,
    address=0x76
)

oled = adafruit_ssd1306.SSD1306_I2C(
    128,
    64,
    i2c,
    addr=0x3C
)

oled.fill(0)
oled.show()

WIDTH = oled.width
HEIGHT = oled.height

image = Image.new("1", (WIDTH, HEIGHT))
draw = ImageDraw.Draw(image)

font_small = ImageFont.load_default()

try:
    font_large = ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        22
    )
except:
    font_large = ImageFont.load_default()

# =====================================================
# HISTORY
# =====================================================

MAX_HISTORY = 120

temp_history = deque(maxlen=MAX_HISTORY)
humidity_history = deque(maxlen=MAX_HISTORY)
pressure_history = deque(maxlen=MAX_HISTORY)

screen = 0
last_screen_change = time.time()

SCREEN_TIME = 6

# =====================================================
# DRAW HEADER
# =====================================================

def draw_header(title):

    draw.rectangle((0, 0, WIDTH, 12), fill=255)

    draw.text(
        (3, 2),
        title,
        font=font_small,
        fill=0
    )

# =====================================================
# DRAW GRAPH
# =====================================================

def draw_graph(data, y_top, height):

    if len(data) < 2:
        return

    values = list(data)

    minimum = min(values)
    maximum = max(values)

    if maximum == minimum:
        maximum += 1

    graph_width = WIDTH - 4

    step = graph_width / (len(values) - 1)

    previous = None

    for i, value in enumerate(values):

        x = 2 + i * step

        y = (
            y_top + height
            - ((value - minimum) / (maximum - minimum))
            * height
        )

        if previous is not None:
            draw.line(
                (
                    previous[0],
                    previous[1],
                    x,
                    y
                ),
                fill=255
            )

        previous = (x, y)

# =====================================================
# WEATHER FORECAST
# =====================================================

def get_forecast():

    if len(pressure_history) < 10:
        return "Collecting..."

    change = pressure_history[-1] - pressure_history[0]

    if change > 1:
        return "Improving ↑"

    elif change < -1:
        return "Rain Possible ↓"

    else:
        return "Stable →"

# =====================================================
# STATISTICS
# =====================================================

def average(values):
    if len(values) == 0:
        return 0
    return sum(values) / len(values)
# =====================================================
# DASHBOARD SCREEN
# =====================================================

def draw_dashboard(temp, humidity, pressure):

    draw_header("LONDON WEATHER")

    draw.text(
        (20, 16),
        f"{temp:.1f}°C",
        font=font_large,
        fill=255
    )

    draw.text(
        (4, 44),
        f"Hum {humidity:.1f}%",
        font=font_small,
        fill=255
    )

    draw.text(
        (68, 44),
        f"{pressure:.1f}",
        font=font_small,
        fill=255
    )

    clock = datetime.now().strftime("%H:%M:%S")

    draw.text(
        (28, 56),
        clock,
        font=font_small,
        fill=255
    )


# =====================================================
# TEMPERATURE GRAPH
# =====================================================

def draw_temperature_screen(temp):

    draw_header("TEMPERATURE")

    draw.text(
        (4, 16),
        f"{temp:.1f}°C",
        font=font_small,
        fill=255
    )

    draw_graph(
        temp_history,
        28,
        30
    )


# =====================================================
# HUMIDITY GRAPH
# =====================================================

def draw_humidity_screen(humidity):

    draw_header("HUMIDITY")

    draw.text(
        (4, 16),
        f"{humidity:.1f} %",
        font=font_small,
        fill=255
    )

    draw_graph(
        humidity_history,
        28,
        30
    )


# =====================================================
# PRESSURE GRAPH
# =====================================================

def draw_pressure_screen(pressure):

    draw_header("PRESSURE")

    draw.text(
        (4, 16),
        f"{pressure:.1f} hPa",
        font=font_small,
        fill=255
    )

    draw_graph(
        pressure_history,
        28,
        30
    )


# =====================================================
# STATISTICS SCREEN
# =====================================================

def draw_statistics():

    draw_header("STATISTICS")

    if len(temp_history) == 0:
        draw.text(
            (18, 28),
            "Collecting data...",
            font=font_small,
            fill=255
        )
        return

    draw.text(
        (2, 16),
        f"Min {min(temp_history):.1f}C",
        font=font_small,
        fill=255
    )

    draw.text(
        (2, 28),
        f"Max {max(temp_history):.1f}C",
        font=font_small,
        fill=255
    )

    draw.text(
        (2, 40),
        f"Avg {average(temp_history):.1f}C",
        font=font_small,
        fill=255
    )

    draw.text(
        (2, 52),
        f"Hum {average(humidity_history):.0f}%",
        font=font_small,
        fill=255
    )


# =====================================================
# FORECAST SCREEN
# =====================================================

def draw_forecast(pressure):

    draw_header("FORECAST")

    forecast = get_forecast()

    draw.text(
        (6, 18),
        forecast,
        font=font_small,
        fill=255
    )

    draw.text(
        (6, 34),
        f"{pressure:.1f} hPa",
        font=font_small,
        fill=255
    )

    if len(pressure_history) > 5:

        trend = pressure_history[-1] - pressure_history[-5]

        if trend > 0.4:
            arrow = "↑ Rising"

        elif trend < -0.4:
            arrow = "↓ Falling"

        else:
            arrow = "→ Stable"

        draw.text(
            (6, 50),
            arrow,
            font=font_small,
            fill=255
        )   
# =====================================================
# DAILY STATISTICS
# =====================================================

today = datetime.now().date()

day_min = None
day_max = None


def update_daily_stats(temp):

    global today
    global day_min
    global day_max

    now = datetime.now().date()

    if now != today:
        today = now
        day_min = temp
        day_max = temp

    if day_min is None or temp < day_min:
        day_min = temp

    if day_max is None or temp > day_max:
        day_max = temp


# =====================================================
# GRAPH GRID
# =====================================================

def draw_grid(y_top, height):

    for i in range(4):

        y = y_top + int(i * height / 3)

        draw.line(
            (0, y, WIDTH, y),
            fill=80
        )


# =====================================================
# IMPROVED GRAPH
# =====================================================

def draw_graph(data, y_top, height):

    if len(data) < 2:
        return

    draw_grid(y_top, height)

    values = list(data)

    minimum = min(values)
    maximum = max(values)

    if maximum == minimum:
        maximum += 1

    usable_width = WIDTH - 6

    previous = None

    for i in range(len(values)):

        x = 3 + (usable_width * i) / (len(values) - 1)

        y = (
            y_top
            + height
            - ((values[i] - minimum) / (maximum - minimum))
            * height
        )

        if previous:

            draw.line(
                (
                    previous[0],
                    previous[1],
                    x,
                    y
                ),
                fill=255
            )

        previous = (x, y)


# =====================================================
# SIMPLE ICONS
# =====================================================

def draw_temp_icon(x, y):

    draw.ellipse((x, y, x + 5, y + 5), outline=255)
    draw.line((x + 2, y - 4, x + 2, y + 2), fill=255)


def draw_humidity_icon(x, y):

    draw.polygon(
        [
            (x + 3, y),
            (x, y + 5),
            (x + 6, y + 5)
        ],
        outline=255
    )


def draw_pressure_icon(x, y):

    draw.arc(
        (x, y, x + 8, y + 8),
        180,
        360,
        fill=255
    )

    draw.line(
        (x + 4, y + 4, x + 7, y + 2),
        fill=255
    )


# =====================================================
# IMPROVED DASHBOARD
# =====================================================

def draw_dashboard(temp, humidity, pressure):

    draw_header("LONDON WEATHER")

    draw.text(
        (18, 14),
        f"{temp:.1f}°C",
        font=font_large,
        fill=255
    )

    draw_temp_icon(2, 19)
    draw_humidity_icon(2, 39)
    draw_pressure_icon(66, 39)

    draw.text(
        (12, 38),
        f"{humidity:.0f}%",
        font=font_small,
        fill=255
    )

    draw.text(
        (78, 38),
        f"{pressure:.0f}",
        font=font_small,
        fill=255
    )

    draw.text(
        (28, 50),
        datetime.now().strftime("%H:%M:%S"),
        font=font_small,
        fill=255
    )

    draw.text(
        (22, 58),
        datetime.now().strftime("%d %b %Y"),
        font=font_small,
        fill=255
    )


# =====================================================
# BETTER STATISTICS PAGE
# =====================================================

def draw_statistics():

    draw_header("TODAY")

    if day_min is None:
        return

    draw.text(
        (2, 16),
        f"Min : {day_min:.1f}C",
        font=font_small,
        fill=255
    )

    draw.text(
        (2, 28),
        f"Max : {day_max:.1f}C",
        font=font_small,
        fill=255
    )

    draw.text(
        (2, 40),
        f"Avg : {average(temp_history):.1f}C",
        font=font_small,
        fill=255
    )

    draw.text(
        (2, 52),
        f"Readings {len(temp_history)}",
        font=font_small,
        fill=255
    )       
# =====================================================
# MAIN LOOP
# =====================================================

while True:

    # -------------------------------
    # Read sensor values
    # -------------------------------

    temp = bme280.temperature
    humidity = bme280.relative_humidity
    pressure = bme280.pressure

    # -------------------------------
    # Store history
    # -------------------------------

    temp_history.append(temp)
    humidity_history.append(humidity)
    pressure_history.append(pressure)

    # -------------------------------
    # Change screen every few seconds
    # -------------------------------

    if time.time() - last_screen_change > SCREEN_TIME:

        screen += 1

        if screen > 5:
            screen = 0

        last_screen_change = time.time()

    # -------------------------------
    # Clear screen
    # -------------------------------

    draw.rectangle(
        (0, 0, WIDTH, HEIGHT),
        fill=0
    )

    # -------------------------------
    # Draw selected screen
    # -------------------------------

    if screen == 0:

        draw_dashboard(
            temp,
            humidity,
            pressure
        )

    elif screen == 1:

        draw_temperature_screen(temp)

    elif screen == 2:

        draw_humidity_screen(humidity)

    elif screen == 3:

        draw_pressure_screen(pressure)

    elif screen == 4:

        draw_statistics()

    elif screen == 5:

        draw_forecast(pressure)

    # -------------------------------
    # Send image to OLED
    # -------------------------------

    oled.image(image)
    oled.show()

    # -------------------------------
    # Wait before next update
    # -------------------------------

    time.sleep(1)       