#!/usr/bin/env bash
# Tüm örnekleri başlıksız (headless) çalıştırır, dosya başına GEÇTİ/KALDI yazar.
# Kullanım (lab klasöründen):  bash kontrol.sh
# Sunucu zaten açıksa onu kullanır; değilse arka planda açar ve sonunda kapatır.
set -u
cd "$(dirname "$0")"
ADRES="http://localhost:8000/"
ZAMAN_ASIMI="${ZAMAN_ASIMI:-120}"
SUNUCU_PID=""

kapat() {
  if [ -n "$SUNUCU_PID" ]; then
    kill "$SUNUCU_PID" 2>/dev/null
    wait "$SUNUCU_PID" 2>/dev/null
    echo "Sunucu kapatıldı."
  fi
}
trap kapat EXIT

if curl -s -o /dev/null "$ADRES"; then
  echo "Sunucu zaten açık: $ADRES"
else
  uv run python sunucu.py --sessiz > /dev/null 2>&1 &
  SUNUCU_PID=$!
  for _ in $(seq 1 50); do
    curl -s -o /dev/null "$ADRES" && break
    sleep 0.2
  done
  if ! curl -s -o /dev/null "$ADRES"; then
    echo "Sunucu açılamadı (port 8000 dolu olabilir)."
    exit 1
  fi
  echo "Sunucu açıldı: $ADRES"
fi

gecen=0; kalan=0
while IFS= read -r dosya; do
  # 2.1 giris.py ve 5.4 oturum_kaydet.py şifreyi ortamdan (.env yoksa) okur; kontrol için sitedeki herkese açık demo şifresi (gerçek şifre değil)
  cikti=$(BASLIKSIZ=1 PM_SIFRE="${PM_SIFRE:-pratik123}" PRATIK_KULLANICI="${PRATIK_KULLANICI:-ogrenci}" PRATIK_SIFRE="${PRATIK_SIFRE:-pratik123}" timeout "$ZAMAN_ASIMI" uv run python "$dosya" 2>&1)
  kod=$?
  beklenen=0
  # 5.3: bot CAPTCHA sayfasında durur ve bilerek 3 koduyla çıkar (ders bunu öğretir)
  [ "$dosya" = "ornekler/5.3/captcha_dur.py" ] && beklenen=3
  if [ $kod -eq $beklenen ]; then
    echo "GEÇTİ  $dosya"
    gecen=$((gecen + 1))
  else
    echo "KALDI  $dosya (çıkış kodu $kod)"
    echo "$cikti" | tail -n 15 | sed 's/^/    | /'
    kalan=$((kalan + 1))
  fi
done < <(find ornekler -name '*.py' -type f | sort)

echo "----"
echo "Toplam: $((gecen + kalan)) · Geçti: $gecen · Kaldı: $kalan"
[ $kalan -eq 0 ]
