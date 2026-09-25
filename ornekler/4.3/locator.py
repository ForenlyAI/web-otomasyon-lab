"""Ders 4.3 — Kullanıcının gördüğüne göre locator yazmak.

1) iletisim.html formunu yalnız get_by_label ve get_by_role ile doldurur,
   gönderir ve sonucu expect ile doğrular.
2) Ürün listesinde filter ile tek bir ürünün kartını daraltıp fiyatını okur.
3) Bilerek birden çok öğeye uyan bir locator'a tıklar ve strict mode
   hatasının ilk satırlarını yazdırır.

Önce sunucuyu açın:  uv run python sunucu.py
Sonra:               BASLIKSIZ=1 uv run python ornekler/4.3/locator.py
"""

import os
import sys
from pathlib import Path

from playwright.sync_api import Error, expect, sync_playwright

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from araclar.ekran import playwright_kaydet  # noqa: E402

SITE = "http://localhost:8000"

with sync_playwright() as p:
    tarayici = p.chromium.launch(headless=os.environ.get("BASLIKSIZ") == "1")
    sayfa = tarayici.new_page(viewport={"width": 1280, "height": 800})

    # 1) Form: etiket (label) ve rol + erişilebilir ad ile
    sayfa.goto(f"{SITE}/iletisim.html")
    sayfa.get_by_label("Adınız").fill("Deneme Öğrenci")
    sayfa.get_by_label("E-posta").fill("ogrenci@example.com")
    sayfa.get_by_label("Konu").select_option("kargo")
    sayfa.get_by_label("Normal").check()
    sayfa.get_by_label("Mesajınız").fill("Kargom ne zaman gelir?")
    sayfa.get_by_label("Aydınlatma metnini okudum").check()
    sayfa.get_by_role("button", name="Gönder").click()
    # expect: sonuç kutusu 1,5 sn sonra gelir; gelene kadar yeniden dener
    expect(sayfa.get_by_role("status")).to_contain_text("Mesajınız alındı")
    print("1) Form doğrulandı:", sayfa.get_by_role("status").inner_text().splitlines()[0])
    playwright_kaydet(sayfa, "4.3", "01-form-gonderildi")

    # 2) Liste: filter ile tek karta daralt, içinden fiyatı al
    sayfa.goto(f"{SITE}/urunler/sayfa-1.html")
    kart = sayfa.locator("article.urun").filter(has_text="Yoga Matı")
    print("2) Yoga Matı fiyatı:", kart.locator(".fiyat").inner_text())

    # 3) Strict mode: "Detayı gör" bağlantısı sayfada 10 tane
    detay = sayfa.get_by_role("link", name="Detayı gör")
    print("3) 'Detayı gör' eşleşme sayısı:", detay.count())
    try:
        detay.click(timeout=2000)
    except Error as hata:
        print("   Hata:", "\n   ".join(str(hata).splitlines()[:3]))
    # Doğrusu: hangisi olduğunu söylemek
    kart.get_by_role("link", name="Detayı gör").click()
    print("   Daraltınca tıklandı →", sayfa.url.rsplit("/", 1)[-1])

    tarayici.close()
