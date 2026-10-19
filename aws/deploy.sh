#!/usr/bin/env bash
# Deploy the prep site to YOUR AWS account. Run on your own machine; credentials stay local.
# Usage: SITE_PASSWORD='at-least-12-chars' ./aws/deploy.sh [stack-name] [region]
# Needs: aws CLI v2 configured (aws sts get-caller-identity works), python3.
set -euo pipefail
STACK="${1:-fintechco-prep-site}"
REGION="${2:-us-east-1}"
: "${SITE_PASSWORD:?Set SITE_PASSWORD (12+ chars)}"
cd "$(dirname "$0")"

python3 build_site.py

echo "Account: $(aws sts get-caller-identity --query Account --output text)  Region: $REGION  Stack: $STACK"
aws cloudformation validate-template --region "$REGION" --template-body file://template.yaml >/dev/null
echo "Template validated. Deploying (CloudFront can take 5-10 minutes)..."

aws cloudformation deploy \
  --region "$REGION" --stack-name "$STACK" --template-file template.yaml \
  --parameter-overrides AuthToken="$(printf '%s' "${SITE_USER:-reviewer}:${SITE_PASSWORD}" | base64 | tr -d '\n')"

BUCKET=$(aws cloudformation describe-stacks --region "$REGION" --stack-name "$STACK" \
  --query "Stacks[0].Outputs[?OutputKey=='BucketName'].OutputValue" --output text)
aws s3 sync site "s3://$BUCKET" --delete --region "$REGION"

URL=$(aws cloudformation describe-stacks --region "$REGION" --stack-name "$STACK" \
  --query "Stacks[0].Outputs[?OutputKey=='SiteUrl'].OutputValue" --output text)
echo "Live: $URL   (user: ${SITE_USER:-reviewer})"
echo "Tear down: aws cloudformation delete-stack --stack-name $STACK --region $REGION  (empty the bucket first)"
