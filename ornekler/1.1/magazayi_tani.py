"""Ders 1.1 — Pratik Mağaza'yı tanıyın.

Alıştırma sitesinin ana sayfasını ve robots.txt dosyasını açar, robots.txt
kurallarını terminale yazdırır, iki sayfanın ekran görüntüsünü kaydeder.
Bu derste henüz kod yazmıyoruz; bu betik yalnızca siteyi ve kurallarını gösterir.

Önce sunucuyu açın:        uv run python sunucu.py
Sonra çalıştırın:          uv run python ornekler/1.1/magazayi_tani.py
Pencere açılmadan:         BASLIKSIZ=1 uv run python ornekler/1.1/magazayi_tani.py
"""

import os
import sys
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from araclar.ekran import selenium_kaydet  # noqa: E402

ADRES = "http://localhost:8000"

secenekler = webdriver.ChromeOptions()
if os.environ.get("BASLIKSIZ") == "1":
    secenekler.add_argument("--headless")
secenekler.add_argument("--window-size=1280,800")

driver = webdriver.Chrome(options=secenekler)
try:
    # 1) Mağazanın ana sayfası: botlarımızı yazacağımız alıştırma sitesi.
    driver.get(ADRES)
    print("Site:", driver.title)
    print("Ürün sayısı:", driver.find_element(By.ID, "toplam-urun").text)
    selenium_kaydet(driver, "1.1", "01-ana-sayfa")

    # 2) robots.txt: sitenin botlardan ricası. Kibar bot işe buradan başlar.
    driver.get(ADRES + "/robots.txt")
    kurallar = driver.find_element(By.TAG_NAME, "body").text
    print("robots.txt kuralları:")
    for satir in kurallar.splitlines():
        if satir and not satir.startswith("#"):
            print("  " + satir)
    # Ekran görüntüsünde okunsun diye yakınlaştır (tarayıcıda Ctrl + gibi).
    driver.execute_script("document.body.style.zoom = '2.2'")
    selenium_kaydet(driver, "1.1", "02-robots")

    # 3) CAPTCHA sayfası: bu kursta bot burada DURUR ve insana haber verir.
    driver.get(ADRES + "/captcha.html")
    if driver.find_elements(By.CSS_SELECTOR, "[data-bot-kontrolu]"):
        print("Bot kontrolü görüldü: dur ve insana haber ver.")
    selenium_kaydet(driver, "1.1", "03-captcha")
finally:
    driver.quit()
