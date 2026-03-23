# Vercel Workflow Fix - Authentication Issue Resolution

## Problem Statement

The Vercel deployment workflow was failing with the following error:

```
Error: No existing credentials found. Please run `vercel login` or pass "--token"
```

**Failed Workflow:** https://github.com/onenoly1010/pi-forge-quantum-genesis/actions/runs/21748376362/job/62739858425

## Root Cause Analysis

The workflow was using `--token=${{ secrets.VERCEL_TOKEN }}` flags in Vercel CLI commands. When the `VERCEL_TOKEN` secret was not configured (or empty), this resulted in:

```bash
vercel pull --yes --environment=production --token=
```

This caused the Vercel CLI to receive an empty token parameter, leading to authentication failure.

## Solution

### Changes Made

1. **Set `VERCEL_TOKEN` as an environment variable** (line 14)
   - The Vercel CLI automatically recognizes the `VERCEL_TOKEN` environment variable
   - This eliminates the need to pass `--token=` flags explicitly

2. **Removed `--token=` flags from all Vercel commands**
   - `vercel pull --yes --environment=preview` (line 102)
   - `vercel build` (line 105)
   - `vercel deploy --prebuilt` (line 109)
   - `vercel pull --yes --environment=production` (line 208)
   - `vercel build --prod` (line 211)
   - `vercel deploy --prebuilt --prod` (line 216)

3. **Added job-level environment variables** (lines 75-78, 185-188)
   - Added explicit `env` blocks at job level for `deploy-preview` and `deploy-production`
   - Ensures VERCEL_TOKEN, VERCEL_ORG_ID, and VERCEL_PROJECT_ID are properly inherited
   - Fixes issue where workflow-level env vars weren't being passed to all steps

4. **Added validation steps** (lines 89-100, 199-210)
   - Check if `VERCEL_TOKEN` secret is configured before attempting deployment
   - Provide clear error messages with setup instructions
   - Exit gracefully if secrets are missing

5. **Added comprehensive documentation** (lines 1-18)
   - Document required secrets in workflow file header
   - Explain how to obtain these secrets
   - Note that `VERCEL_TOKEN` is used as environment variable

### Why This Works

The Vercel CLI has built-in support for the following environment variables:
- `VERCEL_TOKEN` - Authentication token
- `VERCEL_ORG_ID` - Organization/team ID  
- `VERCEL_PROJECT_ID` - Project ID

When these are set as environment variables (both at workflow level and job level), the CLI automatically uses them for authentication. Setting them at both levels ensures they are properly inherited by all steps in the jobs. This is the recommended approach in Vercel's documentation and is more reliable than passing `--token=` flags.

**Important:** GitHub Actions doesn't always inherit workflow-level environment variables properly in all job contexts, especially when using `environment` settings. Setting them at the job level ensures they're always available.

## Required Secrets Configuration

To use this workflow, configure these secrets in your GitHub repository settings:

1. **VERCEL_TOKEN**
   - Get from: https://vercel.com/account/tokens
   - Create a new token with appropriate scopes
   - Add to GitHub Secrets: Settings → Secrets and variables → Actions → New repository secret

2. **VERCEL_ORG_ID** and **VERCEL_PROJECT_ID**
   - Run `vercel link` in your project directory
   - These IDs will be saved in `.vercel/project.json`
   - Copy the values to GitHub Secrets

## Testing

The workflow will now:
1. ✅ Check if secrets are configured before attempting deployment
2. ✅ Provide clear error messages if secrets are missing
3. ✅ Use environment variables for authentication (more reliable)
4. ✅ Fail fast with helpful instructions rather than cryptic errors

## Benefits

- **Better error messages**: Clear instructions when secrets are missing
- **More reliable**: Uses Vercel CLI's native environment variable support
- **Fail fast**: Validates secrets before running deployment commands
- **Better security**: Avoids passing tokens as command arguments (which can appear in logs)
- **Follows best practices**: Aligns with Vercel's official documentation

## References

- [Vercel CLI Authentication Documentation](https://vercel.com/docs/cli#authentication)
- [GitHub Actions Secrets Documentation](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [Failed Workflow Run](https://github.com/onenoly1010/pi-forge-quantum-genesis/actions/runs/21748376362/job/62739858425)
