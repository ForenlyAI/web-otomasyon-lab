"""Ders 1.2 — Kurulum testi.

Selenium sürümünü yazdırır, Chrome'u açar ve Pratik Mağaza'ya gider.
Sürücüyü (ChromeDriver) elle indirmiyoruz: Selenium Manager uygun sürümü
kendisi bulur, gerekirse indirir. Hangi tarayıcı ve sürücü sürümünün
kullanıldığını da terminale yazdırır.

Önce sunucuyu açın:        uv run python sunucu.py
Sonra çalıştırın:          uv run python ornekler/1.2/kurulum_testi.py
Pencere açılmadan:         BASLIKSIZ=1 uv run python ornekler/1.2/kurulum_testi.py
"""

import os
import sys
from pathlib import Path

import selenium
from selenium import webdriver

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from araclar.ekran import selenium_kaydet  # noqa: E402

ADRES = "http://localhost:8000"

print("Selenium sürümü:", selenium.__version__)

secenekler = webdriver.ChromeOptions()
if os.environ.get("BASLIKSIZ") == "1":
    secenekler.add_argument("--headless")
secenekler.add_argument("--window-size=1280,800")

# Sürücü yolu vermiyoruz: Selenium Manager devreye girer.
driver = webdriver.Chrome(options=secenekler)
try:
    yetenek = driver.capabilities
    print("Tarayıcı:", yetenek["browserName"], yetenek["browserVersion"])
    surucu = yetenek["chrome"]["chromedriverVersion"].split(" ")[0]
    print("Sürücü (Selenium Manager buldu):", surucu)

    driver.get(ADRES)
    print("Açılan sayfa:", driver.title)
    selenium_kaydet(driver, "1.2", "03-magaza")
    print("Kurulum tamam.")
finally:
    driver.quit()
