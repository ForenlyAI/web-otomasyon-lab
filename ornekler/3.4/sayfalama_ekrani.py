"""Ders 3.4 — Ürün listesinin alt kısmındaki sayfalama bağlantılarının ekran görüntüsü.

Önce sunucuyu açın:  uv run python sunucu.py
Sonra:               BASLIKSIZ=1 uv run python ornekler/3.4/sayfalama_ekrani.py
"""

import os
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from araclar.ekran import playwright_kaydet  # noqa: E402

with sync_playwright() as p:
    tarayici = p.chromium.launch(headless=os.environ.get("BASLIKSIZ") == "1")
    sayfa = tarayici.new_page(viewport={"width": 1280, "height": 800})
    sayfa.goto("http://localhost:8000/urunler/sayfa-2.html")
    sonraki = sayfa.locator("nav.sayfalama a.sonraki")
    print("Sonraki bağlantısının href değeri:", sonraki.get_attribute("href"))
    # Sayfalamanın ekranın alt kısmında görüneceği yere kaydır
    sayfa.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    sonraki.evaluate("el => { el.style.outline = '3px solid #2f80ed'; el.style.outlineOffset = '3px'; }")
    print("Kaydedildi:", playwright_kaydet(sayfa, "3.4", "01-sayfalama").name)
    tarayici.close()
