"""Ders 3.1 — Ürün sayfasında ad, fiyat ve stok alanlarını DevTools gibi işaretler.

Sayfayı Playwright ile açar, üç alanın çevresine çerçeve ve
"etiket#id.class" yazısı ekler, ekran görüntüsünü kaydeder.
(Çerçeveler yalnız görüntü içindir; sayfanın kendisi değişmez.)

Önce sunucuyu açın:  uv run python sunucu.py
Sonra:               BASLIKSIZ=1 uv run python ornekler/3.1/incele_gorunumu.py
"""

import os
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from araclar.ekran import playwright_kaydet  # noqa: E402

ADRES = "http://localhost:8000/urun/1001.html"
ALANLAR = ["h1#urun-ad", "span#fiyat", "span#stok"]

ISARETLE = """(secici) => {
  const el = document.querySelector(secici);
  el.style.outline = '3px solid #2f80ed';
  el.style.outlineOffset = '3px';
  el.style.background = 'rgba(47,128,237,.12)';
  const etiket = document.createElement('div');
  let yazi = el.tagName.toLowerCase() + '#' + el.id;
  el.classList.forEach(c => yazi += '.' + c);
  etiket.textContent = yazi;
  etiket.style.cssText = 'position:absolute;background:#1f2330;color:#fff;font:600 15px monospace;'
    + 'padding:3px 8px;border-radius:4px;z-index:99';
  const k = el.getBoundingClientRect();
  document.body.appendChild(etiket);
  if (k.right + 18 + etiket.offsetWidth < window.innerWidth) {   // sağında yer varsa sağına
    etiket.style.left = (k.right + window.scrollX + 18) + 'px';
    etiket.style.top = (k.top + window.scrollY + k.height / 2 - 12) + 'px';
  } else {                                                        // yoksa üstüne, sağ köşeye
    etiket.style.left = (k.right + window.scrollX - etiket.offsetWidth) + 'px';
    etiket.style.top = (k.top + window.scrollY - 34) + 'px';
  }
}"""

with sync_playwright() as p:
    tarayici = p.chromium.launch(headless=os.environ.get("BASLIKSIZ") == "1")
    sayfa = tarayici.new_page(viewport={"width": 1280, "height": 800})
    sayfa.goto(ADRES)
    for secici in ALANLAR:
        sayfa.evaluate(ISARETLE, secici)
        print("İşaretlendi:", secici)
    yol = playwright_kaydet(sayfa, "3.1", "01-urun-alanlari")
    print("Ekran görüntüsü:", yol.name)
    tarayici.close()
