#!/usr/bin/env bash
#
# setup-repo.sh — one-shot bootstrapper.
#
# Run this once from Terminal on your Mac:
#
#   cd "$HOME/Documents/Claude/Projects/AI Threat hunting"
#   bash setup-repo.sh
#
# It will:
#   1. Discard the half-initialized .git from the assistant's sandbox attempt.
#   2. Re-init git (main branch).
#   3. Make the initial commit.
#   4. Install gh via Homebrew if needed and authenticate it.
#   5. Create the public GitHub repo `ai-threat-hunt-program` and push.
#
# Idempotent: re-running it after a successful push is a no-op for the commit
# step (no changes to commit) but will not re-run the gh repo create.

set -euo pipefail

REPO_NAME="ai-threat-hunt-program"
COMMIT_MSG=$'Initial commit: AI Threat Hunt Program scaffolding\n\nPaper 1 (LinkedIn launch + fast-track) and Paper 2 (D-Control loop)\nwith original .docx in docs/source/. D-Control 8-step loop in\ndocs/d-control/. 10 starter hunt hypotheses (H-001..H-010) under\nhunts/starter/. 7-level graduated containment ladder under\nplaybooks/containment/. Templates: Asset Register (CSV+JSON Schema),\nRisk Register with inherent/residual scoring, Telemetry Requirements\nMatrix, Vendor DDQ, Executive Risk Brief, Operating Cadence, Decision\nLog, Exception Register. Executive metrics in metrics/. Discover-step\nPython scripts in scripts/asset-inventory/ (stdlib only, read-only,\nkey-redacted): scan_repo_for_ai, scan_env_for_ai,\noauth_grants_to_inventory, merge_inventory. Field-guide outline in\nbook/OUTLINE.md.'

cd "$(dirname "$0")"

say() { printf '\033[1;34m==>\033[0m %s\n' "$*"; }
warn() { printf '\033[1;33m!! \033[0m %s\n' "$*"; }
die() { printf '\033[1;31mxx \033[0m %s\n' "$*"; exit 1; }

# 1. Reset .git ---------------------------------------------------------------
if [[ -d .git ]]; then
  say "Removing partial .git from previous attempt…"
  rm -rf .git
fi

say "Initializing git (main branch)…"
git init -b main >/dev/null

# Use the email Cowork already knew about; you can change this anytime.
git config user.name "${GIT_USER_NAME:-Angie Agee}"
git config user.email "${GIT_USER_EMAIL:-728gf2rss6@privaterelay.appleid.com}"

# 2. Initial commit -----------------------------------------------------------
say "Staging files…"
git add .

if git diff --cached --quiet; then
  warn "Nothing to commit; skipping."
else
  say "Committing…"
  git commit -m "$COMMIT_MSG" >/dev/null
fi

# 3. gh -----------------------------------------------------------------------
if ! command -v gh >/dev/null 2>&1; then
  say "GitHub CLI (gh) not found. Installing via Homebrew…"
  if ! command -v brew >/dev/null 2>&1; then
    die "Homebrew not installed. See https://brew.sh, then re-run this script."
  fi
  brew install gh
fi

if ! gh auth status >/dev/null 2>&1; then
  say "Authenticating with GitHub (browser will open)…"
  gh auth login --hostname github.com --git-protocol https --web
fi

GH_USER=$(gh api user --jq .login)
say "Authenticated as: $GH_USER"

# 4. Create remote and push ---------------------------------------------------
if gh repo view "$GH_USER/$REPO_NAME" >/dev/null 2>&1; then
  warn "Repo $GH_USER/$REPO_NAME already exists on GitHub; pushing to it."
  if ! git remote get-url origin >/dev/null 2>&1; then
    git remote add origin "https://github.com/$GH_USER/$REPO_NAME.git"
  fi
  git push -u origin main
else
  say "Creating public repo $GH_USER/$REPO_NAME and pushing…"
  gh repo create "$REPO_NAME" \
    --public \
    --source . \
    --remote origin \
    --push \
    --description "AI-Securing Threat Hunt Program — D-Control loop, hunts, containment playbooks, and Discover-step scripts."
fi

REPO_URL="https://github.com/$GH_USER/$REPO_NAME"
say "Done."
printf '\nRepository: %s\n' "$REPO_URL"
