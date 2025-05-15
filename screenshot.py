 import os
 import asyncio
-from pyppeteer import launch
+from pyppeteer import launch

 # Heroku chrome-for-testing buildpack’ının sağladığı EXE yolu:
 CHROME_PATH = os.getenv("GOOGLE_CHROME_BIN")  # Buildpack otomatik olarak bu değişkeni ayarlar

 # Chrome ve driver buildpack’leriyle uyumlu args
 LAUNCH_ARGS = [
     "--no-sandbox",
     "--disable-setuid-sandbox",
     "--disable-dev-shm-usage",
     "--single-process",
     "--disable-gpu",
 ]

 async def _capture(symbol: str, tf: str, output_path: str):
-    browser = await launch(args=LAUNCH_ARGS)
+    browser = await launch(
+        executablePath=CHROME_PATH,
+        headless=True,
+        args=LAUNCH_ARGS
+    )
     page = await browser.newPage()
     url = f"https://www.tradingview.com/chart/?symbol=BINANCE%3A{symbol}&interval={tf}"
     await page.goto(url, {"waitUntil": "networkidle2"})
     await asyncio.sleep(10)
     os.makedirs(os.path.dirname(output_path), exist_ok=True)
     await page.screenshot({"path": output_path, "fullPage": True})
     await browser.close()

 def capture_chart(symbol: str, tf: str) -> str:
     fname = f"charts/{symbol}_{tf}.png"
     asyncio.get_event_loop().run_until_complete(_capture(symbol, tf, fname))
     return fname
