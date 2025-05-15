import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# Heroku buildpack değişkenleri
chrome_bin = os.getenv("GOOGLE_CHROME_BIN")
chrome_driver = os.getenv("CHROMEDRIVER_PATH")

def capture_chart(symbol: str, tf: str) -> str:
    options = webdriver.ChromeOptions()
    if chrome_bin:
        options.binary_location = chrome_bin
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(chrome_driver) if chrome_driver else Service()
    driver = webdriver.Chrome(service=service, options=options)

    url = f"https://www.tradingview.com/chart/?symbol=BINANCE%3A{symbol}&interval={tf}"
    driver.get(url)
    time.sleep(8)  # grafik tamamen yüklensin

    os.makedirs("charts", exist_ok=True)
    path = f"charts/{symbol}_{tf}.png"
    driver.save_screenshot(path)
    driver.quit()
    return path
