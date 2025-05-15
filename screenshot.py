import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# Buildpack tarafından tanımlanmış çevresel değişkenler
chrome_bin = os.getenv("GOOGLE_CHROME_BIN") or os.getenv("CHROME_PATH") or os.getenv("CHROME_SHIM")
chrome_driver = os.getenv("CHROMEDRIVER_PATH")  # genelde buildpack ayarlar

def capture_chart(symbol: str, tf: str) -> str:
    options = webdriver.ChromeOptions()
    if chrome_bin:
        options.binary_location = chrome_bin
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    url = f"https://www.tradingview.com/chart/?symbol=BINANCE%3A{symbol}&interval={tf}"
    service = Service(chrome_driver) if chrome_driver else Service()

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    time.sleep(8)  # grafik tam yüklensin

    os.makedirs("charts", exist_ok=True)
    path = f"charts/{symbol}_{tf}.png"
    driver.save_screenshot(path)
    driver.quit()
    return path
