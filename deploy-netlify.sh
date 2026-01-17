#!/bin/sh
npm install
npm run build
cp public/validation-key.txt dist/validation-key.txt
netlify deploy --prod --dir=dist --message="Auto-deploy by Copilot"
