"""Ders 3.1 — Sayfa kaynağı ile canlı DOM aynı mı?

gecikmeli.html listesini JavaScript 2–4 saniye sonra ekler.
1) requests sayfa KAYNAĞINI alır: listede kaç öğe var?
2) Playwright sayfayı tarayıcıda açar, JavaScript çalışır: CANLI DOM'da kaç öğe var?
Sonuca göre "requests yeter mi, tarayıcı mı gerekir" kararını yazdırır.

Önce sunucuyu açın:  uv run python sunucu.py
Sonra:               BASLIKSIZ=1 uv run python ornekler/3.1/kaynak_mi_canli_mi.py
"""

import os
import sys
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from araclar.ekran import playwright_kaydet  # noqa: E402

ADRES = "http://localhost:8000/gecikmeli.html"
BASLIK = {"User-Agent": "PratikMagazaOgrenciBotu/1.0 (Web Otomasyonu 101)"}

# 1) Sayfa kaynağı: sunucunun gönderdiği ham HTML
kaynak = requests.get(ADRES, headers=BASLIK, timeout=10).text
soup = BeautifulSoup(kaynak, "html.parser")
kaynakta = len(soup.select("#liste li.oge"))
print("Sayfa kaynağında  #liste li.oge :", kaynakta)
liste = soup.select_one("#liste")
print("   #liste etiketi kaynakta      :", "var, içi boş" if not liste.find(True) else "var, dolu")

# 2) Canlı DOM: tarayıcı JavaScript'i çalıştırdıktan sonraki hâl
with sync_playwright() as p:
    tarayici = p.chromium.launch(headless=os.environ.get("BASLIKSIZ") == "1")
    sayfa = tarayici.new_page(viewport={"width": 1280, "height": 800})
    sayfa.goto(ADRES)
    sayfa.locator("#liste li.oge").nth(5).wait_for()  # altıncı öğe gelene kadar bekler
    canlida = sayfa.locator("#liste li.oge").count()
    print("Canlı DOM'da      #liste li.oge :", canlida)
    playwright_kaydet(sayfa, "3.1", "03-gecikmeli-canli")
    tarayici.close()

if kaynakta == canlida:
    print("Karar: içerik kaynakta var → requests + BeautifulSoup yeter.")
else:
    print("Karar: içerik yalnız canlı DOM'da → tarayıcı gerekir (Selenium / Playwright).")
