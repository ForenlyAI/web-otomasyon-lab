# Web Otomasyonu 101 — Öğrenci Laboratuvarı

Forenly AI Academy **Web Otomasyonu 101** kursunun çalışma ortamı: çevrimdışı çalışan alıştırma sitesi
**Pratik Mağaza** ve derslerdeki tüm örnek kodlar (Selenium + Playwright).

## En kolay yol: GitHub Codespaces (kurulum yok)

[![Codespace'te aç](https://github.com/codespaces/badge.svg)](https://codespaces.new/ForenlyAI/web-otomasyon-lab)

1. Yukarıdaki düğmeye tıklayın (kişisel GitHub hesabı yeterli; ücretsiz kota içindedir).
2. İlk açılışta ortam birkaç dakika kurulur (uv, paketler, Chromium). Terminalde `Hazır.` yazısını bekleyin.
3. Terminalde tüm örnekleri deneyin:
   ```bash
   bash kontrol.sh
   ```
4. Siteyi tarayıcıda görmek için `uv run python sunucu.py` çalıştırın; **Ports** sekmesindeki 8000 adresini açın.

Codespace'te ekran yoktur; örnekler başlıksız (headless) çalışır (`BASLIKSIZ=1` hazır ayarlıdır).
Ekran görüntüleri `ekran/<ders>/` klasörüne yazılır, soldaki dosya gezgininden açabilirsiniz.
İşiniz bitince Codespace'i durdurun (github.com/codespaces), kotanız boşa harcanmaz.

## Kendi bilgisayarınızda

Bu klasör kursun pratik ortamıdır: **Pratik Mağaza** adlı, tamamen çevrimdışı çalışan bir
alıştırma sitesi ve ders örnekleri. Botlarınızı gerçek sitelere değil buraya yazarsınız;
kimseye yük bindirmez, kural çiğnemezsiniz.

### Kurulum (3 komut)

Önce [uv](https://docs.astral.sh/uv/) kurulu olmalı. Sonra bu klasörde:

```bash
uv sync                                  # Python ve paketleri kurar (sürümler sabit)
uv run playwright install chromium       # Playwright'ın tarayıcısını indirir (bir kez)
uv run python sunucu.py                  # Pratik Mağaza'yı açar: http://localhost:8000
```

Sunucu açıkken tarayıcıda `http://localhost:8000` adresine gidin. Durdurmak için `Ctrl+C`.

Sabit sürümler (`pyproject.toml` + `uv.lock`):

| Paket | Sürüm |
|---|---|
| selenium | 4.49.0 |
| playwright | 1.63.0 |
| beautifulsoup4 | 4.15.0 |
| requests | 2.34.2 |

Python 3.12 veya üzeri gerekir; `uv sync` uygun Python yoksa kendisi indirir.

### Örnekleri çalıştırma

Sunucu bir terminalde açıkken **ikinci bir terminalde**:

```bash
uv run python ornekler/1.3/ilk_otomasyon.py
```

Tarayıcı penceresi açılmadan (headless) çalıştırmak için `BASLIKSIZ=1`:

```bash
BASLIKSIZ=1 uv run python ornekler/1.3/ilk_otomasyon.py      # macOS / Linux
```

Örnekler ekran görüntülerini `ekran/<ders>/` klasörüne kaydeder.

Tüm örnekleri tek seferde denemek için (sunucuyu kendisi açıp kapatır):

```bash
bash kontrol.sh
```

### Windows notları

- uv kurulumu (PowerShell): `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
- Ortam değişkeni PowerShell'de şöyle verilir:
  ```powershell
  $env:BASLIKSIZ = "1"; uv run python ornekler/1.3/ilk_otomasyon.py
  ```
  Komut İstemi'nde (cmd): `set BASLIKSIZ=1` sonra `uv run python ornekler\1.3\ilk_otomasyon.py`
- `kontrol.sh` bir bash betiğidir; Git Bash veya WSL içinde çalıştırın.
- Güvenlik duvarı uyarısı çıkarsa: sunucu yalnızca bu bilgisayarı dinler (127.0.0.1), izin vermeniz gerekmez.

### macOS notları

- uv kurulumu: `curl -LsSf https://astral.sh/uv/install.sh | sh` (veya `brew install uv`)
- Google Chrome kurulu olmalı. Selenium Manager uygun ChromeDriver'ı kendisi indirir;
  elle sürücü indirmeniz gerekmez.
- İlk çalıştırmada macOS "uygulama indirildi" uyarısı verirse bir kez onaylayın.

### Linux notları

- Chrome/Chromium yoksa Selenium Manager "Chrome for Testing" indirir.
- Playwright tarayıcısı sistem kitaplığı isterse: `uv run playwright install --with-deps chromium` (sudo sorar).

### Klasörler

| Yol | Ne işe yarar |
|---|---|
| `site/` | Pratik Mağaza (statik HTML/CSS/JS, harici bağlantı yok) |
| `sunucu.py` | Siteyi `http://localhost:8000` adresinde sunar |
| `site_uret.py` | `site/veri/urunler.json` dosyasından ürün sayfalarını üretir |
| `fiyat_degistir.py` | Fiyat takip dersi için 3 ürünün fiyatını değiştirir; `--geri` ile eski hâline döner |
| `veri/basvurular.csv` | Toplu form doldurma dersi için 5 sahte başvuru |
| `ornekler/<ders>/` | Ders örnekleri |
| `araclar/ekran.py` | Selenium/Playwright ekran görüntüsü yardımcıları (1280×800) |
| `araclar/terminal.py` | Bir komutun gerçek çıktısını terminal görünümünde görüntüler |
| `ekran/<ders>/` | Örneklerin ürettiği ekran görüntüleri (çalıştırınca oluşur) |
| `SITE-HARITASI.md` | Sayfalar, id'ler ve sınıflar (derslerin dayandığı sözleşme) |
| `kontrol.sh` | Tüm örnekleri headless çalıştırıp GEÇTİ/KALDI raporlar |

### Terminal görüntüsü almak (isteğe bağlı)

```bash
uv run python araclar/terminal.py 1.3 03-terminal -- BASLIKSIZ=1 python ornekler/1.3/ilk_otomasyon.py
```

Komut gerçekten çalıştırılır; görüntüde yalnızca komut satırı ve komutun kendi çıktısı yer alır.
Ham çıktı aynı klasöre `.txt` olarak da yazılır.

### Kurallar

- Pratik Mağaza'daki tüm isimler, e-postalar ve telefonlar sahtedir.
- `captcha.html` sayfasında botunuz **durmalıdır**. Bu kurs CAPTCHA aşmayı öğretmez.
- `robots.txt` dosyası `/yonetim/` klasörünü yasaklar; kibar botlar bu kurala uyar.
