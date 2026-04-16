#!/bin/sh
set -exo pipefail

if command -v hugo >/dev/null 2>&1; then
  HUGO=hugo
elif [ -x ./.tools/hugo/hugo ]; then
  HUGO=./.tools/hugo/hugo
else
  echo "hugo not found" >&2
  exit 1
fi

CLOUDFRONT_DISTRIBUTION_ID="${CLOUDFRONT_DISTRIBUTION_ID:-EYB8HL9XV79RV}"

/home/feoh/.openclaw/workspace/.venv/bin/python scripts/convert_nikola_to_hugo.py
"$HUGO" --cleanDestinationDir --destination public
/home/feoh/.openclaw/workspace/.venv/bin/python scripts/generate_legacy_feeds.py
aws s3 cp --recursive public "s3://playingwithquicksilver" --profile personal
aws cloudfront create-invalidation --distribution-id "$CLOUDFRONT_DISTRIBUTION_ID" --paths "/*" --profile personal
