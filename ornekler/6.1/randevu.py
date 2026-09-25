"""Ders 6.1 — Randevu botu: boş saati bulur, kontrolü size bırakır.

Koşul: hafta içi bir gün, öğleden sonra (13:00 ve sonrası) ilk boş saat.
  - Varsayılan DENEME MODU: yalnız bulduğu saati yazdırır, hiçbir şeye tıklamaz.
  - --onay verirseniz: o saati seçer, formu doldurur, onaylar ve onay kodunu okur.
  - Uygun saat yoksa bunu açıkça söyler ve temiz çıkar.

Çalıştırma:
  uv run python ornekler/6.1/randevu.py                      # deneme modu
  uv run python ornekler/6.1/randevu.py --onay               # rezervasyon yapar
  uv run python ornekler/6.1/randevu.py --tarih 2026-10-07   # yalnız o gün (tamamen dolu)
Gerçek randevu sistemlerinde bot kullanmak koşullara aykırı ve diğer insanlara haksız olabilir;
bu bot yalnız Pratik Mağaza içindir.
"""

import argparse
import os
import sys
from datetime import date
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from araclar.ekran import selenium_kaydet  # noqa: E402

arg = argparse.ArgumentParser()
arg.add_argument("--onay", action="store_true", help="bulunan saati gerçekten rezerve et")
arg.add_argument("--tarih", help="yalnız bu günü dene (YYYY-AA-GG)")
arg = arg.parse_args()


def uygun_mu(tarih: str, saat: str) -> bool:
    hafta_ici = date.fromisoformat(tarih).weekday() < 5  # 0 = Pazartesi … 4 = Cuma
    return hafta_ici and saat >= "13:00"


def saatleri_oku(driver, bekle, tarih):
    """Tarihi seçer, saatler gelene kadar bekler, boş saatleri döndürür."""
    Select(driver.find_element(By.ID, "tarih")).select_by_value(tarih)
    bekle.until(lambda d: d.find_elements(By.CSS_SELECTOR, "#saatler button.saat"))
    return [b for b in driver.find_elements(By.CSS_SELECTOR, "#saatler button.saat") if b.is_enabled()]


secenekler = webdriver.ChromeOptions()
if os.environ.get("BASLIKSIZ") == "1":
    secenekler.add_argument("--headless=new")
secenekler.add_argument("--window-size=1280,800")
driver = webdriver.Chrome(options=secenekler)
bekle = WebDriverWait(driver, 10)
try:
    driver.get("http://localhost:8000/randevu.html")
    # Tarih listesi JavaScript ile dolar: ilk boş seçenekten fazlası gelene kadar bekle.
    bekle.until(lambda d: len(Select(d.find_element(By.ID, "tarih")).options) > 1)
    tarihler = [o.get_attribute("value") for o in Select(driver.find_element(By.ID, "tarih")).options][1:]
    if arg.tarih:
        tarihler = [t for t in tarihler if t == arg.tarih]

    bulunan = None
    for tarih in tarihler:
        bos = saatleri_oku(driver, bekle, tarih)
        print(f"{tarih}: {len(bos)} boş saat")
        uyan = [b for b in bos if uygun_mu(tarih, b.get_attribute("data-saat"))]
        if uyan:
            bulunan = (tarih, uyan[0])
            break

    if bulunan is None:
        selenium_kaydet(driver, "6.1", "04-uygun-yok")
        print("Uygun saat yok. Hiçbir şey rezerve edilmedi.")
        sys.exit(0)  # temiz çıkış: bu bir hata değil, bir sonuç

    tarih, dugme = bulunan
    saat = dugme.get_attribute("data-saat")
    if not arg.onay:
        selenium_kaydet(driver, "6.1", "01-bos-saatler")
        print(f"DENEME MODU — bulunan: {tarih} {saat}. Rezervasyon için: --onay")
        sys.exit(0)

    dugme.click()
    driver.find_element(By.ID, "ad-soyad").send_keys("Deneme Örnek")  # ÖRNEK VERİ
    driver.find_element(By.ID, "telefon").send_keys("0555 000 00 00")
    driver.find_element(By.ID, "randevu-onay").click()
    bekle.until(EC.visibility_of_element_located((By.ID, "onay")))
    print("Onay:", driver.find_element(By.ID, "onay-ozet").text)
    print("Onay kodu:", driver.find_element(By.ID, "onay-kodu").text)
    selenium_kaydet(driver, "6.1", "02-onay")
finally:
    driver.quit()
