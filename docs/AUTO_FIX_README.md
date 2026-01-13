# Automated Configuration Fix

## Quick Start

Check for configuration issues:
```bash
npm run fix:check
```

Apply automatic fixes:
```bash
npm run fix
```

## What It Checks

- Vercel framework configuration (prevents Next.js auto-detection)
- Build scripts in package.json
- TypeScript configuration
- JSON syntax validation

## Features

✅ Automatic detection of common misconfigurations  
✅ One-command fixes with `npm run fix`  
✅ Dry-run mode for safety  
✅ Clear reporting of all checks

## Usage

### Local Development
```bash
# Check only (no changes)
npm run fix:check

# Apply fixes
npm run fix
```

### CI/CD
A GitHub Actions workflow can run this automatically on every push.

## What Gets Fixed

1. **Vercel Next.js Detection** - Sets `framework: null` to prevent incorrect framework detection
2. **Missing Build Scripts** - Ensures all required npm scripts are present
3. **TypeScript Config** - Removes incorrect Next.js types if present

## Exit Codes

- `0` - All checks passed or all issues fixed
- `1` - Issues found (dry-run mode) or manual fixes needed

For more details, see `scripts/auto-fix.js`.
