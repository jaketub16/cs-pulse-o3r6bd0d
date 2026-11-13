#!/usr/bin/env bash
# Push the CS Pulse website deck to GitHub Pages (jaketub16). Checks noindex + team-safe terms first.
set -euo pipefail
cd "$(dirname "$0")"
grep -q 'name="robots" content="noindex' index.html || { echo "noindex missing" >&2; exit 1; }
if grep -n -i -E 'invoice|payroll|contract|guarantee|refund|retainer' index.html; then echo "banned term found" >&2; exit 1; fi
printf 'User-agent: *\nDisallow: /\n' > robots.txt; touch .nojekyll
git add -A; git diff --cached --quiet || { git commit -qm "Update $(date +%F)"; git push -q origin main; }
echo "Live: https://jaketub16.github.io/$(cat .repo_name)/"
