"""Fiyat takip botu dersi için fiyat değişikliği taklidi.

Birkaç ürünün fiyatını değiştirir ve ürün sayfalarını yeniden üretir.
İlk çalıştırmada orijinal veri site/veri/urunler.orijinal.json dosyasına yedeklenir.
Kaç kez çalıştırırsanız çalıştırın değişiklik orijinal fiyatlara göre uygulanır.

Kullanım:
    uv run python fiyat_degistir.py         # fiyatları değiştir
    uv run python fiyat_degistir.py --geri  # orijinal fiyatlara dön
"""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

from site_uret import VERI, tl, uret

YEDEK = VERI.with_name("urunler.orijinal.json")

# ürün id -> çarpan (0.85 = %15 indirim)
DEGISIKLIK = {1001: 0.85, 1018: 0.80, 1026: 1.10}


def degistir() -> None:
    if not YEDEK.exists():
        shutil.copyfile(VERI, YEDEK)
    urunler = json.loads(YEDEK.read_text(encoding="utf-8"))
    for u in urunler:
        if u["id"] in DEGISIKLIK:
            eski = u["fiyat"]
            u["fiyat"] = round(eski * DEGISIKLIK[u["id"]], 2)
            print(f"{u['id']}  {u['ad']}: {tl(eski)} -> {tl(u['fiyat'])}")
    VERI.write_text(json.dumps(urunler, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    uret(sessiz=True)
    print("Sayfalar yeniden üretildi. Geri almak için: uv run python fiyat_degistir.py --geri")


def geri_al() -> None:
    if not YEDEK.exists():
        print("Yedek yok, fiyatlar zaten orijinal.")
        return
    shutil.move(YEDEK, VERI)
    uret(sessiz=True)
    print("Orijinal fiyatlar geri yüklendi, sayfalar yeniden üretildi.")


if __name__ == "__main__":
    geri_al() if "--geri" in sys.argv else degistir()
