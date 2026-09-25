"""Ders örnekleri için gerçek ekran görüntüsü yardımcıları.

Tüm görüntüler 1280×800 görüş alanında (viewport) alınır ve
lab/ekran/<ders>/<ad>.png dosyasına kaydedilir.

Selenium:
    from araclar.ekran import selenium_kaydet
    selenium_kaydet(driver, "1.3", "arama-sonucu")

Playwright:
    from araclar.ekran import playwright_kaydet
    playwright_kaydet(page, "4.2", "ilk-sayfa")
"""

from __future__ import annotations

from pathlib import Path

LAB = Path(__file__).resolve().parent.parent
EKRAN = LAB / "ekran"
GENISLIK, YUKSEKLIK = 1280, 800


def ekran_yolu(ders: str, ad: str) -> Path:
    """lab/ekran/<ders>/<ad>.png yolunu döndürür, klasörü oluşturur."""
    klasor = EKRAN / ders
    klasor.mkdir(parents=True, exist_ok=True)
    return klasor / (ad if ad.endswith(".png") else f"{ad}.png")


def selenium_boyutla(driver, genislik: int = GENISLIK, yukseklik: int = YUKSEKLIK) -> None:
    """Pencereyi, iç görüş alanı tam genislik×yukseklik olacak şekilde boyutlar."""
    driver.set_window_size(genislik, yukseklik)
    ic_g, ic_y = driver.execute_script("return [window.innerWidth, window.innerHeight];")
    if (ic_g, ic_y) != (genislik, yukseklik):
        # Pencere çerçevesi (başlık çubuğu vb.) payını ekle.
        driver.set_window_size(genislik + (genislik - ic_g), yukseklik + (yukseklik - ic_y))


def selenium_kaydet(driver, ders: str, ad: str) -> Path:
    """Selenium sürücüsünün şu anki görüntüsünü 1280×800 olarak kaydeder."""
    selenium_boyutla(driver)
    # Yazı tipleri yüklenmeden çekilmesin.
    driver.execute_async_script(
        "const bitti = arguments[arguments.length - 1];"
        "document.fonts.ready.then(() => requestAnimationFrame(() => bitti(true)));"
    )
    yol = ekran_yolu(ders, ad)
    if not driver.save_screenshot(str(yol)):
        raise RuntimeError(f"Ekran görüntüsü kaydedilemedi: {yol}")
    return yol


def playwright_kaydet(page, ders: str, ad: str, tam_sayfa: bool = False) -> Path:
    """Playwright sayfasının görüntüsünü 1280×800 görüş alanında kaydeder."""
    boyut = page.viewport_size
    if not boyut or (boyut["width"], boyut["height"]) != (GENISLIK, YUKSEKLIK):
        page.set_viewport_size({"width": GENISLIK, "height": YUKSEKLIK})
    page.evaluate("document.fonts.ready.then(() => true)")
    yol = ekran_yolu(ders, ad)
    page.screenshot(path=str(yol), full_page=tam_sayfa)
    return yol
