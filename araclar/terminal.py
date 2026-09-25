"""Bir komutu çalıştırır, GERÇEK çıktısını terminal görünümünde ekran görüntüsü yapar.

Kullanım (lab klasöründen):
    uv run python araclar/terminal.py <ders> <ad> -- <komut ...>

Örnek:
    uv run python araclar/terminal.py 1.3 terminal -- BASLIKSIZ=1 python ornekler/1.3/ilk_otomasyon.py

- Komut lab klasöründe çalışır; stdout ve stderr birlikte, geldiği sırayla yakalanır.
- Komutun başındaki AD=DEĞER parçaları ortam değişkeni olarak uygulanır ve istem satırında görünür.
- Görüntü: lab/ekran/<ders>/<ad>.png (1280×800). Ham çıktı: aynı yerde <ad>.txt
- Görüntüde yalnızca istem satırı (çalıştırılan komut) ve komutun kendi çıktısı vardır.
  Çıktı sığmazsa yazı 20 px'ten 16 px'e kadar küçülür; yine sığmazsa baştaki satırlar
  gösterilmez ve bu durum pencere başlığında yazılır.
- Çıkış kodu, çalıştırılan komutunkiyle aynıdır.
"""

from __future__ import annotations

import html
import os
import re
import shlex
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from araclar.ekran import GENISLIK, YUKSEKLIK, LAB, ekran_yolu  # noqa: E402

FONT = LAB / "site" / "fonts"
ANSI = re.compile(r"\x1b\[[0-9;?]*[ -/]*[@-~]")
ORTAM = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=")

SABLON = """<!DOCTYPE html>
<html lang="tr"><head><meta charset="utf-8">
<style>
@font-face {{ font-family: "Terminal Mono"; src: url("{font_latin}") format("woff2");
  unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+2000-206F, U+20AC, U+2122, U+2212; }}
@font-face {{ font-family: "Terminal Mono"; src: url("{font_ext}") format("woff2");
  unicode-range: U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+1E00-1E9F; }}
html, body {{ margin: 0; height: 100%; background: #1b2130; }}
body {{ padding: 28px; box-sizing: border-box; }}
.pencere {{ height: 100%; display: flex; flex-direction: column; border-radius: 12px; overflow: hidden;
  background: #0f141f; box-shadow: 0 18px 50px rgba(0,0,0,.45); border: 1px solid #2a3245; }}
.baslik {{ height: 40px; flex: none; display: flex; align-items: center; gap: 8px; padding: 0 16px;
  background: #1a2130; color: #8b94a8; font: 15px "Terminal Mono", monospace; }}
.baslik i {{ width: 13px; height: 13px; border-radius: 50%; display: inline-block; }}
.baslik .ad {{ margin-left: 12px; }}
.baslik .not {{ margin-left: auto; color: #e0b454; }}
pre {{ margin: 0; padding: 20px 24px; flex: 1; overflow: hidden; white-space: pre-wrap; word-break: break-word;
  font-family: "Terminal Mono", "DejaVu Sans Mono", monospace; font-variant-ligatures: none;
  font-size: {boyut}px; line-height: 1.45; color: #d6dbe6; }}
.istem {{ color: #6fd08c; }}
.komut {{ color: #ffffff; font-weight: 700; }}
.imlec {{ background: #d6dbe6; color: #0f141f; }}
</style></head>
<body><div class="pencere">
<div class="baslik"><i style="background:#ff5f57"></i><i style="background:#febc2e"></i><i style="background:#28c840"></i>
<span class="ad">lab — terminal</span><span class="not">{not_}</span></div>
<pre id="ekran"><span class="istem">~/lab $</span> <span class="komut">{komut}</span>
{cikti}<span class="istem">~/lab $</span> <span class="imlec"> </span></pre>
</div></body></html>
"""


def calistir(parcalar: list[str]) -> tuple[str, int, str]:
    ortam = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUNBUFFERED="1", NO_COLOR="1")
    i = 0
    while i < len(parcalar) and ORTAM.match(parcalar[i]):
        ad, deger = parcalar[i].split("=", 1)
        ortam[ad] = deger
        i += 1
    komut = parcalar[i:]
    if not komut:
        sys.exit("Çalıştırılacak komut yok.")
    sonuc = subprocess.run(
        komut, cwd=LAB, env=ortam, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True, encoding="utf-8", errors="replace",
    )
    cikti = ANSI.sub("", sonuc.stdout).replace("\r\n", "\n")
    return cikti, sonuc.returncode, shlex.join(parcalar)


def html_uret(komut: str, satirlar: list[str], boyut: int, gizli: int) -> str:
    metin = "".join(html.escape(s) + "\n" for s in satirlar)
    not_ = f"ilk {gizli} satır görüntüye sığmadı (tamamı .txt dosyasında)" if gizli else ""
    return SABLON.format(
        font_latin=(FONT / "jetbrains-mono-400-latin.woff2").as_uri(),
        font_ext=(FONT / "jetbrains-mono-400-latin-ext.woff2").as_uri(),
        boyut=boyut, komut=html.escape(komut), cikti=metin, not_=html.escape(not_),
    )


def goruntule(komut: str, cikti: str, hedef: Path) -> None:
    from playwright.sync_api import sync_playwright

    satirlar = cikti.rstrip("\n").split("\n") if cikti.strip() else []
    with sync_playwright() as p, tempfile.TemporaryDirectory() as gecici:
        tarayici = p.chromium.launch()
        sayfa = tarayici.new_page(viewport={"width": GENISLIK, "height": YUKSEKLIK})
        dosya = Path(gecici) / "terminal.html"

        def dene(boyut: int, gizli: int) -> bool:
            dosya.write_text(html_uret(komut, satirlar[gizli:], boyut, gizli), encoding="utf-8")
            sayfa.goto(dosya.as_uri())
            sayfa.evaluate("document.fonts.ready.then(() => true)")
            return sayfa.evaluate(
                "(() => { const e = document.getElementById('ekran'); return e.scrollHeight <= e.clientHeight; })()"
            )

        boyut, gizli = 20, 0
        while not dene(boyut, gizli):
            if boyut > 16:
                boyut -= 1
            elif gizli < len(satirlar):
                gizli += 1
            else:
                break
        sayfa.screenshot(path=str(hedef))
        tarayici.close()


def main() -> int:
    arg = sys.argv[1:]
    if "--" not in arg or arg.index("--") != 2:
        print(__doc__)
        return 2
    ders, ad, parcalar = arg[0], arg[1], arg[3:]
    cikti, kod, komut = calistir(parcalar)
    hedef = ekran_yolu(ders, ad)
    hedef.with_suffix(".txt").write_text(f"$ {komut}\n{cikti}", encoding="utf-8")
    goruntule(komut, cikti, hedef)
    print(f"Terminal görüntüsü: {hedef.relative_to(LAB)} (komut çıkış kodu: {kod})")
    return kod


if __name__ == "__main__":
    sys.exit(main())
