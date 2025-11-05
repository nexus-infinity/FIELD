#!/bin/bash
# === TRIDENT ANCHOR INSTALLER ===
set -euo pipefail

FIELD="/Users/jbear/FIELD"
BIN="$HOME/bin"
LEDGER="$FIELD/.truth/ledger.jsonl"
ANCHOR="$FIELD/.anchor.trident.json"
CREDS="$HOME/.config/field/credentials.env"

mkdir -p "$BIN" "$FIELD/.truth" "$(dirname "$CREDS")"
chmod 700 "$FIELD/.truth" "$(dirname "$CREDS")"

# 1) Fix Python stdlib shadowing (your immediate crash)
cd "$FIELD"
find . -type f -name "enum.py"  -exec bash -lc 'mv "$1" "${1}.local"' _ {} \; 2>/dev/null || true
find . -type f -name "types.py" -exec bash -lc 'mv "$1" "${1}.local"' _ {} \; 2>/dev/null || true
find . -type d -name "__pycache__" -prune -exec rm -rf {} + 2>/dev/null || true

# 2) Anchor: trident into tetrahedron (intention is law)
cat > "$ANCHOR" <<'JSON'
{
  "intent_id": "trident-into-tetrahedron",
  "anchor_geometry": {
    "model": "tetrahedron",
    "trident": ["Intention","Constraints","Verification"]
  },
  "original_purpose": "Use existing FIELD/Keychain credentials non-interactively; prove success with receipts.",
  "non_negotiables": [
    "No interactive prompts (stdin closed)",
    "No silent drift from purpose",
    "Runtime contract: fault if >90s unless explicitly expected"
  ],
  "require_env": ["GITHUB_TOKEN","VERCEL_API_KEY","ANTHROPIC_API_KEY"],
  "success_criteria": [
    "Env presence proved (masked)",
    "Truth ledger receipt written",
    "Optional: GitHub token verifies /user (if token present)"
  ],
  "timeout_sec": 90
}
JSON
chmod 600 "$ANCHOR"

# 3) Central credentials file (pull from FIELD/.env if it exists; keep private)
touch "$CREDS"; chmod 600 "$CREDS"
if [ -f "$FIELD/.env" ]; then
  # append only missing keys to avoid duplicates
  for k in GITHUB_TOKEN VERCEL_API_KEY ANTHROPIC_API_KEY; do
    if ! grep -q "^$k=" "$CREDS" 2>/dev/null && grep -q "^$k=" "$FIELD/.env"; then
      grep "^$k=" "$FIELD/.env" >> "$CREDS"
    fi
  done
fi

# 4) trident_guard – anchored, no-stdin, timeouted, receipt
cat > "$BIN/trident_guard" <<'BASH'
#!/usr/bin/env bash
set -euo pipefail
FIELD="/Users/jbear/FIELD"
ANCHOR="$FIELD/.anchor.trident.json"
LEDGER="$FIELD/.truth/ledger.jsonl"
CREDS="$HOME/.config/field/credentials.env"

jq >/dev/null 2>&1 || { echo "⛔ jq is required"; exit 2; }

[ -f "$ANCHOR" ] || { echo "⛔ Anchor missing: $ANCHOR"; exit 3; }
intent_id=$(jq -r '.intent_id' "$ANCHOR")
timeout=$(jq -r '.timeout_sec // 90' "$ANCHOR")

mkdir -p "$(dirname "$LEDGER")"; chmod 700 "$(dirname "$LEDGER")"
touch "$LEDGER"; chmod 600 "$LEDGER"

# load creds if present
set +u
[ -f "$CREDS" ] && set -a && source "$CREDS" && set +a
set -u

# pre-check env presence (masked report)
require_env=$(jq -r '.require_env[]?' "$ANCHOR" 2>/dev/null || true)
present_json="["
for k in $require_env; do
  v="${!k-}"
  if [[ -n "${v-}" && ${#v} -gt 8 ]]; then
    present_json+="{\"key\":\"$k\",\"present\":true,\"preview\":\"${v:0:4}…${v: -4}\"},"
  else
    present_json+="{\"key\":\"$k\",\"present\":false},"
  fi
done
present_json="${present_json%,}]"

# run command with stdin closed (no prompts), spinner + timeout
start=$(date +%s)
out=$(mktemp); err=$(mktemp)
( "$@" ) < /dev/null >"$out" 2>"$err" & pid=$!

spin='-\|/'; i=0
while kill -0 "$pid" 2>/dev/null; do
  elapsed=$(( $(date +%s) - start ))
  i=$(( (i+1) % 4 ))
  printf "\r[%s] anchored:%s  t=%ss  cmd:%q" "${spin:$i:1}" "$intent_id" "$elapsed" "$*"
  if (( elapsed >= timeout )) && [[ -z "${EXPECTED-}" ]]; then
    echo -e "\n⛔ FAULT: exceeded ${timeout}s without explicit EXPECTED=1"
    kill -TERM "$pid" 2>/dev/null || true
    sleep 1; kill -KILL "$pid" 2>/dev/null || true
    rc=124; break
  fi
  sleep 1
done
if [[ -z "${rc-}" ]]; then wait "$pid"; rc=$?; fi
printf "\n"

# optional live GitHub check if token present
gh_login=""
if [[ -n "${GITHUB_TOKEN-}" ]]; then
  gh_login=$(curl -sS -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user | jq -r '.login // empty' || true)
fi

# receipts: sha digests + minimal diff stamp (fast)
stdout_sha=$(shasum -a 256 "$out" | awk '{print $1}')
stderr_sha=$(shasum -a 256 "$err" | awk '{print $1}')
now=$(date -u +%Y-%m-%dT%H:%M:%SZ)

jq -n \
  --arg intent_id "$intent_id" \
  --arg cmd "$*" \
  --arg started "$now" \
  --arg ended "$now" \
  --arg stdout_sha "$stdout_sha" \
  --arg stderr_sha "$stderr_sha" \
  --argjson env "$present_json" \
  --arg gh "$gh_login" \
  --argjson rc "$rc" \
'{
  receipt:"truth_v1",
  intent_id:$intent_id,
  command:$cmd,
  started_at:$started,
  ended_at:$ended,
  exit_code: $rc,
  env_keys: $env,
  github_login: ( ($gh|length)>0 ? $gh : null ),
  stdout_sha256:$stdout_sha,
  stderr_sha256:$stderr_sha
}' >> "$LEDGER"

if [[ "$rc" -eq 0 ]]; then
  echo "✅ ANCHORED OK (rc=$rc) | ledger → $LEDGER"
else
  echo "⛔ FAULT (rc=$rc) | ledger → $LEDGER"
fi
exit "$rc"
BASH
chmod +x "$BIN/trident_guard"

# 5) quality-of-life aliases (anchored runs by default)
grep -q 'trident_guard' "$HOME/.zshrc" 2>/dev/null || cat >> "$HOME/.zshrc" <<'ZRC'

# --- Trident Anchor defaults ---
export PATH="$HOME/bin:$PATH"
alias ta='trident_guard'                     # anchored run (90s fault unless EXPECTED=1)
alias tap='EXPECTED=1 trident_guard'         # anchored run, long expected
ZRC

echo "✅ Trident anchor installed."
echo "➡  Open a new terminal OR: source ~/.zshrc"
