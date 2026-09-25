"""Ders 2.1 — Giriş formu: oturum açma ve hatalı parola.

Parola koda YAZILMAZ; ortam değişkeninden okunur:
    macOS / Linux:  export PM_SIFRE=pratik123
    PowerShell:     $env:PM_SIFRE = "pratik123"
(pratik123 yalnızca Pratik Mağaza'nın deneme hesabının parolasıdır.)

1) Doğru parolayla giriş yapar, hesap sayfasındaki karşılama metnini yazdırır.
2) Yanlış parolayla dener, sayfadaki hata mesajını yazdırır.

Önce sunucuyu açın:        uv run python sunucu.py
Sonra çalıştırın:          uv run python ornekler/2.1/giris.py
"""

import os
import sys
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from araclar.ekran import selenium_kaydet  # noqa: E402

ADRES = "http://localhost:8000"
KULLANICI = "ogrenci"
SIFRE = os.environ.get("PM_SIFRE")
if not SIFRE:
    sys.exit("PM_SIFRE ortam değişkeni yok. Önce: export PM_SIFRE=pratik123")

secenekler = webdriver.ChromeOptions()
if os.environ.get("BASLIKSIZ") == "1":
    secenekler.add_argument("--headless")
secenekler.add_argument("--window-size=1280,800")


def giris_yap(driver, kullanici, sifre):
    driver.get(ADRES + "/giris.html")
    for kimlik, metin in (("kullanici", kullanici), ("sifre", sifre)):
        alan = driver.find_element(By.ID, kimlik)
        alan.clear()
        alan.send_keys(metin)
    driver.find_element(By.ID, "giris-dugme").click()


driver = webdriver.Chrome(options=secenekler)
try:
    # 1) Doğru parola → hesap sayfası. Sayfa değişimini kısa bir açık
    #    beklemeyle bekliyoruz (ayrıntısı Ders 2.2'de).
    giris_yap(driver, KULLANICI, SIFRE)
    WebDriverWait(driver, 5).until(EC.text_to_be_present_in_element((By.ID, "karsilama"), KULLANICI))
    print("Giriş başarılı:", driver.find_element(By.ID, "karsilama").text)
    selenium_kaydet(driver, "2.1", "02-hesap")

    # Çıkış yap, sonra yanlış parolayla dene.
    driver.find_element(By.ID, "cikis").click()
    WebDriverWait(driver, 5).until(EC.url_contains("giris.html"))

    # 2) Yanlış parola → sayfada hata mesajı görünür.
    giris_yap(driver, KULLANICI, "yanlis-parola")
    hata = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "hata")))
    print("Yanlış parola:", hata.text)
    selenium_kaydet(driver, "2.1", "03-hata")
finally:
    driver.quit()
