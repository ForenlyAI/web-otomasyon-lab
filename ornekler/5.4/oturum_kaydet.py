"""Ders 5.4 — Bir kez giriş yap, oturumu dosyaya kaydet (Playwright storage_state).

Kullanıcı adı ve parola KODDA YAZMAZ: önce ortam değişkenine (PRATIK_KULLANICI,
PRATIK_SIFRE), yoksa bu klasördeki .env dosyasına bakılır. .env ve durum.json
.gitignore içindedir: depoya konmaz, kimseyle paylaşılmaz.

Çalıştırma:  uv run python ornekler/5.4/oturum_kaydet.py
Sonra:       uv run python ornekler/5.4/oturum_kullan.py   (girişsiz açar)
"""

import os
import sys
from pathlib import Path

from playwright.sync_api import expect, sync_playwright

KLASOR = Path(__file__).resolve().parent
DURUM = KLASOR / "durum.json"  # parolanız kadar gizli!


def gizli(ad: str) -> str:
    """Önce ortam değişkeni, sonra .env satırı. İkisi de yoksa dur."""
    if os.environ.get(ad):
        return os.environ[ad]
    env = KLASOR / ".env"
    if env.exists():
        for satir in env.read_text(encoding="utf-8").splitlines():
            if satir.startswith(ad + "="):
                return satir.split("=", 1)[1].strip()
    sys.exit(f"{ad} bulunamadı: .env.ornek dosyasını .env olarak kopyalayıp doldurun.")


with sync_playwright() as p:
    tarayici = p.chromium.launch(headless=os.environ.get("GORUNUR") != "1")
    baglam = tarayici.new_context()
    sayfa = baglam.new_page()
    sayfa.goto("http://localhost:8000/giris.html")
    sayfa.get_by_label("Kullanıcı adı").fill(gizli("PRATIK_KULLANICI"))
    sayfa.get_by_label("Şifre").fill(gizli("PRATIK_SIFRE"))
    sayfa.get_by_role("button", name="Giriş yap").click()
    expect(sayfa.locator("#karsilama")).to_contain_text("Hoş geldin")  # giriş oldu mu?

    for c in baglam.cookies():  # çerezleri okumak
        print(f"çerez: {c['name']} = {c['value'][:12]}… (yol {c['path']})")
    baglam.storage_state(path=str(DURUM))  # çerez + yerel depolama → dosya
    print("Oturum kaydedildi:", DURUM.relative_to(KLASOR.parents[1]))
    tarayici.close()
