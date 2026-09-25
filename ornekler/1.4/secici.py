"""Ders 1.4 — Element bulma yöntemleri.

1) Ana sayfadaki arama kutusunu dört yolla bulur (ID, NAME, CSS seçici, XPath)
   ve dördünün de AYNI elementi gösterdiğini kontrol eder.
2) Ürün listesinin ilk sayfasında ilk ürünün adını CSS seçici ve XPath ile bulur.
3) find_elements ile sayfadaki bütün ürün adlarını listeler.
4) Sayfa düzenine bağlı (kırılgan) bir XPath'i kararlı olanla karşılaştırır.

Önce sunucuyu açın:        uv run python sunucu.py
Sonra çalıştırın:          uv run python ornekler/1.4/secici.py
Pencere açılmadan:         BASLIKSIZ=1 uv run python ornekler/1.4/secici.py
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
    # 1) Aynı element, dört yol. DevTools'ta gördüğümüz: <input id="arama" name="q" ...>
    driver.get(ADRES)
    yollar = {
        "ID   ": (By.ID, "arama"),
        "NAME ": (By.NAME, "q"),
        "CSS  ": (By.CSS_SELECTOR, "form#arama-formu input"),
        "XPATH": (By.XPATH, "//input[@id='arama']"),
    }
    bulunan = {ad: driver.find_element(*yol) for ad, yol in yollar.items()}
    print("Arama kutusu:")
    for ad, element in bulunan.items():
        print(f"  {ad} → placeholder = {element.get_attribute('placeholder')}")
    ayni = len({e.id for e in bulunan.values()}) == 1   # WebElement kimliği
    print("  Dördü aynı element mi?", "EVET" if ayni else "HAYIR")
    if not ayni:
        sys.exit("Seçiciler farklı elementleri buldu!")

    # 2) Ürün listesi, ilk sayfa: ilk ürünün adı iki yolla.
    driver.get(ADRES + "/urunler/sayfa-1.html")
    css = driver.find_element(By.CSS_SELECTOR, "article.urun[data-id='1001'] .urun-ad").text
    xpath = driver.find_element(By.XPATH, "//article[@data-id='1001']/h3").text
    print("İlk ürün (CSS)  :", css)
    print("İlk ürün (XPath):", xpath)

    # 3) find_element tek element, find_elements liste döndürür.
    adlar = driver.find_elements(By.CSS_SELECTOR, "#urun-listesi .urun-ad")
    print(f"Sayfadaki ürün adları ({len(adlar)}):")
    for sira, ad in enumerate(adlar, start=1):
        print(f"  {sira:2}. {ad.text}")

    # 4) Kırılgan seçici: sayfanın düzenine (sıraya) bağlı. Araya bir kutu
    #    eklenirse başka elementi bulur. Kararlısı: kimliğe/özniteliğe bağlı.
    kirilgan = "/html/body/main/section[1]/article[1]/h3"
    print("Kırılgan XPath de şimdilik buluyor:", driver.find_element(By.XPATH, kirilgan).text)

    # Ekran için ilk ürün adını çerçevele (yalnızca görüntü; sayfaya dokunmaz).
    driver.execute_script(
        "arguments[0].style.outline = '4px solid #e8590c';",
        driver.find_element(By.CSS_SELECTOR, "article.urun[data-id='1001'] .urun-ad"),
    )
    selenium_kaydet(driver, "1.4", "02-urun-listesi")
finally:
    driver.quit()
