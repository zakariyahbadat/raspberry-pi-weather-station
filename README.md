# Raspberry Pi Weather Station

A complete weather monitoring system built with a Raspberry Pi 3B and BME280
environmental sensor, developed summer 2026 as part of a self-directed
engineering portfolio project.

## Hardware
- Raspberry Pi 3B (2015)
- BME280 temperature, humidity and barometric pressure sensor (I2C 0x76)
- SSD1306 0.96" OLED display 128x64 (I2C 0x3C)

## Features
- Live temperature, humidity and barometric pressure readings
- OLED multi-screen interface with automatic page cycling
- Temperature, humidity and pressure history graphs on OLED
- Basic weather forecasting from pressure trend
- Statistics page
- Live clock
- Flask web dashboard (local network)
- Cloud deployment via Railway
- CSV data logging
- Overnight data collection and matplotlib visualisation

## Wiring

### BME280
| BME280 | Pi Pin |
|--------|--------|
| VIN | Pin 1 (3.3V) |
| GND | Pin 6 |
| SDA | Pin 3 (GPIO 2) |
| SCL | Pin 5 (GPIO 3) |

### SSD1306 OLED
| OLED | Pi Pin |
|------|--------|
| VCC | Pin 1 (3.3V) |
| GND | Pin 6 |
| SDA | Pin 3 (GPIO 2) |
| SCL | Pin 5 (GPIO 3) |

Both devices share the I2C bus.

## Setup
```bash
python3 -m venv ~/pienv
source ~/pienv/bin/activate
pip install adafruit-circuitpython-bme280 adafruit-circuitpython-ssd1306 flask matplotlib
```

## Version History
| Version | Description |
|---------|-------------|
| v1 | Terminal output of sensor readings |
| v2 | CSV logging every 30 seconds |
| v3 | Matplotlib data visualisation |
| v4 | Flask local web dashboard |
| v5 | Cloud deployment via Railway |
| v6 | OLED multi-screen interface with graphs and forecasting |

## Live Dashboard
[raspberry-pi-projects-production.up.railway.app](https://raspberry-pi-projects-production.up.railway.app)

## Roadmap
- [ ] Professional OLED UI v2 with pixel weather icons
- [ ] Database logging
- [ ] Online weather comparison
- [ ] Historical analytics
- [ ] Complete smart weather station

## Author
Zakariyah — London, 2026
