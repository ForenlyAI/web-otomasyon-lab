"""Ders 3.3 — Sayfadaki tabloyu temiz bir CSV dosyasına çevirmek.

tablo.html'deki kargo tablosunu satır satır, hücre hücre okur:
- başlık satırındaki (thead) metinleri sütun adı yapar,
- "49,90" gibi Türkçe yazılmış parayı sayıya (49.9) çevirir,
- yalnız gereken sütunları alır (veri azaltma),
- csv.DictWriter ile kargo.csv dosyasına yazar.
  Kodlama "utf-8-sig": Excel dosyayı açınca Türkçe harfler bozulmaz.

Önce sunucuyu açın:  uv run python sunucu.py
Sonra:               uv run python ornekler/3.3/kargo.py
"""

import csv
from pathlib import Path

import requests
from bs4 import BeautifulSoup

ADRES = "http://localhost:8000/tablo.html"
BASLIK = {"User-Agent": "PratikMagazaOgrenciBotu/1.0 (Web Otomasyonu 101)"}
DOSYA = Path(__file__).with_name("kargo.csv")
ALINACAK = ["Şehir", "Süre (gün)", "Ücret (TL)"]  # işinize yaramayan sütunu buradan çıkarın


def sayiya_cevir(metin):
    """'1.249,90 TL' → 1249.9 · '49,90' → 49.9"""
    temiz = metin.replace("TL", "").strip()
    temiz = temiz.replace(".", "").replace(",", ".")  # binlik noktayı sil, virgülü nokta yap
    return float(temiz)


cevap = requests.get(ADRES, headers=BASLIK, timeout=10)
cevap.raise_for_status()
soup = BeautifulSoup(cevap.text, "html.parser")
tablo = soup.find("table", id="kargo")

# Başlık satırı → sütun adları
basliklar = [th.get_text(strip=True) for th in tablo.thead.find_all("th")]
print("Başlıklar:", basliklar)

satirlar = []
for tr in tablo.tbody.find_all("tr"):
    hucreler = [td.get_text(strip=True) for td in tr.find_all("td")]
    kayit = dict(zip(basliklar, hucreler))              # {"Şehir": "İstanbul", ...}
    kayit = {ad: kayit[ad] for ad in ALINACAK}          # yalnız gereken sütunlar
    kayit["Süre (gün)"] = int(kayit["Süre (gün)"])
    kayit["Ücret (TL)"] = sayiya_cevir(kayit["Ücret (TL)"])
    satirlar.append(kayit)

with open(DOSYA, "w", newline="", encoding="utf-8-sig") as f:
    yazici = csv.DictWriter(f, fieldnames=ALINACAK)
    yazici.writeheader()
    yazici.writerows(satirlar)

print(f"{len(satirlar)} satır yazıldı →", DOSYA.name)
print("Örnek dönüşüm: '1.249,90 TL' →", sayiya_cevir("1.249,90 TL"))
print("En pahalı:", max(satirlar, key=lambda s: s["Ücret (TL)"]))
