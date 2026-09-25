"""Ders 3.2 — requests ile sayfayı almak, BeautifulSoup ile alan seçmek.

Bir ürün ayrıntı sayfasını tarayıcı açmadan indirir:
- zaman aşımı verir (timeout) — vermezseniz istek sonsuza dek bekleyebilir,
- kendini tanıtan bir User-Agent gönderir,
- durum kodunu kontrol eder (200 değilse o sayfayı ayrıştırmaz),
sonra ürünün adını, fiyatını, açıklamasını ve liste bağlantısını
find ve CSS seçiciyle (select_one) alıp yazdırır.

Önce sunucuyu açın:  uv run python sunucu.py
Sonra:               uv run python ornekler/3.2/urun.py
Başka ürünler:       uv run python ornekler/3.2/urun.py 1018 9999
"""

import sys

import requests
from bs4 import BeautifulSoup

# Kendinizi tanıtın: site sahibi kimin istek attığını görebilsin.
BASLIK = {"User-Agent": "PratikMagazaOgrenciBotu/1.0 (Web Otomasyonu 101)"}


def urun_oku(urun_no):
    adres = f"http://localhost:8000/urun/{urun_no}.html"
    cevap = requests.get(adres, headers=BASLIK, timeout=10)  # en fazla 10 sn bekle
    print(f"[{urun_no}] Durum kodu:", cevap.status_code)
    try:
        cevap.raise_for_status()  # 404, 500 gibi bir hata varsa istisna fırlatır
    except requests.HTTPError as hata:
        print("   Hata:", hata, "→ ayrıştırılmadı")
        return

    soup = BeautifulSoup(cevap.text, "html.parser")
    # 1) find: etiket adı + öznitelik ile (ilk eşleşeni verir)
    ad = soup.find("h1", id="urun-ad").get_text(strip=True)
    # 2) select_one: CSS seçici ile (Ders 1.4'teki seçicinin aynısı)
    fiyat = soup.select_one("span#fiyat").get_text(strip=True)
    aciklama = soup.select_one("#aciklama").get_text(strip=True)
    # 3) Bağlantının adresi metinde değil, href özniteliğinde
    liste = soup.find("a", id="listeye-don")["href"]
    # 4) find_all: aynı türden bütün etiketler (liste döner)
    ozellikler = [th.get_text(strip=True) for th in soup.find_all("th")]

    print("   Ürün     :", ad)
    print("   Fiyat    :", fiyat)
    print("   Açıklama :", aciklama)
    print("   Liste    :", liste)
    print("   Özellik başlıkları:", ", ".join(ozellikler))


for no in sys.argv[1:] or ["1001"]:
    urun_oku(no)
