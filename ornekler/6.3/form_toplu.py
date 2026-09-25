"""Ders 6.3 — CSV'den toplu form doldurma, satır başına hata yakalama.

CSV'nin her satırı için basvuru.html formunu doldurur ve kaydeder.
  - Her satır AYRI try/except içinde: bir satır bozuksa iş durmaz, sonrakine geçilir.
  - Gönderim sayfadaki başvuru sayısının artmasıyla DOĞRULANIR.
  - Hatalı satırlar sebebiyle birlikte hatalar.csv dosyasına yazılır.
  - Her adım form.log günlüğüne yazılır; sonunda "N gönderildi, M hatalı" özeti.
Veri sahtedir (ÖRNEK VERİ). Gerçek kişi verisi işleyecekseniz önce KVKK dayanağını sorun.

Çalıştırma:
  uv run python ornekler/6.3/form_toplu.py                                   # lab/veri/basvurular.csv
  uv run python ornekler/6.3/form_toplu.py ornekler/6.3/basvurular_bozuk.csv # 2 bozuk satırlı
"""

import csv
import logging
import os
import sys
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait

LAB = Path(__file__).resolve().parents[2]
KLASOR = Path(__file__).resolve().parent
sys.path.insert(0, str(LAB))
from araclar.ekran import selenium_kaydet  # noqa: E402

KAYNAK = Path(sys.argv[1]) if len(sys.argv) > 1 else LAB / "veri" / "basvurular.csv"
if not KAYNAK.is_absolute():
    KAYNAK = LAB / KAYNAK
DENEYIM = {"yok": "deneyim-yok", "1-3": "deneyim-1-3", "3+": "deneyim-3-plus"}

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                    datefmt="%H:%M:%S",
                    handlers=[logging.FileHandler(KLASOR / "form.log", mode="w", encoding="utf-8"),
                              logging.StreamHandler()])
gunluk = logging.getLogger("form")


def kayit_sayisi(driver) -> int:
    return int(driver.find_element(By.ID, "basvuru-sayisi").text.strip("()"))


def doldur(driver, satir):
    """Bir satırı forma yazar, kaydeder; kayıt sayısı artmazsa hata fırlatır."""
    once = kayit_sayisi(driver)
    for alan in ("ad", "soyad", "eposta", "telefon", "aciklama"):
        kutu = driver.find_element(By.ID, alan)
        kutu.clear()
        kutu.send_keys(satir[alan])
    Select(driver.find_element(By.ID, "sehir")).select_by_visible_text(satir["sehir"])
    driver.find_element(By.ID, DENEYIM[satir["deneyim"]]).click()
    driver.find_element(By.ID, "kaydet").click()
    # Ya kayıt sayısı artar ya da sayfa bir hata mesajı gösterir: hangisi önce olursa.
    WebDriverWait(driver, 5).until(
        lambda d: kayit_sayisi(d) > once or d.find_element(By.ID, "hata").is_displayed())
    if kayit_sayisi(driver) == once:
        raise ValueError(driver.find_element(By.ID, "hata").text)


secenekler = webdriver.ChromeOptions()
if os.environ.get("BASLIKSIZ") == "1":
    secenekler.add_argument("--headless=new")
secenekler.add_argument("--window-size=1280,800")
driver = webdriver.Chrome(options=secenekler)
gonderilen, hatalar = 0, []
try:
    driver.get("http://localhost:8000/basvuru.html")
    driver.find_element(By.ID, "temizle").click()  # önceki denemenin kayıtlarını sil
    with KAYNAK.open(encoding="utf-8", newline="") as f:
        satirlar = list(csv.DictReader(f))
    gunluk.info("başladı: %s satır (%s)", len(satirlar), KAYNAK.name)

    for no, satir in enumerate(satirlar, start=2):  # 1. satır başlık
        try:
            doldur(driver, satir)
            gonderilen += 1
            gunluk.info("satır %s gönderildi: %s", no, satir["eposta"])
        except Exception as hata:
            # Selenium hatasının yalnız ilk cümlesi yeter (belge bağlantısı ayrı gelir).
            sebep = (getattr(hata, "msg", None) or str(hata)).split(";")[0].strip() or type(hata).__name__
            gunluk.warning("satır %s HATALI (%s): %s", no, satir["eposta"], sebep)
            hatalar.append(satir | {"satir": no, "hata": sebep})
            driver.refresh()  # yarım kalan formu temizle; kayıtlar sekmede kalır

    # Kayıtlı başvurular tablosunu görünür yapıp ekran görüntüsü al.
    driver.execute_script("document.getElementById('basvuru-sayisi').scrollIntoView();")
    selenium_kaydet(driver, "6.3", "01-basvurular")
finally:
    driver.quit()

with (KLASOR / "hatalar.csv").open("w", encoding="utf-8", newline="") as f:
    yazici = csv.DictWriter(f, fieldnames=["satir", "hata", "ad", "soyad", "eposta", "telefon",
                                           "sehir", "deneyim", "aciklama"])
    yazici.writeheader()
    yazici.writerows(hatalar)
gunluk.info("bitti: %s gönderildi, %s hatalı (hatalar.csv)", gonderilen, len(hatalar))
