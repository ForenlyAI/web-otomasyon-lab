"""Ders 4.1 — Aynı iş Selenium ile: beklemeyi biz yazarız.

gecikmeli.html'deki "Hazırım" düğmesi tıklanabilir olana kadar
WebDriverWait + element_to_be_clickable ile açıkça bekleriz (Ders 2.2).

Önce sunucuyu açın:  uv run python sunucu.py
Sonra:               BASLIKSIZ=1 uv run python ornekler/4.1/selenium_bekleme.py
"""

import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

secenekler = webdriver.ChromeOptions()
if os.environ.get("BASLIKSIZ") == "1":
    secenekler.add_argument("--headless=new")
driver = webdriver.Chrome(options=secenekler)  # sürücüyü Selenium Manager bulur
try:
    driver.get("http://localhost:8000/gecikmeli.html")
    basla = time.perf_counter()
    bekle = WebDriverWait(driver, 10)
    dugme = bekle.until(EC.element_to_be_clickable((By.ID, "hazir")))  # açık bekleme
    dugme.click()
    print(f"Düğmeye tıklandı · geçen süre {time.perf_counter() - basla:.1f} sn")
    bekle.until(lambda d: len(d.find_elements(By.CSS_SELECTOR, "#liste li.oge")) == 6)
    print("Listede öğe sayısı:", len(driver.find_elements(By.CSS_SELECTOR, "#liste li.oge")))
finally:
    driver.quit()
