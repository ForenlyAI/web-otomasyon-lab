"""Ders 5.3 — CAPTCHA'yı görünce durmak.

Bot sırayla birkaç sayfayı gezer. Her sayfada bot kontrolü işareti arar:
  <meta name="bot-kontrolu" content="captcha">  ya da  #captcha elemanı.
İşareti görünce:
  1) kanıt olarak ekran görüntüsü alır (ornekler/5.3/captcha.png),
  2) günlüğe "CAPTCHA — durdu, insan gerekiyor" yazar,
  3) tarayıcıyı kapatıp SIFIRDAN FARKLI çıkış koduyla (3) temiz çıkar.
Kutuyu işaretlemeye, çözmeye ya da atlatmaya ÇALIŞMAZ. CAPTCHA sitenin "dur" demesidir.

Çalıştırma:  uv run python ornekler/5.3/captcha_dur.py ; echo "çıkış kodu: $?"
"""

import logging
import os
import sys
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from araclar.ekran import selenium_kaydet  # noqa: E402

KOK = "http://localhost:8000/"
KLASOR = Path(__file__).resolve().parent
CIKIS_CAPTCHA = 3  # zamanlayıcı ya da siz bu koda bakıp insan çağırırsınız

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                    datefmt="%H:%M:%S",
                    handlers=[logging.FileHandler(KLASOR / "bot.log", mode="w", encoding="utf-8"),
                              logging.StreamHandler()])
gunluk = logging.getLogger("bot")


def bot_kontrolu_var(driver) -> bool:
    """Sayfada CAPTCHA / bot kontrolü işareti var mı?"""
    isaret = driver.find_elements(By.CSS_SELECTOR, 'meta[name="bot-kontrolu"], #captcha')
    return len(isaret) > 0


secenekler = webdriver.ChromeOptions()
if os.environ.get("BASLIKSIZ") == "1":
    secenekler.add_argument("--headless=new")
secenekler.add_argument("--window-size=1280,800")
driver = webdriver.Chrome(options=secenekler)
kod = 0
try:
    for yol in ["tablo.html", "urunler/sayfa-1.html", "captcha.html", "urunler/sayfa-2.html"]:
        driver.get(KOK + yol)
        if bot_kontrolu_var(driver):
            selenium_kaydet(driver, "5.3", "01-captcha-sayfasi")
            driver.save_screenshot(str(KLASOR / "captcha.png"))
            gunluk.error("CAPTCHA — durdu, insan gerekiyor: /%s (kanıt: captcha.png)", yol)
            kod = CIKIS_CAPTCHA
            break
        gunluk.info("sayfa tamam: /%s", yol)
    else:
        gunluk.info("bitti, bot kontrolüne rastlanmadı")
finally:
    driver.quit()
sys.exit(kod)
