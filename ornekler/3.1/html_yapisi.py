"""Ders 3.1 — Bir sayfanın HTML yapısını ağaç olarak görmek.

Ürün ayrıntı sayfasını (urun/1001.html) tarayıcı açmadan indirir ve
ürün kutusunun içindeki etiketleri; id, class ve data- öznitelikleriyle
birlikte girintili bir ağaç olarak yazdırır. DevTools'taki Elements
sekmesinde gördüğünüz yapının aynısıdır.

Önce sunucuyu açın:  uv run python sunucu.py
Sonra:               uv run python ornekler/3.1/html_yapisi.py
"""

import requests
from bs4 import BeautifulSoup

ADRES = "http://localhost:8000/urun/1001.html"
BASLIK = {"User-Agent": "PratikMagazaOgrenciBotu/1.0 (Web Otomasyonu 101)"}


def etiket_yazisi(el):
    """<span id="fiyat" class="fiyat" data-fiyat="…"> → span#fiyat.fiyat [data-fiyat=…]"""
    yazi = el.name
    if el.get("id"):
        yazi += "#" + el["id"]
    for sinif in el.get("class", []):
        yazi += "." + sinif
    veri = [f"{ad}={deger}" for ad, deger in el.attrs.items() if ad.startswith("data-")]
    if veri:
        yazi += " [" + ", ".join(veri) + "]"
    return yazi


def agac(el, derinlik=0):
    """Yalnız id ya da class taşıyan etiketleri gezer; yapraksa metnini de yazar."""
    for cocuk in el.find_all(recursive=False):
        if cocuk.name in ("table", "script", "button") or cocuk.get("aria-hidden"):
            continue  # örnekte kalabalık etmesin (tablo, betik, düğme, süs simgesi)
        if "gizli" in cocuk.get("class", []):
            continue  # ekranda görünmeyen mesaj
        if cocuk.get("id") or cocuk.get("class"):
            metin = ""
            if not cocuk.find(True):  # içinde başka etiket yoksa
                metin = "  →  " + cocuk.get_text(strip=True)
            print("   " * derinlik + "└─ " + etiket_yazisi(cocuk) + metin)
            agac(cocuk, derinlik + 1)
        else:
            agac(cocuk, derinlik)  # sınıfsız sarmalayıcıyı atla, içine bak


cevap = requests.get(ADRES, headers=BASLIK, timeout=10)
cevap.raise_for_status()
soup = BeautifulSoup(cevap.text, "html.parser")

kutu = soup.select_one("article.urun-detay")
print("Adres:", ADRES)
print("DOM ağacı (ürün kutusu):")
print(etiket_yazisi(kutu))
agac(kutu, 1)
