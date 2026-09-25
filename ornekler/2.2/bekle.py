"""Ders 2.2 — Açık bekleme ve zaman aşımı.

1) iletisim.html formunu doldurup gönderir; yaklaşık 1,5 saniye sonra gelen
   #sonuc kutusunu WebDriverWait ile bekler ve metnini yazdırır. time.sleep yok.
2) Aynı işi bekleme süresi 1 saniyeye düşürülmüş olarak yapar: sonuç
   gelmeden süre dolar; TimeoutException yakalanır, anlaşılır mesaj yazılır.

Not: Örtük bekleme (implicitly_wait) KULLANILMIYOR. Selenium belgeleri
örtük ve açık beklemeyi karıştırmamayı söyler.

Önce sunucuyu açın:        uv run python sunucu.py
Sonra çalıştırın:          uv run python ornekler/2.2/bekle.py
"""

import os
import sys
from pathlib import Path

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from araclar.ekran import selenium_kaydet  # noqa: E402

ADRES = "http://localhost:8000/iletisim.html"

secenekler = webdriver.ChromeOptions()
if os.environ.get("BASLIKSIZ") == "1":
    secenekler.add_argument("--headless")
secenekler.add_argument("--window-size=1280,800")


def formu_gonder(driver):
    driver.get(ADRES)
    driver.find_element(By.ID, "ad").send_keys("Deniz Deneme")            # ÖRNEK VERİ
    driver.find_element(By.ID, "eposta").send_keys("deniz@example.com")   # ÖRNEK VERİ
    Select(driver.find_element(By.ID, "konu")).select_by_visible_text("Kargo")
    driver.find_element(By.ID, "mesaj").send_keys("Siparişim hangi kargoda?")
    driver.find_element(By.ID, "kvkk").click()
    driver.find_element(By.ID, "gonder").click()


driver = webdriver.Chrome(options=secenekler)
try:
    # 1) Koşul: #sonuc görünür olsun. En fazla 5 saniye; gelir gelmez devam.
    formu_gonder(driver)
    sonuc = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "sonuc")))
    print("Sonuç geldi:", sonuc.text.replace("\n", " · "))
    selenium_kaydet(driver, "2.2", "02-sonuc")

    # 2) Aynı koşul, 1 saniye sınırla: sonuç 1,5 saniyede geldiği için süre dolar.
    formu_gonder(driver)
    try:
        WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.ID, "sonuc")))
        print("Beklenmedik: sonuç 1 saniyede geldi.")
    except TimeoutException:
        print("Zaman aşımı: sonuç 1 saniye içinde gelmedi, betik düzgünce bitiyor.")
finally:
    driver.quit()
