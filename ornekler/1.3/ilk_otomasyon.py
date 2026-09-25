"""Ders 1.3 — İlk tarayıcı otomasyonu.

Pratik Mağaza'yı açar, arama kutusuna "kulaklık" yazıp Enter'a basar,
sonuç sayısını ve ilk 3 ürünün adını yazdırır, ekran görüntüsü kaydeder.

Önce sunucuyu başka bir terminalde açın:  uv run python sunucu.py
Sonra çalıştırın:                          uv run python ornekler/1.3/ilk_otomasyon.py
Pencere açılmadan (headless) çalıştırmak:  BASLIKSIZ=1 uv run python ornekler/1.3/ilk_otomasyon.py
"""

import os
import sys
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Ekran görüntüsü yardımcısı lab/araclar klasöründe.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from araclar.ekran import selenium_kaydet  # noqa: E402

ADRES = "http://localhost:8000"

secenekler = webdriver.ChromeOptions()
if os.environ.get("BASLIKSIZ") == "1":
    secenekler.add_argument("--headless")  # tarayıcı penceresi açılmaz
secenekler.add_argument("--window-size=1280,800")

# Selenium Manager uygun ChromeDriver'ı kendisi bulur/indirir; elle sürücü kurmak yok.
driver = webdriver.Chrome(options=secenekler)
try:
    driver.get(ADRES)
    print("Sayfa başlığı:", driver.title)
    selenium_kaydet(driver, "1.3", "01-ana-sayfa")

    # Arama kutusunu bul, kelimeyi yaz ve Enter'a bas (klavyedeki gibi).
    # Aynı işi Ara düğmesine tıklayarak da yapabilirsiniz:
    #   driver.find_element(By.ID, "ara-dugme").click()
    arama_kutusu = driver.find_element(By.ID, "arama")
    arama_kutusu.send_keys("kulaklık" + Keys.ENTER)

    # Sonuç yazısı "... ürün bulundu" olana kadar en fazla 5 saniye bekle.
    # (Bekleme stratejilerini Ders 2.2'de ayrıntılı göreceğiz.)
    WebDriverWait(driver, 5).until(
        EC.text_to_be_present_in_element((By.ID, "sonuc-sayisi"), "bulundu")
    )
    print("Sonuç:", driver.find_element(By.ID, "sonuc-sayisi").text)

    urun_adlari = driver.find_elements(By.CSS_SELECTOR, "#urun-listesi .urun-ad")
    print("İlk 3 ürün:")
    for sira, urun in enumerate(urun_adlari[:3], start=1):
        print(f"  {sira}. {urun.text}")

    yol = selenium_kaydet(driver, "1.3", "02-arama-sonucu")
    print("Ekran görüntüsü kaydedildi:", yol.relative_to(Path(__file__).resolve().parents[2]))
finally:
    # Hata olsa bile tarayıcıyı kapat: iskeletin son adımı.
    driver.quit()
