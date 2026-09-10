#!/usr/bin/env bash
set -euo pipefail

model_type="${GARAK_MODEL_TYPE:-openai}"
model_name="${GARAK_MODEL_NAME:-}"
probes="${GARAK_PROBES:-promptinject}"
report_dir="${GARAK_REPORT_DIR:-security/garak/reports}"

if [[ -z "$model_name" ]]; then
  if [[ "${GARAK_ALLOW_SKIP:-0}" == "1" ]]; then
    echo "Skipping garak scan: GARAK_MODEL_NAME is not configured."
    exit 0
  fi
  echo "GARAK_MODEL_NAME must be set (for example, gpt-4o-mini)." >&2
  exit 2
fi

mkdir -p "$report_dir"

exec python -m garak \
  --model_type "$model_type" \
  --model_name "$model_name" \
  --probes "$probes" \
  --report_prefix "$report_dir/garak"