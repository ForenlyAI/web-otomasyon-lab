"""Ders 5.2 — 429 (çok fazla istek) cevabına uymayı denemek.

Pratik Mağaza hiç 429 döndürmez. Bu yüzden bu dosya, yalnız bu deneme için
kendi bilgisayarınızda küçük bir sunucu açar: ilk iki isteğe
"429 Too Many Requests" + "Retry-After: 2" der, üçüncüsüne cevap verir.
saygili.py'deki getir() fonksiyonu bekleyip yeniden dener.

Çalıştırma:  uv run python ornekler/5.2/hiz_siniri_deneme.py
"""

import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from saygili import KIMLIK, getir, gunluk, gunluk_kur  # noqa: E402

gunluk_kur("deneme.log")


class YogunSunucu(BaseHTTPRequestHandler):
    sayac = 0

    def do_GET(self):
        YogunSunucu.sayac += 1
        if YogunSunucu.sayac <= 2:
            self.send_response(429)
            self.send_header("Retry-After", "2")  # "2 saniye sonra tekrar gel"
            self.end_headers()
        else:
            self.send_response(200)
            self.end_headers()
            self.wfile.write("tamam".encode())

    def log_message(self, *args):
        pass


sunucu = HTTPServer(("127.0.0.1", 0), YogunSunucu)  # boş bir port seçer
threading.Thread(target=sunucu.serve_forever, daemon=True).start()
adres = f"http://127.0.0.1:{sunucu.server_port}/veri"

bas = time.perf_counter()
with requests.Session() as oturum:
    oturum.headers["User-Agent"] = KIMLIK
    yanit = getir(oturum, adres)
gunluk.info("sonuç: %s, toplam %.1f sn", yanit.status_code if yanit else "yok", time.perf_counter() - bas)
sunucu.shutdown()
