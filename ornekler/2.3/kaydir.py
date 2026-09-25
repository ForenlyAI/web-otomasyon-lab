"""Ders 2.3 — JavaScript ile etkileşim: sonsuz kaydırma.

sonsuz.html sayfasının sonuna kaydırdıkça 10 kart daha yüklenir (en fazla 50).
Döngü: kaydır → yeni kartları bekle → say. Sayı artmıyorsa sayfanın sonu.

- execute_script ile sayfada JavaScript çalıştırılır; "return" ile değer döner.
- Kart sayısı artsın diye açık bekleme kullanılır (time.sleep yok).
- JavaScript ile tıklama kullanıcı gibi davranmaz; yalnızca son çare.

Önce sunucuyu açın:        uv run python sunucu.py
Sonra çalıştırın:          uv run python ornekler/2.3/kaydir.py
"""

import os
import sys
from pathlib import Path

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from araclar.ekran import selenium_kaydet  # noqa: E402

ADRES = "http://localhost:8000/sonsuz.html"
KART = (By.CSS_SELECTOR, "#kartlar article.kart")

secenekler = webdriver.ChromeOptions()
if os.environ.get("BASLIKSIZ") == "1":
    secenekler.add_argument("--headless")
secenekler.add_argument("--window-size=1280,800")

driver = webdriver.Chrome(options=secenekler)
try:
    driver.get(ADRES)
    # JavaScript'ten değer almak: "return" ile sayfa yüksekliği Python'a gelir.
    yukseklik = driver.execute_script("return document.body.scrollHeight;")
    print("Başta sayfa yüksekliği:", yukseklik, "piksel")

    onceki = len(driver.find_elements(*KART))
    print("Başta kart:", onceki)
    while True:
        # Sayfanın en altına kaydır.
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        try:
            # Kart sayısı artana kadar en fazla 3 saniye bekle.
            WebDriverWait(driver, 3).until(lambda d: len(d.find_elements(*KART)) > onceki)
        except TimeoutException:
            print("Yeni kart gelmedi, sayfanın sonu.")
            break
        simdi = len(driver.find_elements(*KART))
        print(f"Kaydırdım: {onceki} → {simdi} kart")
        onceki = simdi

    print("Toplam kart:", onceki)
    selenium_kaydet(driver, "2.3", "03-son")

    # Belirli bir elementi görünür alana getirmek: kart 25'e kaydır.
    kart = driver.find_element(By.CSS_SELECTOR, "article.kart[data-no='25']")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", kart)
    print("Görünür alana getirildi:", kart.find_element(By.TAG_NAME, "h3").text)
finally:
    driver.quit()
