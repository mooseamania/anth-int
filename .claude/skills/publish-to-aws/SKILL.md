---
name: publish-to-aws
description: Use when the user wants to publish, update, verify or tear down the private prep site (S3 + CloudFront with basic auth) in their AWS account using the aws/ bundle. Covers pre-checks, deploy, verification and teardown. Never handles raw credentials.
---

# Publish the prep site to AWS

Deploys `aws/` (CloudFormation template + `deploy.sh` + `build_site.py`) to the user's own account: private S3 bucket, CloudFront with OAC, HTTPS, basic-auth function.

## Credentials rules (non-negotiable)
- Never ask for, accept, echo, or write access keys or secrets in chat, files, logs or commits. If the user pastes any, tell them to rotate those keys now and continue without using them.
- Use the user's existing local CLI auth: an SSO profile (`aws sso login --profile NAME`) or short-lived role credentials already in their environment.
- The site password comes from the `SITE_PASSWORD` environment variable, set by the user. Never hard-code it or commit it.

## Pre-flight (run, report, then pause for a yes)
1. `aws --version` (v2) and `python3 --version`.
2. `aws sts get-caller-identity` and show **account ID and region** back to the user. Confirm this is the intended account before any change.
3. Check the stack does not already exist, or say it will be updated: `aws cloudformation describe-stacks --stack-name fintechco-prep-site`.
4. Remind: this creates billable resources (CloudFront, S3). Small for this content, but not free.

## Deploy
```
SITE_PASSWORD='(user sets, 12+ chars)' ./aws/deploy.sh [stack-name] [region]
```
Region defaults to us-east-1. If it fails, read the CloudFormation event error (`aws cloudformation describe-stack-events`) and fix the cause. Do not retry blindly.

## Verify
- Print the `SiteUrl` stack output.
- `curl -sI <url>` should return 401 without credentials, and 200 with them (`-u reviewer:...`, password supplied by the user, not echoed).
- Open `/`, `/prep-guide.html`, `/graph.html`, `/business-impact.html`, `/repo/index.html`.

## Update content
Re-run `./aws/deploy.sh`. It rebuilds the site, syncs to S3 with `--delete`, and caching is disabled so changes appear immediately.

## Tear down
Only on explicit request, and name the stack and account first:
```
aws s3 rm s3://<bucket> --recursive
aws cloudformation delete-stack --stack-name <stack> --region <region>
```

## If something is blocked
If the environment cannot reach AWS endpoints (for example a restricted sandbox), say so plainly, do not try to work around it, and hand the user the exact commands to run locally.
