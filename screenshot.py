import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# Buildpack tarafından ayarlanan ikincil yollar
CHROME_BINARY = os.getenv("GOOGLE_CHROME_BIN")
CHROME_DRIVER = os.getenv("CHROMEDRIVER_PATH") or "/app/.chromedriver/bin/chromedriver"

def capture_chart(symbol: str, tf: str) -> str:
    # Ayarlar
    options = webdriver.ChromeOptions()
    options.binary_location = CHROME_BINARY
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    url = f"https://www.tradingview.com/chart/?symbol=BINANCE%3A{symbol}&interval={tf}"

    # Tarayıcıyı başlat
    driver = webdriver.Chrome(service=Service(CHROME_DRIVER), options=options)
    driver.get(url)
    # Grafik tam yüklensin diye bekle
    time.sleep(8)

    # Ekran görüntüsü
    os.makedirs("charts", exist_ok=True)
    path = f"charts/{symbol}_{tf}.png"
    driver.save_screenshot(path)
    driver.quit()
    return path
