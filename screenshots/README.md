# Screenshots Directory

This directory contains screenshots for PWA and social media sharing.

## Required Screenshots

### Desktop Screenshot
- **Filename**: `desktop.png`
- **Size**: 1280x720 pixels (16:9 aspect ratio)
- **Content**: Desktop view of the main application
- **Usage**: Open Graph, Twitter cards, PWA manifest

### Mobile Screenshot
- **Filename**: `mobile.png`
- **Size**: 750x1334 pixels (iPhone aspect ratio)
- **Content**: Mobile view of the main application
- **Usage**: PWA manifest, App Store previews

## Usage

Screenshots are referenced in:
- `/manifest.json` - PWA manifest for app stores
- `/index.html` - Open Graph and Twitter meta tags
- Social media sharing previews

## Creation Tips

### Taking Screenshots

**Desktop:**
1. Open application at 1280x720 resolution
2. Ensure all key features visible
3. Use browser DevTools to set exact dimensions
4. Capture with browser screenshot tool

**Mobile:**
1. Open application in mobile viewport (375x667 base)
2. Scale to 750x1334 for retina display
3. Use Chrome DevTools device emulator
4. Capture with device frame if desired

### Design Guidelines

- Show actual application interface
- Include key features and branding
- Use high-quality, crisp images
- Ensure text is readable
- Match theme colors (#8000ff, #1a0033)

## Current Status

⚠️ **Screenshots not yet created** - Placeholder references in manifest.json

Once screenshots are added:
1. They will be copied to `public/screenshots/` during build
2. Shared when application links are posted on social media
3. Displayed in PWA app store listings
4. Used for marketing materials
