#!/usr/bin/env bash

set -euo pipefail

repo_root="$(git rev-parse --show-toplevel)"
cd "$repo_root"

failed=0

while IFS= read -r path; do
  case "$path" in
    *.jsonl|*.sqlite|*.sqlite3|*.db|*.pem|*.key|*.p12|*.pfx|*.kdbx|*.mobileprovision|*.env|*.env.*|*.session|*.history)
      printf 'forbidden tracked file: %s\n' "$path" >&2
      failed=1
      ;;
  esac

  case "/$path/" in
    */.claude/*|*/.codex/*|*/.cursor/*|*/_sessions/*|*/session-logs/*|*/file-history/*|*/handoffs/*)
      printf 'forbidden private-runtime path: %s\n' "$path" >&2
      failed=1
      ;;
  esac
done < <(git ls-files)

private_runtime_pattern='(/Users/[[:alnum:]_.-]+/|/home/[[:alnum:]_.-]+/|~/[.](claude|codex)(/|\b)|[.](claude|codex)/(projects|sessions|file-history)|"(sessionId|parentUuid|isSidechain|toolUseResult|cwd)"[[:space:]]*:|BEGIN ([A-Z ]+ )?PRIVATE KEY|github_pat_|ghp_[[:alnum:]]{20,}|sk-[[:alnum:]_-]{20,}|AKIA[0-9A-Z]{16})'

if git grep -n -I -E "$private_runtime_pattern" -- . \
  ':(exclude)scripts/privacy-check.sh' \
  ':(exclude).github/workflows/privacy.yml'; then
  printf 'private runtime or credential-like content detected\n' >&2
  failed=1
fi

if command -v gitleaks >/dev/null 2>&1; then
  if ! gitleaks dir . --no-banner --redact --exit-code 1; then
    failed=1
  fi
else
  printf 'gitleaks is required\n' >&2
  failed=1
fi

if (( failed != 0 )); then
  exit 1
fi

printf 'privacy check passed\n'
