"""Ders 6.4 — Örnek bitirme botu: parçaları birleştirmek.

İş (önce elle): 5 sayfalık ürün listesini sayfa sayfa gezip her ürünü tabloya kopyalamak.
Bot: aynı işi yapar ve bitirme ölçütlerini (Ç1–Ç8) karşılar:
  Ç2  element için sabit bekleme yok: WebDriverWait (açık bekleme)
      sayfalar arası nezaket beklemesi var: robots.txt Crawl-delay kadar
  Ç3  zaman aşımı yakalanır, günlüğe yazılır, bot temiz çıkar
  Ç4  CSV: başlık satırı, UTF-8, 50 satır, kişisel veri yok
  Ç5  günlük: başlangıç, her sayfa, hata(lar), bitiş + kayıt sayısı
  Ç8  robots.txt'ye uyar, CAPTCHA'da durur, parola yok, kişisel veri yok

Çalıştırma:  uv run python ornekler/6.4/bitirme_ornek.py
Çıktılar:    ornekler/6.4/urunler.csv · ornekler/6.4/bot.log
Rapor örneği: ornekler/6.4/rapor_ornegi.txt
"""

import csv
import logging
import os
import sys
import time
from pathlib import Path
from urllib.robotparser import RobotFileParser

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

KOK = "http://localhost:8000/"
BASLANGIC = KOK + "urunler/sayfa-1.html"
KIMLIK = "PratikBot/1.0 (+bitirme; iletisim: ornek@example.com)"
KLASOR = Path(__file__).resolve().parent
ALANLAR = ["id", "ad", "kategori", "fiyat", "stok"]  # kişisel veri sütunu yok

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
                    handlers=[logging.FileHandler(KLASOR / "bot.log", mode="w", encoding="utf-8"),
                              logging.StreamHandler()])
gunluk = logging.getLogger("bitirme")


def sayfayi_oku(driver, bekle):
    """Ürün kartları gelene kadar bekler, satırları döndürür."""
    bekle.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "article.urun")))
    satirlar = []
    for kart in driver.find_elements(By.CSS_SELECTOR, "article.urun"):
        fiyat = kart.find_element(By.CSS_SELECTOR, ".fiyat")
        stok = kart.find_element(By.CSS_SELECTOR, ".stok")
        satirlar.append({"id": kart.get_attribute("data-id"),
                         "ad": kart.find_element(By.CSS_SELECTOR, ".urun-ad").text,
                         "kategori": kart.get_attribute("data-kategori"),
                         "fiyat": fiyat.get_attribute("data-fiyat"),
                         "stok": stok.get_attribute("data-stok")})
    return satirlar


def main() -> int:
    gunluk.info("başladı: %s", BASLANGIC)
    robots = RobotFileParser(KOK + "robots.txt")
    robots.read()
    gecikme = robots.crawl_delay(KIMLIK) or 1

    secenekler = webdriver.ChromeOptions()
    if os.environ.get("BASLIKSIZ") == "1":
        secenekler.add_argument("--headless=new")
    secenekler.add_argument(f"--user-agent={KIMLIK}")
    driver = webdriver.Chrome(options=secenekler)
    bekle = WebDriverWait(driver, 10)
    kayitlar, kod = [], 0
    try:
        adres = BASLANGIC
        while adres:
            if not robots.can_fetch(KIMLIK, adres):
                gunluk.warning("robots.txt izin vermiyor, atlandı: %s", adres)
                break
            driver.get(adres)
            if driver.find_elements(By.CSS_SELECTOR, 'meta[name="bot-kontrolu"], #captcha'):
                gunluk.error("CAPTCHA — durdu, insan gerekiyor: %s", adres)
                kod = 3
                break
            try:
                satirlar = sayfayi_oku(driver, bekle)
            except TimeoutException:
                gunluk.error("zaman aşımı: %s — ürünler gelmedi, bot duruyor", adres)
                kod = 1
                break
            kayitlar += satirlar
            gunluk.info("%s: %s ürün", adres.rsplit("/", 1)[-1], len(satirlar))
            sonraki = driver.find_elements(By.CSS_SELECTOR, "a.sonraki")
            adres = sonraki[0].get_attribute("href") if sonraki else None
            if adres:
                time.sleep(gecikme)  # nezaket beklemesi: robots.txt Crawl-delay (element beklemesi değil)
    finally:
        driver.quit()

    with (KLASOR / "urunler.csv").open("w", encoding="utf-8", newline="") as f:
        yazici = csv.DictWriter(f, fieldnames=ALANLAR)
        yazici.writeheader()
        yazici.writerows(kayitlar)
    gunluk.info("bitti: %s kayıt yazıldı (urunler.csv), çıkış kodu %s", len(kayitlar), kod)
    return kod


if __name__ == "__main__":
    sys.exit(main())
