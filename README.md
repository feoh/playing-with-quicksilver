Playing With Quicksilver, Hugo branch

This branch is a Hugo-based migration path for the blog.

## Local development

If Hugo is installed globally:

```bash
hugo server
```

If not, you can use the local workspace binary:

```bash
.tools/hugo/hugo server
```

## Build

```bash
python scripts/convert_nikola_to_hugo.py
.tools/hugo/hugo --destination public
python scripts/generate_legacy_feeds.py
```

## Deploy

```bash
./deploy.sh
```

Optional overrides:

```bash
AWS_PROFILE=personal S3_BUCKET=playingwithquicksilver.com ./deploy.sh
```
