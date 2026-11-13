#!/usr/bin/env bash
# Push the CS Pulse website deck to GitHub Pages (jaketub16).
# Team-safe rule: no money/commercial terms; "$" allowed only for ad spend, CPL, cost per MQL / booked call.
set -euo pipefail
cd "$(dirname "$0")"
grep -q 'name="robots" content="noindex' index.html || { echo "noindex missing" >&2; exit 1; }
if grep -n -i -E 'invoice|payroll|contract|guarantee|refund|retainer|payment|pricing|price|commercial|renewal|cash|overdue|revenue|MRR' index.html; then echo "banned term found" >&2; exit 1; fi
echo "Review these \$ figures (must be ad spend / CPL only):"; grep -o -E '.{40}\$[0-9][0-9,.]*' index.html | sed 's/<[^>]*>//g' | wc -l
printf 'User-agent: *\nDisallow: /\n' > robots.txt; touch .nojekyll
git add -A; git diff --cached --quiet || { git commit -qm "Update $(date +%F)"; git push -q origin main; }
echo "Live: https://jaketub16.github.io/$(cat .repo_name)/"
