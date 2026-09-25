"""Ders 5.1 — Playwright headless + gereksiz dosyaları engellemek.

Playwright varsayılan olarak headless çalışır (pencere açmaz).
page.route ile görsel, yazı tipi ve medya isteklerini daha indirilmeden
iptal ederiz: veriyi okumak için bunlara ihtiyacımız yok.
Aynı 5 sayfayı önce engelsiz, sonra engelli gezip süreyi ve istek sayısını karşılaştırır.

Çalıştırma:  uv run python ornekler/5.1/playwright_engelle.py
Pencereyi görmek için:  GORUNUR=1 uv run python ornekler/5.1/playwright_engelle.py
"""

import os
import time

from playwright.sync_api import sync_playwright

ADRES = "http://localhost:8000/urunler/sayfa-{}.html"
GEREKSIZ = {"image", "font", "media"}  # veri için indirilmesi gerekmeyen türler


def gez(tarayici, engelle: bool):
    sayfa = tarayici.new_page()
    sayac = {"istek": 0, "engellenen": 0}

    def yonlendir(route):
        if route.request.resource_type in GEREKSIZ:
            sayac["engellenen"] += 1
            return route.abort()  # isteği hiç gönderme
        sayac["istek"] += 1
        return route.continue_()

    if engelle:
        sayfa.route("**/*", yonlendir)
    else:
        sayfa.on("request", lambda r: sayac.__setitem__("istek", sayac["istek"] + 1))

    bas = time.perf_counter()
    adet = 0
    for no in range(1, 6):
        sayfa.goto(ADRES.format(no))
        adet += sayfa.locator(".urun-ad").count()
    sure = time.perf_counter() - bas
    sayfa.close()
    return adet, sure, sayac


with sync_playwright() as p:
    tarayici = p.chromium.launch(headless=os.environ.get("GORUNUR") != "1")
    for engelle in (False, True):
        adet, sure, sayac = gez(tarayici, engelle)
        ad = "engelli " if engelle else "engelsiz"
        print(f"{ad}: {adet} ürün · {sure:.2f} sn · {sayac['istek']} istek · "
              f"{sayac['engellenen']} engellenen")
    tarayici.close()
print("Not: Pratik Mağaza'da görsel yok; engellenen yalnız yazı tipleri.")
