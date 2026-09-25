"""Ders 2.4 — Çoklu pencere (sekme) ve iframe.

1) pencere.html'deki bağlantı yeni sekme açar. Yeni sekmeyi bekler, ona geçer,
   başlığını ve mesajını okur, sekmeyi kapatıp ana sekmeye döner.
2) Sayfadaki iframe'in içindeki düğmeye, önce çerçeveye geçerek ulaşır;
   tıklar, mesajı okur, sonra ana sayfaya geri çıkar.

Önce sunucuyu açın:        uv run python sunucu.py
Sonra çalıştırın:          uv run python ornekler/2.4/pencere.py
"""

import os
import sys
from pathlib import Path

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from araclar.ekran import selenium_kaydet  # noqa: E402

ADRES = "http://localhost:8000/pencere.html"

secenekler = webdriver.ChromeOptions()
if os.environ.get("BASLIKSIZ") == "1":
    secenekler.add_argument("--headless")
secenekler.add_argument("--window-size=1280,800")

driver = webdriver.Chrome(options=secenekler)
try:
    driver.get(ADRES)
    ana_sekme = driver.current_window_handle      # ana sekmenin tanıtıcısı

    # 1) Yeni sekme: bağlantıya tıkla, ikinci sekme açılana kadar bekle.
    driver.find_element(By.ID, "yeni-sekme-link").click()
    WebDriverWait(driver, 5).until(EC.number_of_windows_to_be(2))
    yeni = [t for t in driver.window_handles if t != ana_sekme][0]
    driver.switch_to.window(yeni)                  # artık yeni sekmeye bakıyoruz
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "sekme-mesaj")))
    print("Yeni sekmenin başlığı:", driver.find_element(By.TAG_NAME, "h1").text)
    print("Yeni sekmedeki mesaj :", driver.find_element(By.ID, "sekme-mesaj").text)
    selenium_kaydet(driver, "2.4", "01-yeni-sekme")
    driver.close()                                 # yeni sekmeyi kapat
    driver.switch_to.window(ana_sekme)             # ana sekmeye dön
    print("Ana sekmeye döndüm:", driver.find_element(By.TAG_NAME, "h1").text)

    # 2) iframe: çerçeveye geçmeden içindeki düğme bulunamaz.
    try:
        driver.find_element(By.ID, "cerceve-dugme")
    except NoSuchElementException:
        print("Çerçeveye girmeden: düğme bulunamadı (beklenen).")
    driver.switch_to.frame("cerceve")              # çerçeveye gir (ad ya da id)
    driver.find_element(By.ID, "cerceve-dugme").click()
    mesaj = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "cerceve-mesaj")))
    print("Çerçevenin içindeki mesaj:", mesaj.text)
    driver.switch_to.default_content()             # ana sayfaya geri çık
    selenium_kaydet(driver, "2.4", "02-iframe")
finally:
    driver.quit()
