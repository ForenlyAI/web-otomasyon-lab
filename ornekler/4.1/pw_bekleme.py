"""Ders 4.1 — Playwright'ın otomatik beklemesi.

gecikmeli.html'deki "Hazırım" düğmesi 3 saniye kapalı (disabled) durur.
Playwright tıklamadan önce düğmenin görünür, sabit ve etkin olmasını
KENDİSİ bekler; bekleme kodu yazmayız. Geçen süreyi ölçüp yazdırırız.
Aynı işin Selenium hâli: ornekler/4.1/selenium_bekleme.py

Önce sunucuyu açın:  uv run python sunucu.py
Sonra:               BASLIKSIZ=1 uv run python ornekler/4.1/pw_bekleme.py
"""

import os
import sys
import time
from pathlib import Path

from playwright.sync_api import expect, sync_playwright

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from araclar.ekran import playwright_kaydet  # noqa: E402

with sync_playwright() as p:
    tarayici = p.chromium.launch(headless=os.environ.get("BASLIKSIZ") == "1")
    sayfa = tarayici.new_page(viewport={"width": 1280, "height": 800})
    sayfa.goto("http://localhost:8000/gecikmeli.html")

    basla = time.perf_counter()
    # Bekleme satırı yok: click() düğme tıklanabilir olana kadar bekler (en fazla 30 sn).
    sayfa.get_by_role("button", name="Hazırım").click()
    print(f"Düğmeye tıklandı · geçen süre {time.perf_counter() - basla:.1f} sn")

    # expect de bekler: 6 öğe gelene kadar yeniden dener.
    expect(sayfa.locator("#liste li.oge")).to_have_count(6)
    print("Listede öğe sayısı:", sayfa.locator("#liste li.oge").count())
    print("Mesaj:", sayfa.locator("#hazir-mesaj").inner_text())

    playwright_kaydet(sayfa, "4.1", "01-pw-tiklandi")
    tarayici.close()
