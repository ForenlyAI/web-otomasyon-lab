"""Ders 5.4 — Kayıtlı oturumla, giriş yapmadan hesap sayfasını açmak.

oturum_kaydet.py'nin yazdığı durum.json yeni bir bağlama yüklenir.
Giriş formu hiç doldurulmaz; hesap.html doğrudan açılır.

Çalıştırma:  uv run python ornekler/5.4/oturum_kullan.py
"""

import os
import sys
from pathlib import Path

from playwright.sync_api import expect, sync_playwright

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from araclar.ekran import playwright_kaydet  # noqa: E402

DURUM = Path(__file__).resolve().parent / "durum.json"
if not DURUM.exists():
    sys.exit("durum.json yok: önce oturum_kaydet.py'yi çalıştırın.")

with sync_playwright() as p:
    tarayici = p.chromium.launch(headless=os.environ.get("GORUNUR") != "1")
    baglam = tarayici.new_context(storage_state=str(DURUM))  # kayıtlı oturum
    sayfa = baglam.new_page()
    sayfa.goto("http://localhost:8000/hesap.html")
    # Çerez geçersizse sayfa giris.html'e döner; o zaman bu satır hata verir.
    expect(sayfa.locator("#karsilama")).to_have_text("Hoş geldin, ogrenci")
    print("Girişsiz açıldı:", sayfa.url)
    print("Sayfada:", sayfa.locator("#karsilama").inner_text())
    playwright_kaydet(sayfa, "5.4", "02-hesap-girissiz")
    tarayici.close()
