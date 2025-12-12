# PWA Icons Directory

This directory contains icons for Progressive Web App (PWA) support.

## Required Icons

To complete the PWA setup, add the following icon files:

### Required Sizes
- `icon-16x16.png` - Favicon
- `icon-32x32.png` - Favicon
- `icon-72x72.png` - Android Chrome
- `icon-96x96.png` - Android Chrome
- `icon-120x120.png` - iOS Safari
- `icon-128x128.png` - Android Chrome
- `icon-144x144.png` - Windows Metro
- `icon-152x152.png` - iOS Safari
- `icon-180x180.png` - iOS Safari
- `icon-192x192.png` - Android Chrome (standard)
- `icon-384x384.png` - Android Chrome
- `icon-512x512.png` - Android Chrome (splash screen)

## Quick Generation

You can generate these icons from a source image using:

### Online Tools
- [Favicon Generator](https://realfavicongenerator.net/)
- [PWA Asset Generator](https://github.com/elegantapp/pwa-asset-generator)

### Command Line
```bash
# Using ImageMagick
convert source-icon.png -resize 192x192 icons/icon-192x192.png
convert source-icon.png -resize 512x512 icons/icon-512x512.png
# ... (repeat for all sizes)

# Using PWA Asset Generator (npm)
npx pwa-asset-generator source-icon.png icons/ --background "#8000ff"
```

## Design Guidelines

**Recommended Design:**
- **Theme**: Quantum/Cosmic theme with purple/cyan gradients
- **Logo**: Pi Forge emblem or Pi symbol
- **Background**: Transparent or #8000ff (theme color)
- **Style**: Modern, clean, high contrast

**Specifications:**
- Format: PNG (with transparency if needed)
- Color depth: 24-bit or 32-bit (with alpha channel)
- Margins: 10% safe area around the icon
- Content: Should be recognizable at all sizes

## Current Status

⚠️ **Icons not yet created** - Placeholder references in manifest.json

Once icons are added to this directory, they will be automatically:
1. Copied to `public/icons/` during build
2. Referenced by `manifest.json` for PWA installation
3. Used for mobile home screen icons
4. Displayed in browser tabs (favicons)

## Integration

Icons are referenced in:
- `/manifest.json` - PWA manifest
- `/index.html` - Meta tags for iOS and favicons
- `/service-worker.js` - Notification icons
