"""Ders 5.2 — Hız sınırı ve saygılı tarama.

Saygılı bir bot:
  - kendini tanıtan bir User-Agent gönderir (kim olduğunu ve nasıl ulaşılacağını söyler),
  - robots.txt'yi okur: yasaklı yolu atlar, Crawl-delay kadar bekler,
  - aynı adresi iki kez indirmez (basit önbellek),
  - 429 / 503 alırsa Retry-After kadar (yoksa artan sürelerle) bekler, birkaç denemeden sonra vazgeçer,
  - yaptığı her şeyi zaman damgasıyla bot.log dosyasına yazar.

Çalıştırma:  uv run python ornekler/5.2/saygili.py
"""

import logging
import time
from pathlib import Path
from urllib.parse import urljoin
from urllib.robotparser import RobotFileParser

import requests

KOK = "http://localhost:8000/"
# Kim olduğunuzu ve size nasıl ulaşılacağını yazın (örnek adres).
KIMLIK = "PratikBot/1.0 (+ders 5.2; iletisim: ornek@example.com)"
KLASOR = Path(__file__).resolve().parent

gunluk = logging.getLogger("bot")


def gunluk_kur(dosya="bot.log"):
    """Zaman damgalı günlük: hem dosyaya hem ekrana yazar."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%H:%M:%S",
        handlers=[logging.FileHandler(KLASOR / dosya, mode="w", encoding="utf-8"),
                  logging.StreamHandler()],
    )


def getir(oturum, adres, deneme_sayisi=3):
    """Adresi indirir; 429/503'te sunucunun istediği kadar bekleyip yeniden dener."""
    for deneme in range(1, deneme_sayisi + 1):
        yanit = oturum.get(adres, timeout=10)
        if yanit.status_code not in (429, 503):
            return yanit
        # Retry-After saniye olarak gelirse ona uy; yoksa 2, 4, 8 sn bekle.
        bekle = yanit.headers.get("Retry-After")
        bekle = int(bekle) if bekle and bekle.isdigit() else 2 ** deneme
        gunluk.warning("%s -> %s, %s sn bekleniyor (deneme %s)", adres, yanit.status_code, bekle, deneme)
        time.sleep(bekle)
    gunluk.error("%s: %s denemede olmadı, vazgeçildi", adres, deneme_sayisi)
    return None


def main():
    gunluk_kur()
    robots = RobotFileParser(urljoin(KOK, "robots.txt"))
    robots.read()
    gecikme = robots.crawl_delay(KIMLIK) or 1  # robots.txt söylemiyorsa yine de 1 sn
    gunluk.info("robots.txt okundu, istekler arası bekleme: %s sn", gecikme)

    hedefler = ["tablo.html", "urunler/sayfa-1.html", "yonetim/index.html",
                "urunler/sayfa-2.html", "tablo.html"]
    onbellek = {}
    with requests.Session() as oturum:
        oturum.headers["User-Agent"] = KIMLIK
        for yol in hedefler:
            adres = urljoin(KOK, yol)
            if not robots.can_fetch(KIMLIK, adres):
                gunluk.warning("robots.txt — yasaklı yol atlandı: /%s", yol)
                continue
            if adres in onbellek:
                gunluk.info("önbellekten: /%s (istek yok)", yol)
                continue
            yanit = getir(oturum, adres)
            if yanit is None:
                break  # site bizi istemiyor: dur
            onbellek[adres] = yanit.text
            gunluk.info("GET /%s -> %s (%s bayt)", yol, yanit.status_code, len(yanit.content))
            time.sleep(gecikme)  # nezaket beklemesi: robots.txt Crawl-delay
    gunluk.info("bitti: %s sayfa indirildi", len(onbellek))


if __name__ == "__main__":
    main()
