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

if command -v python3 >/dev/null 2>&1; then
  PYTHON=python3
elif command -v python >/dev/null 2>&1; then
  PYTHON=python
else
  echo "python not found" >&2
  exit 1
fi

CLOUDFRONT_DISTRIBUTION_ID="${CLOUDFRONT_DISTRIBUTION_ID:-EYB8HL9XV79RV}"

"$PYTHON" scripts/convert_nikola_to_hugo.py
"$HUGO" --cleanDestinationDir --destination public
"$PYTHON" scripts/generate_legacy_feeds.py
aws s3 cp --recursive public "s3://playingwithquicksilver" --profile personal
aws cloudfront create-invalidation --distribution-id "$CLOUDFRONT_DISTRIBUTION_ID" --paths "/*" --profile personal
