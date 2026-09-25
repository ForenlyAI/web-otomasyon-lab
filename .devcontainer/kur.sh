#!/usr/bin/env bash
# Codespace ilk açılışta bir kez çalışır: uv (sabit sürüm) → paketler (uv.lock) → Playwright Chromium + sistem kitaplıkları.
set -euo pipefail
curl -LsSf https://astral.sh/uv/0.12.5/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"
uv sync --locked
uv run playwright install --with-deps chromium
echo "Hazır. Denemek için: bash kontrol.sh"
