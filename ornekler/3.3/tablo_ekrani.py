"""Ders 3.3 — tablo.html sayfasının ekran görüntüsü (derste gösterilen sayfa).

Önce sunucuyu açın:  uv run python sunucu.py
Sonra:               BASLIKSIZ=1 uv run python ornekler/3.3/tablo_ekrani.py
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
    sayfa.goto("http://localhost:8000/tablo.html")
    print("Tablo satır sayısı:", sayfa.locator("#kargo tbody tr").count())
    print("Kaydedildi:", playwright_kaydet(sayfa, "3.3", "01-tablo-sayfasi").name)
    tarayici.close()
