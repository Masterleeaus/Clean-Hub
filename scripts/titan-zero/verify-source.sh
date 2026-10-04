#!/usr/bin/env bash
set -euo pipefail

required=(
  artisan
  composer.json
  app/Domains/WorkCore/WorkCoreServiceProvider.php
  packages/titanzero/interaction-engine/composer.json
  packages/titanzero/interaction-engine/src/Providers/InteractionServiceProvider.php
  app/Extensions/Chatbot/extension.json
  app/Extensions/Chatbot/System/ChatbotServiceProvider.php
  docs/archive/plans/2026-07/titan-zero-chatbot-pwa-upgrade-plan.md
)

for path in "${required[@]}"; do
  if [[ ! -f "$path" ]]; then
    printf 'MISSING: %s\n' "$path" >&2
    exit 1
  fi
  printf 'FOUND: %s\n' "$path"
done

python3 - <<'PY'
from pathlib import Path
import json
for path in Path('.').rglob('*.json'):
    if any(part in {'vendor','node_modules'} for part in path.parts):
        continue
    # TypeScript configuration files are JSONC and may legally contain comments/trailing commas.
    if path.name.startswith('tsconfig') or '.vscode' in path.parts:
        continue
    try:
        # Some legacy extension manifests are valid UTF-8 JSON prefixed by a BOM.
        json.loads(path.read_text(encoding='utf-8-sig'))
    except UnicodeDecodeError:
        continue
    except Exception as exc:
        raise SystemExit(f'Invalid strict JSON {path}: {exc}')
print('Strict JSON validation: PASS')
PY

if grep -RIl --exclude-dir=.git --exclude-dir=vendor --exclude-dir=node_modules \
  -E 'BEGIN (RSA |EC |OPENSSH |DSA )?PRIVATE KEY' . >/tmp/titan-private-key-hits.txt; then
  cat /tmp/titan-private-key-hits.txt >&2
  printf 'Private key material detected.\n' >&2
  exit 1
fi

printf 'Private-key scan: PASS\n'
printf 'Source verification: PASS\n'
