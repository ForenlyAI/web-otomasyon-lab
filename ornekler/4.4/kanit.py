"""Ders 4.4 — Botun gördüğünü kanıt olarak saklamak: ekran görüntüsü ve PDF.

tablo.html için üç dosya üretir, adlarına tarih-saat ekler:
  1) tam sayfa ekran görüntüsü (full_page=True — kaydırılan kısım dahil)
  2) yalnız kargo tablosunun görüntüsü (element ekran görüntüsü)
  3) sayfanın PDF'i (emulate_media ile ekran görünümünde; PDF yalnız Chromium'da)
Sonra bilerek olmayan bir düğmeyi arar; hata olunca o anın görüntüsünü saklar.
Dosyalar: ornekler/4.4/kanitlar/

Önce sunucuyu açın:  uv run python sunucu.py
Sonra:               BASLIKSIZ=1 uv run python ornekler/4.4/kanit.py
"""

import os
from datetime import datetime
from pathlib import Path

from playwright.sync_api import TimeoutError as PWTimeout
from playwright.sync_api import sync_playwright

KLASOR = Path(__file__).with_name("kanitlar")
KLASOR.mkdir(exist_ok=True)
zaman = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # ör. 2026-09-24_14-05-09


def yol(ad):
    return KLASOR / f"{ad}_{zaman}"


with sync_playwright() as p:
    tarayici = p.chromium.launch(headless=os.environ.get("BASLIKSIZ") == "1")
    sayfa = tarayici.new_page(viewport={"width": 1280, "height": 800})
    sayfa.goto("http://localhost:8000/tablo.html")

    # 1) Tam sayfa: görünen alanın dışında kalan kısım da çekilir
    sayfa.screenshot(path=f"{yol('tam-sayfa')}.png", full_page=True)
    # 2) Yalnız tablo: locator'ın kendi ekran görüntüsü
    sayfa.locator("#kargo").screenshot(path=f"{yol('tablo')}.png")
    # 3) PDF: baskı stili yerine ekrandaki görünümle
    sayfa.emulate_media(media="screen")
    sayfa.pdf(path=f"{yol('sayfa')}.pdf", format="A4", print_background=True)

    # 4) Hata anı: bulunamayan düğmede o anki ekranı kanıt olarak sakla
    try:
        sayfa.get_by_role("button", name="Siparişi tamamla").click(timeout=2000)
    except PWTimeout:
        sayfa.screenshot(path=f"{yol('HATA')}.png")
        print("Hata: 'Siparişi tamamla' düğmesi 2 sn içinde bulunamadı → görüntü saklandı")

    tarayici.close()

for dosya in sorted(KLASOR.glob(f"*_{zaman}.*")):
    print(f"{dosya.name:<42} {dosya.stat().st_size / 1024:>7.1f} KB")
