"""Ders 4.2 — Ders 1.3'teki ilk botun Playwright ile yeniden yazılmış hâli.

Pratik Mağaza'yı açar, arama kutusuna "kulaklık" yazar, Ara'ya tıklar,
sonuç sayısını ve ilk 3 ürünün adını yazdırır, ekran görüntüsü kaydeder.
İskelet üç parçadır: tarayıcı → bağlam (temiz bir profil) → sayfa.

Bir kez (tarayıcıyı indirir):  uv run playwright install chromium
Önce sunucuyu açın:            uv run python sunucu.py
Sonra:                         uv run python ornekler/4.2/ilk_pw.py
Pencere açılmadan:             BASLIKSIZ=1 uv run python ornekler/4.2/ilk_pw.py
"""

import os
import sys
from pathlib import Path

from playwright.sync_api import expect, sync_playwright

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from araclar.ekran import playwright_kaydet  # noqa: E402

with sync_playwright() as p:
    tarayici = p.chromium.launch(headless=os.environ.get("BASLIKSIZ") == "1")
    baglam = tarayici.new_context(viewport={"width": 1280, "height": 800})
    sayfa = baglam.new_page()

    sayfa.goto("http://localhost:8000")
    print("Sayfa başlığı:", sayfa.title())

    sayfa.locator("#arama").fill("kulaklık")  # fill: kutuyu temizler ve yazar
    sayfa.locator("#ara-dugme").click()

    # Sonuç yazısı "bulundu" içerene kadar kendiliğinden bekler (açık bekleme kodu yok).
    sonuc = sayfa.locator("#sonuc-sayisi")
    expect(sonuc).to_contain_text("bulundu")
    print("Sonuç:", sonuc.inner_text())

    adlar = sayfa.locator("#urun-listesi .urun-ad").all_inner_texts()
    print("İlk 3 ürün:")
    for sira, ad in enumerate(adlar[:3], start=1):
        print(f"  {sira}. {ad}")

    yol = playwright_kaydet(sayfa, "4.2", "01-arama-sonucu")
    print("Ekran görüntüsü kaydedildi:", yol.relative_to(Path(__file__).resolve().parents[2]))
    baglam.close()
    tarayici.close()
