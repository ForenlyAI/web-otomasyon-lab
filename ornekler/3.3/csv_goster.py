"""Ders 3.3 — Yazılan kargo.csv dosyasını bir tablo programı gibi okur ve gösterir.

Dosyanın başında Excel'in Türkçe harfleri doğru okuması için
UTF-8 imzası (BOM) olup olmadığını da kontrol eder.

Önce:   uv run python ornekler/3.3/kargo.py
Sonra:  uv run python ornekler/3.3/csv_goster.py
"""

import csv
from pathlib import Path

DOSYA = Path(__file__).with_name("kargo.csv")

ham = DOSYA.read_bytes()
print("Dosya:", DOSYA.name, "·", len(ham), "bayt")
print("UTF-8 imzası (BOM) var mı:", "evet" if ham.startswith(b"\xef\xbb\xbf") else "hayır")
print()

with open(DOSYA, newline="", encoding="utf-8-sig") as f:
    satirlar = list(csv.reader(f))

genislik = [max(len(s[i]) for s in satirlar) + 3 for i in range(len(satirlar[0]))]
for no, satir in enumerate(satirlar):
    print("  ".join(h.ljust(g) for h, g in zip(satir, genislik)))
    if no == 0:
        print("  ".join("-" * (g - 1) + " " for g in genislik))
