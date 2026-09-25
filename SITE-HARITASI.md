# Pratik Mağaza — Site Haritası (sözleşme)

Ders örnekleri aşağıdaki id ve sınıflara dayanır. **Bunları değiştirmeyin**; değiştirmek
gerekirse tüm `ornekler/` dosyalarını ve ders metinlerini birlikte güncelleyin.

Adres: `http://localhost:8000/` · Sunucu: `uv run python sunucu.py`

Her sayfada ortak üst menü vardır: `header.ust` › `nav#menu` (etkin sayfa bağlantısında `a.aktif`).

## index.html — Mağaza ana sayfası (JavaScript)

| Seçici | Açıklama |
|---|---|
| `form#arama-formu` | GET formu, `action="index.html"`; `index.html?q=kitap` adresi de aramayı çalıştırır |
| `input#arama` (`name="q"`) | Arama kutusu |
| `button#ara-dugme` | Ara düğmesi |
| `#sonuc-sayisi` | Aramadan önce `Tüm ürünler (50)`, aramadan sonra `N ürün bulundu`; `data-sayi="N"` |
| `#urun-listesi article.urun` | Ürün kartları (JS ile `veri/urunler.json`'dan çizilir, yapısı aşağıdaki gibi) |
| `#toplam-urun` | Toplam ürün sayısı |

Arama ad ve kategori içinde, Türkçe küçük harfe çevirerek yapılır. `kulaklık` → 5 ürün, `kitap` → 7 ürün.

## urunler/sayfa-1.html … sayfa-5.html — Statik ürün listesi (JavaScript yok)

`site_uret.py` tarafından `site/veri/urunler.json` dosyasından üretilir. Sayfa başına 10 ürün.

```html
<section class="urun-izgara" id="urun-listesi">
  <article class="urun" data-id="1001" data-kategori="Ses">
    <span class="kategori">Ses</span>
    <h3 class="urun-ad">Kablosuz Kulaklık X200</h3>
    <span class="fiyat" data-fiyat="1249.90">1.249,90 TL</span>
    <span class="stok" data-stok="24">Stokta: 24 adet</span>
    <a class="detay" href="../urun/1001.html">Detayı gör →</a>
  </article>
</section>
<nav class="sayfalama">
  <a class="onceki" href="sayfa-1.html">Önceki</a>          <!-- ilk sayfada yok -->
  <a class="sayfa-no" href="sayfa-1.html">1</a>
  <a class="sayfa-no aktif" href="sayfa-2.html" aria-current="page">2</a> …
  <a class="sonraki" href="sayfa-3.html">Sonraki</a>       <!-- son sayfada yok -->
</nav>
```

- Stok metni: `Stokta: N adet` (`span.stok`), 1–4 adet için `Son N adet` (`span.stok.az`), 0 için `Tükendi` (`span.stok.tukendi`). Sayı her zaman `data-stok` içinde.
- Fiyat ekranda Türkçe biçimde (`1.249,90 TL`), sayı olarak `data-fiyat` içinde (`1249.90`).
- `#sayfa-bilgi`: `Sayfa 2 / 5 · toplam 50 ürün …`
- Veri: 50 ürün, id 1001–1050, 6 kategori (Ses, Elektronik, Ev & Yaşam, Kitap, Spor, Ofis), 3 üründe stok 0.

## urun/&lt;id&gt;.html — Ürün detayı (1001.html … 1050.html)

| Seçici | Açıklama |
|---|---|
| `article.urun-detay[data-id]` | Kapsayıcı |
| `h1#urun-ad` | Ürün adı |
| `span#fiyat.fiyat[data-fiyat]` | Fiyat |
| `span#stok.stok[data-stok]` | Stok |
| `#kategori`, `#aciklama`, `#urun-kodu` (`PM-1001`) | Diğer bilgiler |
| `button#sepete-ekle` | Stokta yoksa `disabled`; tıklanınca `#sepet-mesaj` görünür |
| `a#listeye-don` | Ürünün bulunduğu liste sayfasına döner |

## tablo.html — Tablo ve liste (JavaScript yok)

- `table#kargo`: `thead` içinde başlık satırı (`Şehir`, `Süre (gün)`, `Ücret (TL)`), `tbody` içinde 8 satır (İstanbul … Van). Ücretler `49,90` biçiminde.
- `ul#sss`: 5 `li`, her birinde `span.soru` ve `span.cevap`.

## giris.html / hesap.html — Oturum ve çerez

| Seçici | Açıklama |
|---|---|
| `#kullanici`, `#sifre`, `button#giris-dugme` | Giriş formu (`form#giris-formu`) |
| `#hata` | Yanlış bilgide görünür: `Kullanıcı adı veya şifre hatalı.` |
| Deneme hesabı | `ogrenci` / `pratik123` (sayfada yazılı) |
| Çerez | Başarılı girişte `oturum=ogrenci-<8 hex>` (path=/), ardından `hesap.html` |
| `hesap.html` › `#karsilama` | `Hoş geldin, ogrenci`; çerez yoksa `giris.html`'e yönlendirir |
| `#cerez-degeri`, `button#cikis` | Çerezin değeri; çıkış çerezi siler |

## iletisim.html — Form doldurma ve açık bekleme

| Seçici | Tür |
|---|---|
| `#ad` | metin |
| `#eposta` | e-posta |
| `select#konu` | değerler: `siparis`, `iade`, `kargo`, `oneri` |
| `input[name="oncelik"]` | radyo: `#oncelik-dusuk` (varsayılan), `#oncelik-normal`, `#oncelik-yuksek` |
| `#kvkk` | onay kutusu (zorunlu) |
| `textarea#mesaj` | mesaj |
| `button#gonder` | gönder |
| `#yukleniyor` | gönderim sırasında görünen dönen simge |
| `div#sonuc` | **1,5 s sonra** görünür: `Mesajınız alındı` + konu/öncelik özeti |
| `#hata` | eksik alan varsa: `Eksik alan: …` |

## gecikmeli.html — Açık bekleme

- `ul#liste`: sayfa açıldıktan **2–4 s sonra** (her seferinde rastgele) 6 adet `li.oge` eklenir. Gecikme `body[data-gecikme-ms]` içinde.
- `#oge-sayisi`: `6 öğe yüklendi`. `#yukleniyor` o ana kadar görünür.
- `button#hazir`: başta `disabled`, **3 s sonra** etkin. Tıklanınca `#hazir-mesaj` görünür.

## sonsuz.html — Sonsuz kaydırma

- `#kartlar article.kart[data-no]`: başta 10 kart; sayfa sonuna kaydırınca 0,6 s içinde 10 kart daha, en fazla 50.
- `#kart-sayisi`: `20 / 50 kart`. `#yukleniyor` yükleme sırasında görünür. `#son` 50'ye ulaşınca görünür.

## pencere.html — Çoklu pencere ve iframe

- `a#yeni-sekme-link` (`target="_blank"`) → `yeni-sekme.html` (`h1` metni `Yeni sekme`, `#sekme-mesaj`).
- `iframe#cerceve` (`name="cerceve"`, `src="cerceve.html"`) → içinde `button#cerceve-dugme`; tıklanınca `#cerceve-mesaj` = `Çerçevenin içinden merhaba!`

## randevu.html — Randevu botu

| Seçici | Açıklama |
|---|---|
| `select#tarih` | İlk seçenek boş (`Tarih seçin…`); sonra 7 gün, değerler `2026-10-05` … `2026-10-11` |
| `#saat-yukleniyor` | Tarih seçilince görünür |
| `#saatler button.saat[data-saat]` | **1 s sonra** 10 saat düğmesi (`09:00` … `15:00`); dolu olanlar `disabled`; seçilen `.secili` |
| `#saat-yok` | Tüm saatler doluysa görünür (7 Ekim Çarşamba tamamen dolu) |
| `#ad-soyad`, `#telefon` | Kişi bilgisi (telefon en az 10 rakam) |
| `button#randevu-onay` | Onay |
| `#randevu-hata` | Eksik alan uyarısı |
| `#onay`, `#onay-ozet`, `#onay-kodu` | Onay kutusu; kod `RND-XXXX` (aynı tarih+saat+ad için hep aynı) |

Tarihler `site/veri/randevu.json` içindeki **sabit** başlangıç gününden (`baz_tarih: 2026-10-05`) gelir; ekran görüntüleri her gün aynı çıkar. Boş saat sayısı: 5 Eki 6, 6 Eki 7, 7 Eki 0, 8 Eki 5, 9 Eki 8, 10 Eki 2, 11 Eki 8.

## basvuru.html — CSV'den toplu form doldurma

| Seçici | Açıklama |
|---|---|
| `#ad`, `#soyad`, `#eposta`, `#telefon` | metin alanları |
| `select#sehir` | seçenek metinleri: Adana, Ankara, Antalya, Bursa, Eskişehir, İstanbul, İzmir, Konya, Trabzon, Van |
| `input[name="deneyim"]` | değerler `yok`, `1-3`, `3+` (id: `#deneyim-yok`, `#deneyim-1-3`, `#deneyim-3-plus`) |
| `textarea#aciklama` | açıklama |
| `button#kaydet` | kaydet (form sıfırlanır, `#kayit-mesaj` 1,5 s görünür) |
| `button#temizle` | kayıtları siler |
| `table#basvurular tbody tr.basvuru` | kayıtlı başvurular (sessionStorage `basvurular`; sekme kapanınca silinir) |
| `#basvuru-sayisi` | `(5)` |
| `#hata` | eksik alan uyarısı |

CSV: `veri/basvurular.csv` — sütunlar `ad,soyad,eposta,telefon,sehir,deneyim,aciklama`, 5 sahte satır (`ornek1@example.com` …).

## captcha.html — Botun durduğu yer

- `#captcha` (`data-bot-kontrolu="captcha"`), `#captcha-kutu`, `input#robot-degilim`, ayrıca `<meta name="bot-kontrolu" content="captcha">`.
- Doğru bot davranışı: bu işaretleri görünce **durmak** ve insana haber vermek. Aşma yöntemi öğretilmez.

## robots.txt ve yonetim/

- `robots.txt`: `User-agent: *` · `Disallow: /yonetim/` · `Crawl-delay: 1`
- `yonetim/index.html`: `h1#yonetim-baslik` — robots.txt'ye uymayan botun geldiği sayfa.

## Fiyat değişikliği (fiyat takip dersi)

`uv run python fiyat_degistir.py` şu fiyatları değiştirir ve sayfaları yeniden üretir:

| id | Ürün | Önce | Sonra |
|---|---|---|---|
| 1001 | Kablosuz Kulaklık X200 | 1.249,90 TL | 1.062,41 TL (−%15) |
| 1018 | Gürültü Önleyici Kulaklık | 3.499,00 TL | 2.799,20 TL (−%20) |
| 1026 | Taşınabilir SSD 1 TB | 2.649,00 TL | 2.913,90 TL (+%10) |

`uv run python fiyat_degistir.py --geri` orijinal veriyi geri yükler. Sunucu önbellek kullanmaz (`Cache-Control: no-store`), değişiklik hemen görünür.
