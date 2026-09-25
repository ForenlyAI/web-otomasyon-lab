"""Ders 2.1 — Form doldurma: metin, açılır liste, radyo düğmesi, onay kutusu.

iletisim.html formunu doldurur ama GÖNDERMEZ (gönderim sonucunu beklemeyi
Ders 2.2'de yapacağız). Her alan için aynı üç hareket: bul → temizle → yaz.

Önce sunucuyu açın:        uv run python sunucu.py
Sonra çalıştırın:          uv run python ornekler/2.1/form_doldur.py
Pencere açılmadan:         BASLIKSIZ=1 uv run python ornekler/2.1/form_doldur.py
"""

import os
import sys
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from araclar.ekran import selenium_kaydet  # noqa: E402

ADRES = "http://localhost:8000"

secenekler = webdriver.ChromeOptions()
if os.environ.get("BASLIKSIZ") == "1":
    secenekler.add_argument("--headless")
secenekler.add_argument("--window-size=1280,800")


def yaz(driver, kimlik, metin):
    """Alanı bul, içini temizle, yeni metni yaz."""
    alan = driver.find_element(By.ID, kimlik)
    alan.clear()
    alan.send_keys(metin)


driver = webdriver.Chrome(options=secenekler)
try:
    driver.get(ADRES + "/iletisim.html")

    yaz(driver, "ad", "Deniz Deneme")              # ÖRNEK VERİ
    yaz(driver, "eposta", "deniz@example.com")     # ÖRNEK VERİ
    yaz(driver, "mesaj", "Siparişim hangi kargoda?")

    # Açılır liste: Select ile görünen metne göre seç.
    konu = Select(driver.find_element(By.ID, "konu"))
    konu.select_by_visible_text("Kargo")

    # Radyo düğmesi ve onay kutusu: tıklamak yeter.
    driver.find_element(By.ID, "oncelik-yuksek").click()
    kvkk = driver.find_element(By.ID, "kvkk")
    if not kvkk.is_selected():
        kvkk.click()

    print("Konu:", konu.first_selected_option.text)
    print("Yüksek öncelik seçili mi?", driver.find_element(By.ID, "oncelik-yuksek").is_selected())
    print("Onay kutusu işaretli mi?", kvkk.is_selected())
    selenium_kaydet(driver, "2.1", "01-form-dolu")
    print("Form dolu, gönderilmedi.")
finally:
    driver.quit()
