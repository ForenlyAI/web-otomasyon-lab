"""Ders 6.2 — Fiyat takip botu.

Her çalıştırmada:
  1) takip listesindeki ürünlerin fiyatını ürün sayfasından çeker (requests + BeautifulSoup),
  2) fiyatlar.csv dosyasındaki BİR ÖNCEKİ kayıtla karşılaştırır,
  3) fiyat eşikten fazla düştüyse UYARI yazar,
  4) yeni fiyatları tarih-saat damgasıyla CSV'nin sonuna EKLER (eski satırlar silinmez).

Çalıştırma:  uv run python ornekler/6.2/fiyat_takip.py
Deneme:      uv run python fiyat_degistir.py      (3 ürünün fiyatını değiştirir)
             uv run python ornekler/6.2/fiyat_takip.py
             uv run python fiyat_degistir.py --geri
Gerçek hayatta günde bir çalıştırmak çoğu iş için yeter (cron / Görev Zamanlayıcı).
"""

import csv
import time
from datetime import datetime
from pathlib import Path

import requests
from bs4 import BeautifulSoup

TAKIP = [1001, 1018, 1026]  # ürün numaraları
ESIK = 5.0  # yüzde: bundan fazla düşüşte uyarı
CSV = Path(__file__).resolve().parent / "fiyatlar.csv"
ALANLAR = ["zaman", "id", "ad", "fiyat"]


def onceki_fiyatlar():
    """CSV'deki her ürünün en son fiyatı: {id: fiyat}."""
    if not CSV.exists():
        return {}
    with CSV.open(encoding="utf-8", newline="") as f:
        return {int(s["id"]): float(s["fiyat"]) for s in csv.DictReader(f)}  # son satır kazanır


def fiyat_cek(oturum, urun_id):
    yanit = oturum.get(f"http://localhost:8000/urun/{urun_id}.html", timeout=10)
    yanit.raise_for_status()
    sayfa = BeautifulSoup(yanit.text, "html.parser")
    ad = sayfa.select_one("#urun-ad").get_text(strip=True)
    fiyat = float(sayfa.select_one("#fiyat")["data-fiyat"])  # sayı, biçimsiz
    return ad, fiyat


onceki = onceki_fiyatlar()
zaman = datetime.now().strftime("%Y-%m-%d %H:%M")
yeni = []
with requests.Session() as oturum:
    oturum.headers["User-Agent"] = "PratikBot/1.0 (+ders 6.2; iletisim: ornek@example.com)"
    for urun_id in TAKIP:
        ad, fiyat = fiyat_cek(oturum, urun_id)
        eski = onceki.get(urun_id)
        if eski is None:
            durum = "ilk kayıt"
        else:
            degisim = (fiyat - eski) / eski * 100
            if degisim <= -ESIK:
                durum = f"UYARI: fiyat düştü %{-degisim:.0f} ({eski:.2f} -> {fiyat:.2f})"
            elif degisim > 0:
                durum = f"arttı %{degisim:.0f} ({eski:.2f} -> {fiyat:.2f})"
            else:
                durum = "değişmedi"
        print(f"{urun_id} {ad:<28} {fiyat:>9.2f} TL  {durum}")
        yeni.append({"zaman": zaman, "id": urun_id, "ad": ad, "fiyat": f"{fiyat:.2f}"})
        time.sleep(1)  # nezaket beklemesi (robots.txt Crawl-delay: 1)

ilk_kez = not CSV.exists()
with CSV.open("a", encoding="utf-8", newline="") as f:  # "a" = sona ekle
    yazici = csv.DictWriter(f, fieldnames=ALANLAR)
    if ilk_kez:
        yazici.writeheader()
    yazici.writerows(yeni)
print(f"{len(yeni)} satır eklendi: ornekler/6.2/fiyatlar.csv")
