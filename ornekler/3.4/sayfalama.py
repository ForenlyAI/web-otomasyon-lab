"""Ders 3.4 — Sayfalamayı gezip bütün ürünleri tek CSV'de toplamak.

1) Önce robots.txt'yi okur: bu adrese girmemize izin var mı, kaç saniye beklemeliyiz?
2) urunler/sayfa-1.html'den başlar; her sayfada ürünlerin adını, fiyatını, stokunu alır.
3) "Sonraki" bağlantısını izler; göreli adresi urljoin ile tam adrese çevirir.
4) Sonraki bağlantısı yoksa YA DA sayfa üst sınırına gelinmişse durur.
5) İki istek arasında nezaket beklemesi yapar (robots.txt'deki Crawl-delay, yoksa 1 sn).
6) Hepsini urunler.csv'ye yazar.

Önce sunucuyu açın:  uv run python sunucu.py
Sonra:               uv run python ornekler/3.4/sayfalama.py
"""

import csv
import time
from pathlib import Path
from urllib.parse import urljoin
from urllib.robotparser import RobotFileParser

import requests
from bs4 import BeautifulSoup

SITE = "http://localhost:8000/"
BASLANGIC = urljoin(SITE, "urunler/sayfa-1.html")
BOT_ADI = "PratikMagazaOgrenciBotu"
BASLIK = {"User-Agent": f"{BOT_ADI}/1.0 (Web Otomasyonu 101)"}
UST_SINIR = 20  # ne olursa olsun en fazla bu kadar sayfa (sonsuz döngüye karşı)
DOSYA = Path(__file__).with_name("urunler.csv")

# 1) robots.txt
robot = RobotFileParser(urljoin(SITE, "robots.txt"))
robot.read()
if not robot.can_fetch(BOT_ADI, BASLANGIC):
    raise SystemExit("robots.txt bu adrese izin vermiyor — durduk.")
bekleme = robot.crawl_delay(BOT_ADI) or 1
print(f"robots.txt: izin var · istekler arası {bekleme} sn beklenecek")
print("(karşılaştırma) /yonetim/ için izin:", robot.can_fetch(BOT_ADI, urljoin(SITE, "yonetim/")))

urunler = []
adres, sayfa_sayisi = BASLANGIC, 0
while adres and sayfa_sayisi < UST_SINIR:
    cevap = requests.get(adres, headers=BASLIK, timeout=10)
    cevap.raise_for_status()
    soup = BeautifulSoup(cevap.text, "html.parser")
    sayfa_sayisi += 1

    for kart in soup.select("article.urun"):
        urunler.append({
            "id": kart["data-id"],
            "ad": kart.select_one(".urun-ad").get_text(strip=True),
            "fiyat": float(kart.select_one(".fiyat")["data-fiyat"]),
            "stok": int(kart.select_one(".stok")["data-stok"]),
        })
    print(f"Sayfa {sayfa_sayisi}: {adres.rsplit('/', 1)[-1]} → toplam {len(urunler)} ürün")

    sonraki = soup.select_one("nav.sayfalama a.sonraki")
    adres = urljoin(adres, sonraki["href"]) if sonraki else None  # yoksa döngü biter
    if adres:
        time.sleep(bekleme)  # nezaket beklemesi: siteyi yormayalım

with open(DOSYA, "w", newline="", encoding="utf-8-sig") as f:
    yazici = csv.DictWriter(f, fieldnames=["id", "ad", "fiyat", "stok"])
    yazici.writeheader()
    yazici.writerows(urunler)

tukenen = sum(1 for u in urunler if u["stok"] == 0)
print(f"Bitti: {sayfa_sayisi} sayfa, {len(urunler)} ürün ({tukenen} tükendi) → {DOSYA.name}")
