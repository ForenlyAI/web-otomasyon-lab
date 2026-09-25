"""Ders 4.1 — Aynı işi iki araçla çalıştırıp sonuçları alt alta gösterir.

Önce sunucuyu açın:  uv run python sunucu.py
Sonra:               BASLIKSIZ=1 uv run python ornekler/4.1/karsilastir.py
"""

import subprocess
import sys
from pathlib import Path

KLASOR = Path(__file__).resolve().parent
for ad, dosya in [("Selenium  · açık bekleme yazdık", "selenium_bekleme.py"),
                  ("Playwright · bekleme satırı yok", "pw_bekleme.py")]:
    print(f"── {ad} ──")
    sonuc = subprocess.run([sys.executable, str(KLASOR / dosya)], capture_output=True, text=True)
    print(sonuc.stdout.rstrip() or sonuc.stderr.rstrip())
    print(f"   çıkış kodu: {sonuc.returncode}\n")
