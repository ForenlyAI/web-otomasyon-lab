"""Pratik Mağaza statik sayfa üreticisi.

site/veri/urunler.json dosyasından şunları üretir:
  - site/urunler/sayfa-1.html ... sayfa-5.html  (JavaScript'siz ürün listesi)
  - site/urun/<id>.html                         (ürün detay sayfaları)
Ayrıca elle yazılmış sayfalardaki ortak üst menü ve alt bilgiyi
(<!-- ust:basla --> ... <!-- ust:bitti --> işaretleri arası) günceller.

Kullanım:
    uv run python site_uret.py
"""

from __future__ import annotations

import html
import json
import re
from pathlib import Path

LAB = Path(__file__).resolve().parent
SITE = LAB / "site"
VERI = SITE / "veri" / "urunler.json"
SAYFA_BASINA = 10

MENU = [
    ("index.html", "Mağaza"),
    ("urunler/sayfa-1.html", "Ürünler"),
    ("tablo.html", "Tablo"),
    ("giris.html", "Giriş"),
    ("iletisim.html", "İletişim"),
    ("gecikmeli.html", "Gecikmeli"),
    ("sonsuz.html", "Sonsuz"),
    ("pencere.html", "Pencere"),
    ("randevu.html", "Randevu"),
    ("basvuru.html", "Başvuru"),
    ("captcha.html", "CAPTCHA"),
]

KATEGORI = {
    "Ses": ("k-ses", "🎧"),
    "Elektronik": ("k-elektronik", "💻"),
    "Ev & Yaşam": ("k-ev", "🏠"),
    "Kitap": ("k-kitap", "📚"),
    "Spor": ("k-spor", "🏃"),
    "Ofis": ("k-ofis", "📎"),
}

ACIKLAMA = {
    "Ses": "Günlük kullanım için dengeli ses, rahat kullanım ve uzun ömür.",
    "Elektronik": "Masaüstü ve dizüstü bilgisayarlarla sorunsuz çalışan pratik bir yardımcı.",
    "Ev & Yaşam": "Evinizde her gün kullanacağınız dayanıklı ve şık bir ürün.",
    "Kitap": "Konuyu sıfırdan, bol örnekle anlatan Türkçe kaynak.",
    "Spor": "Evde ve dışarıda antrenman için hafif ve sağlam.",
    "Ofis": "Çalışma masanızı düzenli ve verimli tutmak için.",
}

e = html.escape


def tl(fiyat: float) -> str:
    """1249.9 -> '1.249,90 TL' (Türkçe biçim)."""
    s = f"{fiyat:,.2f}"  # 1,249.90
    return s.replace(",", "_").replace(".", ",").replace("_", ".") + " TL"


def stok_html(stok: int, etiket: str = "span", ek: str = "") -> str:
    if stok == 0:
        sinif, metin = "stok tukendi", "Tükendi"
    elif stok < 5:
        sinif, metin = "stok az", f"Son {stok} adet"
    else:
        sinif, metin = "stok", f"Stokta: {stok} adet"
    return f'<{etiket} class="{sinif}"{ek} data-stok="{stok}">{metin}</{etiket}>'


def ust_menu(onek: str, aktif: str) -> str:
    linkler = []
    for dosya, etiket in MENU:
        sinif = ' class="aktif"' if dosya == aktif else ""
        linkler.append(f'<a href="{onek}{dosya}"{sinif}>{etiket}</a>')
    return (
        '<header class="ust"><div class="ust-ic">'
        f'<a class="logo" href="{onek}index.html"><span class="logo-isaret">P</span>Pratik Mağaza</a>'
        f'<nav class="menu" id="menu" aria-label="Ana menü">{"".join(linkler)}</nav>'
        "</div></header>"
    )


ALT = (
    '<footer class="alt">Pratik Mağaza — Web Otomasyonu 101 alıştırma sitesi. '
    "Gerçek bir mağaza değildir: sipariş, ödeme ve kişisel veri yoktur.</footer>"
)


def sayfa(baslik: str, onek: str, aktif: str, govde: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(baslik)} · Pratik Mağaza</title>
<link rel="stylesheet" href="{onek}css/stil.css">
</head>
<body>
<!-- ust:basla -->{ust_menu(onek, aktif)}<!-- ust:bitti -->
<main>
{govde}
</main>
<!-- alt:basla -->{ALT}<!-- alt:bitti -->
</body>
</html>
"""


def urun_karti(u: dict) -> str:
    sinif, ikon = KATEGORI[u["kategori"]]
    return f"""<article class="urun" data-id="{u['id']}" data-kategori="{e(u['kategori'])}">
  <div class="urun-gorsel {sinif}" aria-hidden="true">{ikon}</div>
  <span class="kategori">{e(u['kategori'])}</span>
  <h3 class="urun-ad">{e(u['ad'])}</h3>
  <span class="fiyat" data-fiyat="{u['fiyat']:.2f}">{tl(u['fiyat'])}</span>
  {stok_html(u['stok'])}
  <a class="detay" href="../urun/{u['id']}.html">Detayı gör →</a>
</article>"""


def liste_sayfasi(no: int, toplam_sayfa: int, urunler: list[dict], toplam_urun: int) -> str:
    kartlar = "\n".join(urun_karti(u) for u in urunler)
    parcalar = []
    if no > 1:
        parcalar.append(f'<a class="onceki" href="sayfa-{no - 1}.html">Önceki</a>')
    for i in range(1, toplam_sayfa + 1):
        if i == no:
            parcalar.append(f'<a class="sayfa-no aktif" href="sayfa-{i}.html" aria-current="page">{i}</a>')
        else:
            parcalar.append(f'<a class="sayfa-no" href="sayfa-{i}.html">{i}</a>')
    if no < toplam_sayfa:
        parcalar.append(f'<a class="sonraki" href="sayfa-{no + 1}.html">Sonraki</a>')
    govde = f"""<div class="ekmek"><a href="../index.html">Mağaza</a> › Ürünler › Sayfa {no}</div>
<h1>Tüm Ürünler</h1>
<p class="alt-baslik" id="sayfa-bilgi">Sayfa {no} / {toplam_sayfa} · toplam {toplam_urun} ürün · Bu sayfa JavaScript kullanmaz.</p>
<section class="urun-izgara" id="urun-listesi">
{kartlar}
</section>
<nav class="sayfalama" aria-label="Sayfalama">
  {chr(10).join('  ' + p for p in parcalar).strip()}
</nav>"""
    return sayfa(f"Ürünler — Sayfa {no}", "../", "urunler/sayfa-1.html", govde)


def detay_sayfasi(u: dict, liste_no: int) -> str:
    sinif, ikon = KATEGORI[u["kategori"]]
    tukendi = u["stok"] == 0
    dugme = (
        '<button class="dugme" id="sepete-ekle" disabled>Stokta yok</button>'
        if tukendi
        else '<button class="dugme" id="sepete-ekle" type="button">Sepete ekle</button>'
    )
    govde = f"""<div class="ekmek"><a href="../index.html">Mağaza</a> › <a href="../urunler/sayfa-{liste_no}.html">Ürünler</a> › {e(u['ad'])}</div>
<article class="urun-detay panel" data-id="{u['id']}">
  <div class="detay-kutu">
    <div class="detay-gorsel {sinif}" aria-hidden="true">{ikon}</div>
    <div>
      <span class="kategori" id="kategori">{e(u['kategori'])}</span>
      <h1 id="urun-ad">{e(u['ad'])}</h1>
      <p><span class="fiyat" id="fiyat" data-fiyat="{u['fiyat']:.2f}" style="font-size:30px">{tl(u['fiyat'])}</span></p>
      <p>{stok_html(u['stok'], 'span', ' id="stok"')}</p>
      <p id="aciklama">{ACIKLAMA[u['kategori']]}</p>
      <table class="ozellikler">
        <tr><th>Ürün kodu</th><td id="urun-kodu">PM-{u['id']}</td></tr>
        <tr><th>Kategori</th><td>{e(u['kategori'])}</td></tr>
        <tr><th>Kargo</th><td>1–3 iş günü</td></tr>
      </table>
      <p style="margin-top:20px">{dugme}</p>
      <p id="sepet-mesaj" class="basari gizli">Bu bir alıştırma sitesidir, sepet yoktur. Tıklama çalıştı!</p>
      <p><a href="../urunler/sayfa-{liste_no}.html" id="listeye-don">← Ürün listesine dön</a></p>
    </div>
  </div>
</article>
<script>
  var d = document.getElementById('sepete-ekle');
  if (d) d.addEventListener('click', function () {{
    document.getElementById('sepet-mesaj').classList.remove('gizli');
  }});
</script>"""
    return sayfa(u["ad"], "../", "urunler/sayfa-1.html", govde)


def menuyu_guncelle() -> int:
    """Elle yazılmış sayfalardaki üst menü/alt bilgi bloklarını yeniler."""
    sayi = 0
    for yol in sorted(SITE.rglob("*.html")):
        goreli = yol.relative_to(SITE).as_posix()
        if goreli.startswith(("urunler/", "urun/")):
            continue
        metin = yol.read_text(encoding="utf-8")
        if "<!-- ust:basla -->" not in metin:
            continue
        onek = "../" * goreli.count("/")
        yeni = re.sub(
            r"<!-- ust:basla -->.*?<!-- ust:bitti -->",
            lambda _: f"<!-- ust:basla -->{ust_menu(onek, goreli)}<!-- ust:bitti -->",
            metin,
            flags=re.S,
        )
        yeni = re.sub(
            r"<!-- alt:basla -->.*?<!-- alt:bitti -->",
            lambda _: f"<!-- alt:basla -->{ALT}<!-- alt:bitti -->",
            yeni,
            flags=re.S,
        )
        if yeni != metin:
            yol.write_text(yeni, encoding="utf-8")
            sayi += 1
    return sayi


def uret(sessiz: bool = False) -> None:
    urunler = json.loads(VERI.read_text(encoding="utf-8"))
    toplam_sayfa = (len(urunler) + SAYFA_BASINA - 1) // SAYFA_BASINA

    (SITE / "urunler").mkdir(exist_ok=True)
    (SITE / "urun").mkdir(exist_ok=True)
    for eski in list((SITE / "urunler").glob("sayfa-*.html")) + list((SITE / "urun").glob("*.html")):
        eski.unlink()

    for no in range(1, toplam_sayfa + 1):
        dilim = urunler[(no - 1) * SAYFA_BASINA : no * SAYFA_BASINA]
        (SITE / "urunler" / f"sayfa-{no}.html").write_text(
            liste_sayfasi(no, toplam_sayfa, dilim, len(urunler)), encoding="utf-8"
        )
    for i, u in enumerate(urunler):
        (SITE / "urun" / f"{u['id']}.html").write_text(
            detay_sayfasi(u, i // SAYFA_BASINA + 1), encoding="utf-8"
        )
    guncellenen = menuyu_guncelle()
    if not sessiz:
        print(f"{toplam_sayfa} liste sayfası ve {len(urunler)} detay sayfası üretildi.")
        if guncellenen:
            print(f"{guncellenen} sayfanın üst menüsü güncellendi.")


if __name__ == "__main__":
    uret()
