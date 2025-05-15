import os
import asyncio
from pyppeteer import launch

# Chrome ve driver buildpack'leriyle uyumlu args
LAUNCH_ARGS = [
    "--no-sandbox",
    "--disable-setuid-sandbox",
    "--disable-dev-shm-usage",
    "--single-process",
    "--disable-gpu",
]

async def _capture(symbol: str, tf: str, output_path: str):
    browser = await launch(args=LAUNCH_ARGS)
    page = await browser.newPage()
    url = f"https://www.tradingview.com/chart/?symbol=BINANCE%3A{symbol}&interval={tf}"
    await page.goto(url, {"waitUntil": "networkidle2"})
    # Grafiğin tam yüklenmesi için kısa bekleme
    await asyncio.sleep(10)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    await page.screenshot({"path": output_path, "fullPage": True})
    await browser.close()

def capture_chart(symbol: str, tf: str) -> str:
    fname = f"charts/{symbol}_{tf}.png"
    asyncio.get_event_loop().run_until_complete(_capture(symbol, tf, fname))
    return fname
