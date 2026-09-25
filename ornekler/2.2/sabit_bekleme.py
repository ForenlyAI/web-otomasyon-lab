"""Ders 2.2 — Sabit bekleme neden kırılgan?

gecikmeli.html listesi 2–4 saniye içinde (her seferinde farklı) yüklenir.
Sayfayı beş kez açar; her seferinde AYNI sayfada:
  a) 2,5 saniye sabit bekleyip (time.sleep) öğeleri sayar  → bazen 0, bazen 6
  b) sonra açık beklemeyle (WebDriverWait) sayar            → her seferinde 6
Karşılaştırma için sayfanın o seferki gecikmesini de yazdırır.

Önce sunucuyu açın:        uv run python sunucu.py
Sonra çalıştırın:          uv run python ornekler/2.2/sabit_bekleme.py
"""

import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

ADRES = "http://localhost:8000/gecikmeli.html"

secenekler = webdriver.ChromeOptions()
if os.environ.get("BASLIKSIZ") == "1":
    secenekler.add_argument("--headless")
secenekler.add_argument("--window-size=1280,800")

driver = webdriver.Chrome(options=secenekler)
try:
    for deneme in range(1, 6):
        driver.get(ADRES)
        gecikme = driver.find_element(By.TAG_NAME, "body").get_attribute("data-gecikme-ms")

        # a) Sabit bekleme: süre yetmezse liste boş, fazlaysa zaman boşa.
        time.sleep(2.5)
        sabit = len(driver.find_elements(By.CSS_SELECTOR, "#liste li.oge"))

        # b) Aynı sayfada açık bekleme: öğe görünene kadar, en fazla 10 saniye.
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#liste li.oge"))
        )
        acik = len(driver.find_elements(By.CSS_SELECTOR, "#liste li.oge"))

        print(f"Deneme {deneme} · liste {gecikme} ms'de geldi · "
              f"sabit 2,5 sn → {sabit} öğe · açık bekleme → {acik} öğe")
finally:
    driver.quit()
