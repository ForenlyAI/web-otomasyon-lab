"""Ders 5.1 — Aynı işi üç yolla yapıp süreyi ölçmek.

İş: 5 sayfalık ürün listesindeki (urunler/sayfa-1 … sayfa-5) 50 ürün adını toplamak.
  1) Selenium, görünür mod (pencere açılır)
  2) Selenium, headless ('--headless=new', pencere açılmaz)
  3) requests + BeautifulSoup (tarayıcı hiç açılmaz)
Her yolda tarayıcı BİR KEZ açılır ve 5 sayfa aynı tarayıcıda gezilir.
Süreye tarayıcının açılışı da dahildir: gerçek maliyet budur.
Sonuç ekrana ve ornekler/5.1/SURE.txt dosyasına yazılır.

Çalıştırma:  uv run python ornekler/5.1/sure_olcumu.py
BASLIKSIZ=1 verilirse (ya da Linux'ta ekran yoksa) görünür mod atlanır.
"""

import os
import sys
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

ADRES = "http://localhost:8000/urunler/sayfa-{}.html"
SAYFALAR = range(1, 6)
KLASOR = Path(__file__).resolve().parent


def selenium_ile(headless: bool) -> int:
    secenekler = webdriver.ChromeOptions()
    if headless:
        secenekler.add_argument("--headless=new")  # pencere açmadan çalış
    secenekler.add_argument("--window-size=1280,800")
    driver = webdriver.Chrome(options=secenekler)  # tarayıcı bir kez açılır
    try:
        adlar = []
        for no in SAYFALAR:
            driver.get(ADRES.format(no))
            adlar += [e.text for e in driver.find_elements(By.CSS_SELECTOR, ".urun-ad")]
        return len(adlar)
    finally:
        driver.quit()


def requests_ile() -> int:
    adlar = []
    with requests.Session() as oturum:  # bağlantı yeniden kullanılır
        for no in SAYFALAR:
            yanit = oturum.get(ADRES.format(no), timeout=10)
            yanit.raise_for_status()
            sayfa = BeautifulSoup(yanit.text, "html.parser")
            adlar += [e.get_text(strip=True) for e in sayfa.select(".urun-ad")]
    return len(adlar)


def olc(ad, is_):
    bas = time.perf_counter()
    adet = is_()
    sure = time.perf_counter() - bas
    print(f"{ad:<28} {adet:>3} ürün   {sure:6.2f} sn", flush=True)
    return ad, adet, sure


ekran_yok = sys.platform.startswith("linux") and not os.environ.get("DISPLAY")
gorunur_atla = os.environ.get("BASLIKSIZ") == "1" or ekran_yok

print("Yol                          Sonuç      Süre")
print("-" * 46)
sonuclar = []
if gorunur_atla:
    print(f"{'Selenium görünür mod':<28} atlandı (ekran yok / BASLIKSIZ=1)")
else:
    sonuclar.append(olc("Selenium görünür mod", lambda: selenium_ile(headless=False)))
sonuclar.append(olc("Selenium headless", lambda: selenium_ile(headless=True)))
sonuclar.append(olc("requests + BeautifulSoup", requests_ile))

en_hizli = min(sonuclar, key=lambda s: s[2])
en_yavas = max(sonuclar, key=lambda s: s[2])
print("-" * 46)
print(f"En hızlı: {en_hizli[0]} ({en_yavas[2] / en_hizli[2]:.0f} kat daha hızlı)")

satirlar = [f"{ad}\t{adet} ürün\t{sure:.2f} sn" for ad, adet, sure in sonuclar]
satirlar.append("Yorum: veri sayfa kaynağında varsa tarayıcı açmaya gerek yok.")
(KLASOR / "SURE.txt").write_text("\n".join(satirlar) + "\n", encoding="utf-8")
print("Kaydedildi: ornekler/5.1/SURE.txt")
