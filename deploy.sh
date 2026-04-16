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

AWS_PROFILE="${AWS_PROFILE:-personal}"
S3_BUCKET="${S3_BUCKET:-playingwithquicksilver}"
CLOUDFRONT_DISTRIBUTION_ID="${CLOUDFRONT_DISTRIBUTION_ID:-EYB8HL9XV79RV}"

/home/feoh/.openclaw/workspace/.venv/bin/python scripts/convert_nikola_to_hugo.py
"$HUGO" --cleanDestinationDir --destination public
/home/feoh/.openclaw/workspace/.venv/bin/python scripts/generate_legacy_feeds.py
aws s3 cp --recursive public "s3://$S3_BUCKET" --profile "$AWS_PROFILE"
aws cloudfront create-invalidation --distribution-id "$CLOUDFRONT_DISTRIBUTION_ID" --paths "/*" --profile "$AWS_PROFILE"
