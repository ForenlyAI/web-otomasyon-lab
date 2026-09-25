"""Pratik Mağaza yerel sunucusu.

Kullanım:
    uv run python sunucu.py            # http://localhost:8000
    uv run python sunucu.py 8080       # başka bir port
    uv run python sunucu.py --sessiz   # istek günlüğünü yazdırma

Yalnızca bu bilgisayardan erişilir (127.0.0.1). Durdurmak için Ctrl+C.
"""

from __future__ import annotations

import sys
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

SITE = Path(__file__).resolve().parent / "site"


class Isleyici(SimpleHTTPRequestHandler):
    sessiz = False

    def end_headers(self) -> None:
        # Fiyat değişikliği gibi güncellemeler hemen görünsün: önbellek yok.
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def guess_type(self, path):  # noqa: D401 — metin dosyalarına UTF-8 ekle
        tur = super().guess_type(path)
        if tur.startswith("text/") or tur in ("application/json", "application/javascript"):
            return f"{tur}; charset=utf-8"
        return tur

    def log_message(self, format: str, *args) -> None:
        if not self.sessiz:
            super().log_message(format, *args)


def main() -> None:
    argumanlar = [a for a in sys.argv[1:] if not a.startswith("--")]
    port = int(argumanlar[0]) if argumanlar else 8000
    Isleyici.sessiz = "--sessiz" in sys.argv
    isleyici = partial(Isleyici, directory=str(SITE))
    try:
        sunucu = ThreadingHTTPServer(("127.0.0.1", port), isleyici)
    except OSError:
        print(f"Port {port} kullanımda. Sunucu zaten açık olabilir: http://localhost:{port}")
        print(f"Başka port için: uv run python sunucu.py {port + 1}")
        sys.exit(1)
    print(f"Pratik Mağaza hazır: http://localhost:{port}", flush=True)
    print("Durdurmak için Ctrl+C", flush=True)
    try:
        sunucu.serve_forever()
    except KeyboardInterrupt:
        print("\nSunucu durduruldu.")
    finally:
        sunucu.server_close()


if __name__ == "__main__":
    main()
